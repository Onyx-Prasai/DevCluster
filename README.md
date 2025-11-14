
# DevCluster

DevCluster is a tool for GitHub contribution analysis and visualization. It extracts GitHub user data, computes features, and applies unsupervised learning (KMeans clustering) and scoring to profile contributors — for example, identifying high-output professionals, steady contributors, or inactive accounts.

---

Key features
- Extract raw GitHub user data (JSON) via the GitHub API
- Feature extraction and preprocessing (scaling, imputation)
- Unsupervised learning using KMeans for contributor segmentation
- Scoring and human-friendly interpretation of clusters
---

Quick start

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file or export your GitHub API token. The project reads `GITHUB_API_TOKEN`:

```bash
export GITHUB_API_TOKEN="your_token_here"
```

4. Train the model (this runs the training pipeline and saves the trained model into `models/`):

```bash
python training/trainer.py
```

5. Run the main script:

```bash
python main.py
```
---

Notes
- The `training/trainer.py` script fits an unsupervised KMeans model on available data and writes serialized model artifacts to `models/` (e.g., joblib files). Running the trainer first ensures `main.py` can load a trained model for predictions.
- `main.py` will prompt for a GitHub username and will store raw data under `data/raw/<username>.json`.

Project structure

- `main.py` — CLI entrypoint that runs the pipeline
- `data/` — contains raw and processed data (examples included in the repo)
- `data_collection/` — fetches GitHub data (API extractor)
- `feature_engineering/` — feature extraction utilities
- `training/` — clustering, scoring, and model utilities (run `training/trainer.py` to train/save model)
- `models/` — pre-trained or newly trained joblib model artifacts
- `utils/` — logging, save/load helpers, and custom exceptions
- `tests/` — contains test scripts
- `notebooks/` — contains notebooks for data visualization and feature extraction.

---

Configuration

- The project uses environment variables (see `.env` usage in code). At minimum set `GITHUB_API_TOKEN` for API access.

---

License

This project is licensed under the MIT License — see the `LICENSE` file for details.

---

Sample Output
- [Here it is](https://github.com/KhagendraN/DevCluster/tree/main/assets)