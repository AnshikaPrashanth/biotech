# MediaPipe Pose (33) to Kinect v2 / IntelliRehabDS (25) Joint Mapping Documentation

## 1. Coordinate System Mapping Rationale
- **MediaPipe Pose World Landmarks:** Right-handed camera coordinate frame:
  - $+X_{\text{MP}}$ points user-left (screen-right)
  - $+Y_{\text{MP}}$ points down (screen-down)
  - $+Z_{\text{MP}}$ points forward (towards camera relative to hip center)
- **Kinect v2 / IntelliRehabDS Coordinates:** Camera space:
  - $+X_{\text{Kinect}}$ points screen-left (user-right)
  - $+Y_{\text{Kinect}}$ points vertical UP (screen-up)
  - $+Z_{\text{Kinect}}$ points away from sensor (depth)

### Mathematical Coordinate Transformation
To align MediaPipe Pose world landmarks to Kinect coordinates without mirroring left/right extremities:

$$X_{\text{Kinect}} = X_{\text{MediaPipe}}, \quad Y_{\text{Kinect}} = -Y_{\text{MediaPipe}}, \quad Z_{\text{Kinect}} = -Z_{\text{MediaPipe}}$$

---

## 2. Joint Mapping Table (33 $\to$ 25 Joints)

| Kinect Joint Index | Joint Name | Derived from MediaPipe Landmark Index | Formulation / Method |
| :---: | :--- | :---: | :--- |
| `0` | **SpineBase** | 23 (HipLeft), 24 (HipRight) | $(\text{MP}_{23} + \text{MP}_{24}) / 2.0$ |
| `1` | **SpineMid** | 0 (SpineBase), 20 (SpineShoulder) | $(\text{SpineBase}_0 + \text{SpineShoulder}_{20}) / 2.0$ |
| `2` | **Neck** | 20 (SpineShoulder), 3 (Head) | $\text{SpineShoulder}_{20} + 0.3 \times (\text{Head}_3 - \text{SpineShoulder}_{20})$ |
| `3` | **Head** | 0 (Nose) | $\text{MP}_0$ |
| `4` | **ShoulderLeft** | 11 (ShoulderLeft) | $\text{MP}_{11}$ |
| `5` | **ElbowLeft** | 13 (ElbowLeft) | $\text{MP}_{13}$ |
| `6` | **WristLeft** | 15 (WristLeft) | $\text{MP}_{15}$ |
| `7` | **HandLeft** | 15 (Wrist), 19 (Index) | $(\text{MP}_{15} + \text{MP}_{19}) / 2.0$ *(Hand/Palm midpoint)* |
| `8` | **ShoulderRight** | 12 (ShoulderRight) | $\text{MP}_{12}$ |
| `9` | **ElbowRight** | 14 (ElbowRight) | $\text{MP}_{14}$ |
| `10` | **WristRight** | 16 (WristRight) | $\text{MP}_{16}$ |
| `11` | **HandRight** | 16 (Wrist), 20 (Index) | $(\text{MP}_{16} + \text{MP}_{20}) / 2.0$ *(Hand/Palm midpoint)* |
| `12` | **HipLeft** | 23 (HipLeft) | $\text{MP}_{23}$ |
| `13` | **KneeLeft** | 25 (KneeLeft) | $\text{MP}_{25}$ |
| `14` | **AnkleLeft** | 27 (AnkleLeft) | $\text{MP}_{27}$ |
| `15` | **FootLeft** | 31 (FootLeft / Heel) | $\text{MP}_{31}$ |
| `16` | **HipRight** | 24 (HipRight) | $\text{MP}_{24}$ |
| `17` | **KneeRight** | 26 (KneeRight) | $\text{MP}_{26}$ |
| `18` | **AnkleRight** | 28 (AnkleRight) | $\text{MP}_{28}$ |
| `19` | **FootRight** | 32 (FootRight / Heel) | $\text{MP}_{32}$ |
| `20` | **SpineShoulder** | 11 (ShoulderLeft), 12 (ShoulderRight) | $(\text{MP}_{11} + \text{MP}_{12}) / 2.0$ |
| `21` | **HandTipLeft** | 19 (IndexLeft) | $\text{MP}_{19}$ |
| `22` | **ThumbLeft** | 21 (ThumbLeft) | $\text{MP}_{21}$ |
| `23` | **HandTipRight** | 20 (IndexRight) | $\text{MP}_{20}$ |
| `24` | **ThumbRight** | 22 (ThumbRight) | $\text{MP}_{22}$ |

---

## 3. Verification & Non-Duplication
- **Hand vs. Wrist Distance:** By taking the midpoint between `Wrist` ($\text{MP}_{15}$) and `Index` ($\text{MP}_{19}$), $\text{HandLeft}$ is placed at the center of the palm, guaranteeing $dist(\text{Wrist}, \text{Hand}) > 0.0\text{m}$.
- **Anatomical Graph Compatibility:** The generated 25 3D joint coordinates strictly match the `INTELLIREHAB_JOINTS` schema and are fully compatible with `get_edge_index()` and `STGAT`.
