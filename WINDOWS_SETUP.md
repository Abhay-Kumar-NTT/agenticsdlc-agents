# Windows PowerShell Setup Guide

Quick reference for running AgenticSDLC on Windows with PowerShell.

## 1. Install Python Packages

```powershell
pip install -r requirements.txt
```

## 2. Set API Key (PowerShell Syntax)

### Option A: Session Variable (Temporary)
Only lasts for current PowerShell session:

```powershell
# For OpenAI/GPT-4
$env:OPENAI_API_KEY="sk-proj-your-key-here"

# For Anthropic/Claude
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# For Google/Gemini
$env:GOOGLE_API_KEY="your-key-here"
```

### Option B: Permanent User Variable (Recommended)
Persists across sessions:

```powershell
# For OpenAI/GPT-4
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-proj-your-key-here', 'User')

# For Anthropic/Claude
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-your-key-here', 'User')

# For Google/Gemini
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'your-key-here', 'User')
```

**After setting permanent variables, restart PowerShell.**

### Option C: System Environment Variables (GUI)
1. Press `Win + X` → System
2. Advanced system settings → Environment Variables
3. Under "User variables", click "New"
4. Variable name: `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`, etc.)
5. Variable value: Your API key
6. Click OK
7. Restart PowerShell

## 3. Verify API Key is Set

```powershell
# Check if key is set
echo $env:OPENAI_API_KEY

# Or
echo $env:ANTHROPIC_API_KEY
```

You should see your API key printed (or part of it).

## 4. Run Agent

```powershell
python scripts/run_agent.py `
  --agent agents/product-agent/agent.yaml `
  --prompt agents/product-agent/prompt.md `
  --input artifacts/vision.md `
  --output artifacts/product/ `
  --verbose
```

**Note:** In PowerShell, use backtick `` ` `` for line continuation (not `\` like bash).

## 5. Test All Providers

```powershell
python scripts/test_llm.py
```

## Common PowerShell Commands

### Navigate directories
```powershell
cd "c:\Users\267564\OneDrive - NTT Data Group\_GenAI CoE\Exploration\agenticsdlc-agents"
```

### List files
```powershell
ls
# or
dir
```

### View file contents
```powershell
cat artifacts/product/output.md
# or
Get-Content artifacts/product/output.md
```

### Check Python version
```powershell
python --version
```

### Check installed packages
```powershell
pip list
```

## Troubleshooting

### "export is not recognized"
❌ **Wrong (bash syntax):**
```bash
export OPENAI_API_KEY="sk-..."
```

✅ **Correct (PowerShell syntax):**
```powershell
$env:OPENAI_API_KEY="sk-..."
```

### "API key not found"
```powershell
# Check if variable is set
echo $env:OPENAI_API_KEY

# If empty, set it:
$env:OPENAI_API_KEY="sk-proj-your-key-here"

# Try again:
python scripts/run_agent.py --agent agents/product-agent/agent.yaml --prompt agents/product-agent/prompt.md --input artifacts/vision.md --output artifacts/product/ --verbose
```

### "Module not found"
```powershell
# Install missing packages
pip install -r requirements.txt

# Or install specific package:
pip install openai
pip install anthropic
pip install google-generativeai
```

### Line continuation in PowerShell
❌ **Wrong (bash):**
```bash
python script.py \
  --arg1 value \
  --arg2 value
```

✅ **Correct (PowerShell):**
```powershell
python script.py `
  --arg1 value `
  --arg2 value
```

Or use one line:
```powershell
python script.py --arg1 value --arg2 value
```

### Path with spaces
✅ **Always use quotes:**
```powershell
cd "c:\path with spaces\folder"
python scripts/run_agent.py --input "artifacts/my file.md"
```

## Quick Reference

| Task | PowerShell Command |
|------|-------------------|
| Set temp env var | `$env:VAR="value"` |
| Set permanent env var | `[System.Environment]::SetEnvironmentVariable('VAR', 'value', 'User')` |
| View env var | `echo $env:VAR` |
| List env vars | `Get-ChildItem Env:` |
| Remove env var | `Remove-Item Env:\VAR` |
| Change directory | `cd "path"` |
| List files | `ls` or `dir` |
| View file | `cat file.txt` or `Get-Content file.txt` |
| Line continuation | Backtick: `` ` `` |

## Example: Full Workflow

```powershell
# 1. Navigate to project
cd "c:\Users\267564\OneDrive - NTT Data Group\_GenAI CoE\Exploration\agenticsdlc-agents"

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Set API key
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# 4. Verify it's set
echo $env:ANTHROPIC_API_KEY

# 5. Test the setup
python scripts/test_llm.py

# 6. Run product agent
python scripts/run_agent.py --agent agents/product-agent/agent.yaml --prompt agents/product-agent/prompt.md --input artifacts/vision.md --output artifacts/product/ --verbose

# 7. View output
cat artifacts/product/output.md
```

## Using .env File (Alternative)

If you prefer to use a `.env` file:

1. **Install python-dotenv:**
```powershell
pip install python-dotenv
```

2. **Create .env file:**
```powershell
# Copy example
Copy-Item .env.example .env

# Edit .env file in notepad
notepad .env
```

3. **Add keys to .env:**
```
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-key-here
```

4. **Update run_agent.py** to load .env (add at top):
```python
from dotenv import load_dotenv
load_dotenv()
```

## Security Tips

✅ **Do:**
- Use environment variables
- Add `.env` to `.gitignore`
- Use different keys for dev/prod

❌ **Don't:**
- Commit API keys to git
- Share API keys in chat/email
- Hardcode keys in scripts

## Next Steps

- See [QUICKSTART.md](QUICKSTART.md) for general usage
- See [README_LLM_SETUP.md](README_LLM_SETUP.md) for detailed configuration
- See [EXAMPLES.md](EXAMPLES.md) for usage examples
