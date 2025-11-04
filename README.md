# operation_abundance_eden_project
Project and investor place holder

## Getting Started

This repository includes automated CI workflows and notification capabilities for Slack and Discord.

### CI Notifications

The repository includes automated notifications for CI build results. Notifications are sent to Slack and Discord when builds complete, providing real-time updates on the status of your CI pipeline.

#### Setting Up Webhook Secrets

To enable notifications, you need to configure webhook URLs as repository secrets:

1. **Slack Webhook Setup:**
   - Go to your Slack workspace and create an Incoming Webhook: https://api.slack.com/messaging/webhooks
   - Copy the webhook URL
   - In your GitHub repository, go to Settings → Secrets and variables → Actions
   - Create a new secret named `SLACK_WEBHOOK_URL` and paste your webhook URL

2. **Discord Webhook Setup:**
   - In your Discord server, go to Server Settings → Integrations → Webhooks
   - Create a new webhook and copy the webhook URL
   - In your GitHub repository, go to Settings → Secrets and variables → Actions
   - Create a new secret named `DISCORD_WEBHOOK_URL` and paste your webhook URL

#### How It Works

The CI notification workflow (`.github/workflows/notify_ci.yml`) runs automatically on:
- Push to `main` or `develop` branches
- Pull requests
- Manual workflow dispatch

The workflow performs a sample PDF building smoke test and sends notifications with the following information:
- Repository name and branch
- Build status (success/failure)
- Commit SHA and author
- Job name and execution time

**Note:** Notifications are only sent if the respective webhook URL secrets are configured. If a secret is not set, that notification step is skipped gracefully.

#### Artifact Posting

After successful CI builds, artifacts (such as generated PDFs) are automatically uploaded and available for download from the GitHub Actions workflow run page. You can access artifacts by:
1. Go to the Actions tab in your repository
2. Select the workflow run
3. Scroll to the Artifacts section at the bottom
4. Download the artifact (e.g., `sample-pdf`)

#### Manual Notifications with Makefile

You can manually trigger Slack notifications using the provided Makefile:

```bash
# Set your Slack webhook URL
export SLACK_WEBHOOK_URL='your-webhook-url-here'

# Send a success notification
make notify

# Send a failure notification
make notify STATUS=failure MESSAGE="Deployment failed"
```

The `make notify` command will:
- Validate that SLACK_WEBHOOK_URL is set
- Collect git repository information (branch, commit, author)
- Send a formatted JSON payload to Slack using curl
- Display the notification status

**Required:** Ensure the `SLACK_WEBHOOK_URL` environment variable is set before running `make notify`.

### Verifying Repository Secrets

To verify that your webhook secrets are properly configured:

1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Verify that the following secrets exist:
   - `SLACK_WEBHOOK_URL` (if using Slack notifications)
   - `DISCORD_WEBHOOK_URL` (if using Discord notifications)

**Security Note:** Webhook URLs should be kept secret and never committed to the repository. Always use GitHub Secrets to store sensitive values.

For testing purposes, you can trigger the workflow manually:
1. Go to Actions tab
2. Select "CI Notifications" workflow
3. Click "Run workflow" button
4. Select the branch and click "Run workflow"

This will execute the workflow and send notifications if the secrets are properly configured. 
