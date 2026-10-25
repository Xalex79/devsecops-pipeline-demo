# DevSecOps Pipeline Demo

A small FastAPI service used to practise a secure CI/CD pipeline with **GitHub Actions**.
The application is intentionally simple: the interesting part is the pipeline in
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Pipeline

```
push / pull request
        │
        ▼
┌──────────────┐    ┌──────────────────────────┐    ┌─────────────────────────────┐
│ Lint & test  │ ─▶ │ Security scan (Trivy fs) │ ─▶ │ Build, scan & publish image │
│ ruff, pytest │    │ deps · secrets · config  │    │ Trivy image · push to GHCR  │
└──────────────┘    └──────────────────────────┘    └─────────────────────────────┘
```

| Job | What it does |
|---|---|
| **Lint and test** | Runs `ruff` and `pytest`, and uploads the JUnit report as an artifact. |
| **Security scan** | Scans dependencies, hard-coded secrets and misconfigurations (Dockerfile) with Trivy. |
| **Image** | Builds the Docker image, scans it with Trivy and, only on `main`, pushes it to GitHub Container Registry. |

Scan results are uploaded in SARIF format and appear under **Security → Code scanning**.

## Security practices applied

- **Least privilege:** the workflow defaults to `contents: read`, and each job only adds the permissions it needs (`security-events: write`, `packages: write`).
- **Actions pinned to a commit SHA**, not to a movable tag, to protect against supply-chain attacks. The version is kept as a comment.
- **Quality gates:** the pipeline fails on fixable `CRITICAL` or `HIGH` vulnerabilities, while every finding is still reported in the Security tab.
- **No publishing from pull requests:** the image is only pushed from `main`, using the short-lived `GITHUB_TOKEN` (no stored credentials).
- **Non-root container** with a healthcheck.
- **Dependabot** keeps Python packages, GitHub Actions and the Docker base image up to date.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
ruff check . && pytest

uvicorn app.main:app --reload        # http://localhost:8000/docs

docker build -t devsecops-demo .
docker run -p 8000:8000 devsecops-demo
```

## Stack

Python · FastAPI · pytest · ruff · Docker · GitHub Actions · Trivy · GitHub Container Registry · Dependabot
