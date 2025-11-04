.PHONY: notify
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
