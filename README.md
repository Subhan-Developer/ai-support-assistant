🤖 Support Triage Agent
📌 Overview

The Support Triage Agent is an automated system designed to handle customer support tickets efficiently. It analyzes incoming messages and decides whether:

✅ The issue can be handled automatically
👨‍💻 The issue should be escalated to a human agent

This helps reduce workload, improve response time, and prioritize critical cases.

🚀 Features
🔍 Keyword-based classification
⚡ Automatic responses for common queries
🚨 Escalation of sensitive issues (e.g., fraud, stolen cards)
📊 Logs and output tracking
💬 Interactive testing mode
🛠️ How to Run
Step 1: Open Terminal

Navigate to the project folder:

cd your-project-folder
Step 2: Run the Agent
python code/agent.py
Step 3: Output

After execution:

output.csv → Contains processed ticket results
log.txt → Records agent activity
⚙️ How It Works

The agent uses simple rule-based logic:

🚨 Escalation Rules

If a ticket contains keywords like:

"stolen"
"fraud"

➡️ The ticket is sent to a human agent

🤖 Auto-Response Rules

If the ticket is a general question like:

"How do I take a test?"
"How to reset password?"

➡️ The agent generates an automatic response

📂 Project Structure
project-folder/
│
├── code/
│   ├── agent.py          # Main processing script
│   ├── interactive.py    # Interactive testing mode
│
├── output.csv            # Final processed results
├── log.txt               # Execution logs
└── README.md             # Project documentation
🧪 Interactive Testing

You can test the agent manually:

python code/interactive.py
Example Inputs:
My card was stolen
How do I take a test?

Type:

quit

to exit the program.

📊 Results
📥 Total Tickets Processed: 29
🤖 Automatically Answered: 18
👨‍💻 Escalated to Humans: 11
💡 Future Improvements
🧠 Add Machine Learning for smarter classification
🌐 Integrate with real support systems (APIs)
🗣️ Improve response quality using NLP
📈 Dashboard for analytics and monitoring
👨‍💻 Author

Developed as a simple AI-based automation project for handling support tickets efficiently.
