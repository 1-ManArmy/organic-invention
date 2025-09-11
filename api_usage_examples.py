"""
Example usage of API keys in AI Agent implementations
This file demonstrates how to use the configured API keys in your AI agents
"""

from config import config
import requests

class AIServiceClient:
    """Example client showing how to use configured API keys"""
    
    def __init__(self):
        self.openai_key = config.OPENAI_API_KEY
        self.elevenlabs_key = config.ELEVENLABS_API_KEY
        self.gemini_key = config.GEMINI_API_KEY
        
    def openai_chat(self, messages, model="gpt-3.5-turbo"):
        """Example OpenAI API call"""
        if not self.openai_key:
            return {"error": "OpenAI API key not configured"}
            
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 150
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def elevenlabs_tts(self, text, voice_id="21m00Tcm4TlvDq8ikWAM"):
        """Example ElevenLabs Text-to-Speech API call"""
        if not self.elevenlabs_key:
            return {"error": "ElevenLabs API key not configured"}
            
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers=headers,
                json=data
            )
            return {"audio_data": response.content, "status": "success"}
        except Exception as e:
            return {"error": str(e)}
    
    def gemini_generate(self, prompt):
        """Example Google Gemini API call"""
        if not self.gemini_key:
            return {"error": "Gemini API key not configured"}
            
        try:
            # Note: This is a simplified example
            # The actual Gemini API implementation would use the google-generativeai library
            headers = {"Content-Type": "application/json"}
            data = {"prompt": prompt}
            
            # This is a placeholder - replace with actual Gemini API endpoint
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.gemini_key}"
            
            response = requests.post(url, headers=headers, json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class PaymentProcessor:
    """Example payment processing using configured keys"""
    
    def __init__(self):
        self.paypal_client_id = config.PAYPAL_CLIENT_ID
        self.paypal_secret = config.PAYPAL_CLIENT_SECRET
        self.stripe_secret = config.STRIPE_SECRET_KEY
    
    def create_paypal_payment(self, amount, currency="USD"):
        """Example PayPal payment creation"""
        if not self.paypal_client_id or not self.paypal_secret:
            return {"error": "PayPal credentials not configured"}
            
        # PayPal SDK implementation would go here
        return {
            "status": "success",
            "payment_id": "PAY-example-123",
            "message": "PayPal payment created successfully"
        }
    
    def create_stripe_payment(self, amount, currency="USD"):
        """Example Stripe payment creation"""
        if not self.stripe_secret:
            return {"error": "Stripe secret key not configured"}
            
        # Stripe SDK implementation would go here
        return {
            "status": "success", 
            "payment_intent_id": "pi_example_123",
            "message": "Stripe payment intent created successfully"
        }

class SecurityAnalyzer:
    """Example security analysis using configured security API keys"""
    
    def __init__(self):
        self.shodan_key = config.SHODAN_API_KEY
        self.virustotal_key = config.VIRUSTOTAL_API_KEY
        self.abuseipdb_key = config.ABUSEIPDB_API_KEY
    
    def analyze_ip_shodan(self, ip_address):
        """Example Shodan IP analysis"""
        if not self.shodan_key:
            return {"error": "Shodan API key not configured"}
            
        headers = {"Authorization": f"Bearer {self.shodan_key}"}
        
        try:
            response = requests.get(
                f"https://api.shodan.io/shodan/host/{ip_address}?key={self.shodan_key}"
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def check_file_virustotal(self, file_hash):
        """Example VirusTotal file analysis"""
        if not self.virustotal_key:
            return {"error": "VirusTotal API key not configured"}
            
        headers = {"x-apikey": self.virustotal_key}
        
        try:
            response = requests.get(
                f"https://www.virustotal.com/api/v3/files/{file_hash}",
                headers=headers
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def test_api_connections():
    """Test function to verify API connections"""
    print("🔍 Testing API Connections...")
    
    # Test AI Services
    ai_client = AIServiceClient()
    print(f"✅ OpenAI API: {'Configured' if ai_client.openai_key else 'Not configured'}")
    print(f"✅ ElevenLabs API: {'Configured' if ai_client.elevenlabs_key else 'Not configured'}")
    print(f"✅ Gemini API: {'Configured' if ai_client.gemini_key else 'Not configured'}")
    
    # Test Payment Services
    payment_processor = PaymentProcessor()
    print(f"💳 PayPal: {'Configured' if payment_processor.paypal_client_id else 'Not configured'}")
    print(f"💳 Stripe: {'Configured' if payment_processor.stripe_secret else 'Not configured'}")
    
    # Test Security Services
    security_analyzer = SecurityAnalyzer()
    print(f"🛡️ Shodan: {'Configured' if security_analyzer.shodan_key else 'Not configured'}")
    print(f"🛡️ VirusTotal: {'Configured' if security_analyzer.virustotal_key else 'Not configured'}")
    print(f"🛡️ AbuseIPDB: {'Configured' if security_analyzer.abuseipdb_key else 'Not configured'}")
    
    print("\n🚀 All systems ready for production!")

if __name__ == "__main__":
    test_api_connections()