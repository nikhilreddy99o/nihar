import os

# Color codes for formatting
GREEN = "\033[1;32m"
RED = "\033[1;31m"
ORANGE = "\033[1;33m"
PINK = "\033[1;35m"
NC = "\033[0m"

def list_available_branches_repos():
    print(f"{ORANGE}Current branch:{NC} {GREEN}{get_current_branch()}{NC}\n")
    
    print(f"{ORANGE}Available branches:{NC}")
    os.system("git branch -a")
    
    print(f"{ORANGE}Available repositories:{NC}")
    os.system("git remote -v")

def get_current_branch():
    return os.popen("git branch --show-current").read().strip()

def create_new_branch_repository():
    branch_name = input("Enter the name of the new branch/repository: ")
    os.system(f"git checkout -b {branch_name}")

def search_for_file():
    file_name = input("Enter the name of the file to search for: ")
    os.system(f"git ls-files | grep {file_name}")

def handle_git_add():
    os.system("git status")
    print(f"{ORANGE}Untracked files:{NC}")
    untracked_files = os.popen("git ls-files --others --exclude-standard").read().splitlines()
    for index, file_path in enumerate(untracked_files, 1):
        print(f"  {index}. {RED}{file_path}{NC}")
    
    print(f"{ORANGE}Enter the numbers of the files/directories you want to add (separated by spaces) or press 0 to skip:{NC}")
    selected_files = input().split()
    if "0" not in selected_files:
        files_to_add = [untracked_files[int(index) - 1] for index in selected_files]
        os.system(f"git add {' '.join(files_to_add)}")
        print("Files added successfully.")

def list_tracked_files():
    tracked_files = os.popen("git ls-files").read().splitlines()
    untracked_files = os.popen("git ls-files --others --exclude-standard").read().splitlines()
    
    print(f"{ORANGE}Current location:{NC} {PINK}{os.getcwd()}{NC}")
    print(f"{ORANGE}Current branch:{NC} {GREEN}{get_current_branch()}{NC}\n")
    
    if tracked_files:
        print(f"{ORANGE}Tracked files:{NC}")
        for index, file_path in enumerate(tracked_files, 1):
            print(f"  {index}. {GREEN}{file_path}{NC}")
    else:
        print(f"{ORANGE}No tracked files found.{NC}")
    
    if untracked_files:
        print(f"{ORANGE}Untracked files:{NC}")
        for index, file_path in enumerate(untracked_files, 1):
            print(f"  {index}. {RED}{file_path}{NC}")
    else:
        print(f"{ORANGE}No untracked files found.{NC}")

def handle_git_commit():
    list_tracked_files()
    print(f"{ORANGE}Enter the numbers of the files/directories you want to commit (separated by spaces) or press 0 to skip:{NC}")
    selected_files = input().split()
    if "0" not in selected_files:
        files_to_commit = [tracked_files[int(index) - 1] for index in selected_files]
        commit_message = input("Enter the commit message: ")
        os.system(f"git commit {' '.join(files_to_commit)} -m '{commit_message}'")
        print("Files committed successfully.")

def handle_git_push():
    username = input("Username for 'https://github.com': ")
    password = input(f"Password for 'https://{username}@github.com': ")
    os.system(f"git push https://{username}:{password}@github.com/nikhilreddy99o/nihar.git/")

def handle_commit_push():
    handle_git_commit()
    handle_git_push()

while True:
    print(f"{ORANGE}Select an option:{NC}")
    print("1) List available branches and repositories and switch to a branch")
    print("2) Create a new branch or repository")
    print("3) Search for a file")
    print("4) Continue with the Git workflow")
    print("5) Exit")
    
    user_choice = input()
    
    if user_choice == "1":
        list_available_branches_repos()
        
        switch_branch = input(f"{ORANGE}Do you want to switch to a branch? (y/n) {NC}")
        if switch_branch.lower() == "y":
            branch_name = input("Enter the name of the branch to switch to: ")
            os.system(f"git checkout {branch_name}")
        
    elif user_choice == "2":
        create_new_branch_repository()
    
    elif user_choice == "3":
        search_for_file()
    
    elif user_choice == "4":
        while True:
            print(f"{ORANGE}Select an option:{NC}")
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
                list_tracked_files()
            
            elif git_workflow_choice == "3":
                handle_git_commit()
            
            elif git_workflow_choice == "4":
                handle_git_push()
            
            elif git_workflow_choice == "5":
                handle_commit_push()
            
            elif git_workflow_choice == "6":
                os.system("git pull")
                print("Pull successful.")
            
            elif git_workflow_choice == "7":
                os.system("git log --oneline")
                commit_hash = input("Enter the commit hash: ")
                os.system(f"git checkout {commit_hash}")
            
            elif git_workflow_choice == "8":
                break
            
            else:
                print("Invalid option. Please select a valid option.")
            
    elif user_choice == "5":
        break

    else:
        print("Invalid option. Please select a valid option.")

