import argparse
import pathlib
import yaml
import sys
from datetime import datetime
from llm_client import create_llm_client_from_config


def main():
    parser = argparse.ArgumentParser(
        description="Run an AgenticSDLC agent with multi-provider AI support"
    )
    parser.add_argument("--agent", required=True, help="Path to agent.yaml config")
    parser.add_argument("--prompt", required=True, help="Path to agent prompt.md")
    parser.add_argument("--input", required=True, help="Path to input context file")
    parser.add_argument("--output", required=True, help="Path to output directory")
    parser.add_argument("--temperature", type=float, help="Override temperature (0.0-1.0)")
    parser.add_argument("--max-tokens", type=int, help="Override max tokens")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Load configuration
    if args.verbose:
        print(f"Loading agent config from: {args.agent}")
    agent_config = yaml.safe_load(open(args.agent, encoding="utf-8"))

    if args.verbose:
        print(f"Loading prompt from: {args.prompt}")
    system_prompt = pathlib.Path(args.prompt).read_text(encoding="utf-8")

    if args.verbose:
        print(f"Loading input context from: {args.input}")
    input_path = pathlib.Path(args.input)
    if input_path.exists() and input_path.is_file():
        input_context = input_path.read_text(encoding="utf-8")
    else:
        # Input is a raw value (e.g. repo URL, identifier) — use it directly as context
        input_context = args.input

    # Create LLM client
    try:
        if args.verbose:
            provider = agent_config.get("provider", "auto-detect")
            model = agent_config.get("model", "gpt-4")
            print(f"\nInitializing LLM client:")
            print(f"  Provider: {provider}")
            print(f"  Model: {model}")

        llm_client = create_llm_client_from_config(agent_config)
    except Exception as e:
        print(f"Error initializing LLM client: {e}", file=sys.stderr)
        print("\nPlease ensure you have set the appropriate API key environment variable:", file=sys.stderr)
        print("  - OPENAI_API_KEY for OpenAI/GPT models", file=sys.stderr)
        print("  - ANTHROPIC_API_KEY for Claude models", file=sys.stderr)
        print("  - GOOGLE_API_KEY for Gemini models", file=sys.stderr)
        print("  - AZURE_OPENAI_API_KEY for Azure OpenAI", file=sys.stderr)
        sys.exit(1)

    # Build user prompt
    user_prompt = f"""# Input Context

{input_context}

# Task

Generate the required outputs based on the input context above.
"""

    # Generate AI response
    try:
        if args.verbose:
            print(f"\nGenerating response...")
            print(f"  Temperature: {args.temperature or agent_config.get('temperature', 0.7)}")
            print(f"  Max tokens: {args.max_tokens or agent_config.get('max_tokens', 4096)}")

        ai_response = llm_client.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=args.temperature or agent_config.get("temperature", 0.7),
            max_tokens=args.max_tokens or agent_config.get("max_tokens", 4096)
        )

        if args.verbose:
            print(f"✓ Response generated successfully ({len(ai_response)} characters)")

    except Exception as e:
        print(f"Error generating AI response: {e}", file=sys.stderr)
        sys.exit(1)

    # Prepare output
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = f"""# {agent_config['name']} Output

**Generated:** {timestamp}
**Model:** {agent_config.get('model', 'unknown')}
**Agent ID:** {agent_config.get('id', 'unknown')}

---

{ai_response}
"""

    # Write output
    output_dir = pathlib.Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output.md"
    output_file.write_text(result, encoding="utf-8")

    if args.verbose:
        print(f"\n✓ Output written to: {output_file}")
    else:
        print(f"✓ Agent execution complete: {output_file}")

if __name__ == "__main__":
    main()
