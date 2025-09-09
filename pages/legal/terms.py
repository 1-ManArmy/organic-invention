"""
Terms of Service Routes
"""
from flask import Blueprint, render_template

terms_bp = Blueprint('terms', __name__)

@terms_bp.route('/terms')
def terms_of_service():
    """Terms of Service page"""
    
    # Terms of service content - you mentioned you'll provide this text
    terms_content = {
        'title': 'Terms of Service',
        'last_updated': 'September 9, 2025',
        'sections': [
            {
                'title': 'Acceptance of Terms',
                'content': 'By accessing and using the OneLastAI platform, you accept and agree to be bound by the terms and provision of this agreement.'
            },
            {
                'title': 'Description of Service',
                'content': 'OneLastAI provides AI-powered digital agents with unique personalities and capabilities for various use cases including entertainment, business, and personal assistance.'
            },
            {
                'title': 'User Accounts',
                'content': 'You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account.'
            },
            {
                'title': 'Acceptable Use',
                'content': 'You agree to use our services only for lawful purposes and in accordance with these terms. Prohibited uses include illegal activities, harassment, and system abuse.'
            },
            {
                'title': 'Intellectual Property',
                'content': 'The platform, AI agents, and all related content are protected by intellectual property laws. Users retain rights to their own content while granting us necessary licenses.'
            },
            {
                'title': 'Payment Terms',
                'content': 'Subscription fees are billed in advance and are non-refundable except as required by law. Prices may change with advance notice.'
            },
            {
                'title': 'Privacy and Data',
                'content': 'Your privacy is important to us. Please review our Privacy Policy to understand how we collect, use, and protect your information.'
            },
            {
                'title': 'Service Availability',
                'content': 'We strive for high availability but cannot guarantee uninterrupted service. We may perform maintenance or updates that temporarily affect access.'
            },
            {
                'title': 'Limitation of Liability',
                'content': 'Our liability is limited to the maximum extent permitted by law. We are not liable for indirect, incidental, or consequential damages.'
            },
            {
                'title': 'Termination',
                'content': 'Either party may terminate the agreement. Upon termination, your access to the service will cease, but certain provisions will survive.'
            },
            {
                'title': 'Changes to Terms',
                'content': 'We may modify these terms at any time. Continued use of the service after changes constitutes acceptance of the new terms.'
            },
            {
                'title': 'Contact Information',
                'content': 'For questions about these terms, please contact us at legal@onelastai.com.'
            }
        ]
    }
    
    return render_template('pages/legal/terms.html', content=terms_content)