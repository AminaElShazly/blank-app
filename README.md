# The Confidence Trap

An interactive policy brief on AI-generated healthcare chart explanations.

Companion digital artefact to the BSc dissertation
*Evaluating LLM-Generated Explanations for Healthcare Data Visualisations*
by Amina ElShazly · University of Sheffield · IJC319 · May 2026.

---

## What this is

A five-page Streamlit web app that translates the dissertation's findings into a
practitioner-facing tool. It includes the full dataset of 45 healthcare charts
used in the study, both AI explanations for each chart, and complete checklist
and error-taxonomy scoring.

The app has five sections, navigable from the sidebar:

- 🏠 **Home** — the headline finding plus live dataset metadata.
- 🔍 **Visualisation Explorer** — browse all 45 charts. For any chart, see the
  source paper's caption (ground truth), GPT-4o and Claude explanations side by
  side, and how each model scored on every checklist item and error category.
- 📈 **Model Evaluation Dashboard** — aggregate accuracy across the dataset,
  filterable by chart type and complexity, with per-chart drill-down.
- 💡 **Findings & Guidance** — the four key findings from the user study and ten
  practical rules for healthcare communicators and AI tool designers.
- ⚠️ **Common Pitfalls** — the nine-item error taxonomy as a field checklist,
  with frequencies pulled live from the dataset.

---

## Running locally

Requires Python 3.9 or higher.

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Repository layout

```
the-confidence-trap/
├── app.py                       Entry point. Routes between five pages.
├── requirements.txt             Python dependencies.
├── README.md                    This file.
├── DEPLOY.md                    Step-by-step deployment guide.
├── .gitignore
│
├── components/                  Reusable UI building blocks.
│   ├── __init__.py
│   ├── styling.py                 All custom CSS — editorial aesthetic.
│   ├── masthead.py                The top bar shown on every page.
│   └── score_grid.py              The reusable scoring display + chart detail view.
│
├── data/                        The 45-chart dataset.
│   ├── __init__.py
│   ├── loader.py                  Cached CSV loader + label dictionaries.
│   └── charts.csv                 Cleaned data, one row per chart, 50 columns.
│
├── pages_content/               One module per section.
│   ├── __init__.py
│   ├── home.py                    🏠 Home
│   ├── explorer.py                🔍 Visualisation Explorer
│   ├── dashboard.py               📈 Model Evaluation Dashboard
│   ├── findings.py                💡 Findings & Guidance
│   └── pitfalls.py                ⚠️ Common Pitfalls
│
└── assets/
    └── charts/                  viz1.jpg ... viz45.jpg, the 45 study charts.
```

---

## The dataset (`data/charts.csv`)

50 columns, one row per chart:

| Field | Description |
|---|---|
| `chart_id` | 1–45 |
| `chart_type` | bar / line / scatter |
| `complexity` | simple / moderate / complex |
| `title` | The chart's caption as given in the source paper |
| `source_caption` | The source paper's prose interpretation (ground truth) |
| `image_filename` | `viz{chart_id}.jpg` |
| `gpt4o_explanation` | The GPT-4o explanation, as generated |
| `claude_explanation` | The Claude Sonnet 4.6 explanation, as generated |
| `gpt4o_c1` … `gpt4o_c10` | Ten checklist scores (0/1) |
| `gpt4o_total` | Sum of checklist scores (0–10) |
| `claude_c1` … `claude_c10` | Same for Claude |
| `claude_total` | |
| `gpt4o_fe1`, `fe2`, `fe3a`, `fe3b`, `fe4`, `fe5`, `hm1`, `hm2`, `oe1` | Nine error flags (0/1) |
| `gpt4o_err_count` | Sum of error flags (0–9) |
| `claude_fe1` … `oe1` | Same for Claude |
| `claude_err_count` | |

The dataset was consolidated from three Excel files (one per chart type) using
the `consolidate.py` script kept in the project's working notes.

---

## Deploying to Streamlit Community Cloud

See `DEPLOY.md` for the step-by-step guide. The short version:

1. Push this folder to a public GitHub repo.
2. Go to <https://share.streamlit.io>, sign in with GitHub.
3. Create a new app, point it at `app.py` on the `main` branch.
4. Deploy — you'll get a public URL like
   `https://confidence-trap-elshazly.streamlit.app`.

The repo is ~5 MB total (most of it is the 45 chart images, optimised to JPEG),
well under Streamlit Cloud's free-tier limits.

---

## Suggested citation

ElShazly, A. (2026). *The Confidence Trap: Guidelines for AI-Generated Healthcare
Chart Explanations.* Companion brief to *Evaluating LLM-Generated Explanations for
Healthcare Data Visualisations.* University of Sheffield, IJC319.
