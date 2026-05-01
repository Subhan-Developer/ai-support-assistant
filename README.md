🤖 Support Triage Agent
📌 Overview

The Support Triage Agent is an automated system that reads customer support tickets and decides whether to:

Answer automatically 🤖
Escalate to a human 👨‍💻

It helps reduce workload and improves response time for critical issues.

🚀 Features
🔍 Keyword-based classification
⚡ Automatic responses for common queries
🚨 Escalation of sensitive issues (e.g., fraud, stolen cards)
📊 Logs and output tracking
💬 Interactive testing mode
🛠️ How to Run
1. Open Terminal

Navigate to your project folder:

cd your-project-folder
2. Run the Agent
python code/agent.py
3. Output Files
output.csv → Processed ticket results
log.txt → Agent activity log
⚙️ How It Works
🚨 Escalation Rules

If a ticket contains keywords like:

"stolen"
"fraud"

➡️ The ticket is sent to a human agent.

🤖 Auto Response

If the ticket is a normal question:

"How do I take a test?"
"How to reset password?"

➡️ The agent responds automatically.

📂 Project Structure
project-folder/
│
├── code/
│   ├── agent.py
│   ├── interactive.py
│
├── output.csv
├── log.txt
└── README.md
🧪 Interactive Testing

Run:

python code/interactive.py

Example inputs:

My card was stolen
How do I take a test?

Type quit to exit.

📊 Results
Total Tickets: 29
Auto Answered: 18
Escalated: 11
💡 Future Improvements
Add machine learning 🤖
API integration 🌐
Better NLP responses 🧠
Analytics dashboard 📈
👨‍💻 Author

Simple AI-based automation project for support ticket handling.
