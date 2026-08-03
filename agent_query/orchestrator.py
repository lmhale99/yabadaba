import orchestrator_core as core
import sys
import time

def main():
    """Entry point that keeps the main logic in this file while delegating functionality to orchestrator_core."""
    core.load_env()
    args = core.parse_args()

    if args.mode == "mcp":
        db_name = args.db_flag or args.db
        process = core.start_mcp(db_name=db_name)
        try:
            core.wait_for_managed_process(process)
        except KeyboardInterrupt:
            print("\nStopping MCP server...")
            core.stop_process(process)
        return

    if args.mode == "webui":
        process = core.start_webui()
        try:
            core.wait_for_managed_process(process)
        except KeyboardInterrupt:
            print("\nStopping Open WebUI...")
            core.stop_process(process)
        return

    processes: list[core.ManagedProcess] = []
    try:
        processes.append(core.start_mcp())
        processes.append(core.start_webui())
        print("Both services started.")
        print("Press Ctrl+C in this orchestrator window to stop them.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping orchestrator and spawned services...")
    finally:
        for process in processes:
            core.stop_process(process)
        print("All services stopped.")

if __name__ == "__main__":
    main()
