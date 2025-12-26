<div align="center">
  <img src="backend/assets/logo.jpeg" width="180" alt="Nava AI Logo" style="border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);" />

  # Nava AI
  ### The Next-Gen AI Agent Platform

  <p align="center">
    <b>Build. Deploy. Automate.</b><br>
    A full-stack solution for creating intelligent, autonomous agents with a premium web interface.
  </p>
</div>

---

## ⚡ Overview

**Nava AI** bridges the gap between powerful Python-based AI logic and modern React frontends. It is designed for developers who need a production-ready environment for:
*   **Conversational Agents** that can see, hear, and act.
*   **Task Automation** spanning file systems, browsers, and APIs.
*   **Interactive AI Experiences** with real-time feedback and visualization.

---

## ✨ Key Features

| **Core Capabilities** | **Frontend Experience** | **Backend Power** |
| :--- | :--- | :--- |
| 🧠 **Multi-Tool Agents**<br>Python execution, web browsing, file editing | 🎨 **Modern UI**<br>React 18 + TypeScript + Tailwind CSS | 🚀 **FastAPI Server**<br>High-performance async architecture |
| 🛠️ **Sandbox Environment**<br>Safe, real-time code execution | 🌓 **Theming**<br>Dark/Light mode support | 🔌 **MCP Support**<br>Model Context Protocol integration |
| 🗣️ **Human-in-the-Loop**<br>Interactive user input & feedback | 📄 **Smart Viewers**<br>Live preview for HTML, Images, & Code | 🤖 **LLM Flexibility**<br>OpenAI, Azure, Bedrock, & more |
| 📂 **Workspace Manager**<br>Full file system control | 🔐 **Secure Auth**<br>Integrated Clerk authentication | 🕷️ **Browser Automation**<br>Headless Playwright control |

---

## 🏗️ Architecture

Nava AI uses a clean, separated architecture to ensure scalability and maintainability.

```mermaid
graph LR
    User[Web Interface] <-->|WebSocket| Proxy[Node.js Proxy]
    Proxy <-->|WebSocket| API[FastAPI Backend]
    API <--> Agent[Nava Agent]
    Agent <--> Tools[Tools]
    Tools -->|Execute| Sandbox[Sandbox Environment]
```

#### Directory Structure
*   `frontend/` - **React Application** (Vite, Radix UI)
*   `backend/` - **Python Environment** (FastAPI, LangChain)
*   `backend/workspace/` - **Sandboxed Area** for agent outputs

---

## 🚀 Quick Start Guide

### 1. Backend Setup (The Brain)

```bash
# Clone the repo
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus/backend

# Create environment (Python 3.12+)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install

# Configure
cp config/config.example.toml config/config.toml
# (Add your API keys to config.toml)

# Start Server
python start_server.py
```

### 2. Frontend Setup (The Face)

```bash
# In a new terminal
cd frontend

# Install & Configure
npm install
echo "VITE_CLERK_PUBLISHABLE_KEY=your_key_here" > .env

# Start UI
npm run dev
```

### 3. Proxy Setup (The Bridge)

```bash
# In a third terminal
cd frontend/server
npm install
node index.js
```

---

## 🎮 How to Use

1.  Open **`http://localhost:5173`** in your browser.
2.  **Login** to access your secure workspace.
3.  Go to the **Sandbox** and start typing!

### Example Prompts
> *"Create a snake game in Python and save it as game.py"*

> *"Research the latest AI trends and generate a summary report in Markdown"*

> *"Ask me for my budget, then create a travel itinerary for Japan"*

---

## � Tech Stack

<div align="center">

| **Frontend** | **Backend** |
| :--- | :--- |
| ![React](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) | ![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white) | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) |
| ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) | ![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=Playwright&logoColor=white) |
| ![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white) | ![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white) |

</div>

---

## 🤝 Contributing

We love builders! To contribute:
1.  Fork the repo
2.  Create your feature branch (`git checkout -b feature/AmazingThing`)
3.  Commit changes (`git commit -m 'Add AmazingThing'`)
4.  Push to branch (`git push origin feature/AmazingThing`)
5.  Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

<br>
<div align="center">
  <p>Made with ❤️ by the <b>Nava AI Team</b></p>
</div>
