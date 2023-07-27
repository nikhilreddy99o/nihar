#!/bin/bash

# Function to display available branches
display_branches() {
    git branch -a
}

# Function to display available repositories
display_repositories() {
    git remote -v
}

# Function to create a new branch
create_branch() {
    echo "Enter the branch name:"
    read branch_name
    git checkout -b $branch_name
}

# Function to create a new repository
create_repository() {
    echo "Enter the new repository name:"
    read repository_name
    git init $repository_name
}

# Display available branches and repositories
echo "Available branches:"
display_branches
echo "Available repositories:"
display_repositories

# Ask the user to choose a branch or repository
echo "Choose a number to create a new branch or repository (0 to continue with the current branch):"
read selection

if [ "$selection" -eq 0 ]; then
    echo "Continuing with the current branch."
else
    echo "Do you want to create a branch or repository? (branch/repo)"
    read create_choice

    if [ "$create_choice" = "branch" ]; then
        create_branch
    elif [ "$create_choice" = "repo" ]; then
        create_repository
    else
        echo "Invalid choice. Exiting..."
        exit 1
    fi
fi

# Continue with the Git workflow
while true; do
    echo "Select an option:"
    echo "1) Add"
    echo "2) Commit"
    echo "3) Push"
    echo "4) Add, Commit, and Push"
    echo "5) Pull"
    echo "6) Exit"

    read choice

    case $choice in
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
            echo "Exiting..."
            break
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done
