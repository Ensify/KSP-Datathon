# Import required libraries
import cv2
import streamlit as st
from PIL import Image
from ultralytics import YOLO
from graph import infer, load_model, build_representation
from datetime import datetime, timedelta

model_path = 'weights/traffic_model.pt'


initial_values = [
    "128,254,234,23,123,44,55,434,230",
    "150,234,344,53,163,74,75,422,235",
    "133,244,344,63,163,64,65,446,221",
    "148,215,304,33,143,34,75,426,245",
    "125,234,314,23,173,34,25,406,250",
]
# Setting page layout
st.set_page_config(
    page_title="KSP Traffic Flow",  # Setting page title
    page_icon="🚗",     # Setting page icon
    layout="wide",      # Setting layout to wide
    initial_sidebar_state="expanded"    # Expanding sidebar by default
)

tab1, tab2 = st.tabs(["Vehicle and congestion detection", "Traffic Prediction"])

with tab1:
    # Creating sidebar
    with st.sidebar:
        st.header("Image/Video Config")     # Adding header to sidebar
        # Adding file uploader to sidebar for selecting images
        source_img = st.sidebar.file_uploader(
            "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
        source_vid = st.sidebar.file_uploader(
            "Choose a video...", type=("mp4"))
        sample_detection = st.sidebar.button("Detect Objects from sample video", "sample_detection")
        detect_btn = st.sidebar.button("Detect Objects")
    # Creating main page heading
    st.title("Traffic Flow Vechile Detection")
    st.write("Upload Images to get started")

    # Creating two columns on the main page
    col1, col2 = st.columns(2)

    # Adding image to the first column if image is uploaded
    with col1:
        if source_img:
            # Opening the uploaded image
            uploaded_image = Image.open(source_img)
            # Adding the uploaded image to the page with a caption
            st.image(source_img,
                    caption="Uploaded Image",
                    use_column_width=True
                    )

    try:
        model = YOLO(model_path)
    except Exception as ex:
        st.error(
            f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)

    if detect_btn and source_img!=None and uploaded_image!=None:
        res = model.predict(uploaded_image, conf = 0.6)
        boxes = res[0].boxes
        res_plotted = res[0].plot()[:, :, ::-1]
        with col2:
            st.image(res_plotted,
                    caption='Detected Image',
                    use_column_width=True
                    )
            try:
                with st.expander("Detection Results"):
                    for box in boxes:
                        st.write(box.xywh)
            except Exception as ex:
                st.write("No image is uploaded yet!")


    if source_vid is not None:
        with source_vid as video_file:
            video_bytes = video_file.read()
            with open("temp.mp4","wb") as f:
                f.write(video_bytes)
        if video_bytes:
            st.video(video_bytes)
        if detect_btn:
            vid_cap = cv2.VideoCapture("temp.mp4")
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    image = cv2.resize(image, (720, int(720*(9/16))))
                    res = model.predict(image, conf=0.6)
                    result_tensor = res[0].boxes
                    res_plotted = res[0].plot()
                    st_frame.image(res_plotted,
                                caption='Detected Video',
                                channels="BGR",
                                use_column_width=True
                                )
                else:
                    vid_cap.release()
                    break
    
    if sample_detection:
        with open("cut.mp4","rb") as video_file:
            video_bytes = video_file.read()
        if video_bytes:
            st.video(video_bytes)

        vid_cap = cv2.VideoCapture("cut.mp4")
        st_frame = st.empty()
        while (vid_cap.isOpened()):
            success, image = vid_cap.read()
            if success:
                image = cv2.resize(image, (720, int(720*(9/16))))
                res = model.predict(image, conf=0.6)
                result_tensor = res[0].boxes
                res_plotted = res[0].plot()
                st_frame.image(res_plotted,
                            caption='Detected Video',
                            channels="BGR",
                            use_column_width=True
                            )
            else:
                vid_cap.release()
                break


with tab2:
    st.title("Traffic Flow Prediction")
    st.write("The road network is represented as a graph with every point with cctv as a node. The model can predict traffic after 30 mins into the future given current traffic patterns.")
    st.title("Demo")
    input_date = st.date_input("Enter the date", "today")
    input_time = st.time_input("Enter the time", "now")
    vehicle_counts = [st.text_input(f"Vehicle count at current time {-i*5} mins for every node separated by commas (9 nodes)", initial_values[i]) for i in range(5)]
    if st.button("Predict Traffic", key="traffic predict"):
        st.write("Node wise Traffic Prediction")
        try:
            combined_datetime = datetime.combine(input_date, input_time)
            timestamps = [combined_datetime - timedelta(minutes=5 * i) for i in range(5)]
            results = []
            for i, timestamp in enumerate(timestamps):
                minute = timestamp.minute
                hour = timestamp.hour
                day_of_week = timestamp.weekday()
                day = timestamp.day
                month = timestamp.month
                features = [minute, hour, day_of_week, day, month]
                counts = list(map(int,vehicle_counts[i].split(',')))
                nodes = []
                for i in range(9):
                    nodes.append(features + [counts[i]])
                results.append(nodes)

            traffic_model = load_model(weights='weights/stgcn_model_final.pth', edges = "data/edges.csv")
            result = infer(traffic_model, results)
            st.write(result)

            st.image(build_representation(result, "data/edges.csv"))

        except Exception as e:
            raise(e)
            st.error(e)

    st.markdown("""
## Features
- Considers seasonal traffic
- Takes into account of peak hours
- Weekdays and monthly patterns are also considered by the model
- Gives predictions for every node
- Can perform online training to improve performance based on current traffic patterns
                
## Uses
- It is used to predict potential traffic congestion proactively
- Anomaly detection to compare predicted traffic with actual traffic to detect unusual traffic due to accident or congestion.

### Note
- This is trained and tested on dummy data. The model is verified to capture cyclic traffic patterns based on current traffic patterns and time. For accurate results real live data is needed.
""")