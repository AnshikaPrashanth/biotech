# Cross-Validation Data Leakage Audit Report

To guarantee the scientific defensibility of our results, a rigorous data leakage audit has been performed on the dataset splits generated for cross-validation.

## 1. Split Isolation Audit Results

The Leave-One-Subject-Out (LOSO) cross-validation splits were audited for subject ID overlap between the training and validation sets:

| Fold Index | Left-Out Validation Subject | Train Subject Count | Validation Subject Count | Intersection Overlap | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | 101 | 29 | 1 | None | **NO (PASS)** |
| 2 | 102 | 29 | 1 | None | **NO (PASS)** |
| 3 | 103 | 29 | 1 | None | **NO (PASS)** |
| 4 | 104 | 29 | 1 | None | **NO (PASS)** |
| 5 | 105 | 29 | 1 | None | **NO (PASS)** |
| 6 | 106 | 29 | 1 | None | **NO (PASS)** |
| 7 | 107 | 29 | 1 | None | **NO (PASS)** |
| 8 | 201 | 29 | 1 | None | **NO (PASS)** |
| 9 | 202 | 29 | 1 | None | **NO (PASS)** |
| 10 | 203 | 29 | 1 | None | **NO (PASS)** |
| 11 | 204 | 29 | 1 | None | **NO (PASS)** |
| 12 | 205 | 29 | 1 | None | **NO (PASS)** |
| 13 | 206 | 29 | 1 | None | **NO (PASS)** |
| 14 | 207 | 29 | 1 | None | **NO (PASS)** |
| 15 | 209 | 29 | 1 | None | **NO (PASS)** |
| 16 | 210 | 29 | 1 | None | **NO (PASS)** |
| 17 | 211 | 29 | 1 | None | **NO (PASS)** |
| 18 | 212 | 29 | 1 | None | **NO (PASS)** |
| 19 | 213 | 29 | 1 | None | **NO (PASS)** |
| 20 | 214 | 29 | 1 | None | **NO (PASS)** |
| 21 | 215 | 29 | 1 | None | **NO (PASS)** |
| 22 | 216 | 29 | 1 | None | **NO (PASS)** |
| 23 | 217 | 29 | 1 | None | **NO (PASS)** |
| 24 | 301 | 29 | 1 | None | **NO (PASS)** |
| 25 | 302 | 29 | 1 | None | **NO (PASS)** |
| 26 | 303 | 29 | 1 | None | **NO (PASS)** |
| 27 | 304 | 29 | 1 | None | **NO (PASS)** |
| 28 | 305 | 29 | 1 | None | **NO (PASS)** |
| 29 | 306 | 29 | 1 | None | **NO (PASS)** |
| 30 | 307 | 29 | 1 | None | **NO (PASS)** |

## 2. Key Audit Findings

- **Subject Disjointness:** Every fold maintains 100% disjoint subject sets between training and validation. There are zero instances of overlap, ensuring no subject leakage.
- **Temporal Leakage Protection:** Skeletons are grouped entirely by Subject ID. Sequences of the same subject are never split across train and validation sets, ensuring that model predictions generalized to entirely unseen subjects.
- **Generalization Integrity:** The LOSO protocol ensures that performance metrics reflect the model's actual ability to assess movements on new subjects without prior exposure to their physiological or stylistic variations.
