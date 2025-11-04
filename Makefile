.PHONY: help notify

# Default target - show help
help:
	@echo "Available targets:"
	@echo "  make help   - Show this help message"
	@echo "  make notify - Manually trigger Slack notification for project/pipeline state"
	@echo ""
	@echo "Environment variables for notify:"
	@echo "  SLACK_WEBHOOK_URL - Slack webhook URL for notifications (required)"
	@echo "  STATUS           - Build status (default: success, options: success/failure)"
	@echo "  MESSAGE          - Custom message to send (optional)"

# Manual notification target
notify:
	@if [ -z "$$SLACK_WEBHOOK_URL" ]; then \
		echo "Error: SLACK_WEBHOOK_URL environment variable is not set"; \
		echo "Please set it with: export SLACK_WEBHOOK_URL='your-webhook-url'"; \
		exit 1; \
	fi; \
	STATUS=$${STATUS:-success}; \
	MESSAGE=$${MESSAGE:-"Manual notification triggered"}; \
	if [ "$$STATUS" = "success" ]; then \
		COLOR="good"; \
		STATUS_ICON="✅"; \
	else \
		COLOR="danger"; \
		STATUS_ICON="❌"; \
	fi; \
	REPO_NAME=$$(git config --get remote.origin.url 2>/dev/null || echo "local-repository"); \
	BRANCH=$$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"); \
	COMMIT=$$(git rev-parse --short HEAD 2>/dev/null || echo "unknown"); \
	AUTHOR=$$(git config user.name 2>/dev/null || echo "unknown"); \
	JSON_PAYLOAD=$$(cat <<-EOF \
		{ \
		  "attachments": [ \
		    { \
		      "color": "$$COLOR", \
		      "title": "Manual Pipeline Notification", \
		      "fields": [ \
		        { \
		          "title": "Repository", \
		          "value": "$$REPO_NAME", \
		          "short": true \
		        }, \
		        { \
		          "title": "Branch", \
		          "value": "$$BRANCH", \
		          "short": true \
		        }, \
		        { \
		          "title": "Status", \
		          "value": "$$STATUS_ICON $$STATUS", \
		          "short": true \
		        }, \
		        { \
		          "title": "Message", \
		          "value": "$$MESSAGE", \
		          "short": true \
		        }, \
		        { \
		          "title": "Commit", \
		          "value": "$$COMMIT", \
		          "short": true \
		        }, \
		        { \
		          "title": "Triggered by", \
		          "value": "$$AUTHOR", \
		          "short": true \
		        } \
		      ], \
		      "footer": "Makefile Notification", \
		      "ts": $$(date +%s) \
		    } \
		  ] \
		} \
	EOF \
	); \
	echo "Sending notification to Slack..."; \
	curl -X POST -H 'Content-type: application/json' \
		--data "$$JSON_PAYLOAD" \
		"$$SLACK_WEBHOOK_URL"; \
	echo ""; \
	echo "Notification sent successfully!"
