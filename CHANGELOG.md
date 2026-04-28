# Changelog

All notable changes to the SamFair project will be documented in this file.

## [v2.1.0] - 2026-04-28

### Added
- **Vercel Deployment Integration**: Fully implemented `vercel.json` configuring standard `@vercel/next` and `@vercel/python` builder logic. 
- **API Rewrites**: Configured Next.js proxying in `next.config.ts` to seamlessly route `/api/(.*)` to the local FastAPI backend during development while perfectly mapping to serverless functions in production.
- **Firebase Auth Context**: Implemented a comprehensive React Context (`AuthContext.tsx`) wrapping Firebase OAuth sign-in flows.
- **Evaluation Backdoor**: Created a dedicated backdoor for compliance auditors to bypass OAuth and log into the dashboard via a mock identity.
- **DPIA Storage**: Synchronized audit runs to automatically log immutable records into Google Cloud Firestore.
- **Chart.js Visualizations**: Integrated interactive horizontal and vertical bar charts for 4/5ths Rule selection metrics and Post-Prediction Neural Linker feature contributions.

### Changed
- **Stateless Architecture**: Removed global `session_data` dependencies from the FastAPI application. All components now operate deterministically based on seed injections, enabling high-concurrency serverless execution.
- **Strict Typing**: Removed all usage of `any` types across the React UI; strictly enforced types using TS interfaces (`src/types/index.ts`).
- **Pydantic Hardening**: All FastApi endpoints strictly validate inputs using structured Pydantic BaseModel schemas.
- **API Route Convention**: Relocated all FastAPI backend routes to an `APIRouter` with an `/api` prefix, replacing raw `http://localhost:8000/` calls with relative `/api/...` fetch statements.

### Removed
- **Hardcoded Endpoints**: Stripped all local-first hostnames from components.
- **Deprecated Fonts**: Removed legacy Geist `.woff` font files from the layout to resolve Turbopack compilation errors.

### Fixed
- Fixed Playwright UnicodeEncode errors on Windows by wrapping exception printing safely.
- Fixed `setup.py` UnicodeDecode errors by explicitly supplying `encoding="utf-8"` during PyPI generation.
