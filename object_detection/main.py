from ultralytics import YOLO

print("================================")
model = YOLO('yolov8x.pt')

results = model.predict(source="0", show=True, stream=True)

for i in range(10000):
    next(results)
    input()