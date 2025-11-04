#!/usr/bin/env python3
"""
Analyzer for CI — Build Sample Investor PDF (Smoke Test) workflow results.
Generates Markdown summary and JSON metrics suitable for Shields.io badges.
"""

import json
import sys
import os
from datetime import datetime, timezone
from typing import Dict, Any


def get_workflow_conclusion(conclusion: str) -> Dict[str, Any]:
    """Map GitHub workflow conclusion to status information."""
    status_map = {
        'success': {
            'status': 'passing',
            'color': 'brightgreen',
            'emoji': '✅',
            'label': 'Success'
        },
        'failure': {
            'status': 'failing',
            'color': 'red',
            'emoji': '❌',
            'label': 'Failed'
        },
        'cancelled': {
            'status': 'cancelled',
            'color': 'yellow',
            'emoji': '⚠️',
            'label': 'Cancelled'
        },
        'skipped': {
            'status': 'skipped',
            'color': 'lightgrey',
            'emoji': 'ℹ️',
            'label': 'Skipped'
        }
    }
    return status_map.get(conclusion.lower(), {
        'status': 'unknown',
        'color': 'lightgrey',
        'emoji': '❓',
        'label': 'Unknown'
    })


def generate_markdown_summary(workflow_data: Dict[str, Any]) -> str:
    """Generate a Markdown summary of the workflow results."""
    status_info = get_workflow_conclusion(workflow_data['conclusion'])
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    markdown = f"""# CI Build Status Report

## Latest Run Summary

{status_info['emoji']} **Status**: {status_info['label']}

### Run Details
- **Workflow**: {workflow_data['workflow_name']}
- **Run ID**: {workflow_data['run_id']}
- **Run Number**: {workflow_data['run_number']}
- **Trigger**: {workflow_data['event']}
- **Branch**: {workflow_data['branch']}
- **Commit**: {workflow_data['sha'][:7]}
- **Actor**: {workflow_data['actor']}
- **Conclusion**: {workflow_data['conclusion']}
- **Analysis Time**: {timestamp}

### Quick Links
- [View Run]({workflow_data['html_url']})
- [Repository]({workflow_data['repository_url']})

---
*Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*
"""
    return markdown


def generate_metrics_json(workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate JSON metrics suitable for Shields.io badges."""
    status_info = get_workflow_conclusion(workflow_data['conclusion'])
    
    # Shields.io endpoint JSON schema
    metrics = {
        "schemaVersion": 1,
        "label": "build",
        "message": status_info['status'],
        "color": status_info['color'],
        "namedLogo": "github",
        "logoColor": "white",
        "style": "flat",
        "cacheSeconds": 300
    }
    
    return metrics


def main():
    """Main analyzer function."""
    # Get workflow data from environment variables
    workflow_data = {
        'workflow_name': os.environ.get('WORKFLOW_NAME', 'Unknown'),
        'run_id': os.environ.get('RUN_ID', '0'),
        'run_number': os.environ.get('RUN_NUMBER', '0'),
        'conclusion': os.environ.get('CONCLUSION', 'unknown'),
        'event': os.environ.get('EVENT_NAME', 'unknown'),
        'branch': os.environ.get('BRANCH', 'unknown'),
        'sha': os.environ.get('SHA', 'unknown'),
        'actor': os.environ.get('ACTOR', 'unknown'),
        'html_url': os.environ.get('HTML_URL', '#'),
        'repository_url': os.environ.get('REPOSITORY_URL', '#')
    }
    
    # Generate outputs
    markdown_summary = generate_markdown_summary(workflow_data)
    metrics_json = generate_metrics_json(workflow_data)
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Write markdown summary
    with open('reports/ci_latest.md', 'w') as f:
        f.write(markdown_summary)
    print("✅ Generated reports/ci_latest.md")
    
    # Write metrics JSON
    with open('reports/metrics.json', 'w') as f:
        json.dump(metrics_json, f, indent=2)
    print("✅ Generated reports/metrics.json")
    
    # Copy to docs if it exists
    if os.path.isdir('docs'):
        with open('docs/metrics.json', 'w') as f:
            json.dump(metrics_json, f, indent=2)
        print("✅ Copied metrics.json to docs/metrics.json")
    else:
        print("ℹ️  docs/ directory not found, skipping copy")
    
    # Output summary for PR comment (to stdout for capture)
    print("\n" + "="*50)
    print("PR COMMENT CONTENT:")
    print("="*50)
    print(markdown_summary)
    print("="*50)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
