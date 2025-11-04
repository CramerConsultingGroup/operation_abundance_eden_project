# Projects

This directory contains all projects managed in the Operation Abundance Eden Project repository.

## Creating a New Project

To create a new project, use the provided script:

```bash
./scripts/new_project.sh "Your Project Name"
```

This will create a new project directory with the following structure:

```
projects/your_project_name/
├── README.md          - Project documentation
├── project.json       - Project metadata
├── docs/              - Additional documentation
│   └── overview.md
├── src/               - Source code (if applicable)
└── assets/            - Project assets (images, files, etc.)
```

## Project List

To see all projects in this repository, list the subdirectories in this folder:

```bash
ls -l projects/
```

## Project Structure Guidelines

Each project should follow this standard structure:

- **README.md**: Main project documentation including overview, goals, and getting started information
- **project.json**: Structured metadata about the project (name, status, team, tags)
- **docs/**: Additional documentation files
- **src/**: Source code, scripts, or implementation files
- **assets/**: Images, diagrams, files, and other resources

## Managing Projects

### Updating Project Status

Edit the `project.json` file in the project directory to update the status field:

```json
{
  "status": "active|planning|completed|archived"
}
```

### Adding Team Members

Update the team array in `project.json`:

```json
{
  "team": ["@username1", "@username2"]
}
```

### Adding Tags

Update the tags array in `project.json` for categorization:

```json
{
  "tags": ["investment", "technology", "research"]
}
```

## Best Practices

1. Keep project names descriptive and concise
2. Update the README.md regularly with project progress
3. Use the docs/ directory for detailed documentation
4. Keep the project.json metadata up to date
5. Archive projects that are no longer active by updating the status field

## Questions or Issues?

If you encounter any issues creating or managing projects, please open an issue in this repository.
