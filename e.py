def list_tracked_files():
    display_location_branch()

    # Get the git status output
    git_status_output = os.popen('git status -s').readlines()

    tracked_files = []

    # Process git status output and collect tracked files
    for line in git_status_output:
        status = line[:2].strip()
        file_name = line[3:].strip()
        if status != '??':
            tracked_files.append(file_name)

    # Display the tracked files
    print("Tracked files:")
    for index, file_name in enumerate(tracked_files, start=1):
        print(f"  {index}. {file_name}")

    add_numbers = input("Enter the numbers of the files you want to commit "
                        "(separated by spaces) or press 0 to skip: ")

    if add_numbers == '0':
        print("Skipping adding files.")
    else:
        numbers_arr = add_numbers.split()
        selected_files = []

        for number in numbers_arr:
            try:
                file_path = tracked_files[int(number) - 1]
                if file_path:
                    selected_files.append(file_path)
                else:
                    print(f"Invalid number: {number}. Skipping...")
            except ValueError:
                print(f"Invalid number: {number}. Skipping...")
            except IndexError:
                print(f"Invalid number: {number}. Skipping...")

        if not selected_files:
            print("No files selected for commit.")
        else:
            print("Selected files for commit:")
            for index, file_path in enumerate(selected_files, start=1):
                print(f"  {index}. {file_path}")

            commit_choice = input("Do you want to commit the selected files? (y/n) ")

            if commit_choice.lower() == "y":
                commit_message = input("Enter the commit message: ")

                for file_path in selected_files:
                    os.system(f'git add "{file_path}"')

                os.system(f'git commit -m "{commit_message}"')
                print("Files committed successfully.")

                push_choice = input("Do you want to push the changes to the remote repository? (y/n) ")
                if push_choice.lower() == "y":
                    remote_branch = input("Enter the remote branch name: ")
                    os.system(f'git push origin "{remote_branch}"')
                    print("Changes pushed to the remote repository.")
                else:
                    print("Changes not pushed.")

            else:
                print("Files not committed.")
elif choice == "4":
    git_confirm = input("Do you want to continue with the Git workflow? (y/n) ")
    if git_confirm == "y" or git_confirm == "Y":
        while True:
            print("Select an option:")
            print("1) Add files or directories")
            print("2) List tracked files for commit")
            print("3) Commit")
            print("4) Push")
            print("5) Commit and Push")
            print("6) Pull")
            print("7) Select a commit")
            print("8) Go back to the previous menu")

            git_choice = input()

            if git_choice == "1":
                handle_add_file_directory()
            elif git_choice == "2":
                list_tracked_files()
            elif git_choice == "3":
                commit_message = input("Enter the commit message: ")
                os.system(f'git commit -m "{commit_message}"')
            elif git_choice == "4":
                os.system('git push')
            elif git_choice == "5":
                list_tracked_files()
                commit_message = input("Enter the commit message: ")
                os.system(f'git commit -m "{commit_message}"')
                os.system('git push')
            elif git_choice == "6":
                pull_branch = input("Enter the branch to pull from: ")
                os.system(f'git pull origin "{pull_branch}"')
            elif git_choice == "7":
                list_commits()
                commit_hash = input("Enter the commit hash: ")
                os.system(f'git reset --soft {commit_hash}')
                commit_message = input("Enter the new commit message: ")
                os.system(f'git commit --amend -m "{commit_message}"')
            elif git_choice == "8":
                break
            else:
                print("Invalid option. Please try again.")
    else:
        print("Git workflow skipped.")

