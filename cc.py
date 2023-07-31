import os
import getpass

# Color codes for formatting
GREEN = "\033[1;32m"
RED = "\033[1;31m"
ORANGE = "\033[1;33m"
PINK = "\033[1;35m"
NC = "\033[0m"

def get_github_credentials():
    github_username = input("Enter your GitHub username: ")
    github_token = getpass.getpass("Enter your GitHub personal access token: ")
    return github_username, github_token

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
    print(f"{ORANGE}Current working directory:{NC}")
    os.system("pwd")
    
    print(f"{ORANGE}Current branch:{NC}")
    os.system("git branch --show-current")
    
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

def handle_git_commit():
    print(f"{ORANGE}Current working directory:{NC}")
    os.system("pwd")
    
    print(f"{ORANGE}Current branch:{NC}")
    os.system("git branch --show-current")
    
    os.system("git status")
    tracked_files = os.popen("git ls-files").read().splitlines()
    print(f"{ORANGE}Tracked files:{NC}")
    for index, file_path in enumerate(tracked_files, 1):
        print(f"  {index}. {GREEN}{file_path}{NC}")

    print(f"{ORANGE}Enter the numbers of the files/directories you want to commit (separated by spaces) or press 0 to skip:{NC}")
    selected_files = input().split()
    if "0" not in selected_files:
        files_to_commit = [tracked_files[int(index) - 1] for index in selected_files]
        commit_message = input("Enter the commit message: ")
        os.system(f"git commit {' '.join(files_to_commit)} -m '{commit_message}'")
        print("Files committed successfully.")

def handle_git_push(github_username, github_token):
    if not github_username or not github_token:
        print("Please provide your GitHub credentials.")
        return

    repository_url = f"https://{github_username}:{github_token}@github.com/{github_username}/nihar.git"
    os.system(f"git push {repository_url}")
    print("Push successful.")

def handle_commit_push(github_username, github_token):
    handle_git_commit()
    handle_git_push(github_username, github_token)

def handle_git_cherry_pick():
    os.system("git log --oneline")
    commit_hash = input(f"{ORANGE}Enter the commit number to cherry-pick: {NC}")
    os.system(f"git cherry-pick {commit_hash}")
    print("Cherry-pick successful.")

def handle_branch_switch():
    branch_name = input("Enter the name of the branch to switch to: ")
    os.system(f"git checkout {branch_name}")

def handle_git_merge():
    print(f"{ORANGE}Listing all available branches from GitHub...{NC}")
    os.system("git fetch --all")
    os.system("git branch -r")
    remote_branches = os.popen("git branch -r").read().splitlines()
    print(f"{ORANGE}Available remote branches:{NC}")
    for index, branch in enumerate(remote_branches, 1):
        print(f"  {index}. {branch.strip()}")

    print(f"{ORANGE}Enter the numbers of the branches to merge (separated by spaces):{NC}")
    selected_branches = input().split()
    branches_to_merge = [remote_branches[int(index) - 1].strip() for index in selected_branches]

    for branch in branches_to_merge:
        print(f"{ORANGE}Merging {branch} into current branch...{NC}")
        os.system(f"git merge {branch} --allow-unrelated-histories")

github_username = None
github_token = None

while True:
    print(f"{ORANGE}Select an option:{NC}")
    print("1) List available branches and repositories and switch to a branch")
    print("2) Create a new branch or repository")
    print("3) Search for a file")
    print("4) Continue with the Git workflow")
    print("5) Merge branches from GitHub")
    print("6) Exit")
    
    user_choice = input()
    
    if user_choice == "1":
        list_available_branches_repos()
        
        switch_branch = input(f"{ORANGE}Do you want to switch to a branch? (y/n) {NC}")
        if switch_branch.lower() == "y":
            handle_branch_switch()
        
    elif user_choice == "2":
        create_new_branch_repository()
    
    elif user_choice == "3":
        search_for_file()
    
    elif user_choice == "4":
        if not github_username or not github_token:
            github_username, github_token = get_github_credentials()
        else:
            change_credentials = input(f"{ORANGE}Do you want to change GitHub credentials? (y/n) {NC}")
            if change_credentials.lower() == "y":
                github_username, github_token = get_github_credentials()
            
        while True:
            print(f"{ORANGE}Select an option:{NC}")
            print("1) Add files or directories")
            print("2) List tracked files for commit")
            print("3) Commit")
            print("4) Push")
            print("5) Commit and Push")
            print("6) Pull")
            print("7) Select a commit")
            print("8) Cherry-pick")
            print("9) Go back to the previous menu")
            
            git_workflow_choice = input()
            
            if git_workflow_choice == "1":
                handle_git_add()
            
            elif git_workflow_choice == "2":
                handle_git_commit()
            
            elif git_workflow_choice == "3":
                handle_git_commit()
            
            elif git_workflow_choice == "4":
                handle_git_push(github_username, github_token)
            
            elif git_workflow_choice == "5":
                handle_commit_push(github_username, github_token)
            
            elif git_workflow_choice == "6":
                os.system("git pull")
                print("Pull successful.")
            
            elif git_workflow_choice == "7":
                os.system("git log --oneline")
                commit_hash = input("Enter the commit hash: ")
                os.system(f"git checkout {commit_hash}")
            
            elif git_workflow_choice == "8":
                handle_git_cherry_pick()
            
            elif git_workflow_choice == "9":
                break
            
            else:
                print("Invalid option. Please select a valid option.")

    elif user_choice == "5":
        handle_git_merge()

    elif user_choice == "6":
        break

    else:
        print("Invalid option. Please select a valid option.")
