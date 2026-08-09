"""
Generate a synthetic IntelliRehabDS .txt file for pipeline testing.
Format: FrameID,ExerciseType,SubjectID,JointData...
Each joint: (JointName),x,y,z,qx,qy,qz,qw
"""
import os
import numpy as np

# IntelliRehab 25 joints in order
JOINTS = [
    'SpineBase','SpineMid','Neck','Head',
    'ShoulderLeft','ElbowLeft','WristLeft','HandLeft',
    'ShoulderRight','ElbowRight','WristRight','HandRight',
    'HipLeft','KneeLeft','AnkleLeft','FootLeft',
    'HipRight','KneeRight','AnkleRight','FootRight',
    'SpineShoulder','HandTipLeft','ThumbLeft','HandTipRight','ThumbRight'
]

# Reference T-pose positions (in meters, approximate)
T_POSE = {
    'SpineBase':     [0.00, 0.00, 0.00],
    'SpineMid':      [0.00, 0.25, 0.00],
    'Neck':          [0.00, 0.50, 0.00],
    'Head':          [0.00, 0.65, 0.00],
    'ShoulderLeft':  [-0.20, 0.48, 0.00],
    'ElbowLeft':     [-0.40, 0.30, 0.00],
    'WristLeft':     [-0.55, 0.10, 0.00],
    'HandLeft':      [-0.60, 0.05, 0.00],
    'ShoulderRight': [0.20, 0.48, 0.00],
    'ElbowRight':    [0.40, 0.30, 0.00],
    'WristRight':    [0.55, 0.10, 0.00],
    'HandRight':     [0.60, 0.05, 0.00],
    'HipLeft':       [-0.10, -0.02, 0.00],
    'KneeLeft':      [-0.10, -0.30, 0.00],
    'AnkleLeft':     [-0.10, -0.60, 0.00],
    'FootLeft':      [-0.10, -0.65, 0.08],
    'HipRight':      [0.10, -0.02, 0.00],
    'KneeRight':     [0.10, -0.30, 0.00],
    'AnkleRight':    [0.10, -0.60, 0.00],
    'FootRight':     [0.10, -0.65, 0.08],
    'SpineShoulder': [0.00, 0.48, 0.00],
    'HandTipLeft':   [-0.63, 0.00, 0.00],
    'ThumbLeft':     [-0.60, 0.08, 0.00],
    'HandTipRight':  [0.63, 0.00, 0.00],
    'ThumbRight':    [0.60, 0.08, 0.00],
}

def generate_sample_file(output_path, subject_id="101", gesture="0", repetition="1", 
                          correct="1", position="stand", num_frames=80):
    """Generate a synthetic IntelliRehabDS skeleton file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        for frame_id in range(num_frames):
            t = frame_id / num_frames  # 0 to 1
            # Simulate a simple stand-up movement (sine wave on knee angle)
            row_parts = [str(frame_id), position, subject_id]
            
            joint_parts = []
            for joint_name in JOINTS:
                base = T_POSE[joint_name].copy()
                # Add slight oscillation to simulate movement
                noise = np.random.normal(0, 0.005, 3)
                if 'Knee' in joint_name:
                    base[1] += 0.1 * np.sin(2 * np.pi * t)  # knee flex
                if 'Elbow' in joint_name:
                    base[0] += 0.05 * np.cos(2 * np.pi * t)  # elbow swing
                
                x, y, z = base[0] + noise[0], base[1] + noise[1], base[2] + noise[2]
                # Format: (JointName),TrackingState,x,y,z,qx,qy,qz,qw
                joint_str = f"({joint_name}),2,{x:.6f},{y:.6f},{z:.6f},0.0,0.0,0.0,1.0"
                joint_parts.append(joint_str)
            
            row_parts.append(','.join(joint_parts))
            f.write(','.join(row_parts) + '\n')
    
    print(f"Generated: {output_path} ({num_frames} frames)")
    return output_path

if __name__ == '__main__':
    rawdata_dir = "SkeletonData/SkeletonData/RawData"
    
    # Generate healthy trial (correct=1 -> label=0 Healthy)
    healthy_path = generate_sample_file(
        f"{rawdata_dir}/101_18_0_1_1_stand.txt",
        subject_id="101", correct="1", num_frames=80
    )
    
    # Generate compensated trial (correct=2 -> label=1 Compensated)
    comp_path = generate_sample_file(
        f"{rawdata_dir}/101_18_0_2_2_stand.txt",
        subject_id="101", correct="2", num_frames=80
    )
    
    # Generate more subjects for LOSO
    for subj in ["102", "103"]:
        for trial_num, correct in enumerate(["1", "2"], 1):
            generate_sample_file(
                f"{rawdata_dir}/{subj}_18_0_{trial_num}_{correct}_stand.txt",
                subject_id=subj, correct=correct, num_frames=80
            )
    
    print(f"\n✅ Synthetic dataset generated in: {rawdata_dir}")
    print("These files simulate real IntelliRehabDS format for pipeline testing.")
