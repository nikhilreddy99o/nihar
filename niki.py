import os

# Define color variables
GREEN = '\033[0;32m'
RED = '\033[0;31m'
ORANGE = '\033[0;33m'
PINK = '\033[1;35m'
NC = '\033[0m'  # No Color

# Function to display the current location and branch
def display_location_branch():
    print(f"{PINK}Current location: {os.getcwd()}{NC}")
    branch = os.popen('git rev-parse --abbrev-ref HEAD').read().strip()
    print(f"{ORANGE}Current branch: {branch}{NC}\n")

# Function to list available branches and repositories and switch to a branch
def list_branches_repos():
    display_location_branch()
    print(f"{ORANGE}Available branches:{NC}")
    os.system('git branch -a')
    print(f"\n{ORANGE}Available repositories:{NC}")
    os.system('git remote -v')

    switch_choice = input("Do you want to switch to a branch? (y/n) ")
    if switch_choice.lower() == "y":
        switch_branch_name = input("Enter the name of the branch you want to switch to: ")
        os.system(f'git checkout "{switch_branch_name}"')
        print(f"Switched to branch: {ORANGE}{switch_branch_name}{NC}")
    else:
        print("No branch switched.")

# Function to search for a file in the system
def search_file():
    display_location_branch()
    search_choice = input("Do you want to search for a file? (y/n) ")

    if search_choice == "y" or search_choice == "Y":
        file_name = input("Enter the file name: ")
        sudo_choice = input("Do you want to search with sudo? (y/n) ")

        if sudo_choice == "y" or sudo_choice == "Y":
            if os.name == 'posix':
                sudo_find_cmd = f'sudo find / -type f -name "{file_name}" 2>/dev/null'
                print(f"{GREEN}Searching with sudo...{NC}")
                os.system(sudo_find_cmd)
            else:
                print("sudo is not available on this system.")
        else:
            find_cmd = f'find / -type f -name "{file_name}" 2>/dev/null'
            print(f"{GREEN}Searching without sudo...{NC}")
            os.system(find_cmd)
    else:
        print("No search requested.")

# Function to select an available branch or repository
def select_branch_repo():
    display_location_branch()
    select_choice = input("Do you want to select an available branch or repository? (y/n) ")

    if select_choice == "y" or select_choice == "Y":
        select_branch_repo_choice = input("Do you want to select a branch or repository? (branch/repo) ")

        if select_branch_repo_choice == "branch":
            branch_repo_name = input("Enter the name of the branch: ")
            os.system(f'git checkout "{branch_repo_name}"')
            print(f"Switched to branch: {ORANGE}{branch_repo_name}{NC}")
        elif select_branch_repo_choice == "repo":
            branch_repo_name = input("Enter the name of the repository: ")
            print(f"{ORANGE}Selected repository: {branch_repo_name}{NC}")
        else:
            print("Invalid choice. Exiting...")
            return
    else:
        print("No selection requested.")

# Function to list tracked files for commit
def list_tracked_files():
    display_location_branch()

    # Get the git status output
    git_status_output = os.popen('git status -s').readlines()

    tracked_files = []
    for line in git_status_output:
        status = line[:2].strip()
        file_name = line[3:].strip()
        if status != '??':
            tracked_files.append(file_name)

    if not tracked_files:
        print("No tracked files found.")
    else:
        print(f"{GREEN}Tracked files for commit:{NC}")
        for index, file_name in enumerate(tracked_files, start=1):
            print(f"  {index}. {GREEN}{file_name}{NC}")

    return tracked_files

# Function to handle adding files or directories
def handle_add_file_directory():
    display_location_branch()

    # Get the git status output
    git_status_output = os.popen('git status -s').readlines()

    tracked_files = []
    untracked_files = []

    # Process git status output and separate tracked and untracked files
    for line in git_status_output:
        status = line[:2].strip()
        file_name = line[3:].strip()
        if status == '??':
            untracked_files.append(file_name)
        else:
            tracked_files.append(file_name)

    # Display the tracked files in green
    print(f"{GREEN}Tracked files:{NC}")
    for index, file_name in enumerate(tracked_files, start=1):
        print(f"  {index}. {GREEN}{file_name}{NC}")

    # Display the untracked files in red
    print(f"{RED}Untracked files:{NC}")
    for index, file_name in enumerate(untracked_files, start=len(tracked_files) + 1):
        print(f"  {index}. {RED}{file_name}{NC}")

    add_numbers = input("Enter the numbers of the files/directories you want to add "
                        "(separated by spaces) or press 0 to skip: ")

    if add_numbers == '0':
        print("Skipping adding files.")
    else:
        numbers_arr = add_numbers.split()
        selected_files = []

        for number in numbers_arr:
            try:
                file_path = git_status_output[int(number) - 1][3:].strip()
                if file_path:
                    selected_files.append(file_path)
                else:
                    print(f"Invalid number: {number}. Skipping...")
            except ValueError:
                print(f"Invalid number: {number}. Skipping...")
            except IndexError:
                print(f"Invalid number: {number}. Skipping...")

        if not selected_files:
            print("No files selected for add.")
        else:
            print(f"{GREEN}Selected files for add:{NC}")
            for index, file_path in enumerate(selected_files, start=1):
                print(f"  {index}. {GREEN}{file_path}{NC}")

        add_choice = input("Do you want to add the selected files? (y/n) ")

        if add_choice.lower() == "y":
            for file_path in selected_files:
                os.system(f'git add "{file_path}"')
            print("Files added successfully.")
        else:
            print("Files not added.")

# ... (Rest of the code)

# ... (Previous code)

# Main menu loop
while True:
    print("Select an option:")
    print("1) List available branches and repositories and switch to a branch")
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
        handle_git_workflow()
    elif choice == "5":
        print("Exiting...")
        exit(0)
    else:
        print("Invalid option. Please try again.")

