#!/usr/bin/env python3
"""
Anonymous Email Sender NG - Next Generation
Enhanced version using multiple anonymous email services
Original by github.com/technicaldada
Enhanced by Koushik Pal (KP)
"""

import requests
import random
import time
import sys
from typing import Dict, List, Optional, Tuple

class AnonMailNG:
    def __init__(self):
        self.services = [
            {
                'name': 'Anonymouse',
                'url': 'http://anonymouse.org/cgi-bin/anon-email.cgi',
                'method': 'POST',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'http://anonymouse.org',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                'data_fields': {
                    'to': 'to',
                    'subject': 'subject', 
                    'message': 'text'
                },
                'success_indicator': 'The e-mail has been sent',
                'privacy_note': 'Email will be randomly delayed up to 12 hours'
            },
            {
                'name': 'GhostMail',
                'url': 'http://www.guerrillamail.com/ajax.php',
                'method': 'POST',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                },
                'data_fields': {
                    'to': 'email_to',
                    'subject': 'subject',
                    'message': 'body'
                },
                'success_indicator': 'success',
                'privacy_note': 'Temporary email service'
            }
        ]
        
        self.session = requests.Session()
        self.timeout = 30

    def print_banner(self):
        """Display the application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                   ANONYMOUS EMAIL SENDER NG                 ║
║                     Next Generation Version                 ║
╚══════════════════════════════════════════════════════════════╝
        
    ████████╗███████╗██████╗ ███╗   ███╗██╗██╗   ██╗██╗████████╗██╗   ██╗
    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║╚██╗ ██╔╝██║╚══██╔══╝╚██╗ ██╔╝
       ██║   █████╗  ██████╔╝██╔████╔██║██║ ╚████╔╝ ██║   ██║    ╚████╔╝ 
       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║  ╚██╔╝  ██║   ██║     ╚██╔╝  
       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║   ██║   ██║   ██║      ██║   
       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝   ╚═╝      ╚═╝   
                                                                          
        """
        print("\033[1;36m" + banner + "\033[0m")
        print("\033[1;32m📧 Anonymous Email Sender using multiple services\033[0m")
        print("\033[1;33m👨‍💻 Original by: github.com/technicaldada\033[0m")
        print("\033[1;35m🚀 Enhanced by: Koushik Pal (KP)\033[0m")
        print("\033[1;34m🌐 Visit: https://www.kalilinux.in\033[0m")
        print("\033[1;31m⚠️  Use responsibly and ethically!\033[0m")
        print()

    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        if '@' in email and '.' in email and len(email) > 5:
            return True
        return False

    def get_user_input(self) -> Tuple[str, str, str]:
        """Get and validate user input"""
        print("\033[1;36m" + "═" * 50 + "\033[0m")
        
        while True:
            to_email = input("\033[1;32m📨 Recipient Email: \033[0m").strip()
            if self.validate_email(to_email):
                break
            print("\033[1;31m❌ Invalid email format. Please try again.\033[0m")
        
        subject = input("\033[1;33m📝 Subject: \033[0m").strip()
        if not subject:
            subject = "No Subject"
        
        print("\033[1;35m💬 Message (Press Ctrl+D when finished):\033[0m")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        message = '\n'.join(lines)
        if not message:
            message = "No message content"
            
        return to_email, subject, message

    def send_anonymous_email(self, service: Dict, to: str, subject: str, message: str) -> bool:
        """Send email using specified service"""
        try:
            # Prepare data
            data = {}
            for field, service_field in service['data_fields'].items():
                if field == 'to':
                    data[service_field] = to
                elif field == 'subject':
                    data[service_field] = subject
                elif field == 'message':
                    data[service_field] = message

            # Send request
            if service['method'] == 'POST':
                response = self.session.post(
                    service['url'],
                    headers=service['headers'],
                    data=data,
                    timeout=self.timeout,
                    verify=False  # Disable SSL verification for anonymity
                )
            else:
                response = self.session.get(
                    service['url'],
                    params=data,
                    headers=service['headers'],
                    timeout=self.timeout,
                    verify=False
                )

            # Check success
            if service['success_indicator'].lower() in response.text.lower():
                return True, service['privacy_note']
            else:
                return False, "Service might be down or rate limited"

        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def show_service_status(self):
        """Show available services and their status"""
        print("\033[1;36m\n🛠️  Available Services:\033[0m")
        print("\033[1;36m" + "─" * 50 + "\033[0m")
        
        for i, service in enumerate(self.services, 1):
            status = "✅ Available"
            # Quick connectivity check
            try:
                test_response = self.session.head(service['url'], timeout=5, verify=False)
                if test_response.status_code == 200:
                    status = "✅ Online"
                else:
                    status = "⚠️  Limited"
            except:
                status = "❌ Offline"
            
            print(f"\033[1;33m{i}. {service['name']}: {status}\033[0m")
            print(f"   📍 {service['url']}")
            print(f"   🔒 {service['privacy_note']}")
            print()

    def send_emails(self, to: str, subject: str, message: str) -> Dict:
        """Send emails using all available services"""
        results = {}
        
        print("\033[1;36m\n🚀 Sending Anonymous Emails...\033[0m")
        print("\033[1;36m" + "─" * 50 + "\033[0m")
        
        for service in self.services:
            print(f"\033[1;35m📤 Trying {service['name']}...\033[0m")
            
            success, message_info = self.send_anonymous_email(service, to, subject, message)
            
            if success:
                print(f"\033[1;32m✅ {service['name']}: Success!\033[0m")
                print(f"\033[1;36m   💡 Note: {message_info}\033[0m")
                results[service['name']] = {'success': True, 'note': message_info}
            else:
                print(f"\033[1;31m❌ {service['name']}: Failed - {message_info}\033[0m")
                results[service['name']] = {'success': False, 'error': message_info}
            
            # Random delay between services
            delay = random.uniform(2, 5)
            time.sleep(delay)
            print()
        
        return results

    def print_summary(self, results: Dict, to: str):
        """Print sending summary"""
        print("\033[1;36m" + "═" * 50 + "\033[0m")
        print("\033[1;35m📊 SENDING SUMMARY\033[0m")
        print("\033[1;36m" + "─" * 50 + "\033[0m")
        
        successful = sum(1 for result in results.values() if result['success'])
        total = len(results)
        
        print(f"\033[1;32m📨 Recipient: {to}\033[0m")
        print(f"\033[1;33m✅ Successful: {successful}/{total}\033[0m")
        
        if successful > 0:
            print("\033[1;32m🎉 Email(s) sent successfully!\033[0m")
            print("\033[1;36m💡 Some services may delay delivery for privacy.\033[0m")
        else:
            print("\033[1;31m😞 All services failed. Please try again later.\033[0m")
        
        print("\033[1;36m" + "═" * 50 + "\033[0m")

    def run(self):
        """Main application runner"""
        try:
            self.print_banner()
            self.show_service_status()
            
            # Get user input
            to, subject, message = self.get_user_input()
            
            # Confirm sending
            print(f"\n\033[1;33m📧 Ready to send email to: {to}\033[0m")
            print(f"\033[1;33m📝 Subject: {subject}\033[0m")
            print(f"\033[1;33m💬 Message length: {len(message)} characters\033[0m")
            
            confirm = input("\n\033[1;31m🚀 Proceed with sending? (y/N): \033[0m").strip().lower()
            if confirm not in ['y', 'yes']:
                print("\033[1;33m❌ Sending cancelled.\033[0m")
                return
            
            # Send emails
            results = self.send_emails(to, subject, message)
            
            # Show summary
            self.print_summary(results, to)
            
            # Offer to send another
            another = input("\n\033[1;36m🔄 Send another email? (y/N): \033[0m").strip().lower()
            if another in ['y', 'yes']:
                print()
                self.run()
            else:
                print("\n\033[1;32m👋 Thank you for using Anonymous Email Sender NG!\033[0m")
                print("\033[1;34m🌐 Visit https://www.kalilinux.in for more tools\033[0m")
                
        except KeyboardInterrupt:
            print("\n\n\033[1;33m⚠️  Operation cancelled by user.\033[0m")
        except Exception as e:
            print(f"\n\033[1;31m💥 Unexpected error: {str(e)}\033[0m")

def main():
    """Main entry point"""
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("❌ 'requests' module not installed!")
        print("💡 Install it using: pip install requests")
        sys.exit(1)
    
    # Run the application
    app = AnonMailNG()
    app.run()

if __name__ == "__main__":
    main()
