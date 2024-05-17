from inference import InferencePipeline
from dotenv import load_dotenv
import os
load_dotenv()

# Import the built in render_boxes sink for visualizing results
from inference.core.interfaces.stream.sinks import render_boxes
# initialize a pipeline objectq
pipeline = InferencePipeline.init(
    model_id="pothole-detection-i00zy/2", # Roboflow model to use
    video_reference="test_data\mixkit-potholes-in-a-rural-road-25208-large.mp4", # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=render_boxes, # Function to run after each prediction
    api_key= os.environ.get('API_KEY')
)

pipeline.start()
pipeline.join()