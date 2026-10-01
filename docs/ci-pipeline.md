# Deployment pipeline

The GitHub Actions workflow is [pipeline.yml](../.github/workflows/pipeline.yml). Pull requests run test and security. Pushes to main also build and publish a container image. The Kind deployment, rolling update, rollback, and service smoke test are deliberately kept in the reproducible local demonstration because the hosted Kind deploy job was unreliable.

| Stage | Check |
| --- | --- |
| Test | flake8, pytest, 85 percent coverage gate |
| Security | Bandit and pip audit |
| Build | Docker image tagged with commit SHA and latest |
| Local deployment demonstration | Kind, rolling rollout, health smoke test via `scripts/rolling-update-demo.ps1` |

The repository diagram is [pipeline.png](diagrams/pipeline.png). The matching CA II reference diagram is [page-6-1.png](diagrams/ca-ii-reference/page-6-1.png). The historical public workflow capture is [github_actions_green_run.png](screenshots/github_actions_green_run.png); it predates the removal of the unreliable hosted deploy job. Local Kubernetes evidence is recorded in [evidence/SUMMARY.md](evidence/SUMMARY.md).
