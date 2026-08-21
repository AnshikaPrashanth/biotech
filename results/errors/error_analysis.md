# Failure Analysis

Generated: 2026-08-10T09:42:17.282207+00:00

**Total failures: 376 / 2589**

---

## False Positives (275 samples)

### `101_18_0_6_1_chair.txt`
- **Subject:** 101 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5309`
- **Prob (Healthy/Comp):** `[0.4691, 0.5309]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.756), WristRight(0.749)
- **Peak Frame:** 37 (value 0.2039)
- **Attention Entropy:** 3.2072
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `101_18_4_12_1_chair.txt`
- **Subject:** 101 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6673`
- **Prob (Healthy/Comp):** `[0.3327, 0.6673]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.773), WristRight(0.752)
- **Peak Frame:** 62 (value 0.0297)
- **Attention Entropy:** 3.2045
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_7_3_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5284`
- **Prob (Healthy/Comp):** `[0.4716, 0.5284]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.786), WristRight(0.759)
- **Peak Frame:** 60 (value 0.0359)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_7_4_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8276`
- **Prob (Healthy/Comp):** `[0.1724, 0.8276]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.787), WristLeft(0.763)
- **Peak Frame:** 62 (value 0.0688)
- **Attention Entropy:** 3.2037
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_7_5_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8307`
- **Prob (Healthy/Comp):** `[0.1693, 0.8307]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.787), WristLeft(0.763)
- **Peak Frame:** 62 (value 0.0868)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_7_6_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8096`
- **Prob (Healthy/Comp):** `[0.1904, 0.8096]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.781), WristLeft(0.761)
- **Peak Frame:** 2 (value 0.0221)
- **Attention Entropy:** 3.2044
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_8_1_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6554`
- **Prob (Healthy/Comp):** `[0.3446, 0.6554]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.780), WristLeft(0.759)
- **Peak Frame:** 41 (value 0.0205)
- **Attention Entropy:** 3.2050
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_8_2_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5821`
- **Prob (Healthy/Comp):** `[0.4179, 0.5821]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.790), WristLeft(0.762)
- **Peak Frame:** 62 (value 0.1235)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_8_3_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5185`
- **Prob (Healthy/Comp):** `[0.4815, 0.5185]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.788), WristLeft(0.761)
- **Peak Frame:** 62 (value 0.1195)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_8_4_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5187`
- **Prob (Healthy/Comp):** `[0.4813, 0.5187]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.788), WristLeft(0.759)
- **Peak Frame:** 62 (value 0.0921)
- **Attention Entropy:** 3.2042
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_8_5_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8211`
- **Prob (Healthy/Comp):** `[0.1789, 0.8211]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.792), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0529)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `102_18_8_6_1_stand.txt`
- **Subject:** 102 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5068`
- **Prob (Healthy/Comp):** `[0.4932, 0.5068]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.782), WristLeft(0.757)
- **Peak Frame:** 20 (value 0.0216)
- **Attention Entropy:** 3.2048
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `103_18_8_10_1_chair.txt`
- **Subject:** 103 | **Exercise:** 2 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7671`
- **Prob (Healthy/Comp):** `[0.2329, 0.7671]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.784), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0399)
- **Attention Entropy:** 3.2011
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `103_18_8_11_1_chair.txt`
- **Subject:** 103 | **Exercise:** 2 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7766`
- **Prob (Healthy/Comp):** `[0.2234, 0.7766]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.783), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0357)
- **Attention Entropy:** 3.2013
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `103_18_8_12_1_chair.txt`
- **Subject:** 103 | **Exercise:** 2 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5410`
- **Prob (Healthy/Comp):** `[0.4590, 0.5410]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.782), WristRight(0.761)
- **Peak Frame:** 62 (value 0.0490)
- **Attention Entropy:** 3.2015
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `103_18_8_7_1_chair.txt`
- **Subject:** 103 | **Exercise:** 2 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5114`
- **Prob (Healthy/Comp):** `[0.4886, 0.5114]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.781), WristRight(0.761)
- **Peak Frame:** 62 (value 0.0490)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `103_18_8_8_1_chair.txt`
- **Subject:** 103 | **Exercise:** 2 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5595`
- **Prob (Healthy/Comp):** `[0.4405, 0.5595]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.782), WristRight(0.761)
- **Peak Frame:** 62 (value 0.0386)
- **Attention Entropy:** 3.2017
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `103_18_8_9_1_chair.txt`
- **Subject:** 103 | **Exercise:** 2 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7755`
- **Prob (Healthy/Comp):** `[0.2245, 0.7755]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.784), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0380)
- **Attention Entropy:** 3.2011
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `104_18_7_1_1_stand.txt`
- **Subject:** 104 | **Exercise:** 2 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5031`
- **Prob (Healthy/Comp):** `[0.4969, 0.5031]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.782), WristLeft(0.755)
- **Peak Frame:** 62 (value 0.0483)
- **Attention Entropy:** 3.2038
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `107_18_8_1_1_stand.txt`
- **Subject:** 107 | **Exercise:** 2 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9365`
- **Prob (Healthy/Comp):** `[0.0635, 0.9365]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.786), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0381)
- **Attention Entropy:** 3.2045
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_0_5_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9466`
- **Prob (Healthy/Comp):** `[0.0534, 0.9466]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.761), WristRight(0.752)
- **Peak Frame:** 16 (value 0.0270)
- **Attention Entropy:** 3.2061
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_0_6_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9409`
- **Prob (Healthy/Comp):** `[0.0591, 0.9409]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.763), WristRight(0.752)
- **Peak Frame:** 49 (value 0.0232)
- **Attention Entropy:** 3.2057
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_1_11_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9126`
- **Prob (Healthy/Comp):** `[0.0874, 0.9126]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.762), WristRight(0.755)
- **Peak Frame:** 52 (value 0.0264)
- **Attention Entropy:** 3.2055
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_1_12_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9090`
- **Prob (Healthy/Comp):** `[0.0910, 0.9090]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.759), WristRight(0.753)
- **Peak Frame:** 23 (value 0.0265)
- **Attention Entropy:** 3.2062
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_1_13_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9304`
- **Prob (Healthy/Comp):** `[0.0696, 0.9304]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.763), WristRight(0.755)
- **Peak Frame:** 59 (value 0.0321)
- **Attention Entropy:** 3.2051
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_1_14_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8969`
- **Prob (Healthy/Comp):** `[0.1031, 0.8969]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.758), WristRight(0.753)
- **Peak Frame:** 31 (value 0.0317)
- **Attention Entropy:** 3.2063
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_1_15_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9406`
- **Prob (Healthy/Comp):** `[0.0594, 0.9406]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.760), WristRight(0.755)
- **Peak Frame:** 19 (value 0.0231)
- **Attention Entropy:** 3.2060
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_1_16_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9224`
- **Prob (Healthy/Comp):** `[0.0776, 0.9224]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.761), WristRight(0.755)
- **Peak Frame:** 45 (value 0.0240)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_2_35_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9351`
- **Prob (Healthy/Comp):** `[0.0649, 0.9351]`
- **Top-3 Attention Joints:** SpineShoulder(0.801), SpineBase(0.760), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0314)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_2_36_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9546`
- **Prob (Healthy/Comp):** `[0.0454, 0.9546]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.761), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0320)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_2_37_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9365`
- **Prob (Healthy/Comp):** `[0.0635, 0.9365]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.761), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0325)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_2_38_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9646`
- **Prob (Healthy/Comp):** `[0.0354, 0.9646]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.762), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0397)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `201_18_3_11_1_wheelchair.txt`
- **Subject:** 201 | **Exercise:** 5 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9754`
- **Prob (Healthy/Comp):** `[0.0246, 0.9754]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.768), WristLeft(0.751)
- **Peak Frame:** 57 (value 0.0209)
- **Attention Entropy:** 3.2045
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_2_1_3_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9103`
- **Prob (Healthy/Comp):** `[0.0897, 0.9103]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.788), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0223)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_3_2_3_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9395`
- **Prob (Healthy/Comp):** `[0.0605, 0.9395]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.786), WristRight(0.758)
- **Peak Frame:** 0 (value 0.0218)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_4_1_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6355`
- **Prob (Healthy/Comp):** `[0.3645, 0.6355]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.785), WristRight(0.754)
- **Peak Frame:** 63 (value 0.0268)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_4_24_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6449`
- **Prob (Healthy/Comp):** `[0.3551, 0.6449]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.784), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0475)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_4_30_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8618`
- **Prob (Healthy/Comp):** `[0.1382, 0.8618]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.778), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0586)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_4_33_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6351`
- **Prob (Healthy/Comp):** `[0.3649, 0.6351]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.776), WristRight(0.756)
- **Peak Frame:** 62 (value 0.0353)
- **Attention Entropy:** 3.2060
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_4_35_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8004`
- **Prob (Healthy/Comp):** `[0.1996, 0.8004]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.776), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0530)
- **Attention Entropy:** 3.2062
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_4_36_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8385`
- **Prob (Healthy/Comp):** `[0.1615, 0.8385]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.777), WristRight(0.756)
- **Peak Frame:** 0 (value 0.0573)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_4_37_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6559`
- **Prob (Healthy/Comp):** `[0.3441, 0.6559]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.777), WristRight(0.759)
- **Peak Frame:** 61 (value 0.0241)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_7_5_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5108`
- **Prob (Healthy/Comp):** `[0.4892, 0.5108]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.790), WristLeft(0.757)
- **Peak Frame:** 0 (value 0.0496)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_12_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7727`
- **Prob (Healthy/Comp):** `[0.2273, 0.7727]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.797), WristRight(0.766)
- **Peak Frame:** 0 (value 0.0426)
- **Attention Entropy:** 3.2045
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_13_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5954`
- **Prob (Healthy/Comp):** `[0.4046, 0.5954]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.796), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0477)
- **Attention Entropy:** 3.2038
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_14_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5223`
- **Prob (Healthy/Comp):** `[0.4777, 0.5223]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.764)
- **Peak Frame:** 0 (value 0.0454)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_16_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5915`
- **Prob (Healthy/Comp):** `[0.4085, 0.5915]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.794), WristRight(0.764)
- **Peak Frame:** 0 (value 0.0408)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_18_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5139`
- **Prob (Healthy/Comp):** `[0.4861, 0.5139]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.800), WristRight(0.763)
- **Peak Frame:** 0 (value 0.0492)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_19_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5302`
- **Prob (Healthy/Comp):** `[0.4698, 0.5302]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.796), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0395)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_1_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5954`
- **Prob (Healthy/Comp):** `[0.4046, 0.5954]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0461)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_20_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5185`
- **Prob (Healthy/Comp):** `[0.4815, 0.5185]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.796), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0408)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_21_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5285`
- **Prob (Healthy/Comp):** `[0.4715, 0.5285]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.796), WristRight(0.760)
- **Peak Frame:** 0 (value 0.0426)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_25_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5353`
- **Prob (Healthy/Comp):** `[0.4647, 0.5353]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.764)
- **Peak Frame:** 0 (value 0.0507)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_26_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6162`
- **Prob (Healthy/Comp):** `[0.3838, 0.6162]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.791), WristRight(0.765)
- **Peak Frame:** 0 (value 0.0469)
- **Attention Entropy:** 3.2038
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_2_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5505`
- **Prob (Healthy/Comp):** `[0.4495, 0.5505]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.795), WristRight(0.763)
- **Peak Frame:** 0 (value 0.0507)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_30_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5113`
- **Prob (Healthy/Comp):** `[0.4887, 0.5113]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.796), WristRight(0.761)
- **Peak Frame:** 0 (value 0.0410)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_32_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5202`
- **Prob (Healthy/Comp):** `[0.4798, 0.5202]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.800), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0465)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_33_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5475`
- **Prob (Healthy/Comp):** `[0.4525, 0.5475]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.801), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0462)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_34_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5394`
- **Prob (Healthy/Comp):** `[0.4606, 0.5394]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.800), WristRight(0.765)
- **Peak Frame:** 0 (value 0.0556)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_35_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5247`
- **Prob (Healthy/Comp):** `[0.4753, 0.5247]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.800), WristRight(0.767)
- **Peak Frame:** 0 (value 0.0422)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_36_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5188`
- **Prob (Healthy/Comp):** `[0.4812, 0.5188]`
- **Top-3 Attention Joints:** SpineShoulder(0.811), SpineBase(0.801), WristRight(0.765)
- **Peak Frame:** 0 (value 0.0514)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_37_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5901`
- **Prob (Healthy/Comp):** `[0.4099, 0.5901]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.802), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0511)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_38_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5320`
- **Prob (Healthy/Comp):** `[0.4680, 0.5320]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.801), WristRight(0.766)
- **Peak Frame:** 0 (value 0.0482)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_39_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5705`
- **Prob (Healthy/Comp):** `[0.4295, 0.5705]`
- **Top-3 Attention Joints:** SpineShoulder(0.811), SpineBase(0.802), WristRight(0.761)
- **Peak Frame:** 0 (value 0.0489)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_40_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5852`
- **Prob (Healthy/Comp):** `[0.4148, 0.5852]`
- **Top-3 Attention Joints:** SpineShoulder(0.811), SpineBase(0.803), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0513)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_41_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5910`
- **Prob (Healthy/Comp):** `[0.4090, 0.5910]`
- **Top-3 Attention Joints:** SpineShoulder(0.811), SpineBase(0.802), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0519)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_42_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5653`
- **Prob (Healthy/Comp):** `[0.4347, 0.5653]`
- **Top-3 Attention Joints:** SpineShoulder(0.811), SpineBase(0.801), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0557)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_43_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5472`
- **Prob (Healthy/Comp):** `[0.4528, 0.5472]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.802), WristRight(0.765)
- **Peak Frame:** 0 (value 0.0502)
- **Attention Entropy:** 3.2028
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_44_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5293`
- **Prob (Healthy/Comp):** `[0.4707, 0.5293]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.802), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0401)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_45_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5815`
- **Prob (Healthy/Comp):** `[0.4185, 0.5815]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.802), WristRight(0.761)
- **Peak Frame:** 0 (value 0.0482)
- **Attention Entropy:** 3.2037
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_46_1_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5381`
- **Prob (Healthy/Comp):** `[0.4619, 0.5381]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.796), WristRight(0.760)
- **Peak Frame:** 0 (value 0.0442)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_6_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5288`
- **Prob (Healthy/Comp):** `[0.4712, 0.5288]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.795), WristRight(0.764)
- **Peak Frame:** 0 (value 0.0391)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_7_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5338`
- **Prob (Healthy/Comp):** `[0.4662, 0.5338]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.794), WristRight(0.763)
- **Peak Frame:** 0 (value 0.0418)
- **Attention Entropy:** 3.2037
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `202_18_8_9_1_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5543`
- **Prob (Healthy/Comp):** `[0.4457, 0.5543]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.794), WristRight(0.763)
- **Peak Frame:** 0 (value 0.0444)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `203_18_2_33_1_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6751`
- **Prob (Healthy/Comp):** `[0.3249, 0.6751]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.786), WristLeft(0.755)
- **Peak Frame:** 62 (value 0.0405)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `203_18_5_10_1_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6416`
- **Prob (Healthy/Comp):** `[0.3584, 0.6416]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.785), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0298)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `203_18_5_8_1_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6383`
- **Prob (Healthy/Comp):** `[0.3617, 0.6383]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.784), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0410)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `203_18_5_9_1_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6180`
- **Prob (Healthy/Comp):** `[0.3820, 0.6180]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.785), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0459)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_1_1_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9273`
- **Prob (Healthy/Comp):** `[0.0727, 0.9273]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.793), WristRight(0.760)
- **Peak Frame:** 0 (value 0.0312)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_2_14_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5063`
- **Prob (Healthy/Comp):** `[0.4937, 0.5063]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.766), WristRight(0.752)
- **Peak Frame:** 18 (value 0.0288)
- **Attention Entropy:** 3.2064
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_2_52_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8972`
- **Prob (Healthy/Comp):** `[0.1028, 0.8972]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.765), WristLeft(0.752)
- **Peak Frame:** 31 (value 0.0372)
- **Attention Entropy:** 3.2063
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_2_53_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7205`
- **Prob (Healthy/Comp):** `[0.2795, 0.7205]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.766), WristRight(0.751)
- **Peak Frame:** 21 (value 0.0311)
- **Attention Entropy:** 3.2063
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_2_57_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5021`
- **Prob (Healthy/Comp):** `[0.4979, 0.5021]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.779), WristRight(0.752)
- **Peak Frame:** 62 (value 0.0316)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_3_51_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6388`
- **Prob (Healthy/Comp):** `[0.3612, 0.6388]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.766), WristRight(0.752)
- **Peak Frame:** 29 (value 0.0362)
- **Attention Entropy:** 3.2065
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_4_1_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6063`
- **Prob (Healthy/Comp):** `[0.3937, 0.6063]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.775), WristRight(0.756)
- **Peak Frame:** 0 (value 0.0304)
- **Attention Entropy:** 3.2055
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_4_2_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5983`
- **Prob (Healthy/Comp):** `[0.4017, 0.5983]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.776), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0302)
- **Attention Entropy:** 3.2054
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_4_3_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6078`
- **Prob (Healthy/Comp):** `[0.3922, 0.6078]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.776), WristRight(0.755)
- **Peak Frame:** 62 (value 0.0236)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_6_1_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7877`
- **Prob (Healthy/Comp):** `[0.2123, 0.7877]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.781), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0471)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_7_2_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6808`
- **Prob (Healthy/Comp):** `[0.3192, 0.6808]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.786), WristRight(0.750)
- **Peak Frame:** 1 (value 0.0386)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_7_3_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5311`
- **Prob (Healthy/Comp):** `[0.4689, 0.5311]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.780), WristRight(0.751)
- **Peak Frame:** 50 (value 0.0220)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_7_4_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7032`
- **Prob (Healthy/Comp):** `[0.2968, 0.7032]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.787), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0240)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_7_5_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7088`
- **Prob (Healthy/Comp):** `[0.2912, 0.7088]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.787), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0253)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_7_6_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6979`
- **Prob (Healthy/Comp):** `[0.3021, 0.6979]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.789), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0274)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_7_7_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7031`
- **Prob (Healthy/Comp):** `[0.2969, 0.7031]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.789), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0275)
- **Attention Entropy:** 3.2021
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_10_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6131`
- **Prob (Healthy/Comp):** `[0.3869, 0.6131]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.791), WristLeft(0.752)
- **Peak Frame:** 61 (value 0.0275)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_11_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6878`
- **Prob (Healthy/Comp):** `[0.3122, 0.6878]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.793), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0318)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_12_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6537`
- **Prob (Healthy/Comp):** `[0.3463, 0.6537]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.792), WristLeft(0.752)
- **Peak Frame:** 62 (value 0.0445)
- **Attention Entropy:** 3.2022
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_13_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6894`
- **Prob (Healthy/Comp):** `[0.3106, 0.6894]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.795), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0333)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_14_3_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6544`
- **Prob (Healthy/Comp):** `[0.3456, 0.6544]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.793), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0278)
- **Attention Entropy:** 3.2014
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_15_3_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6735`
- **Prob (Healthy/Comp):** `[0.3265, 0.6735]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.790), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0269)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_7_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6898`
- **Prob (Healthy/Comp):** `[0.3102, 0.6898]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.794), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0363)
- **Attention Entropy:** 3.2016
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_8_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6952`
- **Prob (Healthy/Comp):** `[0.3048, 0.6952]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.795), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0350)
- **Attention Entropy:** 3.2017
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `204_18_8_9_1_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6935`
- **Prob (Healthy/Comp):** `[0.3065, 0.6935]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.795), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0338)
- **Attention Entropy:** 3.2017
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `205_18_0_1_1_stand.txt`
- **Subject:** 205 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8585`
- **Prob (Healthy/Comp):** `[0.1415, 0.8585]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.768), WristRight(0.754)
- **Peak Frame:** 12 (value 0.0334)
- **Attention Entropy:** 3.2066
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `205_18_1_10_1_stand.txt`
- **Subject:** 205 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6050`
- **Prob (Healthy/Comp):** `[0.3950, 0.6050]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.764), WristRight(0.753)
- **Peak Frame:** 8 (value 0.0423)
- **Attention Entropy:** 3.2069
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `205_18_1_13_1_stand.txt`
- **Subject:** 205 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6104`
- **Prob (Healthy/Comp):** `[0.3896, 0.6104]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.761), WristRight(0.753)
- **Peak Frame:** 13 (value 0.0584)
- **Attention Entropy:** 3.2072
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `205_18_1_15_1_stand.txt`
- **Subject:** 205 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5430`
- **Prob (Healthy/Comp):** `[0.4570, 0.5430]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.765), WristRight(0.753)
- **Peak Frame:** 9 (value 0.0397)
- **Attention Entropy:** 3.2068
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `205_18_1_2_1_stand.txt`
- **Subject:** 205 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5077`
- **Prob (Healthy/Comp):** `[0.4923, 0.5077]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.764), WristRight(0.754)
- **Peak Frame:** 16 (value 0.0426)
- **Attention Entropy:** 3.2069
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `205_18_5_1_1_stand.txt`
- **Subject:** 205 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7045`
- **Prob (Healthy/Comp):** `[0.2955, 0.7045]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.779), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0669)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_0_1_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6526`
- **Prob (Healthy/Comp):** `[0.3474, 0.6526]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.796), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0262)
- **Attention Entropy:** 3.2016
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_0_2_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5475`
- **Prob (Healthy/Comp):** `[0.4525, 0.5475]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.796), WristRight(0.754)
- **Peak Frame:** 40 (value 0.0225)
- **Attention Entropy:** 3.2013
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_1_2_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8330`
- **Prob (Healthy/Comp):** `[0.1670, 0.8330]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.795), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0190)
- **Attention Entropy:** 3.2015
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_1_5_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9020`
- **Prob (Healthy/Comp):** `[0.0980, 0.9020]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0200)
- **Attention Entropy:** 3.2009
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_1_6_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8772`
- **Prob (Healthy/Comp):** `[0.1228, 0.8772]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0204)
- **Attention Entropy:** 3.2010
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_1_7_1_stand.txt`
- **Subject:** 206 | **Exercise:** 2 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8379`
- **Prob (Healthy/Comp):** `[0.1621, 0.8379]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.790), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0445)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_1_8_1_stand.txt`
- **Subject:** 206 | **Exercise:** 2 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8844`
- **Prob (Healthy/Comp):** `[0.1156, 0.8844]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.789), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0446)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_10_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8769`
- **Prob (Healthy/Comp):** `[0.1231, 0.8769]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.783), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0301)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_11_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8684`
- **Prob (Healthy/Comp):** `[0.1316, 0.8684]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.781), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0308)
- **Attention Entropy:** 3.2043
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_12_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8994`
- **Prob (Healthy/Comp):** `[0.1006, 0.8994]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.781), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0302)
- **Attention Entropy:** 3.2045
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_13_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8641`
- **Prob (Healthy/Comp):** `[0.1359, 0.8641]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.781), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0308)
- **Attention Entropy:** 3.2043
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_2_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7047`
- **Prob (Healthy/Comp):** `[0.2953, 0.7047]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.787), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0464)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_3_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7046`
- **Prob (Healthy/Comp):** `[0.2954, 0.7046]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.780), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0336)
- **Attention Entropy:** 3.2052
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_5_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6795`
- **Prob (Healthy/Comp):** `[0.3205, 0.6795]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.782), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0303)
- **Attention Entropy:** 3.2050
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_6_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5733`
- **Prob (Healthy/Comp):** `[0.4267, 0.5733]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.780), WristRight(0.752)
- **Peak Frame:** 62 (value 0.0309)
- **Attention Entropy:** 3.2051
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_7_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5154`
- **Prob (Healthy/Comp):** `[0.4846, 0.5154]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.781), WristRight(0.752)
- **Peak Frame:** 62 (value 0.0394)
- **Attention Entropy:** 3.2050
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_2_9_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9115`
- **Prob (Healthy/Comp):** `[0.0885, 0.9115]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.782), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0291)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_4_2_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6929`
- **Prob (Healthy/Comp):** `[0.3071, 0.6929]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.771), WristRight(0.752)
- **Peak Frame:** 9 (value 0.0273)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_4_3_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7543`
- **Prob (Healthy/Comp):** `[0.2457, 0.7543]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.784), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0433)
- **Attention Entropy:** 3.2038
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_4_4_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7700`
- **Prob (Healthy/Comp):** `[0.2300, 0.7700]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.786), WristRight(0.754)
- **Peak Frame:** 62 (value 0.0459)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_4_5_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7863`
- **Prob (Healthy/Comp):** `[0.2137, 0.7863]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.786), WristRight(0.754)
- **Peak Frame:** 62 (value 0.0401)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_4_6_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7556`
- **Prob (Healthy/Comp):** `[0.2444, 0.7556]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.785), WristRight(0.753)
- **Peak Frame:** 62 (value 0.0309)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_4_7_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7604`
- **Prob (Healthy/Comp):** `[0.2396, 0.7604]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.786), WristRight(0.753)
- **Peak Frame:** 62 (value 0.0489)
- **Attention Entropy:** 3.2037
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_10_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9837`
- **Prob (Healthy/Comp):** `[0.0163, 0.9837]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.782), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0297)
- **Attention Entropy:** 3.2048
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_11_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9701`
- **Prob (Healthy/Comp):** `[0.0299, 0.9701]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.783), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0287)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_1_1_chair.txt`
- **Subject:** 206 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8149`
- **Prob (Healthy/Comp):** `[0.1851, 0.8149]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.793), WristLeft(0.756)
- **Peak Frame:** 0 (value 0.0482)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_3_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8010`
- **Prob (Healthy/Comp):** `[0.1990, 0.8010]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.787), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0774)
- **Attention Entropy:** 3.2046
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_4_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8680`
- **Prob (Healthy/Comp):** `[0.1320, 0.8680]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.787), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0738)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_5_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8044`
- **Prob (Healthy/Comp):** `[0.1956, 0.8044]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.786), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0495)
- **Attention Entropy:** 3.2046
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_6_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8182`
- **Prob (Healthy/Comp):** `[0.1818, 0.8182]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.786), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0737)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_8_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9837`
- **Prob (Healthy/Comp):** `[0.0163, 0.9837]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.785), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0305)
- **Attention Entropy:** 3.2046
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_6_9_1_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9823`
- **Prob (Healthy/Comp):** `[0.0177, 0.9823]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.784), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0300)
- **Attention Entropy:** 3.2046
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_7_1_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6057`
- **Prob (Healthy/Comp):** `[0.3943, 0.6057]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0280)
- **Attention Entropy:** 3.2015
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_7_3_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6020`
- **Prob (Healthy/Comp):** `[0.3980, 0.6020]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0293)
- **Attention Entropy:** 3.2017
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_7_4_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5261`
- **Prob (Healthy/Comp):** `[0.4739, 0.5261]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.793), WristRight(0.756)
- **Peak Frame:** 0 (value 0.0271)
- **Attention Entropy:** 3.2012
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_7_5_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5403`
- **Prob (Healthy/Comp):** `[0.4597, 0.5403]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0350)
- **Attention Entropy:** 3.2011
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `206_18_7_6_1_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5344`
- **Prob (Healthy/Comp):** `[0.4656, 0.5344]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0267)
- **Attention Entropy:** 3.2011
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `207_18_1_10_1_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8823`
- **Prob (Healthy/Comp):** `[0.1177, 0.8823]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.792), WristRight(0.751)
- **Peak Frame:** 0 (value 0.0319)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `207_18_1_1_1_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8511`
- **Prob (Healthy/Comp):** `[0.1489, 0.8511]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.789), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0334)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `207_18_7_9_1_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8480`
- **Prob (Healthy/Comp):** `[0.1520, 0.8480]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.776), WristLeft(0.758)
- **Peak Frame:** 2 (value 0.0254)
- **Attention Entropy:** 3.2045
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `207_18_8_1_1_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7961`
- **Prob (Healthy/Comp):** `[0.2039, 0.7961]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.780), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0199)
- **Attention Entropy:** 3.2029
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_0_2_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6533`
- **Prob (Healthy/Comp):** `[0.3467, 0.6533]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.791), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0257)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_0_3_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7245`
- **Prob (Healthy/Comp):** `[0.2755, 0.7245]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.791), WristLeft(0.751)
- **Peak Frame:** 0 (value 0.0257)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_0_4_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7605`
- **Prob (Healthy/Comp):** `[0.2395, 0.7605]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.791), WristLeft(0.751)
- **Peak Frame:** 0 (value 0.0267)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_0_5_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7532`
- **Prob (Healthy/Comp):** `[0.2468, 0.7532]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.790), WristLeft(0.751)
- **Peak Frame:** 0 (value 0.0272)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_0_6_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6978`
- **Prob (Healthy/Comp):** `[0.3022, 0.6978]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.790), WristLeft(0.751)
- **Peak Frame:** 0 (value 0.0256)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_2_10_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6345`
- **Prob (Healthy/Comp):** `[0.3655, 0.6345]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.791), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0317)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_2_11_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7224`
- **Prob (Healthy/Comp):** `[0.2776, 0.7224]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.791), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0336)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_2_12_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7298`
- **Prob (Healthy/Comp):** `[0.2702, 0.7298]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.790), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0455)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_2_2_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6971`
- **Prob (Healthy/Comp):** `[0.3029, 0.6971]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.783), WristRight(0.760)
- **Peak Frame:** 0 (value 0.0355)
- **Attention Entropy:** 3.2022
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_2_7_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6726`
- **Prob (Healthy/Comp):** `[0.3274, 0.6726]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.788), WristRight(0.751)
- **Peak Frame:** 0 (value 0.0311)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_2_8_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6499`
- **Prob (Healthy/Comp):** `[0.3501, 0.6499]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.790), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0304)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_2_9_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6254`
- **Prob (Healthy/Comp):** `[0.3746, 0.6254]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.790), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0304)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_5_1_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6972`
- **Prob (Healthy/Comp):** `[0.3028, 0.6972]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.778), WristRight(0.752)
- **Peak Frame:** 62 (value 0.0573)
- **Attention Entropy:** 3.2054
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_5_2_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5419`
- **Prob (Healthy/Comp):** `[0.4581, 0.5419]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.778), WristRight(0.753)
- **Peak Frame:** 62 (value 0.0598)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_6_1_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8759`
- **Prob (Healthy/Comp):** `[0.1241, 0.8759]`
- **Top-3 Attention Joints:** SpineShoulder(0.799), SpineBase(0.786), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0979)
- **Attention Entropy:** 3.2042
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_6_2_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8946`
- **Prob (Healthy/Comp):** `[0.1054, 0.8946]`
- **Top-3 Attention Joints:** SpineShoulder(0.799), SpineBase(0.787), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0456)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_6_3_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8875`
- **Prob (Healthy/Comp):** `[0.1125, 0.8875]`
- **Top-3 Attention Joints:** SpineShoulder(0.800), SpineBase(0.788), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0799)
- **Attention Entropy:** 3.2043
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_6_4_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8130`
- **Prob (Healthy/Comp):** `[0.1870, 0.8130]`
- **Top-3 Attention Joints:** SpineShoulder(0.800), SpineBase(0.789), WristRight(0.753)
- **Peak Frame:** 0 (value 0.1097)
- **Attention Entropy:** 3.2042
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_6_5_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8366`
- **Prob (Healthy/Comp):** `[0.1634, 0.8366]`
- **Top-3 Attention Joints:** SpineShoulder(0.799), SpineBase(0.789), WristRight(0.754)
- **Peak Frame:** 0 (value 0.1156)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_6_6_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7740`
- **Prob (Healthy/Comp):** `[0.2260, 0.7740]`
- **Top-3 Attention Joints:** SpineShoulder(0.800), SpineBase(0.790), WristRight(0.753)
- **Peak Frame:** 62 (value 0.0500)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `209_18_8_2_1_wheelchair.txt`
- **Subject:** 209 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5231`
- **Prob (Healthy/Comp):** `[0.4769, 0.5231]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.783), WristLeft(0.756)
- **Peak Frame:** 63 (value 0.0350)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_1_1_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6127`
- **Prob (Healthy/Comp):** `[0.3873, 0.6127]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.792), WristRight(0.751)
- **Peak Frame:** 0 (value 0.0356)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_1_2_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5971`
- **Prob (Healthy/Comp):** `[0.4029, 0.5971]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.792), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0302)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_1_3_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5958`
- **Prob (Healthy/Comp):** `[0.4042, 0.5958]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.792), WristRight(0.751)
- **Peak Frame:** 0 (value 0.0322)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_1_4_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5006`
- **Prob (Healthy/Comp):** `[0.4994, 0.5006]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.791), WristLeft(0.750)
- **Peak Frame:** 0 (value 0.0320)
- **Attention Entropy:** 3.2022
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_2_1_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7989`
- **Prob (Healthy/Comp):** `[0.2011, 0.7989]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.802), WristRight(0.756)
- **Peak Frame:** 0 (value 0.0398)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_2_2_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7608`
- **Prob (Healthy/Comp):** `[0.2392, 0.7608]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.800), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0631)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_2_3_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8023`
- **Prob (Healthy/Comp):** `[0.1977, 0.8023]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.802), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0470)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_2_4_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6718`
- **Prob (Healthy/Comp):** `[0.3282, 0.6718]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.802), WristRight(0.757)
- **Peak Frame:** 62 (value 0.0318)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_2_5_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6575`
- **Prob (Healthy/Comp):** `[0.3425, 0.6575]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.803), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0270)
- **Attention Entropy:** 3.2028
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_3_1_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8686`
- **Prob (Healthy/Comp):** `[0.1314, 0.8686]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.803), WristRight(0.769)
- **Peak Frame:** 0 (value 0.0533)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_3_2_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7873`
- **Prob (Healthy/Comp):** `[0.2127, 0.7873]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.804), WristRight(0.771)
- **Peak Frame:** 62 (value 0.0359)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_3_3_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7360`
- **Prob (Healthy/Comp):** `[0.2640, 0.7360]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.803), WristRight(0.771)
- **Peak Frame:** 62 (value 0.0445)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_3_4_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8339`
- **Prob (Healthy/Comp):** `[0.1661, 0.8339]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.801), WristRight(0.766)
- **Peak Frame:** 0 (value 0.0399)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_3_5_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8414`
- **Prob (Healthy/Comp):** `[0.1586, 0.8414]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.804), WristRight(0.769)
- **Peak Frame:** 0 (value 0.0375)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_4_1_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8457`
- **Prob (Healthy/Comp):** `[0.1543, 0.8457]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.788), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0312)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_4_2_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8818`
- **Prob (Healthy/Comp):** `[0.1182, 0.8818]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.787), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0595)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_4_3_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8374`
- **Prob (Healthy/Comp):** `[0.1626, 0.8374]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.788), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0251)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_4_4_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8704`
- **Prob (Healthy/Comp):** `[0.1296, 0.8704]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.788), WristRight(0.758)
- **Peak Frame:** 0 (value 0.0263)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_4_5_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8512`
- **Prob (Healthy/Comp):** `[0.1488, 0.8512]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.788), WristRight(0.758)
- **Peak Frame:** 0 (value 0.0306)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_5_1_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8487`
- **Prob (Healthy/Comp):** `[0.1513, 0.8487]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.790), WristRight(0.767)
- **Peak Frame:** 0 (value 0.0781)
- **Attention Entropy:** 3.2026
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_5_2_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8945`
- **Prob (Healthy/Comp):** `[0.1055, 0.8945]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.799), WristRight(0.770)
- **Peak Frame:** 0 (value 0.0780)
- **Attention Entropy:** 3.2027
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_5_3_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8743`
- **Prob (Healthy/Comp):** `[0.1257, 0.8743]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.799), WristRight(0.770)
- **Peak Frame:** 0 (value 0.0723)
- **Attention Entropy:** 3.2026
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_5_4_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8949`
- **Prob (Healthy/Comp):** `[0.1051, 0.8949]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.799), WristRight(0.770)
- **Peak Frame:** 0 (value 0.0635)
- **Attention Entropy:** 3.2026
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `210_18_5_5_1_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8859`
- **Prob (Healthy/Comp):** `[0.1141, 0.8859]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.799), WristRight(0.770)
- **Peak Frame:** 0 (value 0.0624)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_6_1_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8054`
- **Prob (Healthy/Comp):** `[0.1946, 0.8054]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.786), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0342)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_6_2_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6511`
- **Prob (Healthy/Comp):** `[0.3489, 0.6511]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.785), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0691)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_6_3_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7132`
- **Prob (Healthy/Comp):** `[0.2868, 0.7132]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.785), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0279)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_6_4_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5792`
- **Prob (Healthy/Comp):** `[0.4208, 0.5792]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.785), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0408)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_6_5_3_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6613`
- **Prob (Healthy/Comp):** `[0.3387, 0.6613]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.793), WristLeft(0.761)
- **Peak Frame:** 0 (value 0.0318)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_6_6_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7392`
- **Prob (Healthy/Comp):** `[0.2608, 0.7392]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.787), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0413)
- **Attention Entropy:** 3.2057
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_7_5_3_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8422`
- **Prob (Healthy/Comp):** `[0.1578, 0.8422]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.769), WristLeft(0.754)
- **Peak Frame:** 2 (value 0.0237)
- **Attention Entropy:** 3.2061
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_7_6_3_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8459`
- **Prob (Healthy/Comp):** `[0.1541, 0.8459]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.770), WristLeft(0.756)
- **Peak Frame:** 2 (value 0.0219)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_8_1_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8342`
- **Prob (Healthy/Comp):** `[0.1658, 0.8342]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.789), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0331)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_8_2_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5919`
- **Prob (Healthy/Comp):** `[0.4081, 0.5919]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.784), WristLeft(0.756)
- **Peak Frame:** 10 (value 0.0333)
- **Attention Entropy:** 3.2044
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_8_3_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5615`
- **Prob (Healthy/Comp):** `[0.4385, 0.5615]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.781), WristLeft(0.755)
- **Peak Frame:** 10 (value 0.0294)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_8_4_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5307`
- **Prob (Healthy/Comp):** `[0.4693, 0.5307]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.780), WristLeft(0.755)
- **Peak Frame:** 6 (value 0.0214)
- **Attention Entropy:** 3.2048
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_8_5_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5039`
- **Prob (Healthy/Comp):** `[0.4961, 0.5039]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.779), WristLeft(0.755)
- **Peak Frame:** 12 (value 0.0258)
- **Attention Entropy:** 3.2049
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `211_18_8_6_1_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5219`
- **Prob (Healthy/Comp):** `[0.4781, 0.5219]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.779), WristLeft(0.755)
- **Peak Frame:** 36 (value 0.0261)
- **Attention Entropy:** 3.2050
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `212_18_0_1_1_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6276`
- **Prob (Healthy/Comp):** `[0.3724, 0.6276]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.779), WristRight(0.751)
- **Peak Frame:** 18 (value 0.0211)
- **Attention Entropy:** 3.2046
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `212_18_0_2_1_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6247`
- **Prob (Healthy/Comp):** `[0.3753, 0.6247]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.780), WristRight(0.751)
- **Peak Frame:** 19 (value 0.0211)
- **Attention Entropy:** 3.2046
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `212_18_0_4_1_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6218`
- **Prob (Healthy/Comp):** `[0.3782, 0.6218]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.776), WristRight(0.752)
- **Peak Frame:** 34 (value 0.0237)
- **Attention Entropy:** 3.2049
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `212_18_0_5_1_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5560`
- **Prob (Healthy/Comp):** `[0.4440, 0.5560]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.776), WristRight(0.752)
- **Peak Frame:** 26 (value 0.0280)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `212_18_1_5_1_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5239`
- **Prob (Healthy/Comp):** `[0.4761, 0.5239]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.769), WristRight(0.751)
- **Peak Frame:** 19 (value 0.0282)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `212_18_4_4_1_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5347`
- **Prob (Healthy/Comp):** `[0.4653, 0.5347]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.777), WristRight(0.758)
- **Peak Frame:** 29 (value 0.0290)
- **Attention Entropy:** 3.2043
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_1_3_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8560`
- **Prob (Healthy/Comp):** `[0.1440, 0.8560]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.794), WristRight(0.760)
- **Peak Frame:** 0 (value 0.0442)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_1_4_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6581`
- **Prob (Healthy/Comp):** `[0.3419, 0.6581]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.795), WristRight(0.760)
- **Peak Frame:** 0 (value 0.0429)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_1_5_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9025`
- **Prob (Healthy/Comp):** `[0.0975, 0.9025]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0457)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_6_1_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6483`
- **Prob (Healthy/Comp):** `[0.3517, 0.6483]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.789), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0446)
- **Attention Entropy:** 3.2055
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_6_3_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5539`
- **Prob (Healthy/Comp):** `[0.4461, 0.5539]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.788), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0591)
- **Attention Entropy:** 3.2054
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_6_4_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6007`
- **Prob (Healthy/Comp):** `[0.3993, 0.6007]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.786), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0612)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_6_5_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5044`
- **Prob (Healthy/Comp):** `[0.4956, 0.5044]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.785), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0582)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `213_18_6_6_1_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5429`
- **Prob (Healthy/Comp):** `[0.4571, 0.5429]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.784), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0640)
- **Attention Entropy:** 3.2060
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_2_2_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6194`
- **Prob (Healthy/Comp):** `[0.3806, 0.6194]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.778), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0225)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_6_1_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9515`
- **Prob (Healthy/Comp):** `[0.0485, 0.9515]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.781), WristLeft(0.752)
- **Peak Frame:** 62 (value 0.0275)
- **Attention Entropy:** 3.2055
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_6_2_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9140`
- **Prob (Healthy/Comp):** `[0.0860, 0.9140]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.780), WristLeft(0.751)
- **Peak Frame:** 62 (value 0.0240)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_6_3_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9001`
- **Prob (Healthy/Comp):** `[0.0999, 0.9001]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.779), WristLeft(0.751)
- **Peak Frame:** 0 (value 0.0297)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_6_4_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8883`
- **Prob (Healthy/Comp):** `[0.1117, 0.8883]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.782), WristLeft(0.753)
- **Peak Frame:** 61 (value 0.0276)
- **Attention Entropy:** 3.2054
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_7_1_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6569`
- **Prob (Healthy/Comp):** `[0.3431, 0.6569]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.786), WristLeft(0.761)
- **Peak Frame:** 27 (value 0.0197)
- **Attention Entropy:** 3.2015
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_7_2_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6303`
- **Prob (Healthy/Comp):** `[0.3697, 0.6303]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.785), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0265)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_7_3_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5674`
- **Prob (Healthy/Comp):** `[0.4326, 0.5674]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.782), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0252)
- **Attention Entropy:** 3.2021
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_7_4_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5926`
- **Prob (Healthy/Comp):** `[0.4074, 0.5926]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.783), WristLeft(0.760)
- **Peak Frame:** 0 (value 0.0239)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_7_5_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5577`
- **Prob (Healthy/Comp):** `[0.4423, 0.5577]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.783), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0279)
- **Attention Entropy:** 3.2022
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_7_6_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5371`
- **Prob (Healthy/Comp):** `[0.4629, 0.5371]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.783), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0269)
- **Attention Entropy:** 3.2022
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_8_5_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5741`
- **Prob (Healthy/Comp):** `[0.4259, 0.5741]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.784), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0415)
- **Attention Entropy:** 3.2026
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `214_18_8_6_1_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6495`
- **Prob (Healthy/Comp):** `[0.3505, 0.6495]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.785), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0383)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_5_1_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7809`
- **Prob (Healthy/Comp):** `[0.2191, 0.7809]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.777), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0573)
- **Attention Entropy:** 3.2054
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_6_1_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7366`
- **Prob (Healthy/Comp):** `[0.2634, 0.7366]`
- **Top-3 Attention Joints:** SpineShoulder(0.801), SpineBase(0.779), WristLeft(0.752)
- **Peak Frame:** 41 (value 0.0225)
- **Attention Entropy:** 3.2062
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_6_2_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8258`
- **Prob (Healthy/Comp):** `[0.1742, 0.8258]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.784), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0362)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_6_3_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6442`
- **Prob (Healthy/Comp):** `[0.3558, 0.6442]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.779), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0262)
- **Attention Entropy:** 3.2061
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_6_4_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6588`
- **Prob (Healthy/Comp):** `[0.3412, 0.6588]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.781), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0332)
- **Attention Entropy:** 3.2060
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_6_6_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6455`
- **Prob (Healthy/Comp):** `[0.3545, 0.6455]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.782), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0360)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_7_1_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9131`
- **Prob (Healthy/Comp):** `[0.0869, 0.9131]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.783), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0326)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_7_2_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9125`
- **Prob (Healthy/Comp):** `[0.0875, 0.9125]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.785), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0326)
- **Attention Entropy:** 3.2029
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_7_3_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9179`
- **Prob (Healthy/Comp):** `[0.0821, 0.9179]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.785), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0341)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_7_4_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9101`
- **Prob (Healthy/Comp):** `[0.0899, 0.9101]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.786), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0332)
- **Attention Entropy:** 3.2028
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_7_5_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.9080`
- **Prob (Healthy/Comp):** `[0.0920, 0.9080]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.786), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0319)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_7_6_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8765`
- **Prob (Healthy/Comp):** `[0.1235, 0.8765]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.787), WristLeft(0.756)
- **Peak Frame:** 0 (value 0.0362)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_8_1_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8231`
- **Prob (Healthy/Comp):** `[0.1769, 0.8231]`
- **Top-3 Attention Joints:** SpineShoulder(0.811), SpineBase(0.787), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0426)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_8_2_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8114`
- **Prob (Healthy/Comp):** `[0.1886, 0.8114]`
- **Top-3 Attention Joints:** SpineShoulder(0.811), SpineBase(0.788), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0388)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_8_3_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8052`
- **Prob (Healthy/Comp):** `[0.1948, 0.8052]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.788), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0367)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_8_4_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7921`
- **Prob (Healthy/Comp):** `[0.2079, 0.7921]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.791), WristLeft(0.759)
- **Peak Frame:** 0 (value 0.0460)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_8_5_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8078`
- **Prob (Healthy/Comp):** `[0.1922, 0.8078]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.790), WristLeft(0.757)
- **Peak Frame:** 0 (value 0.0406)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `216_18_8_6_1_stand.txt`
- **Subject:** 216 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.8057`
- **Prob (Healthy/Comp):** `[0.1943, 0.8057]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.791), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0380)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_0_8_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5419`
- **Prob (Healthy/Comp):** `[0.4581, 0.5419]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.800), WristRight(0.750)
- **Peak Frame:** 0 (value 0.0437)
- **Attention Entropy:** 3.2029
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_1_1_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 1 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7632`
- **Prob (Healthy/Comp):** `[0.2368, 0.7632]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.772), WristRight(0.752)
- **Peak Frame:** 37 (value 0.0449)
- **Attention Entropy:** 3.2051
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_4_1_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6741`
- **Prob (Healthy/Comp):** `[0.3259, 0.6741]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.785), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0508)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_4_2_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5916`
- **Prob (Healthy/Comp):** `[0.4084, 0.5916]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.785), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0583)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_4_3_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5970`
- **Prob (Healthy/Comp):** `[0.4030, 0.5970]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.785), WristRight(0.759)
- **Peak Frame:** 0 (value 0.0590)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_7_2_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6741`
- **Prob (Healthy/Comp):** `[0.3259, 0.6741]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.794), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0324)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_7_4_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5296`
- **Prob (Healthy/Comp):** `[0.4704, 0.5296]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.794), WristRight(0.755)
- **Peak Frame:** 57 (value 0.0358)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_8_1_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5096`
- **Prob (Healthy/Comp):** `[0.4904, 0.5096]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.794), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0353)
- **Attention Entropy:** 3.2026
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_8_2_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6019`
- **Prob (Healthy/Comp):** `[0.3981, 0.6019]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.794), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0365)
- **Attention Entropy:** 3.2028
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `217_18_8_4_1_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6336`
- **Prob (Healthy/Comp):** `[0.3664, 0.6336]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.793), WristRight(0.755)
- **Peak Frame:** 0 (value 0.0297)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `301_18_0_1_1_chair.txt`
- **Subject:** 301 | **Exercise:** 5 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5970`
- **Prob (Healthy/Comp):** `[0.4030, 0.5970]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.772), WristRight(0.752)
- **Peak Frame:** 14 (value 0.0323)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `302_18_0_5_1_chair.txt`
- **Subject:** 302 | **Exercise:** 5 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5374`
- **Prob (Healthy/Comp):** `[0.4626, 0.5374]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.789), WristLeft(0.758)
- **Peak Frame:** 52 (value 0.0322)
- **Attention Entropy:** 3.2012
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `304_18_1_1_1_chair.txt`
- **Subject:** 304 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5697`
- **Prob (Healthy/Comp):** `[0.4303, 0.5697]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.765), WristLeft(0.750)
- **Peak Frame:** 34 (value 0.0287)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `304_18_1_2_1_chair.txt`
- **Subject:** 304 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5125`
- **Prob (Healthy/Comp):** `[0.4875, 0.5125]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.765), WristLeft(0.751)
- **Peak Frame:** 1 (value 0.0377)
- **Attention Entropy:** 3.2054
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `305_18_0_1_1_chair.txt`
- **Subject:** 305 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6866`
- **Prob (Healthy/Comp):** `[0.3134, 0.6866]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.782), WristRight(0.757)
- **Peak Frame:** 14 (value 0.0234)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `305_18_0_2_1_chair.txt`
- **Subject:** 305 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7793`
- **Prob (Healthy/Comp):** `[0.2207, 0.7793]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.780), WristRight(0.757)
- **Peak Frame:** 16 (value 0.0303)
- **Attention Entropy:** 3.2038
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `305_18_0_3_1_chair.txt`
- **Subject:** 305 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6300`
- **Prob (Healthy/Comp):** `[0.3700, 0.6300]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.788), WristRight(0.759)
- **Peak Frame:** 24 (value 0.0252)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `305_18_0_4_1_chair.txt`
- **Subject:** 305 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5984`
- **Prob (Healthy/Comp):** `[0.4016, 0.5984]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.787), WristRight(0.757)
- **Peak Frame:** 21 (value 0.0275)
- **Attention Entropy:** 3.2025
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `305_18_0_5_1_chair.txt`
- **Subject:** 305 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.7070`
- **Prob (Healthy/Comp):** `[0.2930, 0.7070]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.781), WristRight(0.756)
- **Peak Frame:** 18 (value 0.0289)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `305_18_0_6_1_chair.txt`
- **Subject:** 305 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.6017`
- **Prob (Healthy/Comp):** `[0.3983, 0.6017]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.784), WristRight(0.756)
- **Peak Frame:** 20 (value 0.0269)
- **Attention Entropy:** 3.2029
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)

### `307_18_1_3_1_sit.txt`
- **Subject:** 307 | **Exercise:** 5 | **Position:** sit
- **Ground Truth:** Healthy
- **Prediction:** Compensated
- **Confidence:** `0.5005`
- **Prob (Healthy/Comp):** `[0.4995, 0.5005]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.781), WristRight(0.758)
- **Peak Frame:** 32 (value 0.0221)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Atypical healthy motion (possibly noisy skeleton or edge-case style)


## False Negatives (101 samples)

### `105_18_0_12_2_stand.txt`
- **Subject:** 105 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9507`
- **Prob (Healthy/Comp):** `[0.9507, 0.0493]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.794), WristLeft(0.757)
- **Peak Frame:** 0 (value 0.0448)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `105_18_0_1_2_stand.txt`
- **Subject:** 105 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6441`
- **Prob (Healthy/Comp):** `[0.6441, 0.3559]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.768), WristRight(0.753)
- **Peak Frame:** 15 (value 0.0300)
- **Attention Entropy:** 3.2063
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_4_16_2_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8135`
- **Prob (Healthy/Comp):** `[0.8135, 0.1865]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.786), WristRight(0.754)
- **Peak Frame:** 31 (value 0.0266)
- **Attention Entropy:** 3.2055
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_4_19_2_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5478`
- **Prob (Healthy/Comp):** `[0.5478, 0.4522]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.783), WristRight(0.754)
- **Peak Frame:** 58 (value 0.0359)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_4_31_2_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8069`
- **Prob (Healthy/Comp):** `[0.8069, 0.1931]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.775), WristRight(0.754)
- **Peak Frame:** 31 (value 0.0246)
- **Attention Entropy:** 3.2062
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_4_32_2_stand.txt`
- **Subject:** 202 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6840`
- **Prob (Healthy/Comp):** `[0.6840, 0.3160]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.775), WristRight(0.756)
- **Peak Frame:** 0 (value 0.0468)
- **Attention Entropy:** 3.2061
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_7_22_2_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6734`
- **Prob (Healthy/Comp):** `[0.6734, 0.3266]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.792), WristLeft(0.757)
- **Peak Frame:** 0 (value 0.0466)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_7_23_2_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7007`
- **Prob (Healthy/Comp):** `[0.7007, 0.2993]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.789), WristLeft(0.756)
- **Peak Frame:** 0 (value 0.0426)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_8_22_2_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9263`
- **Prob (Healthy/Comp):** `[0.9263, 0.0737]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.785), WristRight(0.760)
- **Peak Frame:** 15 (value 0.0204)
- **Attention Entropy:** 3.2048
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `202_18_8_28_2_stand.txt`
- **Subject:** 202 | **Exercise:** 3 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6255`
- **Prob (Healthy/Comp):** `[0.6255, 0.3745]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.796), WristLeft(0.755)
- **Peak Frame:** 63 (value 0.0430)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `203_18_2_27_2_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7053`
- **Prob (Healthy/Comp):** `[0.7053, 0.2947]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.782), WristLeft(0.750)
- **Peak Frame:** 43 (value 0.0200)
- **Attention Entropy:** 3.2048
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `203_18_2_28_2_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5286`
- **Prob (Healthy/Comp):** `[0.5286, 0.4714]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.770), WristLeft(0.750)
- **Peak Frame:** 14 (value 0.0264)
- **Attention Entropy:** 3.2062
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `203_18_2_29_2_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5334`
- **Prob (Healthy/Comp):** `[0.5334, 0.4666]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.771), WristLeft(0.750)
- **Peak Frame:** 13 (value 0.0265)
- **Attention Entropy:** 3.2061
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `203_18_2_30_2_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7399`
- **Prob (Healthy/Comp):** `[0.7399, 0.2601]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.785), WristLeft(0.755)
- **Peak Frame:** 18 (value 0.0255)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `203_18_5_12_2_wheelchair.txt`
- **Subject:** 203 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6598`
- **Prob (Healthy/Comp):** `[0.6598, 0.3402]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.785), WristRight(0.753)
- **Peak Frame:** 62 (value 0.0236)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_2_54_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8606`
- **Prob (Healthy/Comp):** `[0.8606, 0.1394]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.774), WristRight(0.752)
- **Peak Frame:** 61 (value 0.0325)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_2_64_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6310`
- **Prob (Healthy/Comp):** `[0.6310, 0.3690]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.773), WristRight(0.749)
- **Peak Frame:** 24 (value 0.0218)
- **Attention Entropy:** 3.2059
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_1_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8664`
- **Prob (Healthy/Comp):** `[0.8664, 0.1336]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.779), WristRight(0.752)
- **Peak Frame:** 43 (value 0.0319)
- **Attention Entropy:** 3.2046
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_2_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8707`
- **Prob (Healthy/Comp):** `[0.8707, 0.1293]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.787), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0254)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_36_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6786`
- **Prob (Healthy/Comp):** `[0.6786, 0.3214]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.782), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0250)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_3_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9373`
- **Prob (Healthy/Comp):** `[0.9373, 0.0627]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.778), WristRight(0.752)
- **Peak Frame:** 35 (value 0.0259)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_4_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9518`
- **Prob (Healthy/Comp):** `[0.9518, 0.0482]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.783), WristRight(0.752)
- **Peak Frame:** 50 (value 0.0245)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_5_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9324`
- **Prob (Healthy/Comp):** `[0.9324, 0.0676]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.782), WristRight(0.753)
- **Peak Frame:** 20 (value 0.0229)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_6_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8839`
- **Prob (Healthy/Comp):** `[0.8839, 0.1161]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.787), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0287)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_3_7_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8440`
- **Prob (Healthy/Comp):** `[0.8440, 0.1560]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.780), WristRight(0.752)
- **Peak Frame:** 42 (value 0.0305)
- **Attention Entropy:** 3.2043
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_5_6_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8106`
- **Prob (Healthy/Comp):** `[0.8106, 0.1894]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.775), WristLeft(0.752)
- **Peak Frame:** 62 (value 0.0551)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_5_7_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8266`
- **Prob (Healthy/Comp):** `[0.8266, 0.1734]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.775), WristLeft(0.751)
- **Peak Frame:** 62 (value 0.0535)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `204_18_8_3_2_chair.txt`
- **Subject:** 204 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5289`
- **Prob (Healthy/Comp):** `[0.5289, 0.4711]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.778), WristRight(0.753)
- **Peak Frame:** 19 (value 0.0213)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `205_18_1_16_2_stand.txt`
- **Subject:** 205 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5609`
- **Prob (Healthy/Comp):** `[0.5609, 0.4391]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.767), WristRight(0.754)
- **Peak Frame:** 23 (value 0.0426)
- **Attention Entropy:** 3.2066
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_1_3_2_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7060`
- **Prob (Healthy/Comp):** `[0.7060, 0.2940]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.793), WristLeft(0.753)
- **Peak Frame:** 0 (value 0.0252)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_2_16_2_stand.txt`
- **Subject:** 206 | **Exercise:** 2 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6223`
- **Prob (Healthy/Comp):** `[0.6223, 0.3777]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.787), WristLeft(0.754)
- **Peak Frame:** 0 (value 0.0346)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_2_1_2_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6516`
- **Prob (Healthy/Comp):** `[0.6516, 0.3484]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.784), WristLeft(0.755)
- **Peak Frame:** 13 (value 0.0338)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_3_10_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6837`
- **Prob (Healthy/Comp):** `[0.6837, 0.3163]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.790), WristLeft(0.760)
- **Peak Frame:** 0 (value 0.0405)
- **Attention Entropy:** 3.2018
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_3_11_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5897`
- **Prob (Healthy/Comp):** `[0.5897, 0.4103]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.790), WristLeft(0.760)
- **Peak Frame:** 0 (value 0.0386)
- **Attention Entropy:** 3.2019
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_3_12_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5742`
- **Prob (Healthy/Comp):** `[0.5742, 0.4258]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.790), WristLeft(0.760)
- **Peak Frame:** 0 (value 0.0388)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_3_13_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9657`
- **Prob (Healthy/Comp):** `[0.9657, 0.0343]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.784), WristRight(0.758)
- **Peak Frame:** 56 (value 0.0254)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_3_14_2_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8906`
- **Prob (Healthy/Comp):** `[0.8906, 0.1094]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.790), WristLeft(0.750)
- **Peak Frame:** 22 (value 0.0335)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_5_11_2_chair.txt`
- **Subject:** 206 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7672`
- **Prob (Healthy/Comp):** `[0.7672, 0.2328]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.782), WristLeft(0.759)
- **Peak Frame:** 25 (value 0.0222)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_5_12_2_chair.txt`
- **Subject:** 206 | **Exercise:** 0 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5760`
- **Prob (Healthy/Comp):** `[0.5760, 0.4240]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.776), WristLeft(0.756)
- **Peak Frame:** 20 (value 0.0252)
- **Attention Entropy:** 3.2043
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_5_15_2_chair.txt`
- **Subject:** 206 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8803`
- **Prob (Healthy/Comp):** `[0.8803, 0.1197]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.781), WristLeft(0.757)
- **Peak Frame:** 24 (value 0.0244)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_5_16_2_chair.txt`
- **Subject:** 206 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6518`
- **Prob (Healthy/Comp):** `[0.6518, 0.3482]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.790), WristLeft(0.756)
- **Peak Frame:** 0 (value 0.0230)
- **Attention Entropy:** 3.2006
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_5_17_2_chair.txt`
- **Subject:** 206 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5286`
- **Prob (Healthy/Comp):** `[0.5286, 0.4714]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.790), WristLeft(0.757)
- **Peak Frame:** 2 (value 0.0210)
- **Attention Entropy:** 3.2008
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_6_12_2_chair.txt`
- **Subject:** 206 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6475`
- **Prob (Healthy/Comp):** `[0.6475, 0.3525]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.789), WristLeft(0.752)
- **Peak Frame:** 2 (value 0.0405)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_6_13_2_chair.txt`
- **Subject:** 206 | **Exercise:** 3 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8787`
- **Prob (Healthy/Comp):** `[0.8787, 0.1213]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.789), WristLeft(0.753)
- **Peak Frame:** 14 (value 0.0285)
- **Attention Entropy:** 3.2041
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_7_14_2_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8808`
- **Prob (Healthy/Comp):** `[0.8808, 0.1192]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.776), WristLeft(0.752)
- **Peak Frame:** 14 (value 0.0195)
- **Attention Entropy:** 3.2042
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_7_25_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5699`
- **Prob (Healthy/Comp):** `[0.5699, 0.4301]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.786), WristRight(0.763)
- **Peak Frame:** 0 (value 0.0430)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_7_8_2_chair.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7364`
- **Prob (Healthy/Comp):** `[0.7364, 0.2636]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.790), WristLeft(0.756)
- **Peak Frame:** 62 (value 0.0354)
- **Attention Entropy:** 3.2014
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_8_10_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7890`
- **Prob (Healthy/Comp):** `[0.7890, 0.2110]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.794), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0465)
- **Attention Entropy:** 3.2024
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_8_8_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7855`
- **Prob (Healthy/Comp):** `[0.7855, 0.2145]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.794), WristRight(0.761)
- **Peak Frame:** 0 (value 0.0467)
- **Attention Entropy:** 3.2023
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `206_18_8_9_2_stand.txt`
- **Subject:** 206 | **Exercise:** 4 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9658`
- **Prob (Healthy/Comp):** `[0.9658, 0.0342]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.775), WristRight(0.752)
- **Peak Frame:** 18 (value 0.0230)
- **Attention Entropy:** 3.2052
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `207_18_0_19_2_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9407`
- **Prob (Healthy/Comp):** `[0.9407, 0.0593]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.778), WristLeft(0.755)
- **Peak Frame:** 22 (value 0.0255)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `207_18_0_5_2_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6319`
- **Prob (Healthy/Comp):** `[0.6319, 0.3681]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.783), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0384)
- **Attention Entropy:** 3.2039
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `207_18_3_15_2_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9596`
- **Prob (Healthy/Comp):** `[0.9596, 0.0404]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.769), WristLeft(0.752)
- **Peak Frame:** 0 (value 0.0274)
- **Attention Entropy:** 3.2050
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `207_18_3_16_2_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9885`
- **Prob (Healthy/Comp):** `[0.9885, 0.0115]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.781), WristLeft(0.752)
- **Peak Frame:** 53 (value 0.0268)
- **Attention Entropy:** 3.2049
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `207_18_3_1_2_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5771`
- **Prob (Healthy/Comp):** `[0.5771, 0.4229]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.788), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0262)
- **Attention Entropy:** 3.2032
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `207_18_8_7_2_stand.txt`
- **Subject:** 207 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6181`
- **Prob (Healthy/Comp):** `[0.6181, 0.3819]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.778), WristLeft(0.755)
- **Peak Frame:** 46 (value 0.0313)
- **Attention Entropy:** 3.2034
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `210_18_1_6_2_wheelchair.txt`
- **Subject:** 210 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6756`
- **Prob (Healthy/Comp):** `[0.6756, 0.3244]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.792), WristRight(0.750)
- **Peak Frame:** 0 (value 0.0257)
- **Attention Entropy:** 3.2020
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `211_18_7_4_2_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9692`
- **Prob (Healthy/Comp):** `[0.9692, 0.0308]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.778), WristLeft(0.755)
- **Peak Frame:** 41 (value 0.0202)
- **Attention Entropy:** 3.2053
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `211_18_7_7_2_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5717`
- **Prob (Healthy/Comp):** `[0.5717, 0.4283]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.790), WristLeft(0.756)
- **Peak Frame:** 0 (value 0.0326)
- **Attention Entropy:** 3.2035
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `211_18_7_8_2_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5847`
- **Prob (Healthy/Comp):** `[0.5847, 0.4153]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.789), WristLeft(0.757)
- **Peak Frame:** 0 (value 0.0241)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `211_18_7_9_2_stand.txt`
- **Subject:** 211 | **Exercise:** 0 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6848`
- **Prob (Healthy/Comp):** `[0.6848, 0.3152]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.792), WristLeft(0.758)
- **Peak Frame:** 0 (value 0.0352)
- **Attention Entropy:** 3.2038
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_1_2_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7227`
- **Prob (Healthy/Comp):** `[0.7227, 0.2773]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.780), WristRight(0.753)
- **Peak Frame:** 19 (value 0.0297)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_2_1_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7528`
- **Prob (Healthy/Comp):** `[0.7528, 0.2472]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.784), WristRight(0.752)
- **Peak Frame:** 0 (value 0.0260)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_3_1_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5332`
- **Prob (Healthy/Comp):** `[0.5332, 0.4668]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.773), WristRight(0.755)
- **Peak Frame:** 16 (value 0.0295)
- **Attention Entropy:** 3.2047
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_3_6_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7039`
- **Prob (Healthy/Comp):** `[0.7039, 0.2961]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.781), WristRight(0.757)
- **Peak Frame:** 28 (value 0.0288)
- **Attention Entropy:** 3.2038
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_5_1_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6342`
- **Prob (Healthy/Comp):** `[0.6342, 0.3658]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.782), WristRight(0.754)
- **Peak Frame:** 62 (value 0.0458)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_5_2_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6720`
- **Prob (Healthy/Comp):** `[0.6720, 0.3280]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.781), WristRight(0.754)
- **Peak Frame:** 62 (value 0.0408)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_6_1_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7363`
- **Prob (Healthy/Comp):** `[0.7363, 0.2637]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.783), WristLeft(0.752)
- **Peak Frame:** 62 (value 0.0367)
- **Attention Entropy:** 3.2040
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_6_2_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9300`
- **Prob (Healthy/Comp):** `[0.9300, 0.0700]`
- **Top-3 Attention Joints:** SpineShoulder(0.805), SpineBase(0.785), WristLeft(0.754)
- **Peak Frame:** 41 (value 0.0281)
- **Attention Entropy:** 3.2036
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_6_3_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6244`
- **Prob (Healthy/Comp):** `[0.6244, 0.3756]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.775), WristLeft(0.753)
- **Peak Frame:** 21 (value 0.0377)
- **Attention Entropy:** 3.2052
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_6_4_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7390`
- **Prob (Healthy/Comp):** `[0.7390, 0.2610]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.776), WristLeft(0.753)
- **Peak Frame:** 24 (value 0.0357)
- **Attention Entropy:** 3.2052
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_7_1_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6662`
- **Prob (Healthy/Comp):** `[0.6662, 0.3338]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.781), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0310)
- **Attention Entropy:** 3.2004
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_7_2_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6523`
- **Prob (Healthy/Comp):** `[0.6523, 0.3477]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.780), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0251)
- **Attention Entropy:** 3.2002
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_7_3_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6535`
- **Prob (Healthy/Comp):** `[0.6535, 0.3465]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.779), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0272)
- **Attention Entropy:** 3.2002
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_7_4_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5506`
- **Prob (Healthy/Comp):** `[0.5506, 0.4494]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.780), WristRight(0.754)
- **Peak Frame:** 0 (value 0.0262)
- **Attention Entropy:** 3.2005
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_7_5_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6263`
- **Prob (Healthy/Comp):** `[0.6263, 0.3737]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.776), WristRight(0.762)
- **Peak Frame:** 0 (value 0.0319)
- **Attention Entropy:** 3.1998
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_8_1_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6335`
- **Prob (Healthy/Comp):** `[0.6335, 0.3665]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.779), WristRight(0.753)
- **Peak Frame:** 0 (value 0.0362)
- **Attention Entropy:** 3.2015
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_8_2_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6311`
- **Prob (Healthy/Comp):** `[0.6311, 0.3689]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.782), WristRight(0.758)
- **Peak Frame:** 0 (value 0.0379)
- **Attention Entropy:** 3.2010
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_8_3_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6235`
- **Prob (Healthy/Comp):** `[0.6235, 0.3765]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.779), WristRight(0.756)
- **Peak Frame:** 0 (value 0.0367)
- **Attention Entropy:** 3.2010
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_8_4_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5950`
- **Prob (Healthy/Comp):** `[0.5950, 0.4050]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.779), WristRight(0.758)
- **Peak Frame:** 0 (value 0.0363)
- **Attention Entropy:** 3.2009
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_8_5_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6225`
- **Prob (Healthy/Comp):** `[0.6225, 0.3775]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.778), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0273)
- **Attention Entropy:** 3.2012
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `212_18_8_6_2_wheelchair.txt`
- **Subject:** 212 | **Exercise:** 0 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6178`
- **Prob (Healthy/Comp):** `[0.6178, 0.3822]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.781), WristRight(0.757)
- **Peak Frame:** 11 (value 0.0206)
- **Attention Entropy:** 3.2005
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `213_18_5_6_2_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8022`
- **Prob (Healthy/Comp):** `[0.8022, 0.1978]`
- **Top-3 Attention Joints:** SpineShoulder(0.807), SpineBase(0.787), WristRight(0.757)
- **Peak Frame:** 0 (value 0.0692)
- **Attention Entropy:** 3.2044
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `213_18_8_3_2_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5152`
- **Prob (Healthy/Comp):** `[0.5152, 0.4848]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.798), WristLeft(0.755)
- **Peak Frame:** 0 (value 0.0325)
- **Attention Entropy:** 3.2033
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `213_18_8_4_2_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6171`
- **Prob (Healthy/Comp):** `[0.6171, 0.3829]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.795), WristLeft(0.756)
- **Peak Frame:** 0 (value 0.0309)
- **Attention Entropy:** 3.2031
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `213_18_8_5_2_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6570`
- **Prob (Healthy/Comp):** `[0.6570, 0.3430]`
- **Top-3 Attention Joints:** SpineShoulder(0.809), SpineBase(0.796), WristRight(0.757)
- **Peak Frame:** 2 (value 0.0273)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `213_18_8_6_2_stand.txt`
- **Subject:** 213 | **Exercise:** 1 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6860`
- **Prob (Healthy/Comp):** `[0.6860, 0.3140]`
- **Top-3 Attention Joints:** SpineShoulder(0.810), SpineBase(0.797), WristRight(0.758)
- **Peak Frame:** 0 (value 0.0255)
- **Attention Entropy:** 3.2030
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `214_18_2_6_2_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8486`
- **Prob (Healthy/Comp):** `[0.8486, 0.1514]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.774), WristRight(0.753)
- **Peak Frame:** 21 (value 0.0195)
- **Attention Entropy:** 3.2052
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `214_18_8_7_2_Stand-frame.txt`
- **Subject:** 214 | **Exercise:** 4 | **Position:** Stand-frame
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6229`
- **Prob (Healthy/Comp):** `[0.6229, 0.3771]`
- **Top-3 Attention Joints:** SpineShoulder(0.806), SpineBase(0.780), WristLeft(0.757)
- **Peak Frame:** 23 (value 0.0289)
- **Attention Entropy:** 3.2037
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_1_1_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.7558`
- **Prob (Healthy/Comp):** `[0.7558, 0.2442]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.773), WristRight(0.760)
- **Peak Frame:** 42 (value 0.0223)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_1_2_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8049`
- **Prob (Healthy/Comp):** `[0.8049, 0.1951]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.773), WristRight(0.761)
- **Peak Frame:** 41 (value 0.0279)
- **Attention Entropy:** 3.2057
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_1_4_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6031`
- **Prob (Healthy/Comp):** `[0.6031, 0.3969]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.772), WristRight(0.759)
- **Peak Frame:** 41 (value 0.0262)
- **Attention Entropy:** 3.2058
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_2_10_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8507`
- **Prob (Healthy/Comp):** `[0.8507, 0.1493]`
- **Top-3 Attention Joints:** SpineShoulder(0.804), SpineBase(0.775), WristLeft(0.755)
- **Peak Frame:** 62 (value 0.0241)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_2_9_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5232`
- **Prob (Healthy/Comp):** `[0.5232, 0.4768]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.767), WristLeft(0.753)
- **Peak Frame:** 37 (value 0.0359)
- **Attention Entropy:** 3.2065
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_3_6_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9769`
- **Prob (Healthy/Comp):** `[0.9769, 0.0231]`
- **Top-3 Attention Joints:** SpineShoulder(0.803), SpineBase(0.776), WristRight(0.755)
- **Peak Frame:** 58 (value 0.0430)
- **Attention Entropy:** 3.2056
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_3_7_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.8593`
- **Prob (Healthy/Comp):** `[0.8593, 0.1407]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.767), WristRight(0.754)
- **Peak Frame:** 31 (value 0.0300)
- **Attention Entropy:** 3.2066
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_4_3_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5062`
- **Prob (Healthy/Comp):** `[0.5062, 0.4938]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.764), WristRight(0.753)
- **Peak Frame:** 14 (value 0.0282)
- **Attention Entropy:** 3.2067
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_4_4_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5957`
- **Prob (Healthy/Comp):** `[0.5957, 0.4043]`
- **Top-3 Attention Joints:** SpineShoulder(0.801), SpineBase(0.763), WristRight(0.753)
- **Peak Frame:** 14 (value 0.0259)
- **Attention Entropy:** 3.2068
- **Inferred Reason:** Low confidence (borderline prediction); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `215_18_6_9_2_stand.txt`
- **Subject:** 215 | **Exercise:** 5 | **Position:** stand
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.9251`
- **Prob (Healthy/Comp):** `[0.9251, 0.0749]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.781), WristLeft(0.754)
- **Peak Frame:** 62 (value 0.0500)
- **Attention Entropy:** 3.2057
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `217_18_7_7_2_wheelchair.txt`
- **Subject:** 217 | **Exercise:** 3 | **Position:** wheelchair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.6621`
- **Prob (Healthy/Comp):** `[0.6621, 0.3379]`
- **Top-3 Attention Joints:** SpineShoulder(0.808), SpineBase(0.791), WristLeft(0.756)
- **Peak Frame:** 0 (value 0.0388)
- **Attention Entropy:** 3.2013
- **Inferred Reason:** High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)

### `302_18_4_13_2_chair.txt`
- **Subject:** 302 | **Exercise:** 5 | **Position:** chair
- **Ground Truth:** Compensated
- **Prediction:** Healthy
- **Confidence:** `0.5460`
- **Prob (Healthy/Comp):** `[0.5460, 0.4540]`
- **Top-3 Attention Joints:** SpineShoulder(0.802), SpineBase(0.762), WristRight(0.752)
- **Peak Frame:** 15 (value 0.0438)
- **Attention Entropy:** 3.2065
- **Inferred Reason:** Low confidence (borderline prediction); Near-equal class probabilities (ambiguous motion); High attention entropy (model uncertain which joints are informative); Flat temporal attention (no dominant movement phase); Subtle compensatory pattern (compensation resembles healthy motion)
