# Goal Description

Develop SamFair, a modular Python library and a Next.js (React) dashboard for auditing AI recruitment tools for bias. The system provides a complete end-to-end flow: mock AEDT discovery, synthetic "golden set" data generation, bias auditing using the 4/5ths rule, explainability via a Post‑Prediction Neural Linker (PPNL), and a fully interactive frontend to visualize and remediate bias.

## Open Questions

- **Next.js Router:** The prompt indicates `src/pages/index.js`. Is it acceptable to use the Next.js Pages Router to match this structure, or would you prefer the newer App Router (`src/app/page.js`)? I will default to Pages Router to match the prompt exactly.
- **Styling Details:** The prompt asks for premium, Karpathy-style design. I'll use standard Tailwind CSS with custom colors/gradients, but should I avoid any specific UI libraries (like shadcn/ui or MUI) and stick strictly to raw Tailwind?

## Proposed Changes

### 1. Repository Initialization & Backend Setup
- Initialize standard project structure `samfair/backend/` and `samfair/frontend/`.
- Create `backend/requirements.txt` containing dependencies: `fastapi`, `uvicorn`, `pandas`, `scikit-learn`, `faker`, `playwright`, `joblib`, `reportlab`, `skope-rules` (optional, for succinct rules).

### 2. Python Library (`samfair/backend/samfair_lib/`)
- **[NEW] `synthetic_data.py`**: Generate 1,000 synthetic Indian profiles. Inject protected attributes (gender, religion, caste proxy) and correlated benign features (name styles, universities, pin codes).
- **[NEW] `discovery.py`**: Implement a mock Playwright scraper to "discover" AEDTs from an HR page.
- **[NEW] `audit.py`**: Calculate selection rates and adverse impact ratios (4/5ths rule) for individual attributes and intersectional slices (e.g., Gender x Caste).
- **[NEW] `ppnl.py`**: Train a surrogate `DecisionTreeClassifier` on non-protected features to explain the model's rejections. Extract decision paths as rules and calculate feature importance.
- **[NEW] `evidence.py`**: Setup a simple SQLite or JSON logger that hashes audit runs and PPNL rules (SHA-256) for regulatory traceability.
- **[NEW] `reports.py`**: Generate a PDF summarizing DPIA, audit results, PPNL rules, and synthetic data provenance using `reportlab`.

### 3. Biased Model Creation
- **[NEW] `train_biased_model.py`**: A one-off script to generate a large dataset and train a `LogisticRegression` model with deliberate bias (e.g., rejecting specific pin codes or name styles correlated with SC/ST or Female/Muslim candidates).
- Outputs: `biased_model.joblib`.

### 4. FastAPI Server (`samfair/backend/app.py`)
- **[NEW] `app.py`**: 
  - Expose `/discover` to run Playwright discovery.
  - Expose `/audit` to generate data, run predictions through `biased_model.joblib`, calculate impact ratios, run PPNL, and build the report.
  - Expose `/hr-dashboard` (a tiny mock HTML endpoint for the Playwright scraper to find).

### 5. Frontend Dashboard (`samfair/frontend/`)
- Initialize Next.js project with Tailwind CSS.
- **[NEW] `src/pages/index.js`**: Main layout assembling the 4 panels.
- **[NEW] `src/components/AedtDiscovery.jsx`**: Input URL, scan, and list discovered endpoints.
- **[NEW] `src/components/AuditResultGrid.jsx`**: Render the impact ratio table, an intersectional heatmap, and an overall gauge.
- **[NEW] `src/components/PpnlExplainer.jsx`**: Show the extracted logical rules and feature importance charts.
- **[NEW] `src/components/RemediationSlider.jsx`**: A slider to adjust the model's internal feature weights for the biased features, dynamically recalculating the audit results on the frontend to show remediation.

## Verification Plan

### Automated/Manual Testing
1. **Backend Tests:** Manually trigger `/discover` and `/audit` via Swagger UI (`/docs`) to ensure the entire Python pipeline (Data -> Model -> Audit -> PPNL -> PDF) runs without errors and produces expected results.
2. **Frontend Interactivity:** Start the Next.js dev server. Verify that the discovery scan works, the audit runs and renders the tables/charts, and the remediation slider dynamically changes the impact ratio gauges.
3. **Report Generation:** Ensure the PDF report is created and can be downloaded from the UI.
