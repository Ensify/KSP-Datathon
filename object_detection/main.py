from ultralytics import YOLO

print("================================")
model = YOLO(r"models/main2.pt")

results = model.predict(source=r"test_data\Traffic Flow Optiomization and Congestion Management\Problem Statement - 3\Russel_Market_Entrance_PTZ_1.mp4", show=True, stream=True)

for i in range(1000):
    next(results)

#['orig_img', 'orig_shape', 'boxes', 'masks', 'probs', 'keypoints', 'obb', 'speed', 'names', 'path', 'save_dir', '_keys']