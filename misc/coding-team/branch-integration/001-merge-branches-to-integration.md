# Task 001: Merge ML + Web branches into a single `integration` branch

## Context

The repo has three branches:
- `main` — contains `.claude/agents/` (architect.md, code-reviewer.md, code-reviewerer.md, developer.md) plus stale files to remove
- `ML` — all Python pipeline code (api/, config.py, ModelToConfig.py, data/, notebooks/, scripts/, src/, requirements.txt, eda.ipynb, eda_executed.ipynb)
- `Web` — SvelteKit frontend under a `Web/` prefix folder

Goal: create an `integration` branch off `main` that has ML code under `ML/` and Web code at the repo root (stripped of `Web/` prefix), plus a new `.gitignore` and slimmed `CLAUDE.md`.

## Objective

Produce a single clean commit on branch `integration` (branched from `main`) containing:
1. All ML branch files nested under `ML/`
2. Selected Web branch files at the repo root (prefix stripped)
3. New `.gitignore`
4. Slimmed `CLAUDE.md` from `misc/coding-team/branch-integration/CLAUDE-slim-draft.md`
5. `.claude/agents/` files (already on main)
6. Stale files removed from tracking

## Step-by-step instructions

### 1. Checkout main and create branch

```bash
git checkout main
git checkout -b integration
```

### 2. Remove stale files from git tracking

```bash
git rm -r --cached .ipynb_checkpoints/ 2>/dev/null || true
git rm --cached .DS_Store 2>/dev/null || true
git rm --cached .claude/.DS_Store 2>/dev/null || true
git rm --cached .claude/task_brief_recommendation_integration.md 2>/dev/null || true
git rm --cached .claude/task_brief_score_holdout.md 2>/dev/null || true
git rm --cached .claude/agents/megaArch.md 2>/dev/null || true
git rm --cached README.md 2>/dev/null || true
```

### 3. Write the new `.gitignore`

Create `.gitignore` at repo root with this exact content:

```
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.venv/
venv/

# Jupyter
.ipynb_checkpoints/

# macOS
.DS_Store

# Node
node_modules/
.svelte-kit/

# Data (large / sensitive)
ML/data/dataRaw/
ML/data/processed/*.parquet
ML/data/models/*.pkl

# Firebase
.firebase/
firebase-debug.log

# IDE
.vscode/

# Env
.env
.env.local
.env.production

# Misc / planning
/misc/

# Claude local settings
.claude/settings.local.json
```

### 4. Bring ML branch files under `ML/`

Use `git read-tree` to place ML branch content under the `ML/` prefix:

```bash
git read-tree --prefix=ML/ -u ML
```

This stages all ML files under `ML/`. The ML branch root had files like `config.py`, `api/`, etc. — they'll become `ML/config.py`, `ML/api/`, etc.

**After read-tree, remove unwanted ML files from the index:**
```bash
git rm --cached ML/.DS_Store 2>/dev/null || true
git rm -r --cached ML/.ipynb_checkpoints/ 2>/dev/null || true
git rm --cached ML/.gitignore 2>/dev/null || true
git rm --cached ML/README.md 2>/dev/null || true
```

Also remove any `.DS_Store` files that may have come in recursively:
```bash
git ls-files --cached | grep '\.DS_Store' | xargs -r git rm --cached
```

### 5. Extract Web branch files to repo root

Use `git archive` to extract, then selectively stage:

```bash
# Extract Web branch into a temp area — the Web branch has everything under Web/
git archive Web -- Web/ | tar -x --strip-components=1
```

This puts all `Web/*` files into the working directory at root level (e.g., `Web/src/app.html` becomes `src/app.html`).

Now selectively `git add` ONLY the wanted files:

```bash
git add package.json package-lock.json svelte.config.js vite.config.ts tsconfig.json eslint.config.js .npmrc .prettierrc .prettierignore
git add src/
git add static/
```

Do NOT stage: `dfg`, `src.fileloc`, `implementation_plan.md`, `seed.js`, `update_seed.py`, `unique_categories.txt`, `processed/`, `README.md`, `.vscode/`

Clean up the unwanted extracted files from the working tree:
```bash
rm -f dfg src.fileloc implementation_plan.md seed.js update_seed.py unique_categories.txt README.md 2>/dev/null || true
rm -rf processed/ .vscode/ 2>/dev/null || true
```

### 6. Copy slimmed CLAUDE.md

```bash
cp misc/coding-team/branch-integration/CLAUDE-slim-draft.md CLAUDE.md
git add CLAUDE.md
```

### 7. Stage `.claude/agents/` (already in working tree from main)

```bash
git add .claude/agents/architect.md .claude/agents/code-reviewer.md .claude/agents/code-reviewerer.md .claude/agents/developer.md
```

Do NOT stage `.claude/settings.local.json`.

### 8. Stage `.gitignore`

```bash
git add .gitignore
```

### 9. Final check

Run `git status` and verify:
- No `.DS_Store` files staged
- No `.ipynb_checkpoints/` staged
- No `README.md` staged
- No `node_modules/`, `.svelte-kit/`, `misc/` staged
- No `dfg`, `src.fileloc`, `seed.js`, etc. staged
- `ML/data/dataRaw/` should NOT be staged (check — raw CSVs may not be in git anyway)
- `.claude/settings.local.json` NOT staged

### 10. Commit

```bash
git commit -m "$(cat <<'EOF'
Integrate ML and Web branches into unified project structure

ML pipeline code placed under ML/. SvelteKit frontend files at repo root.
Slimmed CLAUDE.md, clean .gitignore, stale files removed.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

### 11. Verify

```bash
git log --oneline -5
git ls-files | head -80
```

## Non-goals

- Do NOT run `npm install`, `pip install`, or any build commands
- Do NOT push to remote
- Do NOT modify any source code content — this is purely a structural merge

## Constraints / Caveats

- The ML branch has files at its root (no `ML/` prefix on the branch itself). `git read-tree --prefix=ML/` handles this.
- The Web branch has everything inside a `Web/` directory. `git archive` + `tar --strip-components=1` handles this.
- Some ML data files (parquet, pkl) may be large — they should be gitignored going forward but may already be tracked on ML branch. If they come in via `read-tree`, that's fine for now (they're already in git history).
- The `.gitignore` ignores `ML/data/dataRaw/`, `ML/data/processed/*.parquet`, and `ML/data/models/*.pkl` for future commits, but files already in the index stay tracked until explicitly removed. Don't remove model/data files from tracking in this task — they're needed.

## Acceptance criteria

- Branch `integration` exists, branched from main
- `git ls-files` shows `ML/config.py`, `ML/api/main.py`, `ML/requirements.txt`, `src/app.html`, `src/routes/+page.svelte`, `package.json`, `CLAUDE.md`, `.claude/agents/developer.md`, `.gitignore`
- No `.DS_Store`, `.ipynb_checkpoints`, `README.md`, `dfg`, `seed.js`, `src.fileloc`, `.claude/settings.local.json`, `.claude/megaArch.md`, `.claude/task_brief_*.md` in tracked files
- Single clean commit with the specified message
