import requests
import readline
import fire
from termcolor import colored

BASE_URL_TEMPLATE = "http://{host}:{port}"

def get_pending_approvals(base_url):
    try:
        response = requests.get(f"{base_url}/approvals")
        response.raise_for_status()
        return [a for a in response.json() if a["status"] is None]
    except Exception as e:
        print(colored(f"Error fetching approvals: {e}", "red"))
        return []

def set_status(base_url, approval_id, status):
    try:
        response = requests.patch(f"{base_url}/approvals/{approval_id}", json={"status": status})
        response.raise_for_status()
        print(colored(f"Approval {approval_id} {'accepted' if status else 'rejected'}.", "green"))
    except Exception as e:
        print(colored(f"Error updating approval: {e}", "red"))

def main(host: str = "localhost", port: int = 8005):
    base_url = BASE_URL_TEMPLATE.format(host=host, port=port)
    
    print(colored("Approval CLI", "cyan"))
    print(colored("Commands: list, accept <id>, reject <id>, exit", "cyan"))

    current_ids = []

    def completer(text, state):
        matches = [i for i in current_ids if i.startswith(text)]
        if state < len(matches):
            return matches[state]
        return None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        try:
            cmd = input(">>> ").strip()
            if cmd in ["exit", "quit"]:
                print("Exiting.")
                break
            if cmd == "list":
                approvals = get_pending_approvals(base_url)
                current_ids = [a["id"] for a in approvals]
                if not approvals:
                    print("No pending approvals.")
                else:
                    for a in approvals:
                        print(f"{a['tool_name']} - {a['id']}")
            elif cmd.startswith("accept "):
                _, approval_id = cmd.split(maxsplit=1)
                set_status(base_url, approval_id, True)
            elif cmd.startswith("reject "):
                _, approval_id = cmd.split(maxsplit=1)
                set_status(base_url, approval_id, False)
            else:
                print("Unknown command.")
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(colored(f"Error: {e}", "red"))

if __name__ == "__main__":
    fire.Fire(main)
