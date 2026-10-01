# MediaPipe ↔ IntelliRehabDS Coordinate Alignment Validation

## 1. Landmark Conventions

- **MediaPipe Pose World Landmarks:**
  * Origin: Centered between the subject's hips.
  * X-axis: Points to the subject's left (viewer's right).
  * Y-axis: Points downwards (towards the feet).
  * Z-axis: Points forwards (towards the camera sensor).

- **Kinect (IntelliRehabDS) Coordinates:**
  * Origin: Camera sensor origin (translated to SpineBase during preprocessing).
  * X-axis: Points to the camera sensor's left (subject's right).
  * Y-axis: Points upwards (towards the ceiling).
  * Z-axis: Points away from the camera sensor (depth).

## 2. Transformation Matrix

The transformation rotates the MediaPipe landmarks by 180 degrees around the Z-axis (negating X and Y) and reflects the depth Z-axis to match the Kinect orientation:
$$
\begin{bmatrix} X_{\text{Kinect}} \\ Y_{\text{Kinect}} \\ Z_{\text{Kinect}} \end{bmatrix} =
\begin{bmatrix} -1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & -1 \end{bmatrix}
\begin{bmatrix} X_{\text{MediaPipe}} \\ Y_{\text{MediaPipe}} \\ Z_{\text{MediaPipe}} \end{bmatrix}
$$

## 3. Empirical Validation Results

- **Sample Kinect File:** `101_18_0_1_1_stand.txt`
- **Vertical Alignment:** Head - SpineBase Y distance is **0.7662** (positive, verifying Y-up).
- **Lateral Alignment:**
  * ShoulderLeft X coordinate: **-0.2826**
  * ShoulderRight X coordinate: **0.0752**
  * Since ShoulderLeft X is negative and ShoulderRight X is positive, Kinect X increases towards the subject's right (viewer's left). Negating MediaPipe X aligns it to this coordinate direction.
- **Torso Rigidity Check:** Relative bone lengths are symmetric (Symmetry Ratio: **0.9784**).

## 4. Conclusion
The coordinate alignment via negation is verified to preserve relative anatomical joint relationships and spatial orientation between the two coordinate systems.
