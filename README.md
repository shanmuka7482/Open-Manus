# 🤖 OpenManus - Full Stack AI Agent Platform

<p align="center">
  <img src="backend/assets/logo.jpg" width="200" alt="OpenManus Logo"/>
</p>

<p align="center">
  <a href="https://github.com/mannaandpoem/OpenManus/stargazers"><img src="https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social" alt="GitHub stars"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
  <a href="https://discord.gg/DYn29wFk9z"><img src="https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat" alt="Discord"/></a>
</p>

> **A powerful full-stack platform for building and deploying AI agents with a modern web interface**

OpenManus combines a robust Python backend with a sleek React frontend to provide a complete solution for creating, managing, and interacting with AI agents. Whether you're building conversational agents, automating tasks, or creating interactive AI experiences, OpenManus provides the tools you need.

---

## ✨ Features

### 🎯 Core Capabilities
- **Interactive Sandbox Environment** - Real-time agent execution with live log streaming
- **Multi-Tool Agent System** - Python execution, browser automation, file editing, and more
- **User Input Tool** - Dynamic question-answer flow during agent execution
- **File Workspace Management** - Generate and view code, images, HTML with preview
- **WebSocket Communication** - Real-time bidirectional communication between frontend and backend
- **LLM Model Flexibility** - Support for OpenAI, Azure, AWS Bedrock, and custom models

### 🎨 Frontend Features
- **Modern React UI** - Built with TypeScript, Vite, and Tailwind CSS
- **Authentication** - Clerk-based user authentication
- **Code Viewer** - View generated files with syntax highlighting
- **HTML Preview** - Live preview for HTML files
- **Image Display** - Native rendering for PNG, JPG, and other image formats
- **Responsive Design** - Works seamlessly on desktop and mobile
- **Dark/Light Theme** - Support for theme switching

### 🔧 Backend Features
- **FastAPI Server** - High-performance async API
- **Agent Framework** - Modular tool-based agent architecture
- **Tool Collection** - Extensible system with built-in tools
- **Logging System** - Comprehensive logging with structured output
- **MCP Support** - Model Context Protocol integration
- **Browser Automation** - Powered by Playwright

---

## 🏗️ Architecture

```
OpenManus/
├── frontend/          # React + TypeScript frontend
│   ├── components/    # React components
│   ├── public/        # Static assets
│   └── server/        # Node.js WebSocket proxy
│
├── backend/           # Python FastAPI backend
│   ├── app/          # Core application
│   │   ├── agent/    # Agent implementations
│   │   ├── tool/     # Tool implementations
│   │   ├── prompt/   # System prompts
│   │   └── ...
│   ├── config/       # Configuration files
│   ├── workspace/    # Agent workspace
│   └── api.py        # Main API server
│
└── README.md         # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.11-3.13
- **Node.js**: 18+ (for frontend)
- **Git**: For cloning the repository

### Installation

#### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mannaandpoem/OpenManus.git
   cd OpenManus/backend
   ```

2. **Create virtual environment** (Recommended: using `uv`)
   ```bash
   # Using uv (faster)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv --python 3.12
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt

   # OR using conda
   conda create -n open_manus python=3.12
   conda activate open_manus
   pip install -r requirements.txt
   ```

3. **Install browser automation** (Optional but recommended)
   ```bash
   playwright install
   ```

4. **Configure API keys**
   ```bash
   cp config/config.example.toml config/config.toml
   # Edit config/config.toml with your API keys
   ```

5. **Start the backend server**

   **For Windows users** (to enable browser automation):
   ```bash
   python start_server.py
   ```

   **For Linux/macOS or non-browser usage**:
   ```bash
   python api.py
   # Or with uvicorn directly:
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

   Backend will run on `http://localhost:8000`

   > **Note for Windows**: The `start_server.py` script sets the proper asyncio event loop policy before starting uvicorn, which is required for Playwright browser automation to work correctly when using the web UI.

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file with your Clerk credentials
   echo "VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key" > .env
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

5. **Start the WebSocket proxy** (in a separate terminal)
   ```bash
   cd server
   npm install
   node index.js
   ```
   Proxy will run on `http://localhost:5000`

---

## ⚙️ Configuration

### Backend Configuration (`backend/config/config.toml`)

```toml
# LLM Configuration
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."
max_tokens = 4096
temperature = 0.0

# Vision Model (Optional)
[llm.vision]
model = "gpt-4o"
api_key = "sk-..."

# Browser Configuration
[browser]
headless = true
```

### Frontend Configuration (`.env`)

```env
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
```

---

## 🎮 Usage

### Using the Sandbox

1. **Access the application** at `http://localhost:5173`
2. **Sign in** using Clerk authentication
3. **Navigate to Sandbox** from the sidebar
4. **Enter your prompt**, for example:
   ```
   Create a simple calculator webpage with HTML, CSS and JavaScript
   ```
5. **Watch the agent work** in real-time with live logs
6. **View generated files** in the right panel
7. **Preview HTML files** using the preview button

### Interactive Agent Example

Try this prompt to see the user input feature:
```
Ask me for my favorite color, wait for my answer, and then write a poem about it.
```

The agent will:
1. Ask you for your favorite color
2. Wait for your response
3. Generate a custom poem based on your answer

### Command Line Usage

For terminal-based interaction:
```bash
cd backend
python main.py
```

---

## 🛠️ Available Tools

The Manus agent comes with several built-in tools:

- **`python_execute`** - Execute Python code in a sandboxed environment
- **`browser_use`** - Automate browser interactions using Playwright
- **`str_replace_editor`** - Edit files with search and replace
- **`generate_image`** - Generate images using Clipdrop API
- **`pptx_generation`** - Create PowerPoint presentations
- **`ask_user`** - Request user input during execution
- **`terminate`** - Signal task completion

---

## 📦 Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS
- **Radix UI** - Accessible component primitives
- **Lucide React** - Icon library
- **Clerk** - Authentication
- **React Router** - Routing

### Backend
- **Python 3.12** - Core language
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Playwright** - Browser automation
- **Loguru** - Logging
- **OpenAI API** - LLM integration

---

## 🔧 Development

### Running Tests

Backend:
```bash
cd backend
pytest tests/
```

### Code Quality

Backend:
```bash
cd backend
pre-commit run --all-files
```

Frontend:
```bash
cd frontend
npm run lint
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

Backend:
```bash
cd backend

# For Windows with browser automation
python start_server.py

# For Linux/macOS or non-browser usage
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## 🐛 Recent Fixes & Improvements

### UI Enhancements
- ✅ Fixed horizontal scrollbar overflow in file viewer
- ✅ Added image preview for PNG/JPG files
- ✅ Implemented HTML preview mode with toggle
- ✅ Fixed log ordering after user input
- ✅ Added Sandbox navigation to sidebar
- ✅ Improved responsive layout

### Backend Improvements
- ✅ Enhanced user input tool with proper callback handling
- ✅ Added debug logging for troubleshooting
- ✅ Improved WebSocket message handling
- ✅ Better error handling and recovery

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

Please run `pre-commit run --all-files` before submitting.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenManus](https://github.com/mannaandpoem/OpenManus) - Original backend framework
- [Anthropic Computer Use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) - Inspiration for tool design
- [browser-use](https://github.com/browser-use/browser-use) - Browser automation foundation
- [MetaGPT](https://github.com/geekan/MetaGPT) - Agent architecture insights

---




## 📚 Citation

```bibtex
@misc{openmanus2025,
  author = {Xinbin Liang and Jinyu Xiang and Zhaoyang Yu and Jiayi Zhang and Sirui Hong},
  title = {OpenManus: An open-source framework for building general AI agents},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mannaandpoem/OpenManus}},
}
```

---

<p align="center">Made with ❤️ by the OpenManus Team</p>
