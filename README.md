\# Support Triage Agent



\## What this project does

This is a robot that reads customer support tickets and decides whether to answer automatically or send to a human.



\## How to run it

1\. Open terminal in this folder

2\. Type: python code/agent.py

3\. The robot will process all tickets and create output.csv



\## How it works

\- If ticket has words like "stolen" or "fraud" → Send to human

\- If ticket is normal question → Answer automatically



\## Files

\- code/agent.py - Main robot code

\- code/interactive.py - Test robot by typing questions

\- output.csv - Robot's answers

\- log.txt - Record of what robot did



\## Test it yourself

Type: python code/interactive.py

Then type: "My card was stolen" or "How do I take a test?"

Type "quit" to exit



\## Results

\- Processed 29 tickets

\- Answered 18 automatically

\- Escalated 11 to humans

