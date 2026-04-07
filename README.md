🧾 Project: OpsFlow — Delivery Decision Environment
🚀 Overview

OpsFlow simulates real-world delivery logistics challenges such as address correction, prioritization, and driver allocation under constraints.
Supports integration with OpenAI / HuggingFace models via HF_TOKEN for real agent evaluation.

🌍 Why This Matters

Modern logistics systems (Amazon, Uber) require intelligent decision-making under uncertainty.

🧠 Design Philosophy

OpsFlow focuses on decision-making under real-world uncertainty, rather than static prediction tasks.

Unlike typical AI environments (classification/chatbots), it simulates:
- Noisy inputs
- Resource constraints
- Trade-offs between efficiency and urgency

🧩 Tasks
1. Address Correction (Easy)

Fix noisy real-world address inputs.

2. Delivery Prioritization (Medium)

Order deliveries based on deadlines.

3. Driver Assignment (Hard)

Optimize delivery under resource constraints.

📡 Observation & Action Space
- Observation: Pydantic model (Observation) containing task constraints and noisy inputs (addresses, priorities).
- Action: Pydantic model (Action) defining system corrections or allocation adjustments.

🎯 Reward Design
Incremental scoring (0.0 to 1.0)
Efficiency-based rewards
Penalties for poor decisions (e.g. over-committing drivers)

⚙️ Tech Stack
Python, Pydantic, OpenEnv compliant

▶️ How to Run
pip install -r requirements.txt
python scripts/run_inference.py

🐳 Docker Setup
docker build -t opsflow .
docker run opsflow

📊 Baseline Score
~2.7
