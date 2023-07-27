#!/bin/bash

# Function to display numbered list and prompt for selection
function prompt_with_numbered_list {
    local options=("$@")
    for ((i = 0; i < ${#options[@]}; i++)); do
        echo "$((i + 1)). ${options[i]}"
    done
    read -p "Enter the number of your choice: " choice_number
    choice=$((choice_number - 1))
    echo "${options[choice]}"
}

# Function to display available branches
function show_branches {
    branches=$(git branch | sed 's/*//')
    echo "Available branches:"
    echo "$branches"
}

# Function to add and commit files
function add_and_commit_files {
    local file_names=("$@")
    for file in "${file_names[@]}"; do
        if [ -f "$file" ]; then
            git add "$file"
            read -p "Enter the commit message for '$file': " commit_msg
            git commit -m "$commit_msg"
            echo "File '$file' added and committed successfully!"
        else
            echo "File '$file' does not exist or is not a regular file. Skipping..."
            return 1
        fi
    done
    return 0
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

# Prompt user to select all actions or specific actions
options=("Add and commit files" "Show available files" "Show available branches" "Show available repositories")
echo "Select actions to perform:"
echo "0. Perform all actions"
selected_actions=$(prompt_with_numbered_list "${options[@]}")

case "$selected_actions" in
    "Add and commit files")
        # Get the file name(s) from user input
        read -p "Enter the file name(s) to add and commit (separate multiple files with space): " file_names

        # Check if any file(s) were provided
        if [ -z "$file_names" ]; then
            echo "No files provided. Exiting..."
            exit 1
        fi

        # Convert the user input into an array
        file_array=($file_names)

        # Perform add and commit
        add_and_commit_files "${file_array[@]}"
        if [ $? -ne 0 ]; then
            echo "Error occurred during add and commit. Exiting..."
            exit 1
        fi
        ;;

    "Show available files")
        selected_file=$(prompt_for_file_selection)
        # Perform actions with the selected file (if needed)
        echo "Selected file: $selected_file"
        ;;

    "Show available branches")
        selected_branch=$(prompt_for_branch_selection)
        # Perform actions with the selected branch (if needed)
        echo "Selected branch: $selected_branch"
        ;;

    "Show available repositories")
        selected_repository=$(prompt_for_repository_selection)
        # Perform actions with the selected repository (if needed)
        echo "Selected repository: $selected_repository"
        ;;

    "Perform all actions")
        # Get the file name(s) from user input
        read -p "Enter the file name(s) to add and commit (separate multiple files with space): " file_names

        # Check if any file(s) were provided
        if [ -z "$file_names" ]; then
            echo "No files provided. Exiting..."
            exit 1
        fi

        # Convert the user input into an array
        file_array=($file_names)

        # Perform add and commit
        add_and_commit_files "${file_array[@]}"
        if [ $? -ne 0 ]; then
            echo "Error occurred during add and commit. Exiting..."
            exit 1
        fi

        # Display available branches
        show_branches

        # Prompt for the branch name
        read -p "Enter the name of the branch to push to: " branch_name

        # Push changes to the remote repository
        echo "Pushing changes to $branch_name..."
        git push origin "$branch_name"
        if [ $? -ne 0 ]; then
            echo "Error occurred during push. Exiting..."
            exit 1
        fi

        # Ask for permission to merge
        read -p "Do you want to merge changes? (y/n): " merge_choice

        if [ "$merge_choice" = "y" ] || [ "$merge_choice" = "Y" ]; then
            # Merge changes into the branch
            git checkout "$branch_name"
            git merge origin/"$branch_name"
            if [ $? -ne 0 ]; then
                echo "Error occurred during merge. Exiting..."
                exit 1
            fi
            echo "Changes merged successfully!"
        else
            echo "Changes pushed to the remote repository. Merge skipped."
        fi
        ;;
    
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

