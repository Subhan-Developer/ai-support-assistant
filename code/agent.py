# agent.py - Support Triage Agent for Hackathon
import csv
import re
import os
from datetime import datetime

class SupportTriageAgent:
    def __init__(self):
        # Escalation patterns
        self.escalation_patterns = {
            'critical': [
                r'fraud', r'stolen', r'identity\s+theft', r'security\s+vulnerability',
                r'bug\s+bounty', r'unauthorized', r'compromised', r'hack'
            ],
            'high': [
                r'score\s+dispute', r'recruiter\s+rejected', r'increase\s+my\s+score',
                r'move\s+to\s+next\s+round', r'infosec', r'security\s+process',
                r'aws\s+bedrock.*failing'
            ],
            'sensitive': [
                r'private\s+info', r'delete\s+account', r'remove', r'data'
            ]
        }
    
    def detect_company(self, text):
        """Detect which company the ticket is about"""
        text = text.lower()
        
        if re.search(r'hackerrank|test|assessment|candidate|challenge', text):
            return 'HackerRank'
        elif re.search(r'claude|anthropic', text):
            return 'Claude'
        elif re.search(r'visa|card|payment|cheque', text):
            return 'Visa'
        return 'None'
    
    def classify_request(self, text, company):
        """Classify request type"""
        text = text.lower()
        
        if company == 'HackerRank':
            if re.search(r'test|assessment|challenge', text):
                return 'test_issue'
            elif re.search(r'account|login|access|delete', text):
                return 'account_management'
            elif re.search(r'pay|billing|subscription|refund', text):
                return 'billing'
            elif re.search(r'certificate', text):
                return 'certificate'
            return 'general_support'
        
        elif company == 'Claude':
            if re.search(r'conversation|delete|private', text):
                return 'conversation_management'
            elif re.search(r'data|privacy|crawl', text):
                return 'privacy'
            return 'general_question'
        
        elif company == 'Visa':
            if re.search(r'stolen|fraud|identity', text):
                return 'fraud_report'
            elif re.search(r'lost|blocked', text):
                return 'card_issue'
            elif re.search(r'dispute|refund', text):
                return 'transaction_dispute'
            return 'general_inquiry'
        
        return 'out_of_scope'
    
    def product_area(self, text, company):
        """Determine product area"""
        text = text.lower()
        
        if company == 'HackerRank':
            if re.search(r'test|assessment', text):
                return 'assessments'
            elif re.search(r'candidate', text):
                return 'candidate_management'
            elif re.search(r'account|access', text):
                return 'account_management'
            return 'general'
        
        elif company == 'Claude':
            if re.search(r'conversation', text):
                return 'conversation_management'
            elif re.search(r'privacy|data', text):
                return 'privacy_data'
            return 'general'
        
        elif company == 'Visa':
            if re.search(r'card', text):
                return 'card_services'
            elif re.search(r'fraud|stolen', text):
                return 'fraud_protection'
            return 'general'
        
        return 'unknown'
    
    def should_escalate(self, text):
        """Decide if ticket needs escalation"""
        text = text.lower()
        
        for severity, patterns in self.escalation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return True, f"{severity}_risk"
        
        if re.search(r'[éèêçñáóú]', text):
            return True, "non_english_ticket"
        
        return False, "can_handle"
    
    def generate_response(self, issue, subject, company, escalated):
        """Generate response based on patterns"""
        if escalated[0]:
            return f"""Thank you for contacting {company if company != 'None' else 'support'}.

Due to the sensitive nature of this request ({escalated[1]}), we are escalating this ticket to our specialized support team. They will review your case and respond within 24-48 hours.

For immediate assistance, please contact our priority support line.

Reference: ESC-{abs(hash(issue + subject)) % 10000:04d}"""
        
        text = f"{issue} {subject}".lower()
        
        # HackerRank responses
        if company == 'HackerRank':
            if 'test active' in text or 'how long' in text:
                return "Tests in HackerRank remain active indefinitely unless a start and end time are set. Without these, tests do not expire automatically."
            elif 'variant' in text:
                return "Create variants for different candidate profiles (e.g., React vs Angular). Create a new test when the assessment structure differs significantly."
            elif 'reinvite' in text or 'extra time' in text:
                return """To add extra time: Tests > Candidates > Select checkbox > More > Add Time Accommodation. Enter percentage (multiples of five) and Save."""
            elif 'delete account' in text:
                return """To delete account: Forgot password > Set new password > Login > Settings > Delete Account. This permanently removes all data."""
            elif 'refund' in text:
                return "For refund requests, please contact billing@hackerrank.com with your order ID."
            elif 'pause' in text or 'subscription' in text:
                return "To pause subscription, contact billing@hackerrank.com. Changes take effect next billing cycle."
            elif 'remove user' in text:
                return "To remove a user: Team Management > Users > Find user > Three dots > Remove User. Admin rights required."
            else:
                return "Thank you for contacting HackerRank Support. Please visit support.hackerrank.com for detailed documentation."
        
        # Claude responses
        elif company == 'Claude':
            if 'delete conversation' in text or 'private info' in text:
                return """To delete conversation: Navigate to conversation > Click name > Select 'Delete'. Deleted conversations cannot be recovered."""
            elif 'not responding' in text:
                return "Check status.anthropic.com for outages, refresh browser, or clear cache. Provide error messages if issue persists."
            elif 'data' in text or 'crawl' in text:
                return "To prevent crawling, add 'anthropic.com' to robots.txt or contact privacy@anthropic.com."
            else:
                return "Thank you for contacting Claude Support. Visit support.claude.com for documentation."
        
        # Visa responses
        elif company == 'Visa':
            if 'stolen' in text and 'cheque' in text:
                return """For stolen Traveller's Cheques: Call issuer immediately (1-800-645-6556 for Citicorp). Have serial numbers ready. Refunds within 24 hours."""
            elif 'lost' in text or 'stolen' in text:
                return "To report lost/stolen Visa card from India: Call 000-800-100-1219. Global: +1 303 967 1090. Card blocked within ~30 minutes."
            elif 'dispute' in text:
                return "To dispute a charge: 1) Contact merchant first, 2) Contact your card issuer, 3) File formal dispute within 60-120 days."
            elif 'minimum' in text:
                return "Merchant minimums are set by merchants, not Visa. Visa cards must be accepted for all amounts."
            else:
                return "For Visa support, contact your card issuer directly or visit visa.co.in/support.html"
        
        # Out of scope
        else:
            return "I apologize, but this issue is outside my support scope. I can only assist with HackerRank, Claude, and Visa inquiries."
    
    def process_ticket(self, row):
        """Process single ticket"""
        issue = row.get('Issue', '')
        subject = row.get('Subject', '')
        full_text = f"{issue} {subject}"
        
        company = self.detect_company(full_text)
        request_type = self.classify_request(full_text, company)
        product = self.product_area(full_text, company)
        escalated = self.should_escalate(full_text)
        
        response = self.generate_response(issue, subject, company, escalated)
        status = "Escalated" if escalated[0] else "Replied"
        justification = f"Company:{company}|Type:{request_type}|Escalated:{escalated[0]}"
        
        return {
            'issue': issue,
            'subject': subject,
            'company': company,
            'response': response,
            'product_area': product,
            'status': status,
            'request_type': request_type,
            'justification': justification
        }


def main():
    print("=" * 70)
    print("SUPPORT TRIAGE AGENT - Starting Processing")
    print("=" * 70)
    
    agent = SupportTriageAgent()
    
    # Read the CSV file
    input_file = 'support_tickets.csv'
    output_file = 'output.csv'
    log_file = 'log.txt'
    
    if not os.path.exists(input_file):
        print(f"\n❌ ERROR: Could not find {input_file}")
        print(f"Current directory: {os.getcwd()}")
        print("Files found:")
        for file in os.listdir('.'):
            print(f"  - {file}")
        return
    
    try:
        # Try different encodings
        encodings = ['latin-1', 'cp1252', 'utf-8', 'iso-8859-1']
        tickets = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    tickets = list(reader)
                used_encoding = encoding
                print(f"✓ Successfully read file with {encoding} encoding")
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if tickets is None:
            # Last resort - read as binary and ignore errors
            with open(input_file, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
            lines = content.splitlines()
            reader = csv.DictReader(lines)
            tickets = list(reader)
            print("✓ Successfully read file with fallback method")
        
        print(f"\n✓ Loaded {len(tickets)} tickets from {input_file}")
        
        results = []
        for i, ticket in enumerate(tickets):
            print(f"  Processing [{i+1}/{len(tickets)}]: {ticket.get('Subject', '')[:40]}...")
            result = agent.process_ticket(ticket)
            results.append(result)
        
        # Write output CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['issue', 'subject', 'company', 'response', 'product_area', 'status', 'request_type', 'justification']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        # Write log file
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"SUPPORT TRIAGE AGENT - PROCESSING LOG\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            for i, result in enumerate(results):
                f.write(f"\n--- TICKET {i+1} ---\n")
                f.write(f"Subject: {result['subject']}\n")
                f.write(f"Company: {result['company']}\n")
                f.write(f"Request Type: {result['request_type']}\n")
                f.write(f"Product Area: {result['product_area']}\n")
                f.write(f"Status: {result['status']}\n")
                f.write(f"Justification: {result['justification']}\n")
                f.write(f"Response Preview: {result['response'][:200]}...\n")
                f.write("-" * 40 + "\n")
            
            f.write(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print("\n" + "=" * 70)
        print(f"✅ SUCCESS!")
        print(f"   Processed: {len(results)} tickets")
        print(f"   - Replied: {sum(1 for r in results if r['status'] == 'Replied')}")
        print(f"   - Escalated: {sum(1 for r in results if r['status'] == 'Escalated')}")
        print(f"\n📁 Output file: {output_file}")
        print(f"📝 Log file: {log_file}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()