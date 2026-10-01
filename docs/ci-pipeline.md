# Deployment pipeline

The GitHub Actions workflow is [pipeline.yml](../.github/workflows/pipeline.yml). Pull requests run test and security. Pushes to main also build a container image, create a Kind cluster, deploy the manifests, and run a health smoke test.

| Stage | Check |
| --- | --- |
| Test | flake8, pytest, 85 percent coverage gate |
| Security | Bandit and pip audit |
| Build | Docker image tagged with commit SHA and latest |
| Deploy | Kind, rolling rollout, health smoke test |

The pipeline diagram is [pipeline.png](diagrams/pipeline.png). The real public workflow capture is [github_actions_green_run.png](screenshots/github_actions_green_run.png). The current public deployment result and all repair attempts are recorded in [evidence/SUMMARY.md](evidence/SUMMARY.md).
