#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# AI Real Estate Analyst — Claude Code Skill Installer
# Installs the AI-powered property research & analysis tool
# ============================================================

REPO_URL="https://github.com/zubair-trabzada/ai-realestate-claude.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
INSTALL_DIR="${SKILLS_DIR}/realestate"
TEMP_DIR=$(mktemp -d)

# Detect if running via curl pipe (no interactive input available)
INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   AI Real Estate Analyst — Installer          ║${NC}"
    echo -e "${BLUE}║   AI-Powered Property Research & Analysis     ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}→ $1${NC}"
}

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

main() {
    print_header

    # ---- Check Prerequisites ----
    print_info "Checking prerequisites..."

    # Check for Git
    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed."
        echo "  Install: https://git-scm.com/downloads"
        exit 1
    fi
    print_success "Git found: $(git --version)"

    # Check for Python 3.8+
    PYTHON_CMD=""
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if [ -n "$PYTHON_VERSION" ]; then
            MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
            MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
            if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
                PYTHON_CMD="python"
            fi
        fi
    fi

    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python 3.8+ is required but not found."
        echo "  Install: https://www.python.org/downloads/"
        exit 1
    fi
    print_success "Python found: $($PYTHON_CMD --version)"

    # Check for reportlab
    if $PYTHON_CMD -c "import reportlab" 2>/dev/null; then
        print_success "reportlab found"
    else
        print_warning "reportlab not found — will attempt to install"
    fi

    # Check for Claude Code
    if ! command -v claude &> /dev/null; then
        print_warning "Claude Code CLI not found in PATH."
        echo "  This tool requires Claude Code to function."
        echo "  Install: npm install -g @anthropic-ai/claude-code"
        echo ""
        if [ "$INTERACTIVE" = true ]; then
            read -p "Continue installation anyway? (y/n): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            print_info "Non-interactive mode — continuing anyway..."
        fi
    else
        print_success "Claude Code CLI found"
    fi

    # ---- Create Directories ----
    print_info "Creating directories..."

    mkdir -p "$SKILLS_DIR"
    mkdir -p "$AGENTS_DIR"
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/scripts"

    print_success "Directory structure created"

    # ---- Clone or Copy Repository ----
    print_info "Fetching AI Real Estate Analyst files..."

    # Check if running from the repo directory (local install)
    SCRIPT_DIR=""
    if [ -n "${BASH_SOURCE[0]:-}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || true
    fi

    if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/realestate/SKILL.md" ]; then
        print_info "Installing from local directory..."
        SOURCE_DIR="$SCRIPT_DIR"
    else
        print_info "Cloning from repository..."
        git clone --depth 1 "$REPO_URL" "$TEMP_DIR/repo" || {
            print_error "Failed to clone repository. Check your internet connection."
            exit 1
        }
        SOURCE_DIR="${TEMP_DIR}/repo"
    fi

    # ---- Install Main Skill ----
    print_info "Installing main orchestrator..."

    cp -r "$SOURCE_DIR/realestate/"* "$INSTALL_DIR/"
    print_success "Main skill installed → ${INSTALL_DIR}/"

    # ---- Install Sub-Skills (14 skills) ----
    print_info "Installing sub-skills..."

    SKILL_COUNT=0
    for skill_dir in "$SOURCE_DIR/skills"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            target_dir="${SKILLS_DIR}/${skill_name}"
            mkdir -p "$target_dir"
            cp -r "$skill_dir"* "$target_dir/"
            SKILL_COUNT=$((SKILL_COUNT + 1))
            print_success "  ${skill_name}"
        fi
    done
    echo "  → ${SKILL_COUNT} sub-skills installed"

    # ---- Install Agents (5 agents) ----
    print_info "Installing subagents..."

    AGENT_COUNT=0
    for agent_file in "$SOURCE_DIR/agents/"*.md; do
        if [ -f "$agent_file" ]; then
            cp "$agent_file" "$AGENTS_DIR/"
            AGENT_COUNT=$((AGENT_COUNT + 1))
            print_success "  $(basename "$agent_file")"
        fi
    done
    echo "  → ${AGENT_COUNT} subagents installed"

    # ---- Install Scripts ----
    print_info "Installing utility scripts..."

    if [ -d "$SOURCE_DIR/scripts" ]; then
        cp -r "$SOURCE_DIR/scripts/"* "$INSTALL_DIR/scripts/"
        chmod +x "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true
        print_success "Scripts installed → ${INSTALL_DIR}/scripts/"
    fi

    # ---- Install Python Dependencies ----
    print_info "Installing Python dependencies..."

    if [ -f "$SOURCE_DIR/requirements.txt" ]; then
        $PYTHON_CMD -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet 2>/dev/null && {
            print_success "Python dependencies installed (reportlab, beautifulsoup4, requests)"
        } || {
            print_warning "Some Python dependencies failed to install."
            echo "  Run manually: $PYTHON_CMD -m pip install reportlab beautifulsoup4 requests"
            cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/"
        }
    fi

    # ---- Verify Installation ----
    echo ""
    print_info "Verifying installation..."

    VERIFY_OK=true

    [ -f "$INSTALL_DIR/SKILL.md" ] && print_success "Main skill file" || { print_error "Main skill file missing"; VERIFY_OK=false; }
    [ -d "$SKILLS_DIR/realestate-analyze" ] && print_success "Sub-skills directory" || { print_error "Sub-skills missing"; VERIFY_OK=false; }
    [ "$(ls "$AGENTS_DIR"/realestate-*.md 2>/dev/null | wc -l)" -gt 0 ] && print_success "Agent files" || { print_warning "No agent files found (may not be created yet)"; }
    [ -d "$INSTALL_DIR/scripts" ] && print_success "Utility scripts" || { print_error "Scripts missing"; VERIFY_OK=false; }

    # Verify reportlab
    if $PYTHON_CMD -c "import reportlab" 2>/dev/null; then
        print_success "reportlab available for PDF generation"
    else
        print_warning "reportlab not available — PDF reports will not work until installed"
        echo "  Install: $PYTHON_CMD -m pip install reportlab"
    fi

    # ---- Print Summary ----
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║          Installation Complete!               ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  Installed to: ${INSTALL_DIR}"
    echo "  Skills:       ${SKILL_COUNT} sub-skills"
    echo "  Agents:       ${AGENT_COUNT} subagents"
    echo ""
    echo -e "${CYAN}Quick Start:${NC}"
    echo "  Open Claude Code and try:"
    echo ""
    echo "    /realestate analyze 123 Main St, Austin TX 78701"
    echo "    /realestate quick 456 Oak Ave, Denver CO 80202"
    echo "    /realestate invest 789 Pine Dr, Tampa FL 33602"
    echo ""
    echo -e "${CYAN}Command Reference:${NC}"
    echo "    /realestate analyze <address>    Full property analysis (5 parallel agents)"
    echo "    /realestate quick <address>      60-second property snapshot"
    echo "    /realestate comps <address>      Comparable sales analysis"
    echo "    /realestate rental <address>     Rental income & cash flow projection"
    echo "    /realestate listing <address>    Professional MLS-ready listing"
    echo "    /realestate invest <address>     Investment analysis (buy-hold, BRRRR, flip)"
    echo "    /realestate neighborhood <addr>  Schools, crime, walkability, demographics"
    echo "    /realestate flip <address>       Fix-and-flip analysis with rehab budget"
    echo "    /realestate commercial <address> Commercial property analysis (NOI, cap rate)"
    echo "    /realestate mortgage <price>     Mortgage calculator & affordability"
    echo "    /realestate market <city/zip>    Local market conditions & trends"
    echo "    /realestate compare <a1> <a2>    Side-by-side property comparison"
    echo "    /realestate screen <criteria>    Property screener by investment criteria"
    echo "    /realestate report-pdf           Generate professional PDF report"
    echo ""
    echo "  Documentation: https://github.com/zubair-trabzada/ai-realestate-claude"
    echo ""
}

main "$@"
