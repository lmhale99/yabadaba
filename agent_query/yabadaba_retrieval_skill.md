# Yabadaba Database Retrieval Skill

This skill provides a structured workflow for retrieving data from the Yabadaba database.

## Workflow: Yabadaba Database Retrieval

If the user requests data, records, or properties from the Yabadaba database, then activate this workflow and execute the following steps in exact order:

### Step 1: Style Identification
If you need to identify the correct table, then call `list_available_styles` and verify if the requested style exists.

### Step 2: Handbook Validation (Mandatory)
If a style has been identified, then call `get_handbook(style=...)` to retrieve allowed values and technical terms.
If the handbook return is empty, then document the attempt before proceeding.

### Step 3: Schema Verification (Mandatory)
If handbook validation is complete, then call `get_style_schema(style=...)` to obtain verbatim field names and data types.

### Step 4: Query Execution
If both handbook and schema have been verified, then construct `query_params` using verbatim keys and maximized filtering.
Then, execute `query_database`.

**If the query returns no results, then:**
If parameters may have been too restrictive, then re-examine the handbook, loosen constraints, and retry `query_database`.

## Guardrails
- If Steps 1, 2, and 3 have not been completed in sequence, then you are **FORBIDDEN** from calling `query_database`.
- If a technical parameter is needed, then it must be derived verbatim from `get_style_schema` or `get_handbook`; do not guess.
