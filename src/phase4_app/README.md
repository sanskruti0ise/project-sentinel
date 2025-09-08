# Project Sentinel: Phase 4 - API and Frontend Integration

## 1. Objective
The primary goal of Phase 4 was to **productionize the LangGraph workflow** built in Phase 3.  
We moved the system from a command-line script to a fully interactive **client-server application**, making it accessible and usable for non-technical users.  

This phase demonstrates the ability to **build and serve a complete, end-to-end AI-powered application**.

---

## 2. Architecture
To achieve this, we implemented a **decoupled, two-part architecture**:

- **Backend API Server**: Built with **FastAPI**, loads and serves the compiled LangGraph workflow. Exposes a single endpoint for risk assessment.  
- **Frontend Web Application**: Built with **Streamlit**, providing a user-friendly interface to input transaction data and interact with the backend API.  

This **client-server model** is a standard, scalable pattern for deploying modern AI-powered web applications.

### Client-Server Architecture Diagram
```mermaid
graph TD
    A[Frontend UI <br> (Streamlit)] -- HTTP Request (JSON) --> B[Backend API <br> (FastAPI)];
    B -- Invokes --> C[LangGraph Workflow];
    C -- Returns Result --> B;
    B -- HTTP Response (JSON) --> A;
    C -- Uses --> D[ML Model <br> (XGBoost)];
```

---

## 3. Key Components & Implementation

### 3.1. Backend: FastAPI (`src/phase4_app/api.py`)
- **API Framework**: FastAPI chosen for high performance, auto-generated docs (Swagger UI), and modern Python support.  
- **Workflow Integration**: API imports `get_graph_app` from Phase 3 to load the LangGraph workflow on startup.  
- **Endpoint**: Single POST endpoint `/assess-transaction`, accepts `transaction_details` in JSON.  
- **Data Validation**: FastAPI validates requests automatically.  
- **Response**: Runs LangGraph → waits for final state → returns JSON with:
  - `final_recommendation`
  - Full workflow state

### 3.2. Frontend: Streamlit (`src/phase4_app/ui.py`)
- **UI Framework**: Streamlit enabled rapid UI development without manual HTML/CSS/JS.  
- **User-Friendly Input**: Fields for **Time** and **Amount** instead of long, error-prone strings.  
- **State Management**: `st.session_state` provides smooth UX, enabling example buttons ("Load Fraud Example," "Load Legitimate Example").  
- **API Communication**: On "Assess Transaction," the frontend sends an HTTP POST request to FastAPI backend.  
- **Dynamic Results**: Displays:
  - **Green** → Approved
  - **Red** → Blocked  
  An expandable section shows raw JSON output for transparency.

---

## 4. How to Run
The application requires two processes running in separate terminals:

### Start the Backend
```bash
# In terminal 1, from the project root
python src/phase4_app/api.py
```

### Start the Frontend
```bash
# In terminal 2, from the project root
streamlit run src/phase4_app/ui.py
```

---

## 5. Achievements
- **Operational AI System**: Productionized workflow into a functional, real-time service.  
- **Improved Usability**: Intuitive graphical interface makes AI accessible to all users.  
- **Full-Stack Skills**: Covered backend (API, model serving) and frontend (UI, state management).  
- **Modular & Scalable**: Decoupled architecture allows independent scaling and maintenance of backend and frontend.  
