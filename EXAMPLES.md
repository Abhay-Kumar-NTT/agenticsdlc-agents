# Usage Examples

## Example 1: Run Product Agent with Claude

```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Run agent
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --verbose
```

**Output:** `artifacts/product/output.md`

## Example 2: Run Architecture Agent with GPT-4

1. Update `agents/architecture-agent/agent.yaml`:
```yaml
model: gpt-4
provider: openai
```

2. Set API key and run:
```bash
export OPENAI_API_KEY="sk-your-key-here"

python scripts/run_agent.py \
  --agent agents/architecture-agent/agent.yaml \
  --prompt agents/architecture-agent/prompt.md \
  --input artifacts/product/output.md \
  --output artifacts/architecture/ \
  --verbose
```

## Example 3: Run with Gemini (More Creative)

1. Update agent.yaml:
```yaml
model: gemini-pro
provider: google
temperature: 0.9
```

2. Run:
```bash
export GOOGLE_API_KEY="your-key-here"

python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product-creative/ \
  --temperature 0.9
```

## Example 4: Compare Models Side-by-Side

```bash
# Run with Claude
export ANTHROPIC_API_KEY="sk-ant-..."
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product-claude/

# Update to GPT-4 in agent.yaml, then:
export OPENAI_API_KEY="sk-..."
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product-gpt4/

# Update to Gemini in agent.yaml, then:
export GOOGLE_API_KEY="..."
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product-gemini/

# Compare outputs:
diff artifacts/product-claude/output.md artifacts/product-gpt4/output.md
```

## Example 5: Chain Agents (Sequential Processing)

```bash
# Step 1: Product Agent generates PRD
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/

# Step 2: Architecture Agent uses PRD as input
python scripts/run_agent.py \
  --agent agents/architecture-agent/agent.yaml \
  --prompt agents/architecture-agent/prompt.md \
  --input artifacts/product/output.md \
  --output artifacts/architecture/

# Step 3: Developer Agent uses architecture as input
python scripts/run_agent.py \
  --agent agents/developer-agent/agent.yaml \
  --prompt agents/developer-agent/prompt.md \
  --input artifacts/architecture/output.md \
  --output artifacts/development/
```

## Example 6: Deterministic Output (Low Temperature)

```bash
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --temperature 0.1 \
  --verbose
```

## Example 7: Long-Form Output

```bash
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --max-tokens 8000 \
  --verbose
```

## Example 8: Test All Your API Keys

```bash
# Set all your API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."

# Run test script
python scripts/test_llm.py
```

**Expected output:**
```
AgenticSDLC LLM Client Test
============================================================

============================================================
Testing OPENAI with gpt-4o-mini
============================================================
✓ API key found: OPENAI_API_KEY
✓ Client initialized successfully
  Sending test prompt...
✓ Response received: Hello, AgenticSDLC!

============================================================
Testing ANTHROPIC with claude-3-5-sonnet-20241022
============================================================
✓ API key found: ANTHROPIC_API_KEY
✓ Client initialized successfully
  Sending test prompt...
✓ Response received: Hello, AgenticSDLC!

============================================================
Testing GOOGLE with gemini-pro
============================================================
✓ API key found: GOOGLE_API_KEY
✓ Client initialized successfully
  Sending test prompt...
✓ Response received: Hello, AgenticSDLC!

============================================================
SUMMARY
============================================================
openai       ✓ PASS
anthropic    ✓ PASS
google       ✓ PASS

✓ At least one provider is working!
  You can now run agents with run_agent.py
```

## Example 9: Azure OpenAI

1. Update agent.yaml:
```yaml
model: gpt-4
provider: azure-openai
azure_endpoint: https://your-resource.openai.azure.com
azure_deployment: your-deployment-name
```

2. Set environment variables:
```bash
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
```

3. Run:
```bash
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/
```

## Example 10: Batch Processing Multiple Inputs

```bash
# Process multiple vision documents
for input_file in artifacts/vision-*.md; do
  output_name=$(basename "$input_file" .md)
  python scripts/run_agent.py \
    --agent agents/product-agent/agent.yaml \
    --prompt agents/product-agent/prompt.md \
    --input "$input_file" \
    --output "artifacts/product-$output_name/"
done
```

## Model Recommendations by Use Case

### For Product Discovery (PRD, User Stories)
- **Best:** `claude-3-5-sonnet-20241022` (balanced, follows structure well)
- **Alternative:** `gpt-4` (creative, good at personas)
- **Fast:** `gemini-1.5-flash` (quick iterations)

### For Architecture (HLD, LLD, ADRs)
- **Best:** `claude-3-opus-20240229` (technical depth)
- **Alternative:** `gpt-4` (good at diagrams/mermaid)
- **Fast:** `claude-3-5-sonnet-20241022` (good balance)

### For Code Generation
- **Best:** `gpt-4` (wide training on code)
- **Alternative:** `claude-3-5-sonnet-20241022` (careful, secure)
- **Fast:** `gpt-3.5-turbo` (quick prototypes)

### For Testing & QA
- **Best:** `claude-3-5-sonnet-20241022` (thorough edge cases)
- **Alternative:** `gpt-4` (creative test scenarios)

### For DevOps & Infrastructure
- **Best:** `gpt-4` (good at YAML/configs)
- **Alternative:** `claude-3-5-sonnet-20241022` (security-conscious)

## Cost Optimization Tips

1. **Start with cheaper models for drafts:**
   ```yaml
   model: gpt-3.5-turbo  # or gemini-1.5-flash
   ```

2. **Limit max_tokens for structured output:**
   ```yaml
   max_tokens: 2000  # Instead of 4096
   ```

3. **Use temperature 0 for deterministic output:**
   ```yaml
   temperature: 0.0  # No need to regenerate
   ```

4. **Cache responses locally:**
   - Outputs are saved to `artifacts/`
   - Reuse when possible instead of re-running

## Troubleshooting Examples

### Issue: "API key not found"
```bash
# Check current environment
env | grep API_KEY

# Set the key (must be in same shell session)
export ANTHROPIC_API_KEY="sk-ant-..."

# Verify it's set
echo $ANTHROPIC_API_KEY
```

### Issue: Output is cut off
```bash
# Increase max_tokens
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --max-tokens 8000
```

### Issue: Output is too random/inconsistent
```bash
# Lower temperature
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --temperature 0.2
```

### Issue: Want to see what's happening
```bash
# Add verbose flag
python scripts/run_agent.py \
  --agent agents/product-agent/agent.yaml \
  --prompt agents/product-agent/prompt.md \
  --input artifacts/vision.md \
  --output artifacts/product/ \
  --verbose
```
