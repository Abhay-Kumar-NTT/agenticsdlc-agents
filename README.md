# AgenticSDLC - Multi-Provider AI Agent System

An AI-native SDLC orchestration platform using specialized agents for product discovery, architecture, development, QA, and DevOps.

## 🚀 Quick Start (3 Steps)

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
# Choose your provider:
export ANTHROPIC_API_KEY="sk-ant-..."  # Claude (recommended)
export OPENAI_API_KEY="sk-..."         # GPT-4
export GOOGLE_API_KEY="..."            # Gemini
```

### 3. Run
```bash
# Using shortcut script
./run.sh product --verbose

# Or directly
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --verbose
```

**Output:** `artifacts/product/output.md` ✨

## 🎯 What It Does

Transforms product vision into structured deliverables using AI agents:

```
Vision.md
    ↓
[Product Agent] → PRD, Epics, User Stories
    ↓
[Architecture Agent] → HLD, LLD, ADRs, API Contracts
    ↓
[Developer Agent] → Code, Documentation
    ↓
[QA Agent] → Test Plans, Test Cases
    ↓
[DevOps Agent] → Infrastructure, CI/CD, Deployment
```

## ✨ Features

- 🤖 **Multi-Provider Support**: OpenAI (GPT-4), Anthropic (Claude), Google (Gemini), Azure OpenAI
- 🔌 **Auto-Detection**: Automatically detects provider from model name
- ⚙️ **Configurable**: Temperature, max tokens, model per agent
- 🔄 **Chainable**: Output of one agent → input to next
- 📝 **Structured Output**: Clean markdown suitable for GitHub Issues
- 🐛 **Verbose Mode**: See what's happening step-by-step

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 4 steps
- **[README_LLM_SETUP.md](README_LLM_SETUP.md)** - Detailed provider setup
- **[EXAMPLES.md](EXAMPLES.md)** - Usage examples and patterns
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical architecture

## 🤖 Available Agents

| Agent | Input | Output |
|-------|-------|--------|
| **Product Agent** | Raw vision | PRD, Epics, User Stories |
| **Architecture Agent** | PRD | HLD, LLD, ADRs, API Contracts |
| **Developer Agent** | Architecture | Code, Documentation |
| **QA Agent** | Code | Test Plans, Test Cases |
| **DevOps Agent** | Architecture | Infrastructure, CI/CD |

## 📦 Supported AI Models

### Anthropic Claude (Recommended)
```yaml
model: claude-3-5-sonnet-20241022
provider: anthropic
```
- Best for: Structured output, following instructions
- Speed: Fast
- Quality: Excellent

### OpenAI GPT-4
```yaml
model: gpt-4
provider: openai
```
- Best for: Creative content, code generation
- Speed: Medium
- Quality: Excellent

### Google Gemini
```yaml
model: gemini-pro
provider: google
```
- Best for: Fast iterations, prototyping
- Speed: Very fast
- Quality: Good

### Azure OpenAI
```yaml
model: gpt-4
provider: azure-openai
azure_endpoint: https://your-resource.openai.azure.com
azure_deployment: your-deployment-name
```
- Best for: Enterprise, compliance requirements
- Speed: Medium
- Quality: Excellent (same as OpenAI)

## 🛠️ Usage Examples

### Run Product Agent
```bash
./run.sh product --verbose
```

### Run Architecture Agent
```bash
./run.sh architecture --verbose
```

### Chain Multiple Agents
```bash
./run.sh product && \
./run.sh architecture && \
./run.sh developer
```

### Override Configuration
```bash
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --temperature 0.3 \
  --max-tokens 8000 \
  --verbose
```

### Test All Providers
```bash
python scripts/test_llm.py
```

## 🔧 Configuration

### Per-Agent Config (`agents/*/agent.yaml`)
```yaml
id: product-agent
name: Product Agent
model: claude-3-5-sonnet-20241022  # Model to use
provider: anthropic                # Optional: auto-detected
temperature: 0.7                   # Creativity (0.0-1.0)
max_tokens: 4096                   # Max output length
```

### Environment Variables
```bash
OPENAI_API_KEY=sk-...          # For OpenAI/GPT
ANTHROPIC_API_KEY=sk-ant-...   # For Claude
GOOGLE_API_KEY=...             # For Gemini
```

### Command-Line Overrides
```bash
--temperature 0.5    # Override config temperature
--max-tokens 8000    # Override config max_tokens
--verbose            # Show detailed progress
```

## 📁 Project Structure

```
agenticsdlc-agents/
├── scripts/
│   ├── run_agent.py       # Main entry point
│   ├── llm_client.py      # Multi-provider LLM client
│   └── test_llm.py        # Test all providers
├── agents/
│   ├── product-agent/
│   │   ├── agent.yaml     # Agent configuration
│   │   └── prompt.md      # System prompt
│   ├── architecture-agent/
│   ├── developer-agent/
│   ├── qa-agent/
│   └── devops-agent/
├── artifacts/
│   ├── vision.md          # Input: Product vision
│   ├── product/           # Output: PRD, user stories
│   ├── architecture/      # Output: HLD, LLD
│   └── .../
├── run.sh                 # Convenience wrapper
├── requirements.txt       # Python dependencies
├── .env.example          # API key template
└── *.md                   # Documentation
```

## 🔐 Security

- ✅ API keys in environment variables only
- ✅ `.env` excluded from git
- ✅ No secrets in code or configs
- ⚠️ Rotate keys regularly
- ⚠️ Use separate keys for dev/prod

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "API key not found" | Set `ANTHROPIC_API_KEY` environment variable |
| Nothing happens | Add `--verbose` flag to see progress |
| Output cut off | Increase `--max-tokens 8000` |
| Too random | Decrease `--temperature 0.2` |

## 📊 Cost Optimization

1. **Use cheaper models for drafts**: `gpt-3.5-turbo`, `gemini-1.5-flash`
2. **Limit tokens**: Set `max_tokens: 2000` instead of 4096
3. **Use temperature 0**: More deterministic = less regeneration
4. **Cache locally**: Reuse outputs instead of re-running

## 🔗 Get API Keys

- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/settings/keys
- **Google:** https://makersuite.google.com/app/apikey
- **Azure:** https://portal.azure.com/

## 🚀 Advanced Usage

### Chain All Agents
```bash
#!/bin/bash
./run.sh product && \
./run.sh architecture && \
./run.sh developer && \
./run.sh qa && \
./run.sh devops
echo "✓ Full SDLC pipeline complete!"
```

### Compare Models
```bash
# Run with different models
./run.sh product  # Uses Claude (from config)

# Edit agent.yaml to use GPT-4, then:
./run.sh product

# Compare outputs
diff artifacts/product-claude/ artifacts/product-gpt4/
```

### Batch Processing
```bash
for vision in artifacts/vision-*.md; do
  ./run.sh product --input "$vision"
done
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-agent`
3. Commit changes: `git commit -am 'Add new agent'`
4. Push to branch: `git push origin feature/new-agent`
5. Submit pull request

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with:
- [OpenAI API](https://platform.openai.com/)
- [Anthropic Claude API](https://www.anthropic.com/)
- [Google Generative AI](https://ai.google.dev/)

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/your-repo/issues)
- **Docs:** See documentation files
- **Examples:** See [EXAMPLES.md](EXAMPLES.md)

---

**Made with ❤️ for better software development workflows**
