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
    echo "Do you want to create a new branch or repository? (y/n)"
    read create_choice

    if [ "$create_choice" = "y" ]; then
        echo "Enter the name of the new branch or repository:"
        read new_name
        git checkout -b $new_name || git init $new_name
    elif [ "$create_choice" = "n" ]; then
        echo "No creation requested."
    else
        echo "Invalid choice. Exiting..."
        exit 1
    fi
}

# Function to search for Git-related files in the system
function search_git_files() {
    echo "Do you want to search for Git-related files? (y/n)"
    read search_choice

    if [ "$search_choice" = "y" ]; then
        echo "Enter the file name:"
        read file_name

        if [ -n "$(command -v git)" ]; then
            echo "Searching for Git-related files..."
            sudo_command=""
            if [ "$(id -u)" -ne 0 ]; then
                echo "Searching without sudo..."
            else
                echo "Searching with sudo..."
                sudo_command="sudo"
            fi

            $sudo_command find / -type f -name "$file_name" -exec sh -c 'git rev-parse --is-inside-work-tree "{}" >/dev/null 2>&1 && echo {}' \; 2>/dev/null
        else
            echo "Git is not installed. Cannot search for Git-related files."
        fi
    elif [ "$search_choice" = "n" ]; then
        echo "No search requested."
    else
        echo "Invalid choice. Exiting..."
        exit 1
    fi
}

# Function to select an available branch or repository
function select_branch_repo() {
    echo "Do you want to select an available branch or repository? (y/n)"
    read select_choice

    if [ "$select_choice" = "y" ]; then
        echo "Enter the name of the branch or repository:"
        read branch_repo_name
        git checkout $branch_repo_name
    elif [ "$select_choice" = "n" ]; then
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
    echo "3) Search for Git-related files"
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
            search_git_files
            ;;
        4)
            select_branch_repo
            ;;
        5)
            # Ask for confirmation for each step
            echo "Do you want to continue with the Git workflow? (y/n)"
            read git_confirm
            if [ "$git_confirm" = "y" ]; then
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

