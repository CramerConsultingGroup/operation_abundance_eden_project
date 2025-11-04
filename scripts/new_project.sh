#!/bin/bash

# Script to create a new project in the repository
# Usage: ./scripts/new_project.sh "Project Name"

set -e

# Check if project name is provided
if [ -z "$1" ]; then
    echo "Error: Project name is required"
    echo "Usage: ./scripts/new_project.sh \"Project Name\""
    exit 1
fi

PROJECT_NAME="$1"
# Convert project name to a valid directory name (lowercase, replace spaces with underscores)
PROJECT_DIR=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')

# Base directory for projects
PROJECTS_BASE="projects"
PROJECT_PATH="$PROJECTS_BASE/$PROJECT_DIR"

# Check if project already exists
if [ -d "$PROJECT_PATH" ]; then
    echo "Error: Project '$PROJECT_NAME' already exists at $PROJECT_PATH"
    exit 1
fi

# Create project directory
echo "Creating new project: $PROJECT_NAME"
mkdir -p "$PROJECT_PATH"

# Create project structure
mkdir -p "$PROJECT_PATH/docs"
mkdir -p "$PROJECT_PATH/src"
mkdir -p "$PROJECT_PATH/assets"

# Create README for the project
cat > "$PROJECT_PATH/README.md" << EOF
# $PROJECT_NAME

## Overview

This is the $PROJECT_NAME project.

## Description

[Add project description here]

## Status

- **Created**: $(date +%Y-%m-%d)
- **Status**: Active

## Team

- [Add team members here]

## Resources

- [Add relevant links and resources here]

## Documentation

Additional documentation can be found in the \`docs/\` directory.

## Getting Started

[Add instructions for getting started with this project]

EOF

# Create a basic project info file
cat > "$PROJECT_PATH/project.json" << EOF
{
  "name": "$PROJECT_NAME",
  "directory": "$PROJECT_DIR",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "active",
  "description": "Add project description",
  "team": [],
  "tags": []
}
EOF

# Create an example document
cat > "$PROJECT_PATH/docs/overview.md" << EOF
# $PROJECT_NAME Overview

## Purpose

[Describe the purpose of this project]

## Goals

- [Goal 1]
- [Goal 2]
- [Goal 3]

## Timeline

[Add timeline information]

## Notes

[Add any additional notes]

EOF

echo "✓ Project created successfully at: $PROJECT_PATH"
echo ""
echo "Project structure:"
echo "  $PROJECT_PATH/"
echo "  ├── README.md          - Project documentation"
echo "  ├── project.json       - Project metadata"
echo "  ├── docs/              - Additional documentation"
echo "  │   └── overview.md"
echo "  ├── src/               - Source code (if applicable)"
echo "  └── assets/            - Project assets (images, files, etc.)"
echo ""
echo "Next steps:"
echo "1. Edit $PROJECT_PATH/README.md to add project details"
echo "2. Update $PROJECT_PATH/project.json with metadata"
echo "3. Add documentation to $PROJECT_PATH/docs/"
echo "4. Commit your changes: git add $PROJECT_PATH && git commit -m 'Add $PROJECT_NAME project'"
