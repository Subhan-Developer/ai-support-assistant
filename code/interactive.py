import re

class SupportTriageAgent:
    def __init__(self):
        self.escalation_keywords = ['fraud', 'stolen', 'identity']
    
    def detect_company(self, text):
        text = text.lower()
        if 'hackerrank' in text or 'test' in text:
            return 'HackerRank'
        elif 'claude' in text:
            return 'Claude'
        elif 'visa' in text or 'card' in text:
            return 'Visa'
        return 'None'
    
    def should_escalate(self, text):
        text = text.lower()
        for kw in self.escalation_keywords:
            if kw in text:
                return True
        return False
    
    def generate_response(self, q, c, e):
        if e:
            return '?? ESCALATED: Human will contact you'
        if c == 'HackerRank':
            return '? Check support.hackerrank.com'
        elif c == 'Claude':
            return '? Check support.claude.com'
        elif c == 'Visa':
            return '? Call your bank'
        return '?? I only help with HackerRank, Claude, Visa'

agent = SupportTriageAgent()
print('='*50)
print('SUPPORT AGENT - Type your question or "quit"')
print('='*50)

while True:
    q = input('\nYour question: ')
    if q.lower() == 'quit':
        break
    c = agent.detect_company(q)
    e = agent.should_escalate(q)
    r = agent.generate_response(q, c, e)
    print(f'Company: {c}')
    print(f'Escalate: {e}')
    print(f'Response: {r}')
