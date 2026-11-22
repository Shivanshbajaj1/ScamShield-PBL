# Apply this update to the existing GitHub repository

This ZIP is an **update bundle**, not a replacement for the whole repository. It contains the refreshed root README/contribution map plus the complete Phase 2, Phase 3 and shared research/dataset content. It intentionally does not contain `phase 1/`; keep the Phase 1 files already in your repository.

1. Clone `https://github.com/Shivanshbajaj1/ScamShield-PBL.git` with GitHub Desktop.
2. Extract this ZIP into the cloned repository's root folder, allowing files/folders with the same names to be replaced. Do not extract it into an extra nested folder.
3. Confirm the repository root contains `README.md`, `phase 1/`, `phase 2/`, `phase 3/`, `research_and_datasets/` and `team member contributions/`.
4. In GitHub Desktop, review the changed-file list. It should include the new phase sources/docs and updates to README/contribution files.
5. Commit with message `Complete Phase 2 and Phase 3 project sources`, then click **Push origin**.

Equivalent PowerShell commands from the cloned repository root:

```powershell
git status
git add .
git commit -m "Complete Phase 2 and Phase 3 project sources"
git push origin main
```

The URL dataset CSV is about 56.9 MB, below GitHub's 100 MB per-file limit but above its 50 MB warning threshold. Keep it in the commit only if you are comfortable with the larger clone; Git LFS is an alternative if configured by the team.
