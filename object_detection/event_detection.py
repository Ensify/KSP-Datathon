from ultralytics import YOLO
from datetime import datetime

TOLERANCE_INTERVAL = {
    'car': 10 * 60,
    'auto': 5 * 60,
    'pothole': 10
}

DISPLACEMENT_TOLERANCE = 10

UPDATE_INTERVAL = 100

class Detector:
    def __init__(self, model, node_id):
        self.model = YOLO(model)
        self.node_id = node_id
        self.object_states = {}

    def main_loop(self, video):
        self.results = self.model.track(source=video, stream=True, show = True)
        i = 0
        for result in self.results:
            boxes = result.boxes
            ids = boxes.id
            cls = boxes.cls
            xyxy = boxes.xyxy
            
            for idx, id in enumerate(ids):
                id = int(id.item())
                class_name = result.names[int(cls[idx].item())]
                if id in self.object_states:
                    if self.time_detla(id) > TOLERANCE_INTERVAL.get(class_name, 10):
                        mid = self.get_center_from_xyxy(xyxy[idx].numpy())
                        if self.distance_detla(self.object_states[id]['mid'], mid) < DISPLACEMENT_TOLERANCE:
                            self.raise_event(class_name, self.object_states[id]['begin_time'], datetime.now())
                        self.object_states[id]['mid'] = mid


                else:
                    self.object_states[id] = {
                        'cls': (result.names[int(cls[idx].item())]),
                        'mid': self.get_center_from_xyxy(xyxy[idx].numpy()),
                        'begin_time': datetime.now()
                    }
            if i % UPDATE_INTERVAL == 0:
                state = {}
                for c in cls:
                    c = result.names[int(c.item())]
                    state[c] = state.get(c, 0) + 1
                
                self.update_instance_state(state)
            i += 1

    def time_detla(self, id):
        val = (datetime.now() - self.object_states[id]['begin_time']).total_seconds()
        return val
    
    def distance_detla(self, mid1, mid2):
        x1 = mid1[0]
        y1 = mid1[1]
        x2 = mid2[0]
        y2 = mid2[1]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    
    def get_center_from_xyxy(self, xyxy):
        x_mid = (xyxy[0] + xyxy[2]) / 2
        y_mid = (xyxy[1] + xyxy[3]) / 2
        return (x_mid, y_mid)

    def raise_event(self, class_name, start, end):
        print('raise event')

    def update_instance_state(self, state):
        print(state)


if __name__ == '__main__':
    detector = Detector(model=r"models\last.pt", node_id= 1)
    detector.main_loop(video=r'test_data\Traffic Flow Optiomization and Congestion Management\Problem Statement - 3\Russel_Market_Entrance_PTZ_1.mp4')
