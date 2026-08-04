# Yabadaba Agent Query

A lightweight extension of the core **yabadaba** package that supplies a WebSocket‑based Multi‑Channel Protocol (MCP) server together with an orchestrator for routing queries.

**Linux and macOS still in testing**

---

## Overview

- **MCP server** (`mcp_server.py`): WebSocket endpoint that accepts JSON‑encoded queries.
- **Orchestrator** (`orchestrator.py`): Sets environment variables, copies `openweb-config.json` to the Open WebUI data directory, launches the MCP server, starts Open WebUI, monitors health, and shuts down cleanly on interrupt.
- **Skill system**: Markdown‑defined skills (see `yabadaba_retrieval_skill.md`) are automatically exposed by the orchestrator.

---

## Prerequisites

- Python 3.11
- Core **yabadaba** package
- Optional virtual environment (`.venv/`) for the bundled Open WebUI executable.

## Configuration

Runtime settings are stored in `owu.env`. Important variables include:

```env
ORCH_CONFIG_FILE = "owu.env"
ORCH_MCP_SERVER_SCRIPT = "mcp_server.py"
ORCH_MCP_PORT = "8001"
# ORCH_DATABASE_NAME must be set explicitly; no default is provided.
```

> **Note:**
> - Ensure `mcpo` is installed and on your `$PATH`. Use `uv tool install mcpo` or add the installation directory to `$PATH`.
> - Edit `owu.env` to set your API key and provider details before launching.

---

## Setup & Usage

1. **Install dependencies** – ensure all dependencies are installed (configured in `setup.py`).
                            - ensure mcpo is installed
2. **Configure the server** – edit `agent_query/owu.env` to insert your API key, provider, and database name.
3. **Start the orchestrator** – run `agent_query/orchestrator.py`
                              - For more options see [Ways to invoke the Orchestrator](#ways-to-invoke-the-orchestrator).
4. Open a browser and navigate to `http://localhost:8081` (the default Open WebUI address).
5. In the Open WebUI UI, add a new skill:
   - Expand the side bar on the left
   - Select Workspace -> Select Skills at the top
   - Select the dropdown next to the create button at the top right corner
   - Import `yabadaba_retrieval_skill` as a json
6. Tweak **Settings**:
   - Select **User** at the bottom left of the screen, select **Admin Panel**, then select **Settings** at the top of the screen
   - Go to the **Models** subsection in Settings
   - Press the edit button (Pencil Icon) next to your preferred model
   - Select both **Tools** and **Skills** and enable them respectively
   - Expand **Advanced Parameters** → enable **Native Function Calling**
7. Return to the main menu, select the model from the dropdown and begin making queries.

---

## Ways to invoke the Orchestrator

The script `orchestrator.py` can be run in three ways:

- **No arguments** – starts both the MCP server **and** Open WebUI.
- **`mcp` sub‑command** – starts only the MCP server. Optionally provide a database name:
  ```bash
  python orchestrator.py mcp [db_name]
  ```
- **`webui` sub‑command** – starts only the Open WebUI service:
  ```bash
  python orchestrator.py webui
  ```

These options let you run the components independently or together.
