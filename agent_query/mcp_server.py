'''
Yabadaba MCP Server
===================
This module implements a Model Context Protocol (MCP) server that exposes the
Yabadaba database retrieval system to LLM agents.

Configuration:
    - YABADABA_DB_NAME: Environment variable specifying the database to load.

Transport:
    - Uses stdio for communication with MCP clients (e.g., Open WebUI, Claude Desktop).

Setup:
    - Start venv
    - Configure your database
    - Other libraries needed: fastmcp
    - Run uv run mcpo --port 8000 -- python .\mcp_server.py
'''
import sys
import os
import json
import shutil
from pathlib import Path

# Ensure the project root is in PYTHONPATH for relative imports
sys.path.append(Path(__file__).resolve().parents[1].as_posix())

import pandas as pd
try:
    from fastmcp import FastMCP
except ImportError as exc:
    raise ImportError(
        "fastmcp is required to run the MCP server. Install it via \"pip install 'yabadaba[fastmcp]'\" or \"uv pip install 'yabadaba[fastmcp]'\"."
    ) from exc
from tqdm import tqdm
if not shutil.which("uv") or not shutil.which("mcpo"):
    sys.exit("Error: MCP or required 'uv' tool is not installed. Aborting MCP server.")
from yabadaba.database import load_database
from yabadaba.querydoc import querydoc

# Atomman fallback removed; only explicit DB via YABADABA_DB_NAME is supported.

# Initialize FastMCP server
if FastMCP is None:
    raise ImportError(
        "fastmcp is required to run the MCP server. Install it via \"pip install 'yabadaba[fastmcp]'\" or \"uv pip install 'yabadaba[fastmcp]'\"."
    )
mcp = FastMCP("yabadaba")
DB_NAME = os.getenv("YABADABA_DB_NAME")

def initialize_db() -> "object | None":
    """Initialize and return the Yabadaba database.

    Priority order:
    1. ``YABADABA_DB_NAME`` environment variable (explicit override).

    Returns:
        The database object if successful, otherwise ``None``.
    """
    if DB_NAME:
        try:
            return load_database(name=DB_NAME)
        except Exception as e:
            print(f"Warning: Yabadaba Database ({DB_NAME}) init failed: {e}", file=sys.stderr)
    # No Atomman fallback; return None if DB not configured.
    return None

# Initialize the database once at startup
DB = initialize_db()
if DB is None:
    raise SystemExit("Database not configured. Set YABADABA_DB_NAME environment variable to specify a database.")

@mcp.tool()
def list_available_styles() -> str:
    """
    List all available record styles (tables) in the database.

    Yabadaba Database Retrieval Workflow:
    Step 1: Style Identification - Call list_available_styles to verify if the requested style exists.
    Step 2: Handbook Validation (Mandatory) - Call get_handbook(style=...).
    Step 3: Schema Verification (Mandatory) - Call get_style_schema(style=...).
    Step 4: Query Execution - Execute query_database.
    """
    from yabadaba.record import recordmanager
    try:
        styles_info = []
        for name, cls in recordmanager.loaded_styles.items():
            doc = cls.__doc__ or "No description available."
            styles_info.append(f"{name}: {doc}")
        
        if not styles_info:
            return "No available styles found in the database."
        return "Available record styles:\n" + "\n".join(styles_info)
    except Exception as e:
        return f"Error listing styles: {str(e)}"


@mcp.tool()
def get_style_schema(style: str) -> str:
    """
    Returns the schema (fields and types) for a specific record style.

    Yabadaba Database Retrieval Workflow:
    Step 1: Style Identification - Call list_available_styles.
    Step 2: Handbook Validation (Mandatory) - Call get_handbook(style=...).
    Step 3: Schema Verification (Mandatory) - Call get_style_schema(style=...) to obtain verbatim field names and data types.
    Step 4: Query Execution - Execute query_database.
    """
    # LLM Hallucination Mitigation:
    # Agents sometimes pass arguments as "style: table_name" instead of just "table_name".
    # This cleaning ensures we extract only the actual identifier.
    cleaned_style = style.split(':')[-1].strip() if ':' in style else style.strip()
    
    try:
        return querydoc(style=cleaned_style, render=False)
    except Exception as e:
        return f"Error retrieving schema for style '{cleaned_style}' (original input: '{style}'): {str(e)}"

@mcp.tool()
def get_handbook(style: str = None) -> str:
    """
    Retrieve the authoritative handbook guide. If a style is provided, return the entry for that style.
    Otherwise, return the list of all available styles in the handbook.

    Yabadaba Database Retrieval Workflow:
    Step 1: Style Identification - Call list_available_styles.
    Step 2: Handbook Validation (Mandatory) - Call get_handbook(style=...) to retrieve allowed values and technical terms.
    Step 3: Schema Verification (Mandatory) - Call get_style_schema(style=...).
    Step 4: Query Execution - Execute query_database.
    """
    try:
        # The MCP server process has OS-level access to the local filesystem
        # where the server is installed, so this is the correct way to expose
        # the handbook content to the agent.
        handbook_path = os.path.join(os.path.dirname(__file__), "handbook.json")
        
        if not os.path.exists(handbook_path):
            return "Handbook does not exist."
            
        with open(handbook_path, "r", encoding="utf-8") as f:
            handbook = json.load(f)
        
        if not handbook:
            return "Handbook does not exist."
            
        styles = handbook.get("record_styles", {})
        
        if style is None:
            return "Available styles in handbook: " + ", ".join(styles.keys())

        # LLM Hallucination Mitigation:
        # Agents sometimes pass arguments as "style: table_name" instead of just "table_name".
        # This cleaning ensures we extract only the actual identifier.
        cleaned_style = style.split(':')[-1].strip() if ':' in style else style.strip()
        
        if cleaned_style not in styles:
            return f"Style '{cleaned_style}' not found in the handbook. Available styles: {', '.join(styles.keys())}"
        
        entry = styles[cleaned_style]
        return json.dumps({
            "description": entry.get("description"),
            "root_element": entry.get("root_element"),
            "properties": entry.get("properties")
        }, indent=2)
    except Exception as e:
        # If cleaned_style isn't defined yet (e.g. error happened before line 102),
        # provide a generic error.
        style_info = f" for style '{cleaned_style}'" if 'cleaned_style' in locals() else ""
        return f"Error retrieving handbook entry{style_info}: {str(e)}"


@mcp.tool()
async def query_database(style: str, query_params: dict = None) -> str:
    """
    Query the database for records of a specific style using the provided filters.

    Yabadaba Database Retrieval Workflow:
    Step 1: Style Identification - Call list_available_styles.
    Step 2: Handbook Validation (Mandatory) - Call get_handbook(style=...).
    Step 3: Schema Verification (Mandatory) - Call get_style_schema(style=...).
    Step 4: Query Execution - Construct query_params using verbatim keys and maximized filtering, then execute query_database.

    Guardrails:
    - If Steps 1, 2, and 3 have not been completed in sequence, you are FORBIDDEN from calling query_database.
    - Technical parameters must be derived verbatim from get_style_schema or get_handbook; do not guess.
    - If no results return, re-examine the handbook, loosen constraints, and retry.

    Parameters:
        style (str): The record style (table name) to query.
        query_params (dict, optional): A dictionary of filters.
            Keys MUST be verbatim matches of field names found in the schema.

    Returns:
        str: A JSON string containing the results. Large results are automatically
             truncated to the first 50 entries with a summary note included.
    """
    if DB is None:
        return "Database not configured. Set YABADABA_DB_NAME environment variable to specify a database."
    
    # yabadaba style
    if hasattr(DB, "get_records"):
        params = query_params or {}
        def do_query():
            with tqdm(total=1, desc=f"Querying {style}", file=sys.stderr) as pbar:
                res = DB.get_records_df(style=style, **params)
                return res
        try:
            result = do_query()
            # Write result to a JSON file and return its relative path
            limit = 50
            if isinstance(result, pd.DataFrame):
                total_count = len(result)
                if limit is not None and total_count > limit:
                    result = result.head(limit)
                    summary_row = pd.DataFrame([{"__summary__": f"Showing {limit} of {total_count} total entries."}])
                    result = pd.concat([result, summary_row], ignore_index=True)
                return result.to_json(orient="records", date_format="iso", indent=2)
            
            if isinstance(result, list):
                total_count = len(result)
                if limit is not None and total_count > limit:
                    result = result[:limit]
                    result.append({"__summary__": f"Showing {limit} of {total_count} total entries."})
            
            return json.dumps(result, default=lambda x: x.isoformat() if hasattr(x, 'isoformat') else str(x), indent=2)
        except Exception as e:
            return f"Error during query: {str(e)}"


if __name__ == "__main__":
    # Run as a stdio server for mcpo/MCP clients
    mcp.run()
