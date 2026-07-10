.PHONY: notify new-project help

help:
	@echo "Available targets:"
	@echo "  make notify          - Run manual pipeline checks"
	@echo "  make new-project     - Create a new project (will prompt for name)"
	@echo "  make help            - Show this help message"

new-project:
	@if [ -z "$$PROJECT_NAME" ]; then \
		read -p "Enter project name: " project_name; \
		./scripts/new_project.sh "$$project_name"; \
	else \
		./scripts/new_project.sh "$$PROJECT_NAME"; \
	fi

notify:
	@echo "Running manual pipeline checks..."
	@if [ -z "$$SLACK_WEBHOOK_URL" ]; then \
		echo "Warning: SLACK_WEBHOOK_URL environment variable is not set."; \
		echo "Slack notifications will not be sent."; \
	else \
		echo "SLACK_WEBHOOK_URL is configured."; \
	fi
	@if [ -z "$$DISCORD_WEBHOOK_URL" ]; then \
		echo "Warning: DISCORD_WEBHOOK_URL environment variable is not set."; \
		echo "Discord notifications will not be sent."; \
	else \
		echo "DISCORD_WEBHOOK_URL is configured."; \
	fi
	@echo "Manual pipeline check complete."
	@echo "To trigger the CI notification workflow, push to the main branch or create a pull request."
