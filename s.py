import subprocess

def get_git_user_info():
    name = subprocess.run(['git', 'config', '--global', 'user.name'], capture_output=True, text=True).stdout.strip()
    email = subprocess.run(['git', 'config', '--global', 'user.email'], capture_output=True, text=True).stdout.strip()
    return name, email

def set_git_user_info(name, email):
    subprocess.run(['git', 'config', '--global', 'user.name', name])
    subprocess.run(['git', 'config', '--global', 'user.email', email])
    print(f"Git user info set: name='{name}', email='{email}'.")

def make_changes(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Made changes to '{filename}'.")

def commit_changes(message):
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', message])
    print(f"Committed changes with message: '{message}'.")

def list_branches():
    subprocess.run(['git', 'fetch', '--all'])  # Fetch all remote branches
    result = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True)
    branches = result.stdout.strip().splitlines()
    print("Branches:")
    for branch in branches:
        current_indicator = '*' if branch.startswith('*') else ' '
        branch_name = branch.strip('* ')
        print(f" {current_indicator} {branch_name}")

# Rest of the functions and menu remain unchanged

if __name__ == "__main__":
    name, email = get_git_user_info()

    if not name or not email:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        set_git_user_info(name, email)

    while True:
        print("\nOptions:")
        print("1. List branches")
        print("2. Create and switch to a new branch")
        print("3. Make changes on the current branch")
        print("4. Commit changes")
        print("5. Merge branches")
        print("6. Display git status")
        print("7. Git add and commit changes")
        print("8. Git push to branch")
        print("9. Exit")

        # Show the current branch at all times
        current_branch_result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        current_branch = current_branch_result.stdout.strip()
        print(f"\nCurrent branch: {current_branch}")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_branches()
        elif choice == "2":
            branch_name = input("Enter the new branch name: ")
            create_branch(branch_name)
            switch_to_branch(branch_name)
        elif choice == "3":
            filename = input("Enter the filename to change: ")
            content = input("Enter the content to add to the file: ")
            make_changes(filename, content)
        elif choice == "4":
            commit_message = input("Enter the commit message: ")
            commit_changes(commit_message)
        elif choice == "5":
            branch_name = input("Enter the branch name to merge into the current branch: ")
            merge_branch(branch_name)
        elif choice == "6":
            display_status_with_numbers()
        elif choice == "7":
            git_add_and_commit()
        elif choice == "8":
            branch_name = input("Enter the branch name to push changes: ")
            git_push(branch_name)
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Git workflow completed successfully.")

