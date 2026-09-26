# 🚢 Odyssey: Intelligent Maritime Freight & Voyage Decision Platform
**Developed by Team 963Hz**

**Odyssey** is an enterprise-grade decision-support application engineered for the **Smart India Hackathon (SIH)**. It optimizes complex maritime chartering operations by converging real-time market data, predictive machine learning models, and dynamic scenario evaluation into a unified, actionable interface.

Designed to replace intuition-driven chartering with deterministic data science, Odyssey empowers chartering managers with algorithmic recommendations on whether to **Book Now, Wait, or Change Plans** based on freight rate forecasts, vessel compatibility constraints, and stringent delivery deadlines.

---

## ✨ Core Capabilities

1. **🚢 Voyage Parameterization**: Seamlessly define operational parameters including Origin, Destination, Commodity, Cargo Volume, Delivery Target, and Laycan windows.
2. **📈 Predictive Market Engine**: Powered by an underlying LightGBM machine learning model, Odyssey forecasts freight rates (USD/MT) across 7-day, 14-day, and 30-day horizons.
3. **⚖️ Decision Workspace**: Concurrently evaluates multiple strategic timing scenarios. It computes total projected costs (Freight, Bunker, Port, and Demurrage/Waiting), assesses risk coefficients, and validates strict delivery feasibility.
4. **🧑‍💻 Human-in-the-Loop Validation**: Presents the AI's mathematically optimized recommendation for human review, allowing managers to approve the system's choice or override it by modifying the vessel, port, or timing strategy.
5. **🧾 Final Voyage Blueprint**: Generates a comprehensive, finalized voyage receipt detailing the exhaustive cost breakdown, operational buffers, and validated routing.

---

## 🏗️ Technical & Backend Architecture

Odyssey is built upon a modern, decoupled, service-oriented architecture prioritizing scalability, low-latency machine learning inference, and maintainability.

### 1. Presentation Layer (Frontend)
- **Technology:** React 18, TypeScript, Vite, Tailwind CSS.
- **Architecture:** A highly responsive Single Page Application (SPA). It utilizes advanced context-based state management to seamlessly pass complex voyage evaluations across the 5-step chartering workflow without redundant API polling.

### 2. Application & API Layer (Backend)
- **Technology:** Python 3.10+, FastAPI, Uvicorn.
- **Architecture:** 
  - **Asynchronous Design:** Built on FastAPI to leverage asynchronous request handling (sync/wait), ensuring high throughput when processing complex datasets and ML inference requests simultaneously.
  - **Stateless REST API:** Exposes clean, stateless RESTful endpoints for dataset querying, user authentication, and scenario computation.
  - **Decoupled Business Logic:** Separation of concerns is maintained strictly between route handlers (
outers/), core business logic/services, and data access layers.

### 3. Predictive AI/ML Engine
- **Technology:** LightGBM, Scikit-Learn, Pandas, NumPy.
- **Architecture:** A specialized pipeline that processes historical Baltic indices, fluctuating bunker prices, and port congestion metrics. The models are pre-trained and serialized, allowing the backend to load them into memory on startup for sub-millisecond inference during live voyage evaluations.

### 4. Data & Persistence Layer
- **Technology:** SQLite, Pandas DataFrames.
- **Architecture:** Utilizes lightweight, highly-portable local databases (users.db, sih_database.db) optimized for read-heavy operations, alongside robust in-memory processing of massive maritime CSV/Excel datasets for rapid feasibility filtering.

---

## 📂 Project Structure

The repository is modularized into distinct foundational domains:

`	ext
SIH/
├── SIH-FRONTEND/       # React/Vite Presentation Layer
│   ├── src/            # Components, Pages, Context, and Utils
│   ├── scripts/        # UI maintenance and build scripts
│   └── package.json    # Node.js dependencies
│
├── SIH-BACKEND/        # FastAPI Application Layer
│   ├── app/            # API Routers, Auth, and Core Business Logic
│   ├── scripts/        # Backend test suites and DB initialization
│   ├── requirements.txt# Python dependencies
│   └── *.db            # SQLite Databases
│
├── SIH-AI-ML/          # Machine Learning Engine
│   └── ...             # Jupyter Notebooks, training pipelines, and models
│
├── DATASETS/           # Raw and Processed Maritime Data
│   └── ...             # PDFs, CSVs, Excel tables, and historical metrics
│
├── docs/               # Technical Documentation
│   └── report_out.md   # Hackathon reports and data dictionaries
│
└── README.md           # Project Documentation (You are here)
`

---

## 🚀 Local Deployment Guide

### Prerequisites
- **Node.js** (v18+ recommended)
- **Python** (v3.10+ recommended)

### 1. Initialize the Backend (FastAPI)
Open a terminal and navigate to the backend directory:
`ash
cd SIH-BACKEND

# Create and activate a Python virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Boot the ASGI server
uvicorn app.main:app --reload --port 8080
`
*The API will be available at http://localhost:8080 (Interactive Swagger Docs at http://localhost:8080/docs).*

### 2. Initialize the Frontend (React/Vite)
Open a new, separate terminal and navigate to the frontend directory:
`ash
cd SIH-FRONTEND

# Install NPM dependencies
npm install

# Start the Vite development server
npm run dev
`
*The application will be accessible at http://localhost:5173.*

---

*Engineered with precision for the Smart India Hackathon by Team 963Hz.*
