#!/bin/bash

# Function to display a numbered menu and prompt for selection
function prompt_with_numbered_menu {
    local options=("$@")
    for ((i = 0; i < ${#options[@]}; i++)); do
        echo "$((i + 1)). ${options[i]}"
    done
    read -p "Enter the number of your choice: " choice_number
    if [[ $choice_number =~ ^[1-9]$ ]]; then
        choice=$((choice_number - 1))
        echo "${options[choice]}"
    else
        echo "Invalid choice. Please select a valid option."
        echo
        return 1
    fi
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
    selected_file=$(prompt_with_numbered_menu "${files[@]}")
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
    selected_branch=$(prompt_with_numbered_menu "${branches[@]}")
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
    selected_repository=$(prompt_with_numbered_menu "${repositories[@]}")
    echo "$selected_repository"
}

# Show the main menu
main_menu=("Add files" "Commit files" "Show available files" "Show available branches" "Show available repositories" "Exit")

while true; do
    echo "Select an action:"
    selected_action=$(prompt_with_numbered_menu "${main_menu[@]}")

    case "$selected_action" in
        "Add files")
            # Get the file name(s) from user input
            read -p "Enter the file name(s) to add (separate multiple files with space): " file_names

            # Check if any file(s) were provided
            if [ -z "$file_names" ]; then
                echo "No files provided."
            else
                # Convert the user input into an array
                file_array=($file_names)

                # Perform add
                git add "${file_array[@]}"
                echo "File(s) added successfully!"
            fi
            ;;

        "Commit files")
            # Get the file name(s) from user input
            read -p "Enter the file name(s) to commit (separate multiple files with space): " file_names

            # Check if any file(s) were provided
            if [ -z "$file_names" ]; then
                echo "No files provided."
            else
                # Convert the user input into an array
                file_array=($file_names)

                # Perform commit
                add_and_commit_files "${file_array[@]}"
                if [ $? -ne 0 ]; then
                    echo "Error occurred during commit."
                fi
            fi
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

