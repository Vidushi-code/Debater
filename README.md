# Multi-Agent Debater System

A sophisticated AI system that evaluates ideas through multiple distinct perspectives using a multi-agent architecture.

## 🔄 Workflow

The system employs a smart, interactive pipeline:

1.  **Intent Classification** 🚦
    *   **Chat Mode**: For greetings ("hi") or casual questions, the system responds instantly with a conversational agent.
    *   **Analysis Mode**: When a concrete idea is detected, the full multi-agent analysis is triggered.

2.  **Multi-Agent Analysis** 🧠
    *   **Research Agent** 🔍: Provides historical context and market data.
    *   **Optimist Agent** 👍: Highlights strengths and opportunities.
    *   **Devil's Advocate** ⚠️: Critically examines risks and flaws.
    *   **Response Composer** 📝: Synthesizes all perspectives into a balanced report.

3.  **Frontend Experience** 💻
    *   **Interactive Chat**: A familiar chat interface with history and message bubbles.
    *   **Smart Layout**: Chat history appears above the input; analysis results appear below.
    *   **Rich Formatting**: Full Markdown support for bold text, lists, and headers.

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   Cerebras API Key

### Installation

1.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    *   Create a `.env` file in the root directory:
        ```bash
        cp .env.example .env
        ```
    *   Add your API Key:
        ```
        CEREBRAS_API_KEY=your_api_key_here
        ```

### Running the Application

1.  **Start the Backend API**:
    ```bash
    uvicorn src.api:app --reload --port 8001
    ```

2.  **Start the Frontend**:
    Open a new terminal:
    ```bash
    cd frontend
    python3 server.py
    ```

3.  **Access the App**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.

### Usage
*   **Chat**: Type "Hi" or "Hello" to chat with the assistant.
*   **Analyze**: Type a business idea (e.g., "Flying cars") to trigger the full analysis.
*   **Review**: See the breakdown from different agents and a final conclusion.
