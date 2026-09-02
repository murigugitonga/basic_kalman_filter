# Air-Gapped Real-Time 1D Kalman Filter Simulation

An ultra-fast, zero-dependency virtualization dashboard built with Python 3.12, **FastAPI**, **WebSockets**, and the **uv** package manager. The frontend utilizes responsive **Native SVG vectors** to enable real-time charting in network-restricted, firewalled development environments like GitHub Codespaces.

---

## 💡 What is a Kalman Filter?

A **Kalman Filter** is an optimal recursive mathematical algorithm that estimates the true, hidden state of a dynamic system from a series of incomplete and noisy measurements. 

Instead of looking at data as isolated snapshots, the filter combines the **laws of physics (a predictive model)** with **sensor readings (measurement updates)**. It continuously balances both inputs based on their statistical uncertainties to find the mathematical ground truth.

### The Dynamic Loop
The algorithm operates indefinitely in a two-step cycle:
1. **Predict:** Projects the system state and uncertainty covariance forward in time using physical laws (e.g., position = previous position + velocity $	imes$ time).
2. **Update:** Accepts a new sensor reading, computes the **Kalman Gain ($K$)** to determine which data source is more trustworthy and updates the state estimate.

$$	ext{Kalman Gain } (K) = rac{	ext{Model Error}}{	ext{Model Error} + 	ext{Sensor Error}}$$

* If the sensor is highly noisy, $K$ drops close to $0$, and the filter trusts the physical model rules.
* If the physical model is highly uncertain, $K$ climbs close to $1$, and the filter trusts the new sensor data.

---

## 🏃‍♂️ What This Simulation Does

This application virtualizes a vehicle moving at a constant baseline target position of **100 meters**.

* **The Reality (Blue Line):** The absolute true position of the vehicle. It includes a minor random walk variance ($\sigma = 0.2$) to simulate minor environmental impacts (like wind resistance or track micro-shifts).
* **The Sensor (Red Line):** Simulates a noisy tracker (like a low-cost GPS unit). It adds heavy Gaussian noise ($\sigma = 5.0$), causing the raw telemetry data to bounce erratically between 80m and 120m.
* **The Filter (Green Line):** The Kalman algorithm tracking the sensor. We initialize the filter with a bad guess (**80m** position estimate with a high error variance of **100**). Within milliseconds, the filter recognizes that the red sensor data is swinging wildly while the physical state remains steady. It quickly converges, filters out the spikes and tracks the blue true position smoothly.

---

## 🛠️ Local Development Quickstart

This project is fully managed under the `uv` toolchain.

### 1. Initialize Context & Dependencies
```bash
# Initialize venv and sync dependencies
uv sync
```

### 2. Boot Up the Production Reloader Server
```bash
uv run uvicorn main:app --reload
```
Open your local forwarding terminal port to view the live dashboard.

---

## 🐳 Docker Production Setup
The project uses a structured multi-stage Docker build matching the native `uv` format:
```dockerfile
FROM ghcr.io/astral-sh/uv:python3.11-alpine
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY main.py index.html ./
EXPOSE 10000
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
```
