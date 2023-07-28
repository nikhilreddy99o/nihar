#!/bin/bash

# Function to list available branches and repositories
function list_branches_repos() {
    echo "Available branches:"
    git branch -a
    echo "Available repositories:"
    git remote -v
}

# Function to create a new branch or repository
function create_branch_repo() {
    echo "Do you want to create a new branch or repository? (branch/repo)"
    read create_choice

    if [ "$create_choice" = "branch" ]; then
        echo "Enter the name of the new branch:"
        read new_branch_name
        git checkout -b $new_branch_name
    elif [ "$create_choice" = "repo" ]; then
        echo "Enter the name of the new repository:"
        read new_repo_name
        git init $new_repo_name
    else
        echo "Invalid choice. Exiting..."
        exit 1
    fi
}

# Function to search for a file in the system
function search_file() {
    echo "Do you want to search for a file? (yes/no)"
    read search_choice

    if [ "$search_choice" = "yes" ]; then
        echo "Enter the file name:"
        read file_name
        echo "Do you want to search with sudo? (yes/no)"
        read sudo_choice

        if [ "$sudo_choice" = "yes" ]; then
            # Check if sudo is available
            if command -v sudo &>/dev/null; then
                # Ask for sudo credentials
                sudo -v
                echo "Searching with sudo..."
                sudo find / -type f -name "$file_name" 2>/dev/null
            else
                echo "sudo is not available. Searching without sudo..."
                find / -type f -name "$file_name" 2>/dev/null
            fi
        else
            echo "Searching without sudo..."
            find / -type f -name "$file_name" 2>/dev/null
        fi
    elif [ "$search_choice" = "no" ]; then
        echo "No search requested."
    else
        echo "Invalid choice. Exiting..."
        exit 1
    fi
}

# Function to select an available branch or repository
function select_branch_repo() {
    echo "Do you want to select an available branch or repository? (yes/no)"
    read select_choice

    if [ "$select_choice" = "yes" ]; then
        echo "Do you want to select a branch or repository? (branch/repo)"
        read select_branch_repo_choice

        if [ "$select_branch_repo_choice" = "branch" ]; then
            echo "Enter the name of the branch:"
            read branch_repo_name
            git checkout $branch_repo_name
        elif [ "$select_branch_repo_choice" = "repo" ]; then
            echo "Enter the name of the repository:"
            read branch_repo_name
            # Some additional checks here if the repository exists
            echo "Selected repository: $branch_repo_name"
        else
            echo "Invalid choice. Exiting..."
            exit 1
        fi
    elif [ "$select_choice" = "no" ]; then
        echo "No selection requested."
    else
        echo "Invalid choice. Exiting..."
        exit 1
    fi
}

# Continue with the Git workflow
while true; do
    echo "Select an option:"
    echo "1) List available branches and repositories"
    echo "2) Create a new branch or repository"
    echo "3) Search for a file"
    echo "4) Select an available branch or repository"
    echo "5) Continue with the Git workflow"
    echo "6) Exit"

    read choice

    case $choice in
        1)
            list_branches_repos
            ;;
        2)
            create_branch_repo
            ;;
        3)
            search_file
            ;;
        4)
            select_branch_repo
            ;;
        5)
            # Ask for confirmation for each step
            echo "Do you want to continue with the Git workflow? (yes/no)"
            read git_confirm
            if [ "$git_confirm" = "yes" ]; then
                # Git workflow
                while true; do
                    echo "Select an option:"
                    echo "1) Add"
                    echo "2) Commit"
                    echo "3) Push"
                    echo "4) Add, Commit, and Push"
                    echo "5) Pull"
                    echo "6) Go back to the previous menu"

                    read git_choice

                    case $git_choice in
                        1)
                            git add .
                            ;;
                        2)
                            echo "Enter the commit message:"
                            read commit_message
                            git commit -m "$commit_message"
                            ;;
                        3)
                            git push
                            ;;
                        4)
                            git add .
                            echo "Enter the commit message:"
                            read commit_message
                            git commit -m "$commit_message"
                            git push
                            ;;
                        5)
                            echo "Enter the branch to pull from:"
                            read pull_branch
                            git pull origin $pull_branch
                            ;;
                        6)
                            break
                            ;;
                        *)
                            echo "Invalid option. Please try again."
                            ;;
                    esac
                done
            else
                echo "Git workflow skipped."
            fi
            ;;
        6)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done

