# Multi-Provider LLM Setup Guide

The AgenticSDLC agent system now supports multiple AI providers: OpenAI (GPT-4), Anthropic (Claude), Google (Gemini), and Azure OpenAI.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install only what you need:
```bash
# For OpenAI/GPT-4
pip install openai pyyaml

# For Anthropic/Claude
pip install anthropic pyyaml

# For Google/Gemini
pip install google-generativeai pyyaml
```

### 2. Set Up API Keys

**Option A: Environment Variables (Recommended)**

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-key-here"
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
$env:GOOGLE_API_KEY="your-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export GOOGLE_API_KEY="your-key-here"
```

**Option B: .env File**

1. Copy `.env.example` to `.env`
2. Fill in your API keys
3. Install python-dotenv: `pip install python-dotenv`
4. Add to run_agent.py: `from dotenv import load_dotenv; load_dotenv()`

### 3. Configure Agent Model

Edit your `agents/*/agent.yaml` file:

**For OpenAI/GPT-4:**
```yaml
model: gpt-4
# or: gpt-4-turbo, gpt-4o, gpt-3.5-turbo
```

**For Anthropic/Claude:**
```yaml
model: claude-3-5-sonnet-20241022
provider: anthropic
# or: claude-3-opus-20240229, claude-3-haiku-20240307
```

**For Google/Gemini:**
```yaml
model: gemini-pro
provider: google
# or: gemini-1.5-pro, gemini-1.5-flash
```

**For Azure OpenAI:**
```yaml
model: gpt-4
provider: azure-openai
azure_endpoint: https://your-resource.openai.azure.com
azure_deployment: your-deployment-name
```

### 4. Run Agent

```bash
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --verbose
```

## Advanced Configuration

### Optional Parameters in agent.yaml

```yaml
id: product-agent
name: Product Agent
model: gpt-4              # Required: model name
provider: openai          # Optional: auto-detected from model name
temperature: 0.7          # Optional: default 0.7
max_tokens: 4096          # Optional: default 4096

# Azure-specific (if using Azure OpenAI)
azure_endpoint: https://your-resource.openai.azure.com
azure_deployment: your-deployment-name
api_version: 2024-02-15-preview
```

### Command-Line Overrides

```bash
# Override temperature and max tokens
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --temperature 0.5 \
  --max-tokens 8000 \
  --verbose
```

## Supported Models

### OpenAI
- `gpt-4`, `gpt-4-turbo`, `gpt-4o`
- `gpt-3.5-turbo`
- `o1-preview`, `o1-mini`

### Anthropic
- `claude-3-5-sonnet-20241022` (recommended)
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`

### Google
- `gemini-pro`
- `gemini-1.5-pro`
- `gemini-1.5-flash`

### Azure OpenAI
- Any model available in your Azure deployment

## Troubleshooting

### "API key not found" error
- Ensure environment variable is set in your current shell session
- Check variable name matches: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`
- Restart your terminal after setting variables

### "Module not found" error
- Run: `pip install -r requirements.txt`
- Or install specific package: `pip install openai` / `anthropic` / `google-generativeai`

### Provider auto-detection not working
- Explicitly set `provider:` in your `agent.yaml`
- Supported values: `openai`, `anthropic`, `google`, `azure-openai`

## API Key Setup Links

- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/settings/keys
- **Google AI Studio:** https://makersuite.google.com/app/apikey
- **Azure OpenAI:** https://portal.azure.com/

## Security Best Practices

1. ✅ Use environment variables, not hardcoded keys
2. ✅ Add `.env` to `.gitignore`
3. ✅ Never commit API keys to version control
4. ✅ Use separate keys for dev/prod
5. ✅ Rotate keys regularly
