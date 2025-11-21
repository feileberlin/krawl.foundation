#!/bin/bash
# =============================================================================
# Quick TODO Helper - krawl.foundation
# =============================================================================
# Usage:
#   ./scripts/add_todo.sh high "Task beschreibung"
#   ./scripts/add_todo.sh medium "Task" --command "./cli/script.py"
#   ./scripts/add_todo.sh low "Task" --file "path/to/file.py"
#   ./scripts/add_todo.sh done "Task" (moves to completed)
#
# Alias Setup:
#   echo 'alias todo="./scripts/add_todo.sh"' >> ~/.bashrc
#   source ~/.bashrc
#   todo high "Neue wichtige Aufgabe"
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
PRIORITY="${1:-medium}"
TASK="$2"
DATE=$(date +%Y-%m-%d)
COMMAND=""
FILE=""
NOTE=""
URL=""

# Validate
if [ -z "$TASK" ]; then
    echo -e "${RED}❌ Error: Task beschreibung fehlt${NC}"
    echo "Usage: $0 <priority> <task> [--command <cmd>] [--file <path>] [--note <text>] [--url <link>]"
    echo "Priority: high|medium|low|done"
    exit 1
fi

# Parse optional flags
shift 2
while [[ $# -gt 0 ]]; do
    case $1 in
        --command|-c)
            COMMAND="$2"
            shift 2
            ;;
        --file|-f)
            FILE="$2"
            shift 2
            ;;
        --note|-n)
            NOTE="$2"
            shift 2
            ;;
        --url|-u)
            URL="$2"
            shift 2
            ;;
        *)
            echo -e "${YELLOW}⚠️  Unknown option: $1${NC}"
            shift
            ;;
    esac
done

# Determine priority key
case $PRIORITY in
    high|h|1)
        PRIORITY_KEY="high_priority"
        PRIORITY_LABEL="HIGH"
        COLOR=$RED
        ;;
    medium|m|2)
        PRIORITY_KEY="medium_priority"
        PRIORITY_LABEL="MEDIUM"
        COLOR=$YELLOW
        ;;
    low|l|3)
        PRIORITY_KEY="low_priority"
        PRIORITY_LABEL="LOW"
        COLOR=$BLUE
        ;;
    nice|n|4)
        PRIORITY_KEY="nice_to_have"
        PRIORITY_LABEL="NICE"
        COLOR=$BLUE
        ;;
    done|d|✓)
        PRIORITY_KEY="completed"
        PRIORITY_LABEL="DONE"
        COLOR=$GREEN
        ;;
    *)
        echo -e "${RED}❌ Invalid priority: $PRIORITY${NC}"
        echo "Valid: high|medium|low|nice|done"
        exit 1
        ;;
esac

# Find the YAML file
YAML_FILE="_data/features.yml"
if [ ! -f "$YAML_FILE" ]; then
    echo -e "${RED}❌ Error: $YAML_FILE not found${NC}"
    exit 1
fi

# Create temporary file
TMP_FILE=$(mktemp)

# Find insertion point (before next section or at end)
awk -v priority="$PRIORITY_KEY" -v task="$TASK" -v date="$DATE" -v cmd="$COMMAND" -v file="$FILE" -v note="$NOTE" -v url="$URL" -v completed="$PRIORITY_LABEL" '
BEGIN { inserted = 0; in_section = 0; }

# Detect if we are in the target section
/^  '"$PRIORITY_KEY"':/ { in_section = 1; next; }

# If in target section and we hit next section (same indentation), insert before it
in_section && /^  [a-z_]+:/ && !inserted {
    # Insert new TODO
    print "    - task: \"" task "\""
    if (completed == "DONE") {
        print "      status: done"
        print "      completed: " date
    } else {
        print "      status: pending"
        print "      added: " date
    }
    if (cmd != "") print "      command: \"" cmd "\""
    if (file != "") print "      file: \"" file "\""
    if (note != "") print "      note: \"" note "\""
    if (url != "") print "      url: \"" url "\""
    print ""
    inserted = 1
    in_section = 0
}

# Print current line
{ print }

# If we reach end of file and havent inserted, add at end
END {
    if (!inserted) {
        print "    - task: \"" task "\""
        if (completed == "DONE") {
            print "      status: done"
            print "      completed: " date
        } else {
            print "      status: pending"
            print "      added: " date
        }
        if (cmd != "") print "      command: \"" cmd "\""
        if (file != "") print "      file: \"" file "\""
        if (note != "") print "      note: \"" note "\""
        if (url != "") print "      url: \"" url "\""
    }
}
' "$YAML_FILE" > "$TMP_FILE"

# Replace original file
mv "$TMP_FILE" "$YAML_FILE"

# Update metadata
sed -i "s/last_updated: .*/last_updated: $DATE/" "$YAML_FILE"

# Git operations
echo -e "${COLOR}✅ TODO added to $PRIORITY_KEY${NC}"
echo -e "${COLOR}📝 $TASK${NC}"

if [ -n "$COMMAND" ]; then
    echo -e "   💻 Command: ${BLUE}$COMMAND${NC}"
fi
if [ -n "$FILE" ]; then
    echo -e "   📄 File: ${BLUE}$FILE${NC}"
fi

# Ask for git commit
echo ""
echo -e "${YELLOW}Git commit? [Y/n]${NC}"
read -r COMMIT_CHOICE

if [[ "$COMMIT_CHOICE" != "n" && "$COMMIT_CHOICE" != "N" ]]; then
    git add "$YAML_FILE"
    
    if [ "$PRIORITY_LABEL" = "DONE" ]; then
        COMMIT_MSG="✅ Complete TODO: $TASK"
    else
        COMMIT_MSG="📋 Add $PRIORITY_LABEL TODO: $TASK"
    fi
    
    git commit -m "$COMMIT_MSG"
    echo -e "${GREEN}✅ Committed!${NC}"
    
    echo -e "${YELLOW}Push to GitHub? [Y/n]${NC}"
    read -r PUSH_CHOICE
    
    if [[ "$PUSH_CHOICE" != "n" && "$PUSH_CHOICE" != "N" ]]; then
        git push
        echo -e "${GREEN}✅ Pushed to GitHub!${NC}"
        echo -e "${BLUE}🌐 Dashboard: https://feileberlin.github.io/krawl.foundation/dashboard.html${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Not committed. Run manually:${NC}"
    echo "   git add $YAML_FILE"
    echo "   git commit -m 'todo: $TASK'"
    echo "   git push"
fi
