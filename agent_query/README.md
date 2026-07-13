# Yabadaba Agent Query

A lightweight extension of the core **yabadaba** package that supplies a WebSocket‑based Multi‑Channel Protocol (MCP) server together with an orchestrator for routing queries.

---

## Overview

- **MCP server** (`mcp_server.py`): WebSocket endpoint that accepts JSON‑encoded queries.
- **Orchestrator** (`orchestrator.py`): Sets environment variables, copies `openweb-config.json` to the Open WebUI data directory, launches the MCP server, starts Open WebUI, monitors health, and shuts down cleanly on interrupt.
- **Skill system**: Markdown‑defined skills (see `yabadaba_retrieval_skill.md`) are automatically exposed by the orchestrator.

---

## Prerequisites

- Python 3.10+ (tested with 3.11)
- Core **yabadaba** package (`pip install yabadaba` or install from this repository)
- Optional virtual environment (`.venv/`) for the bundled Open WebUI executable.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/yabadaba.git
cd yabadaba

# Install the package in editable mode
pip install -e .
```

---

## Configuration

Runtime settings are stored in `agent_query/openweb-config.json`. A minimal example looks like this:

```json
{
  "host": "127.0.0.1",
  "port": 8765,
  "log_level": "INFO"
}
```

> **Note:** Before launching the orchestrator, edit `openweb-config.json` to add your API key and provider information required by the underlying services.

---

## Running the Server

```bash
python yabadaba/agent_query/orchestrator.py
```

The orchestrator starts both the MCP server and Open WebUI, and handles graceful shutdown on **Ctrl‑C**.

---

## Setup & Usage

1. **Install dependencies** – Ensure FastMCP is installed (configured in setup.py)
2. **Configure the server** – Open `agent_query/openweb-config.json` and insert your API key and provider settings.
3. **Start the orchestrator** using the command above.
4. Open a browser and navigate to `http://localhost:8081` (the default Open WebUI address).
5. In the Open WebUI workspace, add a new skill:
   - Import `yabadaba_retrieval_skill`
6. Open **Admin Settings**:
   - Go to the *Models* subsection in Settings
   - Choose and edit your default model
   - Enable both *Tools* and *Skills* checkmarks
   - Expand *Advanced Parameters* → enable *Native Function Calling*
7. Select the model from the top‑left dropdown and begin making queries.

