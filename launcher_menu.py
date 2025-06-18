import subprocess
import sys
import time

servers = {
    "1": {"name": "Chatroom Server", "script": "backend/web_chat_server.py", "process": None},
    "2": {"name": "File Server", "script": "backend/web_file_server.py", "process": None},
    "3": {"name": "Email Server", "script": "backend/web_email_server.py", "process": None},
    "4": {"name": "SMTP Server", "script": "backend/simple_smtp_server.py", "process": None},
}

def print_menu():
    print("\n=== Python Server Launcher Menu ===")
    for key, srv in servers.items():
        status = "RUNNING" if srv["process"] and srv["process"].poll() is None else "STOPPED"
        print(f"{key}. {srv['name']} [{status}]")
    print("s. Stop a server")
    print("q. Quit")

def start_server(choice):
    srv = servers[choice]
    if srv["process"] and srv["process"].poll() is None:
        print(f"{srv['name']} is already running.")
    else:
        print(f"Starting {srv['name']}...")
        srv["process"] = subprocess.Popen([sys.executable, srv["script"]])
        time.sleep(1)

def stop_server(choice):
    srv = servers[choice]
    if srv["process"] and srv["process"].poll() is None:
        print(f"Stopping {srv['name']}...")
        srv["process"].terminate()
        srv["process"].wait()
        print(f"{srv['name']} stopped.")
    else:
        print(f"{srv['name']} is not running.")

def main():
    while True:
        print_menu()
        choice = input("Select an option: ").strip().lower()
        if choice in servers:
            start_server(choice)
        elif choice == "s":
            stop_choice = input("Enter server number to stop: ").strip()
            if stop_choice in servers:
                stop_server(stop_choice)
            else:
                print("Invalid server number.")
        elif choice == "q":
            print("Quitting and terminating all servers...")
            for key in servers:
                stop_server(key)
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()