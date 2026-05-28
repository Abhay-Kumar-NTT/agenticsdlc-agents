#!/bin/bash
# Convenience wrapper for running AgenticSDLC agents

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
VERBOSE=""
AGENT=""
INPUT=""
OUTPUT=""
TEMPERATURE=""
MAX_TOKENS=""

# Help function
show_help() {
    cat << EOF
AgenticSDLC Agent Runner

Usage: ./run.sh [OPTIONS]

Common Shortcuts:
  ./run.sh product          Run product agent (vision -> PRD)
  ./run.sh architecture     Run architecture agent (PRD -> HLD/LLD)
  ./run.sh developer        Run developer agent (HLD -> Code)
  ./run.sh qa               Run QA agent (Code -> Tests)
  ./run.sh devops           Run DevOps agent (Code -> Infrastructure)

Options:
  --agent PATH              Path to agent.yaml
  --input PATH              Path to input file
  --output PATH             Path to output directory
  --temperature VALUE       Temperature (0.0-1.0)
  --max-tokens VALUE        Max tokens to generate
  -v, --verbose             Verbose output
  -h, --help                Show this help

Examples:
  ./run.sh product
  ./run.sh product --verbose
  ./run.sh architecture --temperature 0.3
  ./run.sh --agent agents/custom/agent.yaml --input input.md --output out/

Environment Variables:
  OPENAI_API_KEY           For OpenAI/GPT models
  ANTHROPIC_API_KEY        For Claude models
  GOOGLE_API_KEY           For Gemini models
  AZURE_OPENAI_API_KEY     For Azure OpenAI

EOF
}

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python not found${NC}"
    echo "Please install Python 3.7 or later"
    exit 1
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        product)
            AGENT="agents/product-agent/agent.yaml"
            INPUT="artifacts/vision.md"
            OUTPUT="artifacts/product/"
            shift
            ;;
        architecture)
            AGENT="agents/architecture-agent/agent.yaml"
            INPUT="artifacts/product/output.md"
            OUTPUT="artifacts/architecture/"
            shift
            ;;
        developer)
            AGENT="agents/developer-agent/agent.yaml"
            INPUT="artifacts/architecture/output.md"
            OUTPUT="artifacts/development/"
            shift
            ;;
        qa)
            AGENT="agents/qa-agent/agent.yaml"
            INPUT="artifacts/development/output.md"
            OUTPUT="artifacts/qa/"
            shift
            ;;
        devops)
            AGENT="agents/devops-agent/agent.yaml"
            INPUT="artifacts/architecture/output.md"
            OUTPUT="artifacts/devops/"
            shift
            ;;
        --agent)
            AGENT="$2"
            shift 2
            ;;
        --input)
            INPUT="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --temperature)
            TEMPERATURE="$2"
            shift 2
            ;;
        --max-tokens)
            MAX_TOKENS="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Check required arguments
if [ -z "$AGENT" ] || [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo -e "${RED}Error: Missing required arguments${NC}"
    echo "Use: ./run.sh product|architecture|developer|qa|devops"
    echo "Or:  ./run.sh --agent PATH --input PATH --output PATH"
    exit 1
fi

# Check if agent file exists
if [ ! -f "$AGENT" ]; then
    echo -e "${RED}Error: Agent config not found: $AGENT${NC}"
    exit 1
fi

# Check if input file exists
if [ ! -f "$INPUT" ]; then
    echo -e "${RED}Error: Input file not found: $INPUT${NC}"
    exit 1
fi

# Get agent name from config
AGENT_NAME=$(grep "^name:" "$AGENT" | cut -d: -f2- | xargs)

# Display what we're doing
echo -e "${GREEN}Running AgenticSDLC Agent${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Agent:  ${YELLOW}$AGENT_NAME${NC}"
echo -e "Input:  $INPUT"
echo -e "Output: $OUTPUT"

# Check API keys
MODEL=$(grep "^model:" "$AGENT" | cut -d: -f2- | xargs)
PROVIDER=$(grep "^provider:" "$AGENT" | cut -d: -f2- | xargs || echo "auto")

echo -e "Model:  ${YELLOW}$MODEL${NC}"

# Warn if API key might be missing
if [[ "$MODEL" == *"gpt"* ]] || [[ "$PROVIDER" == "openai" ]]; then
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${YELLOW}Warning: OPENAI_API_KEY not set${NC}"
    fi
elif [[ "$MODEL" == *"claude"* ]] || [[ "$PROVIDER" == "anthropic" ]]; then
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo -e "${YELLOW}Warning: ANTHROPIC_API_KEY not set${NC}"
    fi
elif [[ "$MODEL" == *"gemini"* ]] || [[ "$PROVIDER" == "google" ]]; then
    if [ -z "$GOOGLE_API_KEY" ]; then
        echo -e "${YELLOW}Warning: GOOGLE_API_KEY not set${NC}"
    fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get prompt file path (same directory as agent.yaml)
AGENT_DIR=$(dirname "$AGENT")
PROMPT="$AGENT_DIR/prompt.md"

if [ ! -f "$PROMPT" ]; then
    echo -e "${RED}Error: Prompt file not found: $PROMPT${NC}"
    exit 1
fi

# Build command
CMD="python scripts/run_agent.py --agent $AGENT --prompt $PROMPT --input $INPUT --output $OUTPUT"

if [ -n "$TEMPERATURE" ]; then
    CMD="$CMD --temperature $TEMPERATURE"
fi

if [ -n "$MAX_TOKENS" ]; then
    CMD="$CMD --max-tokens $MAX_TOKENS"
fi

if [ -n "$VERBOSE" ]; then
    CMD="$CMD --verbose"
fi

# Run the command
eval $CMD

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Agent execution completed successfully${NC}"
    echo -e "Output: ${YELLOW}$OUTPUT/output.md${NC}"
else
    echo ""
    echo -e "${RED}✗ Agent execution failed${NC}"
    exit 1
fi
