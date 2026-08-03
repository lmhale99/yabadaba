import argparse
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()

@dataclass
# Simple dataclass to hold process metadata
class ManagedProcess:
    popen: subprocess.Popen | None
    title: str
    pidfile: Path | None = None
    launcher_script: Path | None = None
    kill_process_group: bool = False

# Load environment variables from a file

def _load_env_file(env_path: Path):
    if not env_path.exists():
        return
    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip("\"'") )

# Load .env or owu.env into the process environment

def load_env():
    owu_env = SCRIPT_DIR / "owu.env"
    dot_env = SCRIPT_DIR / ".env"
    if owu_env.exists():
        _load_env_file(owu_env)
    else:
        _load_env_file(dot_env)

# Determine if the current OS is Windows

def is_windows() -> bool:
    return os.name == "nt"

# Determine if the current OS is macOS

def is_macos() -> bool:
    return sys.platform == "darwin"

# Check if multiple console windows are desired

def wants_multi_console() -> bool:
    return os.getenv("ORCH_MULTI_CONSOLE", "1").lower() not in {"0", "false", "no", "off"}

# Locate the virtual environment directory

def get_venv_dir() -> Path | None:
    env_venv = os.getenv("ORCH_VENV_DIR")
    if env_venv:
        path = Path(env_venv).expanduser().resolve()
        if path.exists():
            return path
    candidates: list[Path] = [SCRIPT_DIR / ".venv", SCRIPT_DIR.parent / ".venv"]
    for parent in SCRIPT_DIR.parents:
        candidates.append(parent / ".venv")
    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate
    if hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix:
        return Path(sys.prefix).resolve()
    return None

# Get the path to the virtual environment's bin directory

def get_venv_bin_dir() -> Path:
    venv_dir = get_venv_dir()
    if venv_dir:
        return venv_dir / ("Scripts" if is_windows() else "bin")
    return Path(sys.executable).parent

# Find an executable in the venv or system PATH

def find_executable(name: str, venv_bin: Path) -> str:
    executable_name = f"{name}.exe" if is_windows() else name
    venv_executable = venv_bin / executable_name
    if venv_executable.exists():
        return str(venv_executable)
    found = shutil.which(name) or shutil.which(executable_name)
    if found:
        return found
    raise FileNotFoundError(f"Could not find executable '{name}'. Checked {venv_executable} and system PATH.")

# Build the base environment for subprocesses

def build_base_env() -> dict:
    env = os.environ.copy()
    venv_bin = get_venv_bin_dir()
    env["PATH"] = str(venv_bin) + os.pathsep + env.get("PATH", "")
    return env

# Determine the data directory for Open WebUI

def get_open_webui_data_dir() -> Path:
    configured = os.getenv("ORCH_OPEN_WEBUI_DATA_DIR") or os.getenv("OPEN_WEBUI_DATA_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    open_webui_root = os.getenv("OPEN_WEBUI_ROOT")
    if open_webui_root:
        return Path(open_webui_root).expanduser().resolve() / "data"
    return Path.home() / ".open-webui"

# Validate that a string is a safe shell identifier

def shell_identifier_is_safe(key: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key))

# Create a temporary POSIX launch script for terminals

def create_posix_launcher_script(cmd: list[str], env: dict, title: str) -> tuple[Path, Path]:
    unique = uuid.uuid4().hex
    safe_title = re.sub(r"[^A-Za-z0-9_.-]+", "_", title).strip("_") or "service"
    temp_dir = Path(tempfile.gettempdir())
    launcher_script = temp_dir / f"orchestrator_{safe_title}_{unique}.sh"
    pidfile = temp_dir / f"orchestrator_{safe_title}_{unique}.pid"
    export_lines = []
    for key, value in sorted(env.items()):
        if not shell_identifier_is_safe(key):
            continue
        export_lines.append(f"export {key}={shlex.quote(str(value))}")
    script_contents = "\n".join([
        "#!/usr/bin/env bash",
        "set -e",
        f"cd {shlex.quote(str(SCRIPT_DIR))}",
        f"echo $$ > {shlex.quote(str(pidfile))}",
        "",
        *export_lines,
        "",
        f"echo 'Starting {title}...'",
        f"exec {shlex.join(cmd)}",
        "",
    ])
    launcher_script.write_text(script_contents, encoding="utf-8")
    launcher_script.chmod(0o700)
    return launcher_script, pidfile

# Quote a string for AppleScript usage

def applescript_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\\\').replace('"', '\\"') + '"'

# Launch a process in a new Windows console window

def launch_in_new_windows_console(cmd: list[str], env: dict, title: str) -> ManagedProcess:
    print(f"Opening new Windows console for {title}...")
    popen = subprocess.Popen(cmd, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)
    return ManagedProcess(popen=popen, title=title)

# Launch a process in a new macOS Terminal window

def launch_in_macos_terminal(cmd: list[str], env: dict, title: str) -> ManagedProcess:
    print(f"Opening new macOS Terminal window for {title}...")
    launcher_script, pidfile = create_posix_launcher_script(cmd, env, title)
    terminal_command = f"bash {shlex.quote(str(launcher_script))}"
    osa_cmd = ["osascript", "-e", f'tell application "Terminal" to do script {applescript_quote(terminal_command)}', "-e", 'tell application "Terminal" to activate']
    popen = subprocess.Popen(osa_cmd)
    return ManagedProcess(popen=popen, title=title, pidfile=pidfile, launcher_script=launcher_script)

# Find an available Linux terminal emulator command

def find_linux_terminal_command(launcher_script: Path, title: str) -> list[str] | None:
    script = str(launcher_script)
    candidates = [
        ["x-terminal-emulator", "-T", title, "-e", "bash", script],
        ["gnome-terminal", "--title", title, "--", "bash", script],
        ["konsole", "--new-tab", "-p", f"tabtitle={title}", "-e", "bash", script],
        ["xfce4-terminal", "--title", title, "--command", f"bash {shlex.quote(script)}"],
        ["mate-terminal", "--title", title, "--", "bash", script],
        ["lxterminal", "--title", title, "-e", "bash", script],
        ["xterm", "-T", title, "-e", "bash", script],
        ["alacritty", "--title", title, "-e", "bash", script],
        ["kitty", "--title", title, "bash", script],
    ]
    for candidate in candidates:
        if shutil.which(candidate[0]):
            return candidate
    return None

# Launch a process in a new Linux terminal window

def launch_in_linux_terminal(cmd: list[str], env: dict, title: str) -> ManagedProcess:
    launcher_script, pidfile = create_posix_launcher_script(cmd, env, title)
    terminal_cmd = find_linux_terminal_command(launcher_script, title)
    if terminal_cmd is None:
        print(f"No supported Linux terminal emulator found for {title}. Falling back to attached process.")
        launcher_script.unlink(missing_ok=True)
        pidfile.unlink(missing_ok=True)
        return launch_attached(cmd, env, title)
    print(f"Opening new Linux terminal for {title}...")
    popen = subprocess.Popen(terminal_cmd, env=env)
    return ManagedProcess(popen=popen, title=title, pidfile=pidfile, launcher_script=launcher_script)

# Launch a process attached to the orchestrator without opening a new terminal

def launch_attached(cmd: list[str], env: dict, title: str) -> ManagedProcess:
    print(f"Starting {title} attached to orchestrator...")
    if is_windows():
        popen = subprocess.Popen(cmd, env=env)
        return ManagedProcess(popen=popen, title=title)
    popen = subprocess.Popen(cmd, env=env, start_new_session=True)
    return ManagedProcess(popen=popen, title=title, kill_process_group=True)

# General process launcher respecting console preferences

def launch_process(cmd: list[str], env: dict, title: str) -> ManagedProcess:
    if not wants_multi_console():
        return launch_attached(cmd, env, title)
    if is_windows():
        return launch_in_new_windows_console(cmd, env, title)
    if is_macos():
        return launch_in_macos_terminal(cmd, env, title)
    return launch_in_linux_terminal(cmd, env, title)

# PID utilities

def pid_is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except Exception:
        return False

def read_pidfile(pidfile: Path | None) -> int | None:
    if not pidfile or not pidfile.exists():
        return None
    try:
        raw = pidfile.read_text(encoding="utf-8").strip()
        return int(raw) if raw else None
    except Exception:
        return None

def wait_for_pidfile(pidfile: Path | None, timeout: float = 10.0) -> int | None:
    if not pidfile:
        return None
    start = time.time()
    while time.time() - start < timeout:
        pid = read_pidfile(pidfile)
        if pid:
            return pid
        time.sleep(0.1)
    return None

def wait_for_managed_process(process: ManagedProcess):
    if process.pidfile:
        pid = wait_for_pidfile(process.pidfile)
        if pid:
            while pid_is_alive(pid):
                time.sleep(1)
            return
    if process.popen:
        process.popen.wait()

def cleanup_temp_files(process: ManagedProcess):
    for path in [process.pidfile, process.launcher_script]:
        if path:
            try:
                path.unlink(missing_ok=True)
            except Exception:
                pass

def stop_process(process: ManagedProcess):
    print(f"Stopping {process.title}...")
    pid = read_pidfile(process.pidfile)
    if pid and not is_windows():
        try:
            os.kill(pid, signal.SIGTERM)
            start = time.time()
            while time.time() - start < 5:
                if not pid_is_alive(pid):
                    break
                time.sleep(0.2)
            if pid_is_alive(pid):
                os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except Exception:
            pass
        cleanup_temp_files(process)
        return
    if process.popen and process.popen.poll() is None:
        try:
            if not is_windows() and process.kill_process_group:
                os.killpg(process.popen.pid, signal.SIGTERM)
            else:
                process.popen.terminate()
            process.popen.wait(timeout=5)
        except Exception:
            try:
                if not is_windows() and process.kill_process_group:
                    os.killpg(process.popen.pid, signal.SIGKILL)
                else:
                    process.popen.kill()
                process.popen.wait(timeout=5)
            except Exception:
                pass
    cleanup_temp_files(process)

# Build the command and environment for the MCP server

def build_mcp_command(db_name: str | None = None) -> tuple[list[str], dict]:
    env = build_base_env()
    mcp_server_script = SCRIPT_DIR / os.getenv("ORCH_MCP_SERVER_SCRIPT", "mcp_server.py")
    env_db_name = os.getenv("ORCH_DATABASE_NAME")
    if env_db_name == "default_db":
        env_db_name = None
    if db_name:
        database_name = db_name
    elif env_db_name:
        database_name = env_db_name
    else:
        raise SystemExit("Database name not provided and no default set.")
    port = os.getenv("ORCH_MCP_PORT", "8000")
    env["YABADABA_DB_NAME"] = database_name
    env["MCP_PORT"] = port
    venv_bin = get_venv_bin_dir()
    mcpo_exe = find_executable("mcpo", venv_bin)
    cmd = [mcpo_exe, "--port", str(port), "--", sys.executable, str(mcp_server_script)]
    return cmd, env

# Build the command and environment for Open WebUI

def build_webui_command() -> tuple[list[str], dict]:
    env = build_base_env()
    open_webui_data_dir = get_open_webui_data_dir()
    env["DATA_DIR"] = str(open_webui_data_dir)
    port = os.getenv("ORCH_WEBUI_PORT", "8081")
    venv_bin = get_venv_bin_dir()
    open_webui_exe = find_executable("open-webui", venv_bin)
    cmd = [open_webui_exe, "serve", "--port", str(port)]
    return cmd, env

# Functions to start services (without the main orchestration logic)

def start_mcp(db_name: str | None = None) -> ManagedProcess:
    cmd, env = build_mcp_command(db_name)
    database_name = env["YABADABA_DB_NAME"]
    port = env["MCP_PORT"]
    print(f"Starting MCP server on port {port} using database '{database_name}'...")
    return launch_process(cmd, env, "MCP Server")

def start_webui() -> ManagedProcess:
    cmd, env = build_webui_command()
    port = os.getenv("ORCH_WEBUI_PORT", "8081")
    print(f"Starting Open WebUI on port {port}...")
    print(f"Open WebUI data directory: {env['DATA_DIR']}")
    return launch_process(cmd, env, "Open WebUI")

# Argument parsing helper (used by orchestrator.py)

def parse_args():
    parser = argparse.ArgumentParser(description="Cross-platform orchestrator for MCP and Open WebUI.")
    subparsers = parser.add_subparsers(dest="mode")
    mcp_parser = subparsers.add_parser("mcp", help="Start only the MCP server.")
    mcp_parser.add_argument("db", nargs="?", default=None, help="Optional database name.")
    mcp_parser.add_argument("--db", dest="db_flag", default=None, help="Optional database name.")
    subparsers.add_parser("webui", help="Start only Open WebUI.")
    return parser.parse_args()
