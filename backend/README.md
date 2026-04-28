# SamFair

**SamFair** is an algorithmic bias audit and explainability library designed to meet the strict regulatory requirements of the upcoming DPDP Act and India AI Bill 2025. 

It provides an end-to-end suite for auditing AI recruitment tools (AEDTs) and extracting readable logic from opaque AI models using our proprietary **Post-Prediction Neural Linker (PPNL)** algorithm.

## 🚀 Features

- **Synthetic Golden Data Generation**: Creates robust, culturally-aware synthetic candidate profiles containing intersectional protected attributes (e.g., Gender, Religion, Caste proxy).
- **Adverse Impact Engine**: Computes the 4/5ths Rule (80% Rule) across intersectional slices to detect hidden bias.
- **Post-Prediction Neural Linker (PPNL)**: Mines surrogate decision tree rules that lead to rejection for flagged groups. Translates opaque predictions into actionable, human-readable logic (`IF feature X THEN reject`).
- **Immutable Evidence Logging**: Every audit and rule extraction is hashed (SHA-256) into a tamper-proof JSONL trail.
- **Automated DPIA Reports**: Generates ready-to-share PDF Data Protection Impact Assessments outlining the found biases and remediation steps.

## 📦 Installation

```bash
pip install samfair
```

## 💻 Quick Start

### 1. Generating Golden Sets
Generate a synthetic dataset of Indian candidate profiles with embedded protected attributes.

```python
from samfair_lib.synthetic_data import generate_golden_set

df = generate_golden_set(n=1000)
print(df.head())
```

### 2. Bias Auditing (4/5ths Rule)
Pass your model's predictions into the audit engine to calculate adverse impact ratios.

```python
from samfair_lib.audit import compute_adverse_impact

# df is your DataFrame containing protected columns
# predictions is a list/array of model outputs (1 for accept, 0 for reject)
protected_cols = ['gender', 'religion', 'caste_indicator']

results = compute_adverse_impact(df, predictions, protected_cols)
flagged_groups = results[results['flagged'] == True]
print(flagged_groups)
```

### 3. Explainability with PPNL
If biases are found, use PPNL to extract the logic leading to rejections for flagged intersectional groups.

```python
from samfair_lib.ppnl import ppnl_explain

ppnl_output = ppnl_explain(df, predictions, flagged_groups)
print(f"Extracted Rule: {ppnl_output['rule']}")
print(f"Feature Contributions: {ppnl_output['feature_contributions']}")
```

### 4. Logging & Reports
Create tamper-proof audit trails and PDF reports.

```python
from samfair_lib.evidence import log_evidence
from samfair_lib.reports import build_report

evidence_hash = log_evidence("AUDIT_RUN", {"flagged_count": len(flagged_groups)})
report_path = build_report(results, ppnl_output, evidence_hash)
```

## 🏗️ Architecture
SamFair operates entirely locally without sending data to third-party APIs. It uses lightweight Scikit-Learn surrogates for high-fidelity rule mining, ensuring you have total control over the audit workflow.

## 📄 License
MIT License.
