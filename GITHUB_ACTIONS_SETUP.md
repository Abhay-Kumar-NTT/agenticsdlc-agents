# GitHub Actions Setup Guide

This guide explains how to set up GitHub Actions to run AgenticSDLC agents automatically.

## Prerequisites

1. Your code is pushed to a GitHub repository
2. You have admin access to the repository
3. You have API keys for the AI providers you want to use

## Step 1: Add API Keys as GitHub Secrets

### Navigate to Secrets Settings

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Add Your API Key(s)

Add one or more of these secrets depending on which AI providers you're using:

#### For OpenAI (GPT-4, GPT-4o, etc.)
- **Name:** `OPENAI_API_KEY`
- **Value:** `sk-proj-your-openai-api-key-here`

#### For Anthropic (Claude)
- **Name:** `ANTHROPIC_API_KEY`
- **Value:** `sk-ant-your-anthropic-api-key-here`

#### For Google (Gemini)
- **Name:** `GOOGLE_API_KEY`
- **Value:** `your-google-api-key-here`

#### For Azure OpenAI
- **Name:** `AZURE_OPENAI_API_KEY`
- **Value:** `your-azure-api-key-here`
- **Name:** `AZURE_OPENAI_ENDPOINT`
- **Value:** `https://your-resource.openai.azure.com`

### Screenshot Guide

```
Repository → Settings → Secrets and variables → Actions → New repository secret

┌─────────────────────────────────────────────────────┐
│ Name *                                              │
│ ┌─────────────────────────────────────────────┐   │
│ │ OPENAI_API_KEY                              │   │
│ └─────────────────────────────────────────────┘   │
│                                                     │
│ Secret *                                            │
│ ┌─────────────────────────────────────────────┐   │
│ │ sk-proj-...                                 │   │
│ └─────────────────────────────────────────────┘   │
│                                                     │
│ [ Add secret ]                                      │
└─────────────────────────────────────────────────────┘
```

## Step 2: Verify Workflow Files

The workflow files should already be updated to:
- ✅ Install Python dependencies from `requirements.txt`
- ✅ Use secrets for API keys
- ✅ Run with `--verbose` flag

### Product Agent Workflow
File: `.github/workflows/product-agent.yml`

```yaml
- name: Install dependencies
  run: pip install -r requirements.txt

- name: Run Product Agent
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    python scripts/run_agent.py \
      --agent agents/product-agent/agent.yaml \
      --prompt agents/product-agent/prompt.md \
      --input ${{ github.event.inputs.vision_path }} \
      --output artifacts/product/ \
      --verbose
```

## Step 3: Run a Workflow

### Manual Trigger (workflow_dispatch)

1. Go to **Actions** tab in your repository
2. Select a workflow (e.g., "Product Agent")
3. Click **Run workflow** button
4. Fill in any required inputs
5. Click **Run workflow**

### Monitor Progress

1. Click on the running workflow
2. Click on the job name (e.g., "run-product-agent")
3. Expand each step to see logs
4. Look for the `--verbose` output to see AI generation progress

## Step 4: Verify Secrets Are Working

If you see this error:
```
Error initializing LLM client: API key not found
```

**Solution:**
1. Verify the secret name matches exactly (case-sensitive)
2. Verify the secret is added to the repository (not organization)
3. Check that the workflow file references the correct secret name

## Common Issues

### Issue: "OpenAI package not installed"

**Solution:** Workflow needs to install dependencies.

Fixed in workflow:
```yaml
- name: Install dependencies
  run: pip install -r requirements.txt
```

### Issue: "API key not found"

**Causes:**
1. Secret not added to repository
2. Secret name mismatch (e.g., `OPENAI_API_KEY` vs `OPENAI_KEY`)
3. Workflow not updated to pass secrets as environment variables

**Solution:**
1. Add secret to repository settings
2. Verify workflow has `env:` section with correct secret name:
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Issue: "Model not found" or "Invalid model"

**Solution:** Check your `agent.yaml` has a valid model name:
- ✅ `gpt-4o`, `gpt-4`, `gpt-3.5-turbo`
- ✅ `claude-3-5-sonnet-20241022`
- ✅ `gemini-pro`
- ❌ `gpt-5.4-mini` (unless available in your account)

### Issue: Workflow succeeds but no output

**Check:**
1. Look at workflow logs for errors
2. Verify input file exists (e.g., `artifacts/vision.md`)
3. Check if commit step failed (may need to pull before push)

## Step 5: Chain Multiple Agents

You can trigger agents in sequence:

### Option A: Manual Chaining
1. Run Product Agent → generates PRD
2. Wait for completion
3. Run Architecture Agent → uses PRD as input

### Option B: Workflow Dependency (Advanced)

Create a workflow that runs all agents in sequence:

```yaml
name: Full SDLC Pipeline

on:
  workflow_dispatch:

jobs:
  product:
    runs-on: ubuntu-latest
    steps:
      # ... product agent steps

  architecture:
    needs: product  # Wait for product to complete
    runs-on: ubuntu-latest
    steps:
      # ... architecture agent steps

  developer:
    needs: architecture
    runs-on: ubuntu-latest
    steps:
      # ... developer agent steps
```

## Security Best Practices

✅ **Do:**
- Store API keys as GitHub Secrets
- Use repository secrets for private repos
- Use environment secrets for organization-wide keys
- Rotate keys regularly
- Use separate keys for different environments

❌ **Don't:**
- Commit API keys to the repository
- Use secrets in PR comments or logs
- Share secrets across public forks
- Print secrets in workflow logs (`echo $OPENAI_API_KEY`)

## Cost Management

To control API costs:

1. **Limit max_tokens** in `agent.yaml`:
```yaml
max_tokens: 2000  # Instead of 4096
```

2. **Use cheaper models**:
```yaml
model: gpt-3.5-turbo  # Instead of gpt-4
```

3. **Disable auto-trigger**: Only use `workflow_dispatch` (manual)

4. **Set up billing alerts** in your AI provider dashboard

## Workflow Permissions

Each workflow needs appropriate permissions:

```yaml
permissions:
  contents: write  # To commit generated files
  issues: write    # To create GitHub issues
  pull-requests: write  # To create PRs
```

## Debugging Workflows

### View Detailed Logs

Add `--verbose` flag to see AI generation progress:
```yaml
python scripts/run_agent.py ... --verbose
```

### Test Locally First

Before pushing to GitHub, test locally:
```powershell
# Windows PowerShell
$env:OPENAI_API_KEY="sk-proj-..."
python scripts/run_agent.py --agent agents/product-agent/agent.yaml --prompt agents/product-agent/prompt.md --input artifacts/vision.md --output artifacts/product/ --verbose
```

### Enable Workflow Debug Logging

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add **New repository variable**:
   - Name: `ACTIONS_STEP_DEBUG`
   - Value: `true`

## Next Steps

1. ✅ Add API key secrets
2. ✅ Verify workflow files are updated
3. ✅ Test one workflow manually
4. ✅ Chain multiple agents if needed
5. ✅ Set up cost monitoring

## Example: Full Setup Checklist

- [ ] Code pushed to GitHub
- [ ] API key added as secret (e.g., `OPENAI_API_KEY`)
- [ ] Workflow file has `pip install -r requirements.txt`
- [ ] Workflow file has `env:` section with API key
- [ ] Input file exists (e.g., `artifacts/vision.md`)
- [ ] Agent config has valid model name
- [ ] Run workflow manually from Actions tab
- [ ] Check logs for errors
- [ ] Verify output file created
- [ ] Verify commit pushed

## Support Resources

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **GitHub Secrets Docs:** https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **OpenAI API Docs:** https://platform.openai.com/docs
- **Anthropic API Docs:** https://docs.anthropic.com/

## Quick Reference

| Task | Location |
|------|----------|
| Add API key secret | Settings → Secrets and variables → Actions |
| Run workflow | Actions tab → Select workflow → Run workflow |
| View logs | Actions tab → Click workflow run → Click job |
| Edit workflow | `.github/workflows/*.yml` |
| Check secrets | Settings → Secrets and variables → Actions |
