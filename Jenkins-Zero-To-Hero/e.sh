#!/bin/bash

# Function to display numbered list and prompt for selection
function prompt_with_numbered_list {
    local options=("$@")
    for ((i = 0; i < ${#options[@]}; i++)); do
        echo "$i) ${options[i]}"
    done
    read -p "Enter the number of your choice: " choice_number
    if [[ "$choice_number" == "0" ]]; then
        echo "all"
    elif [[ $choice_number =~ ^[1-9]$ ]] && [ "$choice_number" -le "${#options[@]}" ]; then
        choice=$((choice_number - 1))
        echo "${options[choice]}"
    else
        echo "Invalid choice. Please select a valid option."
        echo
        return 1
    fi
}

# Function to add and commit files
function add_and_commit_files {
    git add .
    read -p "Enter the commit message: " commit_msg
    git commit -m "$commit_msg"
    echo "Files added and committed successfully!"
}

# Function to push changes to the remote repository
function push_to_remote {
    read -p "Enter the name of the remote repository: " remote_name
    read -p "Enter the name of the branch: " branch_name
    git push "$remote_name" "$branch_name"
    echo "Changes pushed to $remote_name/$branch_name"
}

# Function to get list of files in current directory and its subdirectories
function get_files_in_current_directory {
    files=()
    while IFS= read -r -d $'\0' file; do
        files+=("$file")
    done < <(find . -type f -print0)
    echo "${files[@]}"
}

# Function to display available files and prompt for selection
function prompt_for_file_selection {
    local files=($(get_files_in_current_directory))
    if [ ${#files[@]} -eq 0 ]; then
        echo "No files found in the current directory and its subdirectories. Exiting..."
        exit 1
    fi
    echo "Available files:"
    selected_file=$(prompt_with_numbered_list "${files[@]}")
    echo "$selected_file"
}

# Function to display available branches and prompt for selection
function prompt_for_branch_selection {
    branches=($(git branch | sed 's/*//'))
    if [ ${#branches[@]} -eq 0 ]; then
        echo "No branches found. Exiting..."
        exit 1
    fi
    echo "Available branches:"
    selected_branch=$(prompt_with_numbered_list "${branches[@]}")
    echo "$selected_branch"
}

# Function to display available repositories and prompt for selection
function prompt_for_repository_selection {
    # You can replace the following line with the command to get the list of repositories (if available).
    # Replace the placeholder text with the actual list of repositories.
    repositories=("repo1" "repo2" "repo3" "repo4")
    if [ ${#repositories[@]} -eq 0 ]; then
        echo "No repositories found. Exiting..."
        exit 1
    fi
    echo "Available repositories:"
    selected_repository=$(prompt_with_numbered_list "${repositories[@]}")
    echo "$selected_repository"
}

# Show the main menu
main_menu=("Add and commit files" "Show available files" "Show available branches" "Show available repositories" "Exit")

while true; do
    echo "Select the task to perform:"
    selected_action=$(prompt_with_numbered_list "${main_menu[@]}")

    case "$selected_action" in
        "Add and commit files")
            add_and_commit_files
            ;;

        "Show available files")
            selected_file=$(prompt_for_file_selection)
            # Perform actions with the selected file (if needed)
            echo "Selected file: $selected_file"
            ;;

        "Show available branches")
            show_branches
            ;;

        "Show available repositories")
            selected_repository=$(prompt_for_repository_selection)
            # Perform actions with the selected repository (if needed)
            echo "Selected repository: $selected_repository"
            ;;

        "all")
            add_and_commit_files
            push_to_remote
            ;;

        "Exit")
            echo "Exiting the script."
            exit 0
            ;;

        *)
            # Invalid choice. Loop will continue without exiting.
            ;;
    esac

    echo # Add a blank line for separation
done

