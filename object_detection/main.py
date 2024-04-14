from ultralytics import YOLO

print("================================")
model = YOLO(r"models\yolov8x.pt")

results = model.track(source=r"test_data\Traffic Flow Optiomization and Congestion Management\Problem Statement - 3\Nr_ABVMCRI_Gate_FIX_1.mp4",persist=True, show=True)


#['orig_img', 'orig_shape', 'boxes', 'masks', 'probs', 'keypoints', 'obb', 'speed', 'names', 'path', 'save_dir', '_keys']