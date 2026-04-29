#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# AI Real Estate Analyst — Claude Code Skill Uninstaller
# ============================================================

CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}AI Real Estate Analyst — Uninstaller${NC}"
echo ""
echo "This will remove the following:"
echo ""

# List what will be removed
[ -d "$SKILLS_DIR/realestate" ] && echo "  → ${SKILLS_DIR}/realestate/"
for skill_dir in "$SKILLS_DIR"/realestate-*/; do
    [ -d "$skill_dir" ] && echo "  → ${skill_dir}"
done
for agent_file in "$AGENTS_DIR"/realestate-*.md; do
    [ -f "$agent_file" ] && echo "  → ${agent_file}"
done

echo ""
read -p "Are you sure you want to uninstall? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""

# Remove main skill
if [ -d "$SKILLS_DIR/realestate" ]; then
    rm -rf "$SKILLS_DIR/realestate"
    echo -e "${GREEN}✓ Removed main skill${NC}"
fi

# Remove sub-skills
for skill_dir in "$SKILLS_DIR"/realestate-*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        rm -rf "$skill_dir"
        echo -e "${GREEN}✓ Removed ${skill_name}${NC}"
    fi
done

# Remove agents
for agent_file in "$AGENTS_DIR"/realestate-*.md; do
    if [ -f "$agent_file" ]; then
        agent_name=$(basename "$agent_file")
        rm -f "$agent_file"
        echo -e "${GREEN}✓ Removed ${agent_name}${NC}"
    fi
done

echo ""
echo -e "${GREEN}AI Real Estate Analyst has been uninstalled.${NC}"
echo ""
echo "Note: Python dependencies were not removed."
echo "To remove them manually:"
echo "  pip uninstall reportlab beautifulsoup4 requests"
echo ""
