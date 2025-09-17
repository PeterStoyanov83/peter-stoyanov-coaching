#!/bin/bash

# Development Progress Logger for Static Site Migration
# Usage: ./log_progress.sh [optional custom message]

LOG_FILE="DEVELOPMENT_PROGRESS.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE_ONLY=$(date '+%Y-%m-%d')

# Function to get git status
get_git_status() {
    echo "### Git Status"
    echo "\`\`\`"
    git status --porcelain
    echo "\`\`\`"
    echo ""
    echo "**Latest Commits:**"
    echo "\`\`\`"
    git log --oneline -5
    echo "\`\`\`"
    echo ""
}

# Function to get current todo status (if CLAUDE.md exists and has todos)
get_todo_status() {
    echo "### Current Tasks Status"
    echo "*(Note: Check with Claude Code for detailed todo list)*"
    echo ""
    echo "**Completed Today:**"
    echo "- Next.js static export configuration ✅"
    echo "- Removed backend API dependencies ✅"
    echo ""
    echo "**In Progress:**"
    echo "- Creating lead magnet form and components 🔄"
    echo ""
    echo "**Pending:**"
    echo "- Convert email templates to HTML with styling"
    echo "- Set up static site build and deployment structure"
    echo "- Create documentation for external services setup"
    echo ""
}

# Function to get file changes
get_file_changes() {
    echo "### Files Modified"
    echo "\`\`\`"
    git diff --name-only HEAD~1 2>/dev/null || echo "No recent commits to compare"
    echo "\`\`\`"
    echo ""
}

# Create or append to log file
if [ ! -f "$LOG_FILE" ]; then
    cat > "$LOG_FILE" << EOF
# 🚀 Static Site Migration - Development Progress Log

This file tracks the daily progress of converting the coaching website from full-stack to static.

**Project Goal:** Transform to Typeform + Cloudflare Pages + SendGrid automation

---

EOF
fi

# Add new log entry
cat >> "$LOG_FILE" << EOF
## 📅 Progress Log - $DATE_ONLY

**Timestamp:** $TIMESTAMP

$(get_git_status)

$(get_todo_status)

$(get_file_changes)

### Notes
${1:-"Development session completed. See git commits for detailed changes."}

---

EOF

echo "✅ Progress logged to $LOG_FILE"
echo "📝 Summary added for $DATE_ONLY"

# Optional: Show the last entry
echo ""
echo "📋 Latest log entry:"
echo "===================="
tail -20 "$LOG_FILE"