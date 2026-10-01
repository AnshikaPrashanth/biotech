# OOF Pipeline Validation

This is a pipeline-integrity smoke test, not a performance experiment.

## Dataset
- Manifest: `results/final/dataset_manifest.csv`
- Valid dataset size: 2577 samples; predictions in this run: 217.
- Subject count: 30.
- Data loaded only from valid manifest rows; label 3 is excluded.

## Evaluation Path
- Training source: valid manifest samples from all subjects except the outer held-out subject and one internal-validation subject; smoke mode uses the recorded deterministic subset from each training subject.
- Training implementation: `train.run_fold()` and `train.train_one_epoch()`; validation/checkpoint selection uses `train.evaluate()` on the internal-validation subject only.
- Inner-validation policy: choose the first subject in sorted subject-ID order after excluding the outer test subject; train on the remaining 28 development subjects. This deterministic rule uses no outer-test performance.
- Validation source: all valid manifest samples for the selected internal-validation subject; checkpoint selection minimizes validation error rate (1 - accuracy), with the configured early-stopping delta applied to that same value.
- Checkpoint source: best internal-validation state saved with exact training sample IDs and subject provenance, then reloaded before test inference.
- Outer test source: valid manifest samples belonging only to the held-out subject.
- Prediction output: `results/final/smoke_OOF_PREDICTIONS.csv`; metric aggregation: `evaluate_oof_predictions()` reads this CSV and loads no model checkpoint.

## Fold Boundaries and Provenance
### fold_101
- Held-out subject: `101`
- Training subjects: `103, 104, 105, 106, 107, 201, 202, 203, 204, 205, 206, 207, 209, 210, 211, 212, 213, 214, 215, 216, 217, 301, 302, 303, 304, 305, 306, 307`
- Validation subjects: `102`
- Test subject: `101`; test predictions: 107.
- Training examples used: 47 (smoke subset, represented by every training subject).
- Checkpoint: `results/final/smoke_checkpoints/fold_101.pt`; see `results/final/smoke_checkpoint_provenance.csv`.
- Checkpoint epoch, validation accuracy, and its error-rate selection value are recorded in checkpoint metadata and provenance CSV.
- Training time: 5.93 seconds; total fold runtime: 15.03 seconds.
- Approximate RSS before fold cleanup: 864.734375 MB; after releasing model/loaders: 864.7421875 MB.
- Split assertions: held-out subject excluded from training and validation; training/test and validation/test intersections are empty.

### fold_102
- Held-out subject: `102`
- Training subjects: `103, 104, 105, 106, 107, 201, 202, 203, 204, 205, 206, 207, 209, 210, 211, 212, 213, 214, 215, 216, 217, 301, 302, 303, 304, 305, 306, 307`
- Validation subjects: `101`
- Test subject: `102`; test predictions: 110.
- Training examples used: 47 (smoke subset, represented by every training subject).
- Checkpoint: `results/final/smoke_checkpoints/fold_102.pt`; see `results/final/smoke_checkpoint_provenance.csv`.
- Checkpoint epoch, validation accuracy, and its error-rate selection value are recorded in checkpoint metadata and provenance CSV.
- Training time: 5.56 seconds; total fold runtime: 9.28 seconds.
- Approximate RSS before fold cleanup: 840.8359375 MB; after releasing model/loaders: 840.8359375 MB.
- Split assertions: held-out subject excluded from training and validation; training/test and validation/test intersections are empty.

## OOF Integrity
- Every prediction belongs to its fold's held-out subject and expected valid manifest sample set.
- No training-subject predictions, duplicate sample IDs, invalid/missing manifest samples, or label-3 rows.
- Every prediction has exactly one fold; per-fold prediction counts equal held-out valid manifest counts.
- Integrity assertions: PASS (217 predictions).

## Calibration and DTW Provenance
- The classifier OOF runner does not instantiate a calibrator or call calibration/DTW functions.
- Calibration reference source: none; calibration sample IDs: none; training/test sample IDs used for calibration: none.
- Separate legacy `evaluate_and_report.py` Part 7 fits ROM calibration from each subject's healthy sequences and evaluates that subject's compensated sequences. That is not an outer-subject OOF calibration protocol and is not invoked here.

## EMA / Baseline Adaptation
- No EMA or baseline adaptation is used by the classifier OOF prediction path.
- The clinical `src/analysis_pipeline.py` has optional persisted ROM baseline drift: it updates after scoring a sequence under confidence/quality conditions, so prior sequences may influence later ROM-derived assessment. It does not update ST-GAT weights or its class prediction; it uses no ground-truth labels or future sequences. This is online downstream adaptation, outside this OOF experiment.

## Baseline Split Compatibility
- The legacy Part 8 baseline implementation groups by the same sorted subject IDs and uses `subject_ids != held_out_subject` for fitting and equality for that fold's held-out predictions; scaler/PCA fit only on its training rows.
- Baselines were inspected but not run. Their current implementation aggregates per-fold arrays rather than writing the required OOF prediction schema; baseline OOF persistence remains follow-up work before baseline comparisons.

## Padding and Masking
- Train, internal validation, and held-out test loaders use 64-frame zero padding via `sequence_collate_fn` and its boolean `mask`.
- The mask is passed to `STGAT.forward`, temporal attention, and masked temporal pooling; padded temporal-attention outputs were checked as zero.
- Mask verification: PASS.

## Runtime and Memory
- Model parameters: 53,090.
- CPU only; sequential folds; `num_workers=0`; model/optimizer/loaders are released and garbage-collected after each fold.
- Per-fold runtime and approximate RSS are listed above.

## OOF Metrics Reproduction
- Metrics calculated from the OOF CSV only; metric file deleted and recomputed identically: PASS.
- Smoke metrics (not final performance): `{"accuracy": 0.48847926267281105, "balanced_accuracy": 0.411993769470405, "confusion_matrix": [[105, 109], [2, 1]], "macro_f1": 0.33595236126044165, "mcc": -0.04110765452815519, "n_predictions": 217, "pr_auc": 0.05626357474228495, "precision_macro": 0.49519966015293115, "recall_macro": 0.411993769470405, "roc_auc": 0.4034267912772585}`.

## Issues and Scope
- OOF training uses a deterministic smoke subset (one sample per available class per training subject); full mode uses every valid training sample.
- Legacy `train.py` uses its sole held-out subject as both validation data and the basis for checkpoint selection, so it has no independent outer test set; it is not used as the OOF split constructor.
- Legacy full-dataset inference in `evaluate_and_report.py` is explicitly gated as `legacy_full_dataset_evaluation`; it is not the OOF entry point.
- No full 30-fold experiment was run. Smoke metrics are not paper-ready performance estimates.
