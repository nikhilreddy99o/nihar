import subprocess

# Define color variables
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

# Function to display the current location and branch
def display_location_branch():
    current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True).stdout.strip()
    print(f"{YELLOW}Current location:{NC} {subprocess.run(['pwd'], capture_output=True, text=True).stdout.strip()}")
    print(f"{YELLOW}Current branch:{NC} {current_branch}")

# Function to list available branches, repositories, and prompt for switching to a branch
def list_branches_repos():
    display_location_branch()
    branches = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True).stdout.strip().split('\n')
    print(f"{YELLOW}Available branches and repositories:{NC}")
    for idx, branch in enumerate(branches, 1):
        branch_name = branch.strip('* ')
        if branch.startswith('*'):
            print(f"* {branch_name}")
        else:
            print(f"{idx}. {branch_name}")

    selected_number = input("Select a branch number to switch (or press '0' to skip): ")
    if selected_number != "0":
        try:
            branch_number = int(selected_number)
            selected_branch = branches[branch_number - 1].strip('* ').strip()
            subprocess.run(['git', 'checkout', selected_branch])
            print(f"Switched to branch '{selected_branch}' successfully.")
        except (ValueError, IndexError):
            print("Invalid branch number. Skipping switch.")

    print(f"\n{YELLOW}Available repositories:{NC}")
    subprocess.run(['git', 'remote', '-v'])

# ... (rest of the code remains unchanged)

# Main menu loop
while True:
    print("Select an option:")
    print("1) List available branches and repositories")
    print("2) Create a new branch or repository")
    print("3) Search for a file")
    print("4) Continue with the Git workflow")
    print("5) Exit")

    choice = input()

    if choice == "1":
        list_branches_repos()
    elif choice == "2":
        create_branch_repo()
    elif choice == "3":
        search_file()
    elif choice == "4":
        git_confirm = input("Do you want to continue with the Git workflow? (y/n) ")
        if git_confirm.lower() == "y":
            while True:
                print("Select an option:")
                print("1) Add files or directories")
                print("2) Commit")
                print("3) Push")
                print("4) Commit and Push")
                print("5) Pull")
                print("6) Select a commit")
                print("7) Go back to the previous menu")

                git_choice = input()

                if git_choice == "1":
                    handle_add_file_directory()
                elif git_choice == "2":
                    select_commit()
                elif git_choice == "3":
                    subprocess.run(['git', 'push'])
                elif git_choice == "4":
                    handle_add_file_directory()
                    subprocess.run(['git', 'push'])
                elif git_choice == "5":
                    pull_branch = input("Enter the branch to pull from: ")
                    subprocess.run(['git', 'pull', 'origin', pull_branch])
                elif git_choice == "6":
                    select_commit()
                elif git_choice == "7":
                    break
                else:
                    print("Invalid option. Please try again.")
        else:
            print("Git workflow skipped.")
    elif choice == "5":
        print("Exiting...")
        exit(0)
    else:
        print("Invalid option. Please try again.")

