# KSP Datathon


## Modules and their description
1. Database: Consists of db schema and their handlers.
2. Mobile_app_Flutter
3. Monitoring: Continuous Monitoring and Alert
        1. Automated Alerting: Backend Python code continuously monitors traffic events, generating alerts if vehicles exceed designated waiting times at nodes.
        2. Real-time Display: JavaScript dynamically updates the frontend, displaying the latest alerts to users, facilitating quick response to traffic disruptions.
        3. Scheduled Execution: BackgroundScheduler manages periodic event checks, optimizing resource usage and maintaining timely alert generation.

4. Object Detection: ML model for detecting objects and raising event in case of parking time exceeds 15 mins.

5. Visualization: For Visualizing the map.


## How to run?

1. Make sure you have python and pip (Package manager for python) installed.
   
2. Clone the repository using 
   
   ```
   git clone 
   ```
3. Install the requirements
   
   ```
   pip install -r requirements.txt
   ```

4. To run main the main website (if you get "python not found" error, use python3 instead)
   
   ```
   python monitoring/app.py
   ```
5. The app will be launched in port 5000

## Website link

The site is currently up on render. Can be accessed using the links below

1. Website:
        `https://codeone-ksp-traffic-monitoring-site.onrender.com/report`

2. ML Model testing:


3. Mobile application:
        Headover to releases page by simply linking the below link where you can find the road-report.apk which you can download and can be used to report traffic.

`https://github.com/Ensify/KSP-Datathon/releases/download/V1.0/road-report.apk`

