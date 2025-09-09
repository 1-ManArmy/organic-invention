"""
Privacy Policy Routes
"""
from flask import Blueprint, render_template

privacy_bp = Blueprint('privacy', __name__)

@privacy_bp.route('/privacy')
def privacy_policy():
    """Privacy Policy page"""
    
    # Privacy policy content - you mentioned you'll provide this text
    privacy_content = {
        'title': 'Privacy Policy',
        'last_updated': 'September 9, 2025',
        'sections': [
            {
                'title': 'Information We Collect',
                'content': 'We collect information you provide directly to us, such as when you create an account, interact with our AI agents, or contact us for support.'
            },
            {
                'title': 'How We Use Your Information', 
                'content': 'We use the information we collect to provide, maintain, and improve our AI agent services, process transactions, and communicate with you.'
            },
            {
                'title': 'Information Sharing',
                'content': 'We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this policy.'
            },
            {
                'title': 'Data Security',
                'content': 'We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.'
            },
            {
                'title': 'Your Rights',
                'content': 'You have the right to access, update, or delete your personal information. You may also opt out of certain communications from us.'
            },
            {
                'title': 'Cookies and Tracking',
                'content': 'We use cookies and similar technologies to enhance your experience and analyze usage patterns on our platform.'
            },
            {
                'title': 'International Transfers',
                'content': 'Your information may be transferred to and processed in countries other than your own, where data protection laws may differ.'
            },
            {
                'title': 'Changes to This Policy',
                'content': 'We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page.'
            },
            {
                'title': 'Contact Us',
                'content': 'If you have any questions about this privacy policy, please contact us at privacy@onelastai.com.'
            }
        ]
    }
    
    return render_template('pages/legal/privacy.html', content=privacy_content)

@privacy_bp.route('/cookies')
def cookie_policy():
    """Cookie Policy page"""
    
    cookie_content = {
        'title': 'Cookie Policy',
        'last_updated': 'September 9, 2025',
        'sections': [
            {
                'title': 'What Are Cookies',
                'content': 'Cookies are small text files that are stored on your device when you visit our website. They help us provide you with a better experience.'
            },
            {
                'title': 'Types of Cookies We Use',
                'content': 'We use essential cookies for basic functionality, analytics cookies to understand usage, and preference cookies to remember your settings.'
            },
            {
                'title': 'Managing Cookies',
                'content': 'You can control cookies through your browser settings. However, disabling certain cookies may affect the functionality of our platform.'
            },
            {
                'title': 'Third-Party Cookies',
                'content': 'We may use third-party services that set their own cookies, such as analytics providers and payment processors.'
            }
        ]
    }
    
    return render_template('pages/legal/privacy.html', content=cookie_content)