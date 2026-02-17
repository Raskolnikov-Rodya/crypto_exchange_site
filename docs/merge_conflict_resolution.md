# Merge Conflict Resolution Guide (main -> feature branches)

This project recently moved frontend entry/components from `.js` to `.jsx`.
To reduce rename/delete conflicts during merges, compatibility shims now exist:

- `frontend/src/App.js` -> re-exports from `App.jsx`
- `frontend/src/contexts/AuthContext.js` -> re-exports from `AuthContext.jsx`
- `frontend/src/index.js` -> imports `index.jsx`

## If you still hit conflicts

Run from your conflicted branch:

```bash
# 1) See unresolved files
git status --short

# 2) Prefer canonical backend/docs files from the merged result where appropriate
# (inspect each file before accepting)

# 3) For frontend rename/delete conflicts, keep BOTH .jsx canonical files and .js shims:
#    frontend/src/App.jsx
#    frontend/src/App.js
#    frontend/src/contexts/AuthContext.jsx
#    frontend/src/contexts/AuthContext.js
#    frontend/src/index.jsx
#    frontend/src/index.js

# 4) Ensure no conflict markers remain
rg -n "^<<<<<<<|^=======|^>>>>>>>" backend frontend docs

# 5) Re-run repository checks
scripts/verify_repo_state.sh
scripts/dependency_health_check.sh
cd frontend && npm run build && cd ..

# 6) Finalize merge
git add -A
git commit
```

## Why this works

The `.js` shim files absorb old references and reduce `modify/delete` merge conflicts when one branch edits `.js` and the other branch renamed to `.jsx`.
