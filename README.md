📦 Customer Support Agent (ADK 2.2.0)

An AI-powered customer support workflow agent built using Google Agent Development Kit (ADK 2.2.0).
This project demonstrates a graph-based AI workflow that classifies user queries and routes them intelligently to the correct handler.

🚀 Project Overview

This agent simulates a shipping company customer support system:

📦 Handles shipping-related questions (tracking, rates, delivery, returns)
🤖 Uses an LLM-based classifier to understand user intent
🔀 Routes queries using a workflow graph
❌ Politely declines unrelated questions
🧠 How It Works (Workflow)
User Query
   ↓
Classifier Agent (LLM)
   ↓
Route Decision
   ├── Shipping Query → FAQ Agent (answers from predefined knowledge)
   └── Unrelated Query → Decline Node (polite refusal)
⚙️ Tech Stack
🧠 Google ADK 2.2.0 (Agent Development Kit)
🤖 Gemini LLM (Flash Lite)
🐍 Python 3.10+
⚡ Async Workflow Execution
🔧 In-memory runner for local testing
📂 Project Structure
customer_support_agent/
│── agent.py              # Main workflow (nodes, edges, agents)
│── __init__.py
│── .env                  # API keys (not pushed to GitHub)
│
main.py                  # CLI test runner
pyproject.toml          # Project configuration
.gitignore              # Ignored files
🧩 Key Features
🔹 1. Query Classification

Automatically detects whether a query is:

Shipping-related
Unrelated
🔹 2. FAQ Agent

Answers questions like:

Shipping rates
Delivery time
Tracking orders
Return policy
🔹 3. Guardrail Node

Politely declines unrelated queries:

“I am a shipping support assistant and can only answer shipping-related questions.”

🔹 4. Graph-Based Workflow

Uses ADK workflow edges for routing logic instead of linear code.

▶️ How to Run
1. Clone repo
git clone https://github.com/palaksoni23/Customer_Support_Agent.git
cd Customer_Support_Agent
2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Add API key

Create .env file:

GOOGLE_API_KEY=your_api_key_here
5. Run agent locally
python main.py
6. Launch ADK Playground (optional)
python -m google.adk.cli web

Then open:

http://127.0.0.1:8000
💬 Example Queries
✅ Shipping-related
How do I track my package?
What are your delivery charges?
How long does shipping take?
❌ Unrelated
What is the capital of Japan?
Write a Python function for sorting
🧠 Key Learning

This project demonstrates:

LLM-powered classification
Workflow-based AI systems
Agent routing logic (graph execution)
Tool-free reasoning vs structured responses
Real-world AI agent architecture
📌 Author

👤 Palak Soni
🔗 GitHub: @palaksoni23

⭐ If you like this project

Give it a ⭐ on GitHub and explore more AI agent projects!
