# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set API Key

Choose one provider and set its API key:

**For Claude (Anthropic) - Recommended:**
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**For GPT-4 (OpenAI):**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
```

**For Gemini (Google):**
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-key-here"

# Linux/Mac
export GOOGLE_API_KEY="your-key-here"
```

## 3. Test Setup (Optional)

```bash
python scripts/test_llm.py
```

## 4. Run Your First Agent

```bash
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --verbose
```

Output will be in: `artifacts/product/output.md`

## 5. Switch Models

Edit `agents/product-agent/agent.yaml`:

**For Claude:**
```yaml
model: claude-3-5-sonnet-20241022
provider: anthropic
```

**For GPT-4:**
```yaml
model: gpt-4
provider: openai
```

**For Gemini:**
```yaml
model: gemini-pro
provider: google
```

## Next Steps

- See [README_LLM_SETUP.md](README_LLM_SETUP.md) for detailed configuration
- Create more agents in the `agents/` directory
- Customize prompts in `agents/*/prompt.md`
- Chain agents: output of one → input of next

## Troubleshooting

**"Module not found"** → Run `pip install -r requirements.txt`

**"API key not found"** → Check environment variable is set in current shell

**"Nothing happens"** → Add `--verbose` flag to see what's happening

## Get API Keys

- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys
- Google: https://makersuite.google.com/app/apikey
