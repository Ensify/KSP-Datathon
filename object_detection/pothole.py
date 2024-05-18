from inference import InferencePipeline
from dotenv import load_dotenv
from typing import Union, List, Optional
from inference.core.interfaces.camera.entities import VideoFrame
import os
import cv2
import supervision as sv
load_dotenv()

annotator =  sv.BoundingBoxAnnotator()
labelannotator = sv.LabelAnnotator()

def on_prediction(
    predictions: Union[dict, List[Optional[dict]]],
    video_frame: Union[VideoFrame, List[Optional[VideoFrame]]],
) -> None:
    image = video_frame.image
    labels = [p["class"] for p in predictions["predictions"]]
    detections = sv.Detections.from_inference(predictions)
    image = labelannotator.annotate(
            scene=video_frame.image.copy(), detections=detections, labels= labels
        )
    image = annotator.annotate(
        scene=image.copy(), detections=detections
    )
    print(image)
    cv2.imwrite("test.png", image)

# initialize a pipeline objectq
pipeline = InferencePipeline.init(
    model_id="pothole-detection-i00zy/2", # Roboflow model to use
    video_reference="test_data\mixkit-potholes-in-a-rural-road-25208-large.mp4", # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=on_prediction, # Function to run after each prediction
    api_key= os.environ.get('API_KEY')
)

pipeline.start()
pipeline.join()
