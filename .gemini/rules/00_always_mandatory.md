# Enforced Standard Operating Procedure for All Tasks

Whenever making changes, adding features, or modifying code in this codebase, you MUST automatically execute the following steps without needing reminders:

1. **100% Test Coverage**:
   - Write/update unit tests in `tests/unit/` for all changed or added functions and modules.
   - Run `uv run pytest --cov=app --cov-report=term-missing` and ensure 100% code coverage across all files in `app/`.

2. **Complete Documentation Sync**:
   - Update `project_brief.md` with any new architectures, tools, sub-agents, or data schemas.
   - Update `README.md` and `walkthrough.md` with architecture diagrams, sample prompts, testing instructions, and deployment IDs.
   - Keep docstrings and comments up to date.

3. **Automatic GitHub Push**:
   - Perform `git add .`
   - Commit with a clear, descriptive commit message.
   - Push to `origin main` on GitHub.

4. **Agent Redeployment**:
   - Automatically redeploy the agent to Agent Runtime (`agents-cli deploy -d agent_runtime --no-confirm-project --project qwiklabs-gcp-03-ef713aa8c2c9 --region us-central1`).
   - Verify local playground server (`agents-cli playground`) is running and healthy.
