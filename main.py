import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()

class KalmanFilter1D:
    def __init__(self, process_variance, measurement_variance, initial_estimate, initial_error):
        self.Q = process_variance      
        self.R = measurement_variance  
        self.x = initial_estimate      
        self.P = initial_error         

    def update(self, measurement):
        K = (self.P + self.Q) / (self.P + self.Q + self.R)
        self.x = self.x + K * (measurement - self.x)
        self.P = (1 - K) * (self.P + self.Q)
        return self.x

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    true_value = 100.0
    kf = KalmanFilter1D(process_variance=0.1, measurement_variance=25.0, initial_estimate=80.0, initial_error=100.0)
    step = 0
    try:
        while True:
            step += 1
            true_value += random.normalvariate(0, 0.2)
            measurement = true_value + random.normalvariate(0, 5.0)
            estimate = kf.update(measurement)
            
            await websocket.send_json({
                "step": step,
                "true": true_value,
                "measured": measurement,
                "estimated": estimate
            })
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print(f"Connection dropped at step {step}")
