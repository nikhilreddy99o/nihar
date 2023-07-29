import os

# Constants for colored output
ORANGE = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
PINK = "\033[95m"
NC = "\033[0m"  # No color

# Function to list available branches and repositories
def list_branches_repos():
    os.system("git branch -a")
    os.system("git remote -v")

# Function to switch to a branch
def switch_branch():
    branch_name = input("Enter the name of the branch you want to switch to: ")
    os.system(f"git checkout {branch_name}")

# Function to create a new branch or repository
def create_branch_repo():
    branch_repo_name = input("Enter the name of the branch or repository you want to create: ")
    os.system(f"git branch {branch_repo_name}")

# Function to search for a file
def search_file():
    file_name = input("Enter the name of the file you want to search for: ")
    os.system(f"git ls-files | grep {file_name}")

# Function to list tracked files for commit
def list_tracked_files():
    tracked_files = []
    output = os.popen("git status --porcelain").read()
    lines = output.splitlines()
    for line in lines:
        if line.startswith("M ") or line.startswith("A "):
            tracked_files.append(line[3:])
    return tracked_files

# Function to handle Git add operation
def handle_git_add():
    display_location_branch()

    # Get the list of tracked and untracked files
    tracked_files = list_tracked_files()
    untracked_files = []
    output = os.popen("git status --porcelain").read()
    lines = output.splitlines()
    for line in lines:
        if line.startswith("??"):
            untracked_files.append(line[3:])

    # Display the tracked and untracked files with numbers
    print(f"{ORANGE}Tracked files:{NC}")
    for index, file_path in enumerate(tracked_files, start=1):
        print(f"  {index}. {GREEN}{file_path}{NC}")

    print(f"{ORANGE}Untracked files:{NC}")
    for index, file_path in enumerate(untracked_files, start=1):
        print(f"  {index}. {RED}{file_path}{NC}")

    # Get user's selection for files to add
    add_choices = input("Enter the numbers of the files/directories you want to add (separated by spaces) "
                        "or press 0 to skip: ")
    if add_choices.strip() == "0":
        print("Skipping adding files.")
    else:
        try:
            add_choices = [int(choice) for choice in add_choices.split()]
            for choice in add_choices:
                if 1 <= choice <= len(tracked_files):
                    file_path = tracked_files[choice - 1]
                    os.system(f'git add "{file_path}"')
                    print(f"Added {file_path} to the staging area.")
                elif 1 <= choice - len(tracked_files) <= len(untracked_files):
                    file_path = untracked_files[choice - len(tracked_files) - 1]
                    os.system(f'git add "{file_path}"')
                    print(f"Added {file_path} to the staging area.")
                else:
                    print(f"Invalid file number: {choice}")
        except ValueError:
            print("Invalid input. Skipping adding files.")

# Function to handle Git commit operation
def handle_git_commit():
    display_location_branch()

    # Get the list of tracked files
    tracked_files = list_tracked_files()

    # Display the tracked files with numbers
    print("Tracked files for commit:")
    for index, file_path in enumerate(tracked_files, start=1):
        print(f"  {index}. {GREEN}{file_path}{NC}")

    commit_choice = input("Do you want to commit any of these files? (y/n) ")

    if commit_choice.lower() == "y":
        commit_numbers = input("Enter the numbers of the files you want to commit (separated by spaces): ")
        try:
            commit_numbers = [int(number) for number in commit_numbers.split()]
            commit_message = input("Enter the commit message: ")
            for number in commit_numbers:
                if 1 <= number <= len(tracked_files):
                    file_path = tracked_files[number - 1]
                    os.system(f'git add "{file_path}"')
                else:
                    print(f"Invalid file number: {number}")
            os.system(f'git commit -m "{commit_message}"')
            print("Files committed successfully.")
        except ValueError:
            print("Invalid input.")
    else:
        print("No files committed.")

# Function to handle Git push operation
def handle_git_push():
    git_username = input("Username for 'https://github.com': ")
    git_password = input(f"Password for 'https://{git_username}@github.com': ")
    os.system(f'git config credential.helper store')
    os.system(f'echo "https://{git_username}:{git_password}@github.com" >> .git/credentials')
    os.system(f'git push origin {current_branch}')

# Main program loop
while True:
    print(f"{ORANGE}Select an option:{NC}")
    print("1) List available branches and repositories and switch to a branch")
    print("2) Create a new branch or repository")
    print("3) Search for a file")
    print("4) Continue with the Git workflow")
    print("5) Exit")

    user_choice = input()

    if user_choice == "1":
        list_branches_repos()
        switch_choice = input("Do you want to switch to a branch? (y/n) ")
        if switch_choice.lower() == "y":
            switch_branch()

    elif user_choice == "2":
        create_branch_repo()

    elif user_choice == "3":
        search_file()

    elif user_choice == "4":
        git_choice = input("Do you want to continue with the Git workflow? (y/n) ")
        if git_choice.lower() == "y":
            print("Select an option:")
            print("1) Add files or directories")
            print("2) List tracked files for commit")
            print("3) Commit")
            print("4) Push")
            print("5) Commit and Push")
            print("6) Pull")
            print("7) Select a commit")
            print("8) Go back to the previous menu")
            
            git_workflow_choice = input()
            
            if git_workflow_choice == "1":
                handle_git_add()
            
            elif git_workflow_choice == "2":
                handle_git_commit()
            
            elif git_workflow_choice == "3":
                handle_git_commit()
            
            elif git_workflow_choice == "4":
                handle_git_push()
            
            elif git_workflow_choice == "5":
                handle_git_commit()
                handle_git_push()
            
            elif git_workflow_choice == "6":
                os.system("git pull")
                print("Pull successful.")
            
            elif git_workflow_choice == "7":
                os.system("git log --oneline")
                commit_hash = input("Enter the commit hash: ")
                os.system(f"git checkout {commit_hash}")
            
            elif git_workflow_choice == "8":
                continue
            
            else:
                print("Invalid option. Please select a valid option.")
            
        else:
            continue

    elif user_choice == "5":
        break

    else:
        print("Invalid option. Please select a valid option.")

           
