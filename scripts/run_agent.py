import argparse
import pathlib
import yaml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    agent_config = yaml.safe_load(open(args.agent, encoding="utf-8"))
    prompt = pathlib.Path(args.prompt).read_text(encoding="utf-8")
    input_context = pathlib.Path(args.input).read_text(encoding="utf-8")

    # Replace this with GitHub Models, OpenAI API, Azure OpenAI, Anthropic, etc.
    result = f"""
# {agent_config['name']} Output

## Input Context
{input_context}

## Generated Output
TODO: Call selected AI model here using prompt + input context.
"""

    output_dir = pathlib.Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "output.md").write_text(result, encoding="utf-8")

if __name__ == "__main__":
    main()
