<div align="center">
  <img src="backend/assets/logo.jpeg" width="350" alt="Nava AI Logo" style="border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.2);" />

  # Nava AI
  ### The Next-Gen Autonomous Agent Platform

  <p align="center">
    <b>Build. Deploy. Automate.</b>
  </p>

  <!-- Badge Wall -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/React-18-20232A?style=flat-square&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/FastAPI-High%20Performance-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License" />
  </p>

  <p align="center">
    <i>A robust full-stack solution bridging the gap between chat interfaces and real-world task automation.</i>
  </p>
</div>

<br>

## 🚀 Why Nava AI?

**Nava AI** isn't just another chatbot. It's a configured **agentic runtime** that gives LLMs hands and eyes.

*   **⚡ Real-World Action**: Unlike standard chat, Nava can edit files, run Python code, and generate documents.
*   **🛡️ Secure Sandbox**: Every action happens in a controlled workspace, keeping your host system safe.
*   **🧠 Tool-Use First**: Built from the ground up for "Reasoning Models" (like GPT-4o and Claude 3.5) that plan before they act.

---

## ✨ Capabilities Grid

| **💻 Coding & Logic** | **🖼️ Creative Suite** | **⚡ Productivity** |
| :--- | :--- | :--- |
| **Python Sandbox**<br>Executes logic, math, and data analysis in real-time. | **Image Generation**<br>Creates stunning visuals on command. | **Web Search**<br>Tavily-powered deep research and answers. |
| **Jupyter Notebooks**<br>Auto-generates and runs notebooks for data science. | **Presentation**<br>Builds professional PPTX slide decks instantly. | **Doc Generator**<br>Compiles reports into PDF, DOCX, and Excel. |
| **File Ops**<br>Safe read/write access to a dedicated workspace. | **HTML Preview**<br>Live-renders generated web apps. | **Session Summary**<br>Auto-notes on what was accomplished. |

---

## 🧠 How it Works

Nava AI operates on a **Plan-Execute-Observe** loop, ensuring high reliability for complex tasks.

```mermaid
graph LR
    User[User Request] -->|WebSocket| Brain[Agent Core]
    
    subgraph "Reasoning Loop"
        Brain -->|1. Plan| Planner[Step-by-Step Plan]
        Planner -->|2. Select Tool| ToolBox
    end
    
    subgraph "Capabilities"
        ToolBox -->|Run Code| Python[Python Runtime]
        ToolBox -->|Search| Web[Tavily Search]
        ToolBox -->|Create| Files[File System]
    end
    
    Python -->|Output| Brain
    Web -->|Results| Brain
    Files -->|Content| Brain
    
    Brain -->|Final Response| UI[Web Interface]
```

---

## �️ Installation

Get up and running in minutes. We recommend **Python 3.12+** and **Node.js 18+**.

<details open>
<summary><b>1️⃣ Backend Setup (The Brain)</b></summary>

```bash
# Clone the repo
git clone https://github.com/shanmuka7482/Open-Manus
cd OpenManus/backend

# Create environment (Using uv is recommended for speed)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.12
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Configure API Keys
cp config/config.example.toml config/config.toml
# ⚠️ Edit config.toml: Insert your OpenAI/Anthropic and Tavily keys!

# Start Server
python start_server.py
```
</details>

<details>
<summary><b>2️⃣ Frontend Setup (The Interface)</b></summary>

```bash
# Open a new terminal
cd frontend

# Install & Config
npm install
echo "VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key" > .env

# Run Dev Server
npm run dev
```
</details>

<details>
<summary><b>3️⃣ Proxy Setup (The Bridge)</b></summary>

```bash
# Open a third terminal
cd frontend/server
npm install
node index.js
```
</details>

---

## 🎮 Usage Examples

Once running at `http://localhost:5173`, try these prompts to test Nava's full range:

#### 📊 Data Analysis
> *"Read `sales_data.csv` (I'll upload it), analyze the trends using Pandas, and plot a chart in a Jupyter Notebook."*

#### 📝 Research & Reporting
> *"Research the top 5 competitors to Spotify. Write a comprehensive comparison report and save it as `competitors.pdf`."*

#### 🎨 Creative Design
> *"Generate a slide deck for a startup pitch about 'AI for Cats'. Make it 5 slides long and use a professional theme."*

---

## 📦 Tech Stack

<div align="center">

| **Frontend** | **Backend** |
| :--- | :--- |
| ![React](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) | ![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white) | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) |
| ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) | ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white) |
| ![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white) | ![Tavily](https://img.shields.io/badge/Tavily_Search-FF0000?style=for-the-badge&logo=target&logoColor=white) |

</div>

---

## 🤝 Contributing

We welcome contributions! Please fork the repository and submit a Pull Request.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

<br>
<div align="center">
  <p>Made with ❤️ by the <b>Nava AI Team</b></p>
  <p><i>Built on top of <a href="https://github.com/mannaandpoem/OpenManus">OpenManus</a></i></p>
</div>
