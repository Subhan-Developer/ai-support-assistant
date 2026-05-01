from flask import Flask, request, jsonify
import sys
import os

# Add code folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

from agent import SupportTriageAgent

app = Flask(__name__)
agent = SupportTriageAgent()

@app.route('/triage', methods=['POST'])
def triage():
    try:
        data = request.json
        issue = data.get('issue', '')
        subject = data.get('subject', '')
        
        ticket = {'Issue': issue, 'Subject': subject}
        result = agent.process_ticket(ticket)
        
        return jsonify({
            'success': True,
            'company': result['company'],
            'status': result['status'],
            'response': result['response'],
            'product_area': result['product_area'],
            'request_type': result['request_type'],
            'justification': result['justification']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'agent': 'Support Triage Agent'})

@app.route('/')
def home():
    return jsonify({
        'message': 'Support Triage Agent API',
        'endpoints': {
            '/triage': 'POST - Process a support ticket',
            '/health': 'GET - Check API status',
            '/web': 'GET - Web interface'
        },
        'example': {
            'method': 'POST',
            'url': '/triage',
            'body': {
                'issue': 'My Visa card was stolen',
                'subject': 'Help!'
            }
        }
    })

# NEW WEB ROUTE - ADD THIS
@app.route('/web')
def web():
    try:
        with open('code/web.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Web page not found. Please make sure web.html exists."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)