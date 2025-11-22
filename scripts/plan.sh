#!/usr/bin/env bash
# =============================================================================
# scripts/plan.sh - TODO Management für krawl.foundation
# =============================================================================
# Zeigt offene Pläne aus _data/features.yml an und ermöglicht das Hinzufügen
# neuer TODOs mit automatischer Prioritätserkennung via Suffix.
#
# Usage:
#   ./scripts/plan.sh                    # Interaktiver Modus
#   ./scripts/plan.sh "New task"         # nice_to_have
#   ./scripts/plan.sh "Important task!"  # low_priority  
#   ./scripts/plan.sh "Urgent task!!"    # high_priority
#
# Requires: yq (YAML processor)
#   Install: sudo snap install yq
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
GRAY='\033[0;90m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Paths
FEATURES_FILE="_data/features.yml"
BACKUP_FILE=".features.yml.backup"

# Check if features.yml exists
if [[ ! -f "$FEATURES_FILE" ]]; then
    echo -e "${RED}❌ Error: $FEATURES_FILE not found${NC}"
    exit 1
fi

# Check if yq is installed
if ! command -v yq &> /dev/null; then
    echo -e "${YELLOW}⚠️  yq not installed - using Python fallback${NC}"
    USE_PYTHON=true
else
    USE_PYTHON=false
fi

# =============================================================================
# FUNCTIONS
# =============================================================================

show_todos() {
    echo -e "${BOLD}📋 OFFENE PLÄNE${NC}"
    echo "=================================================="
    echo ""
    
    # High Priority
    echo -e "${RED}${BOLD}🔴 HIGH PRIORITY${NC}"
    echo "--------------------------------------------------"
    
    if $USE_PYTHON; then
        python3 << 'PYEOF'
import yaml
with open("_data/features.yml") as f:
    data = yaml.safe_load(f)
    todos = data.get("todos", {}).get("high_priority", [])
    if todos:
        for i, todo in enumerate(todos, 1):
            status = todo.get("status", "pending")
            task = todo.get("task", "No description")
            print(f"  [{i}] {task}")
            if status != "pending":
                print(f"      Status: {status}")
    else:
        print("  (keine)")
PYEOF
    else
        yq '.todos.high_priority[] | "  [\(.task)]"' "$FEATURES_FILE" 2>/dev/null || echo "  (keine)"
    fi
    
    echo ""
    
    # Low Priority
    echo -e "${YELLOW}${BOLD}🟡 LOW PRIORITY${NC}"
    echo "--------------------------------------------------"
    
    if $USE_PYTHON; then
        python3 << 'PYEOF'
import yaml
with open("_data/features.yml") as f:
    data = yaml.safe_load(f)
    todos = data.get("todos", {}).get("low_priority", [])
    if todos:
        for i, todo in enumerate(todos, 1):
            status = todo.get("status", "pending")
            task = todo.get("task", "No description")
            print(f"  [{i}] {task}")
    else:
        print("  (keine)")
PYEOF
    else
        yq '.todos.low_priority[] | "  [\(.task)]"' "$FEATURES_FILE" 2>/dev/null || echo "  (keine)"
    fi
    
    echo ""
    
    # Nice to Have
    echo -e "${GRAY}${BOLD}⚪ NICE TO HAVE${NC}"
    echo "--------------------------------------------------"
    
    if $USE_PYTHON; then
        python3 << 'PYEOF'
import yaml
with open("_data/features.yml") as f:
    data = yaml.safe_load(f)
    todos = data.get("todos", {}).get("nice_to_have", [])
    if todos:
        for i, todo in enumerate(todos, 1):
            task = todo.get("task", "No description")
            print(f"  [{i}] {task}")
    else:
        print("  (keine)")
PYEOF
    else
        yq '.todos.nice_to_have[] | "  [\(.task)]"' "$FEATURES_FILE" 2>/dev/null || echo "  (keine)"
    fi
    
    echo ""
    echo "=================================================="
}

add_todo() {
    local task_text="$1"
    local priority="nice_to_have"
    
    # Detect priority from suffix
    if [[ "$task_text" =~ !!$ ]]; then
        priority="high_priority"
        task_text="${task_text%!!}"
    elif [[ "$task_text" =~ !$ ]]; then
        priority="low_priority"
        task_text="${task_text%!}"
    fi
    
    # Trim whitespace
    task_text="$(echo "$task_text" | xargs)"
    
    if [[ -z "$task_text" ]]; then
        echo -e "${RED}❌ Error: Empty task description${NC}"
        return 1
    fi
    
    # Backup
    cp "$FEATURES_FILE" "$BACKUP_FILE"
    
    # Add todo using Python
    python3 << PYEOF
import yaml
from datetime import date

with open("$FEATURES_FILE") as f:
    data = yaml.safe_load(f)

new_todo = {
    "task": "$task_text",
    "status": "pending",
    "added": str(date.today())
}

if "todos" not in data:
    data["todos"] = {}
if "$priority" not in data["todos"]:
    data["todos"]["$priority"] = []

data["todos"]["$priority"].append(new_todo)

with open("$FEATURES_FILE", "w") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print(f"✅ Added to $priority: $task_text")
PYEOF
    
    # Git commit (optional)
    read -p "💾 Git commit? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add "$FEATURES_FILE"
        git commit -m "feat: Add TODO - $task_text"
        echo -e "${GREEN}✅ Committed${NC}"
    fi
}

# =============================================================================
# MAIN
# =============================================================================

if [[ $# -eq 0 ]]; then
    # Interactive mode
    show_todos
    echo ""
    echo -e "${BOLD}Optionen:${NC}"
    echo "  [a] Add new TODO"
    echo "  [r] Reload/Refresh"
    echo "  [q] Quit"
    echo ""
    read -p "Auswahl: " choice
    
    case "$choice" in
        a|A)
            read -p "Task (! = low, !! = high): " task
            add_todo "$task"
            ;;
        r|R)
            exec "$0"
            ;;
        q|Q)
            exit 0
            ;;
        *)
            echo "Invalid choice"
            exit 1
            ;;
    esac
else
    # Non-interactive mode
    add_todo "$*"
fi
