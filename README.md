# operation_abundance_eden_project

[![CI Build Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/CramerConsultingGroup/operation_abundance_eden_project/main/reports/metrics.json)](https://github.com/CramerConsultingGroup/operation_abundance_eden_project/actions/workflows/smoke_test.yml)

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

## CI Build Status and Analysis

This repository includes automated CI build analysis that monitors the "CI — Build Sample Investor PDF (Smoke Test)" workflow and generates comprehensive reports.

### Build Status Badge

The badge at the top of this README shows the current build status and is automatically updated after each workflow run. It uses [Shields.io](https://shields.io/) dynamic badges powered by the `reports/metrics.json` file.

**Note**: The badge always reflects the status of the `main` branch, regardless of which branch you're viewing. This provides a consistent indication of the production build health.

### Automated Reports

After each smoke test run, the analysis workflow automatically:

1. **Generates Reports**
   - `reports/ci_latest.md` - Human-readable Markdown summary with workflow details
   - `reports/metrics.json` - JSON metrics in Shields.io endpoint format

2. **Comments on Pull Requests**
   - Automatically adds/updates a comment on the PR with build results
   - Includes workflow status, run details, and quick links

3. **Copies to GitHub Pages** (if applicable)
   - If a `docs/` directory exists, copies `metrics.json` for GitHub Pages badge support

### How It Works

The analysis workflow is triggered automatically when the smoke test workflow completes:

```
Smoke Test Workflow → Completes → Analysis Workflow → Generates Reports → Updates PR
```

### Files

- `.github/workflows/smoke_test.yml` - Main smoke test workflow
- `.github/workflows/analyze_smoke_test.yml` - Analysis workflow (triggered on smoke test completion)
- `.github/scripts/analyze_workflow.py` - Python analyzer that generates reports
- `reports/ci_latest.md` - Latest build status report
- `reports/metrics.json` - Badge metrics (Shields.io format)

