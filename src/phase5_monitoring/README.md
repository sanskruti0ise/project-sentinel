# Project Sentinel: Phase 5 - MLOps and Production Monitoring

## 1. Introduction
Phase 5 is the final and most critical stage of Project Sentinel, elevating it from an interactive application to a production-ready, enterprise-grade system.  
This phase focuses on **MLOps (Machine Learning Operations)**, which encompasses the practices for deploying, governing, and maintaining AI systems reliably and efficiently.

The primary goal is to demonstrate the ability to build not just a model, but a **complete, automated lifecycle** around it, ensuring quality, consistency, and long-term viability.

---

## 2. Architecture Overview
This phase introduces three core MLOps components that work together to automate the path to production and provide visibility into the system's health post-deployment.

- **Containerization (Docker):** Package the FastAPI application into a lightweight, portable Docker container to ensure consistent environments across dev, staging, and prod.
- **CI/CD Pipeline (GitHub Actions):** Automate build and test workflows on every push, and build Docker images only if checks pass.
- **Production Monitoring (Streamlit Dashboard):** Simulate real-time monitoring of deployed models—tracking drift, fraud detection rates, and API performance.

---

## 3. Implementation Details

### 3.1. Containerization (`Dockerfile`)
The Dockerfile provides a recipe for building the application container image:

1. **Base Image:** Starts from official `python:3.10-slim`.
2. **Dependency Management:** Copies `requirements.txt` and installs all dependencies.
3. **Code Packaging:** Copies project source code into the container.
4. **Execution:** Runs `uvicorn` to serve FastAPI on port 8000.

---

### 3.2. CI/CD Pipeline (`.github/workflows/ci.yml`)
The GitHub Actions workflow automates builds and tests:

- **Trigger:** Runs on every push/pull request to `master`.
- **Build & Test:**
  - Checks out code
  - Sets up Python 3.10
  - Installs dependencies
  - Runs `ruff check .` (linting & style checks)
- **Docker Build & Push:**
  - Runs only if build/tests succeed
  - Logs into GitHub Container Registry
  - Builds Docker image and pushes it with commit ID tag

---

### 3.3. Monitoring Dashboard (`src/phase5_monitoring/dashboard.py`)
A **Streamlit dashboard** simulates production monitoring:

- **Data Drift:** Compares new transaction `Amount` distributions to training data.
- **Live Fraud Rate:** Tracks percentage of flagged fraudulent transactions.
- **API Latency:** Simulates response times for API health monitoring.

---

## 4. How to Run and Showcase

### Run the Containerized App
```bash
# Build the image
docker build -t project-sentinel .

# Run the container
docker run -p 8000:8000 project-sentinel
```

### Trigger the CI/CD Pipeline
Commit and push to the `master` branch.  
View results under the **Actions** tab in GitHub.

### View the Monitoring Dashboard
```bash
streamlit run src/phase5_monitoring/dashboard.py
```

---

## 5. Conclusion
Phase 5 demonstrates **modern MLOps principles**:  

- Containerization for portability  
- CI/CD pipelines for automated quality gates and builds  
- Monitoring dashboards for visibility and reliability  

With these, Project Sentinel evolves into a **production-ready AI system**, robust and maintainable for real-world deployment.