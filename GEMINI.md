# Coding Agent Guide

> ⚠️ **MANDATORY SOP FOR ALL CODE CHANGES**:
> 1. **100% Test Coverage**: Always run `pytest --cov=app` and maintain 100% coverage across `app/`.
> 2. **Doc Sync**: Always update `project_brief.md`, `README.md`, and `walkthrough.md`.
> 3. **GitHub Push**: Always `git commit` and `git push origin main`.
> 4. **Redeploy & Test**: Always redeploy to Agent Runtime and ensure local playground (`http://localhost:8000/dev-ui/?app=app`) is healthy.

## Prerequisites

Install the CLI (one-time):
```bash
uv tool install google-agents-cli
```

---

## Development Phases

### Phase 1: Understand Requirements
Before writing any code, understand the project's requirements, constraints, and success criteria.

### Phase 2: Build and Implement
Implement agent logic in `app/`. Use `agents-cli playground` for interactive testing. Iterate based on user feedback.

### Phase 3: The Evaluation Loop (Main Iteration Phase)
Start with 1-2 eval cases, run `agents-cli eval generate`, then `agents-cli eval grade`, iterate by making changes and rerunning both commands until satisfied. Expect 5-10+ iterations. Once you have a baseline, reach for `agents-cli eval compare` (regression diffs), `agents-cli eval analyze` (cluster failure modes), and `agents-cli eval optimize` (auto-tune prompts). See the **Evaluation Guide** for metrics, dataset schema, LLM-as-judge config, and common gotchas.

### Phase 4: Pre-Deployment Tests & 100% Coverage
Run `uv run pytest tests/unit tests/integration --cov=app`. Fix issues until all tests pass with 100% coverage.

### Phase 5: Deploy to Dev
Run `agents-cli deploy` after tests pass. See the **Deployment Guide** for details.

### Phase 6: Push to GitHub & Update Docs
Update `project_brief.md`, `README.md`, and `walkthrough.md`. Perform `git commit` and `git push origin main`.

---

## Development Commands

| Command | Purpose |
|---------|---------|
| `agents-cli playground` | Interactive local testing |
| `uv run pytest tests/unit tests/integration --cov=app` | Run unit/integration tests with 100% coverage check |
| `agents-cli eval dataset synthesize` | Synthesize multi-turn eval scenarios for your agent |
| `agents-cli eval generate` | Run agent on eval dataset, produce traces |
| `agents-cli eval grade` | Run agent evaluations on the traces |
| `agents-cli eval compare` | Compare two grade-results files (regression check) |
| `agents-cli eval analyze` | Cluster failure modes from grade results |
| `agents-cli eval metric list` | List built-in metrics available in the SDK |
| `agents-cli eval optimize` | Auto-tune agent prompts using eval data |
| `agents-cli lint` | Check code quality |
| `agents-cli infra single-project` | Set up project infrastructure (Terraform) |
| `agents-cli deploy` | Deploy to Agent Runtime |
| `agents-cli scaffold enhance` | Add deployment target or CI/CD to project |
| `agents-cli scaffold upgrade` | Upgrade project to latest version |

---

## Operational Guidelines for Coding Agents

- **Code preservation**: Only modify code directly targeted by the user's request. Preserve all surrounding code, config values (e.g., `model`), comments, and formatting.
- **NEVER change the model** unless explicitly asked.
- **Model 404 errors**: Fix `GOOGLE_CLOUD_LOCATION` (e.g., `global` instead of `us-east1`), not the model name.
- **ADK tool imports**: Import the tool instance, not the module: `from google.adk.tools.load_web_page import load_web_page`
- **Run Python with `uv`**: `uv run python script.py`. Run `agents-cli install` first.
- **Stop on repeated errors**: If the same error appears 3+ times, fix the root cause instead of retrying.
- **Terraform conflicts** (Error 409): Use `terraform import` instead of retrying creation.
