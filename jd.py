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

# ... (rest of the functions remain unchanged)

# Function to handle adding a file or directory
def handle_add_file_directory():
    display_location_branch()
    git_status = subprocess.run(['git', 'status', '-s'], capture_output=True, text=True).stdout.strip().split('\n')
    for idx, status in enumerate(git_status, 1):
        print(f"{idx}. {status}")

    add_numbers = input("Enter the numbers of the files/directories you want to add (separated by spaces): ")
    if add_numbers:
        try:
            numbers_arr = list(map(int, add_numbers.split()))
            for number in numbers_arr:
                if 1 <= number <= len(git_status):
                    file_path = git_status[number - 1].split(maxsplit=1)[1]
                    subprocess.run(['git', 'add', file_path])
                    print(f"{GREEN}Added: {file_path}{NC}")
                else:
                    print(f"Invalid number: {number}. Skipping...")
        except ValueError:
            print("Invalid input. Please enter space-separated numbers.")
    else:
        print("No files/directories selected for adding.")

# Function to select an available commit and create a new commit with its changes
def handle_select_commit():
    display_location_branch()
    git_log = subprocess.run(['git', 'log', '--oneline', '--name-status'], capture_output=True, text=True).stdout.strip().split('\n')
    for idx, commit in enumerate(git_log, 1):
        print(f"{idx}. {commit}")

    commit_numbers = input("Enter the numbers of the commits you want to include in the new commit (separated by spaces): ")
    if commit_numbers:
        try:
            numbers_arr = list(map(int, commit_numbers.split()))
            commit_messages = []
            for number in numbers_arr:
                if 1 <= number <= len(git_log):
                    commit_hash = git_log[number - 1].split(maxsplit=1)[0]
                    commit_messages.append(commit_hash)
                else:
                    print(f"Invalid commit number: {number}. Skipping...")

            if commit_messages:
                new_commit_message = input("Enter the commit message: ")
                for commit_message in commit_messages:
                    subprocess.run(['git', 'reset', '--soft', 'HEAD^'])
                    subprocess.run(['git', 'commit', '-m', f"{commit_message}: {new_commit_message}"])
            else:
                print("No valid commits selected. Aborting commit creation.")
        except ValueError:
            print("Invalid input. Please enter space-separated numbers.")
    else:
        print("No commits selected. Aborting commit creation.")

# ... (continuation of other functions)

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
                    handle_select_commit()
                elif git_choice == "3":
                    subprocess.run(['git', 'push'])
                elif git_choice == "4":
                    handle_add_file_directory()
                    subprocess.run(['git', 'push'])
                elif git_choice == "5":
                    pull_branch = input("Enter the branch to pull from: ")
                    subprocess.run(['git', 'pull', 'origin', pull_branch])
                elif git_choice == "6":
                    handle_select_commit()
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

