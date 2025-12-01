# Multi-Agent Debater System

A sophisticated AI system that evaluates ideas through multiple distinct perspectives using a multi-agent architecture.

## 🔄 Workflow

The system employs a structured pipeline to analyze user inputs:

1.  **Research Agent** 🔍
    *   Analyzes the idea for historical context, similar startups, and evidence-based patterns.
    *   *Output*: Historical data and market context.

2.  **Parallel Analysis** ⚡
    *   **Optimist Agent** 👍: Identifies strengths, opportunities, and potential benefits.
    *   **Devil's Advocate** ⚠️: Critically examines flaws, risks, and potential failure points.
    *   *Note*: These agents run simultaneously for efficiency.

3.  **Response Composer** 📝
    *   Synthesizes the Research, Positive, and Critical outputs into a balanced, comprehensive report.

4.  **Conversational Agent** 💬
    *   Delivers the final analysis in a natural, empathetic, and context-aware manner, maintaining conversation history.

## 🚀 Getting Started (Backend Only)

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

To start the interactive CLI backend:

```bash
./venv/bin/python3 main.py
```

Type your idea when prompted, and watch the agents analyze it in real-time!
