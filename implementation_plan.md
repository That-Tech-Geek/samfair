# Goal Description

Update the SamFair prototype to match the highly detailed architecture specification, integrating Firebase/Firestore for user data storage, adding Chart.js visualizations, refining the bias auditing algorithm, and providing a cohesive `run.sh` script for the demo flow.

## Open Questions

- **Next.js Router**: Our current scaffolding uses the Next.js App Router (`src/app/page.tsx`). Your spec mentions `pages/index.js`. I will adapt the components to work perfectly within the existing App Router setup unless you strictly prefer rebuilding it with the Pages Router.
- **Firebase Auth**: Should I implement a mock/simple anonymous Firebase login before saving to Firestore, or just write directly to the database without auth rules for the hackathon prototype? (I will assume direct writes to Firestore are fine for the prototype).

## Proposed Changes

### 1. Backend Updates (`samfair/backend/`)
- **[MODIFY] `requirements.txt`**: Pin exact versions as requested (`fastapi==0.110.0`, `pandas==2.2.0`, etc.) and add `python-multipart`.
- **[NEW] `mock_hr.html`**: Create the dummy HR page with `data-aedt` attributes.
- **[NEW] `train_model.py`**: A revised training script that creates 10,000 samples and specifically injects intersectional bias against SC women and penalizes specific pin codes, saving to `biased_model.joblib`.
- **[MODIFY] `samfair_lib/synthetic_data.py`**: Update to generate `university_tier`, `language_medium`, `pin_code` (biased), and encode `name_feat1`/`name_feat2`.
- **[MODIFY] `samfair_lib/discovery.py`**: Update to read `data-name` and `data-endpoint`.
- **[MODIFY] `samfair_lib/audit.py`**: Ensure it strictly flags ratios < 0.80 and calculates the intersectional slices specified.
- **[MODIFY] `samfair_lib/ppnl.py`**: Ensure it outputs the exact dict format: `rule`, `group_impacted`, `surrogate_accuracy`, `feature_contributions`.
- **[MODIFY] `samfair_lib/evidence.py`**: Update `log_audit` to hash and save to `audit_log.json`.
- **[MODIFY] `samfair_lib/reports.py`**: Update `generate_report` to save to `/tmp/audit_report.pdf` (or local temp dir on Windows).
- **[MODIFY] `app.py`**: 
  - Add `POST /remediate` to recalculate metrics based on slider weights.
  - Add `GET /download_report` to fetch the generated PDF.
  - Add `GET /mock_hr.html` to serve the mock file.

### 2. Frontend Updates (`samfair/frontend/`)
- **Dependencies**: Install `firebase`, `chart.js`, `react-chartjs-2`.
- **[NEW] `src/lib/firebase.js`**: Initialize Firebase and Firestore. The API keys will be read from `.env.local` to remain BYOK (Bring Your Own Key), falling back to the provided keys if not set.
- **[MODIFY] `src/app/page.tsx`**: Update state management for the new flow and integrate Firestore to log audit sessions.
- **[MODIFY] `src/components/AedtDiscovery.tsx`**: Update UI to match the new endpoints.
- **[MODIFY] `src/components/AuditResultGrid.tsx`**: Add Chart.js bar chart for impact ratios.
- **[MODIFY] `src/components/PpnlExplainer.tsx`**: Add Chart.js horizontal bar chart for feature contributions.
- **[MODIFY] `src/components/RemediationSlider.tsx`**: Add visual gauge and call `POST /remediate`.

### 3. Execution Script
- **[NEW] `run.sh`**: Create the bash script to install dependencies, run `train_model.py`, start Uvicorn, and start Next.js dev server.

## Verification Plan

### Automated/Manual Testing
1. Execute `run.sh` (via bash on Windows/WSL) and verify both backend and frontend start cleanly.
2. Follow the 9-step demo flow exactly:
   - Scan `http://localhost:8000/mock_hr.html`.
   - Run audit on AI Resume Screener.
   - Verify SC Women are flagged RED.
   - Click to view PPNL and verify Chart.js visualizations.
   - Adjust the Remediation Slider and verify the gauge turns green.
   - Download the PDF report.
   - Check Firestore console to ensure the audit log was saved successfully.
