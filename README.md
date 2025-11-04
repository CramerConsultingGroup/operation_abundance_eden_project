# operation_abundance_eden_project
Project and investor place holder 

## CI Notifications

This repository includes automated CI notifications that integrate with Slack and Discord. Notifications are triggered on pushes to the `main` branch, pull requests targeting `main`, or can be manually triggered via the workflow dispatch.

### Setup Instructions

To enable CI notifications, configure the following secrets in your GitHub repository settings:

1. **SLACK_WEBHOOK_URL** (Optional)
   - Navigate to your Slack workspace and create an Incoming Webhook
   - Go to: https://api.slack.com/messaging/webhooks
   - Copy the webhook URL
   - Add it as a repository secret: Settings → Secrets and variables → Actions → New repository secret
   - Name: `SLACK_WEBHOOK_URL`
   - Value: Your Slack webhook URL

2. **DISCORD_WEBHOOK_URL** (Optional)
   - Open your Discord server settings
   - Go to: Server Settings → Integrations → Webhooks
   - Create a new webhook or use an existing one
   - Copy the webhook URL
   - Add it as a repository secret: Settings → Secrets and variables → Actions → New repository secret
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: Your Discord webhook URL

### Manual Pipeline Checks

You can perform manual pipeline checks using the Makefile:

```bash
# Check if webhook environment variables are configured
make notify

# Run with webhook URLs set
SLACK_WEBHOOK_URL=your_slack_url DISCORD_WEBHOOK_URL=your_discord_url make notify
```

### Notification Details

The CI notifications include the following information:
- Repository name
- Branch name (properly handles both pushes and pull requests)
- Commit SHA (shortened)
- Commit author
- Workflow status (currently always reports success for basic notification tracking)
- Commit message
- Timestamp (Discord notifications only)

### Workflow File

The notification workflow is defined in `.github/workflows/notify_ci.yml` and runs automatically on:
- Pushes to the `main` branch
- Pull requests targeting the `main` branch
- Manual trigger via workflow dispatch

Both Slack and Discord notifications are optional and will only be sent if the corresponding webhook URL secret is configured. The workflow will continue to run successfully even if no webhooks are configured.

