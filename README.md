# 💊 PKPD-SiAn-Tools (v2.0.1)

PKPD SiAn Tools is a Streamlit application that helps students and researchers simulate and analyze pharmacokinetic/pharmacodynamic (PK/PD) scenarios. The current 2.0.1 release reorganizes the app into Individual (flexible dosing) and Population simulations, all powered by the shared `pkpd_sian` Python package.

📘 **Mechanism overview:** https://pkpdsian.serve.scilifelab.se/Helps

## Repository Layout
- `app.py` – Streamlit landing page, global layout, and update history.
- `pages/` – Feature-specific Streamlit pages rendered in sidebar order.
- `pkpd_sian/` – Reusable simulation, preprocessing, analysis, and visualization modules.
- `testdata/` – Demo datasets and regression fixtures.
- `.streamlit/` – Deployment-ready Streamlit configuration.
- `tests/` – Pytest suite (currently focused on package metadata, extend as you add logic).
- `Dockerfile`, `.dockerignore` – Production container definition.

## Environment Setup
```bash
git clone <repo>
cd PKPD-Simulation-Tools
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # installs app + quality tooling
```

## Development Workflow
- `streamlit run app.py` – Launch the UI locally.
- `black app.py pages pkpd_sian && isort app.py pages pkpd_sian` – Enforce formatting.
- `flake8 app.py pages pkpd_sian` – Static linting.
- `pytest` – Execute the growing test suite; name tests after the scenario being validated.
- `bandit -qr pkpd_sian` – Quick security sweep before shipping.
- `rm -rf .venv .pytest_cache .mypy_cache **/__pycache__` – Clean local artifacts when needed.

## Testing & Quality
Automated coverage is intentionally growing. Mirror the `pkpd_sian` module layout inside `tests/`, describe scenarios in the test name (e.g., `test_multiple_compartment_iv_profile`), and use datasets from `testdata/` for reproducible assertions. Run `pytest --maxfail=1 --disable-warnings` locally and ensure Streamlit flows still render before opening a PR.

## Container Deployment
```bash
docker build -t pkpd-sian-tools .
docker run --rm -p 8501:8501 pkpd-sian-tools    # exposes http://localhost:8501
```
The Docker image uses Python 3.13, runs as a non-root user, and bakes in a health check via Streamlit’s `_stcore/health` endpoint.

## Configuration
- `.streamlit/config.toml` enforces headless, dark-theme deployments and raises the upload ceiling to 1 GB.
- Environment variables `DATA_DIR` and `IMG_DIR` (exported in the container) point to `testdata/` and `images/`. Extend `app.py` to read additional secrets via Streamlit’s secret manager instead of hardcoding them.

The ongoing 2.1.0 roadmap will incorporate Physiologically Based Pharmacokinetic (PBPK) models. Please review `AGENTS.md` for contributor expectations before submitting changes.
