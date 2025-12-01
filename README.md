# Multi-Agent Debater System

A sophisticated AI system that evaluates ideas through multiple distinct perspectives using a multi-agent architecture.

## 🔄 Workflow

The system employs a structured pipeline to analyze user inputs:

1.  **Intent Classifier (Router)** 🚦
    *   Determines if the user is just chatting or providing a concrete idea.
    *   *Chat Mode*: Responds naturally to greetings and questions.
    *   *Analysis Mode*: Triggers the full multi-agent pipeline when a valid idea is detected.

2.  **Research Agent** 🔍
    *   Analyzes the idea for historical context, similar startups, and evidence-based patterns.
    *   *Output*: Historical data and market context.

3.  **Parallel Analysis** ⚡
    *   **Optimist Agent** 👍: Identifies strengths, opportunities, and potential benefits.
    *   **Devil's Advocate** ⚠️: Critically examines flaws, risks, and potential failure points.
    *   *Note*: These agents run simultaneously for efficiency.

4.  **Response Composer** 📝
    *   Synthesizes the Research, Positive, and Critical outputs into a balanced, comprehensive report.

5.  **Conversational Agent** 💬
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

### Running the Application (Full Stack)

1.  **Start the Backend API**:
    ```bash
    uvicorn src.api:app --reload --port 8001
    ```

2.  **Start the Frontend**:
    Open a new terminal and run:
    ```bash
    cd frontend
    python3 -m http.server 8000
    ```

3.  **Access the App**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.

### Usage
*   **Chat**: Start by saying "Hello". The backend will detect this as chat and respond conversationally.
*   **Analyze**: Describe a concrete idea. The backend will trigger the full multi-agent analysis and return structured results to the UI.
