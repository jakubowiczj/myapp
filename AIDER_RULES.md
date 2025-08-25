# Aider Session Rules – Plan First, Then Act

**Always follow this workflow:**

1) PLAN
   - Before making ANY edits, output a concise plan with sections:
     - Objectives (1–3 bullets)
     - Proposed changes (exact file paths to create/modify/delete)
     - Touch points (frameworks, env vars, APIs)
     - Risks & open questions (list)
     - Test plan (how we’ll verify locally; URLs, commands, checks)
     - Rollback plan (how to revert if needed)
   - End your plan with a prompt for approval:
     “Reply with **APPROVE** to proceed, or **ADJUST:** <your changes>”.

2) WAIT
   - Do nothing until I respond with **APPROVE**.
   - If I reply with **ADJUST**, update the plan and ask again.

3) EXECUTE (after APPROVE)
   - Implement in small, reviewable chunks.
   - For each chunk:
     - Show exact diffs for each file you change.
     - Keep commits atomic with clear messages (Conventional Commits style).
     - Run any relevant checks/tests/build if configured and paste key output.
     - Stop after each chunk and ask: “Proceed with next chunk? (APPROVE/ADJUST)”.

4) CONSTRAINTS
   - Don’t invent endpoints or env vars. If unknown, list as open questions.
   - Don’t refactor unrelated code unless explicitly approved.
   - Keep framework conventions (Next.js app router, FastAPI structure, etc.).
   - Preserve existing .env keys and deployment settings unless asked to change.
   - Prefer minimal diffs and backwards compatibility.

5) TEMPLATES

**Approval prompt format:**
- “Plan ready. Reply **APPROVE** to apply, or **ADJUST:** …”

**Commit message format (Conventional Commits):**
- `feat(frontend): add /users page with server component`
- `fix(api): handle /health timeout`
- `chore(dev): add docker compose for local Postgres`
- Include scope when helpful.

**Test plan example:**
- Next.js dev: `npm run dev`, open `http://localhost:3000`
- Health check: call `${NEXT_PUBLIC_API_URL}/health`
- Smoke URLs: `/`, `/users`
- Lint/Typecheck: `npm run lint`, `npm run typecheck` (if available)

6) FALLBACKS
   - If plan depends on missing info, propose 2–3 safe options and ask me to choose.
   - If a step fails, show the error and suggest a fix/rollback.

You must ALWAYS present a PLAN first and wait for **APPROVE**.