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
    result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
    branches = result.stdout.strip().splitlines()
    print("Branches:")
    for branch in branches:
        print(f"  - {branch.strip('* ')}")

def create_branch(branch_name):
    subprocess.run(['git', 'branch', branch_name])
    print(f"Created branch '{branch_name}'.")

def switch_to_branch(branch_name):
    subprocess.run(['git', 'checkout', branch_name])
    print(f"Switched to branch '{branch_name}'.")

def merge_branch(branch_name):
    subprocess.run(['git', 'merge', branch_name])
    print(f"Merged branch '{branch_name}' into the current branch.")

def handle_conflicts():
    # The user should manually resolve any conflicts before continuing.
    print("Please resolve any conflicts and then continue.")

def display_status_with_numbers():
    result = subprocess.run(['git', 'status', '-s'], capture_output=True, text=True)
    output_lines = result.stdout.splitlines()
    if not output_lines:
        print("No changes found.")
        return None

    print("Files with status:")
    for idx, line in enumerate(output_lines, start=1):
        print(f"{idx}. {line}")

    return output_lines

def git_add_and_commit():
    status_lines = display_status_with_numbers()
    if status_lines:
        selected_files = input("Enter the file numbers to add (space-separated): ").split()
        selected_files = [int(num) for num in selected_files]
        files_to_add = [status_lines[idx - 1].split(" ", 1)[-1] for idx in selected_files]

        commit_message = input("Enter the commit message: ")
        commit_changes(commit_message)

def git_push(branch_name):
    subprocess.run(['git', 'push', 'origin', branch_name])
    print(f"Pushed changes to branch '{branch_name}'.")

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

