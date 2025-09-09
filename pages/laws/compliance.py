"""
Compliance and Legal Requirements Routes
"""
from flask import Blueprint, render_template, request, jsonify

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/')
def index():
    """Compliance overview page"""
    return render_template('pages/laws/compliance.html', title='Compliance & Legal')

@compliance_bp.route('/gdpr')
def gdpr():
    """GDPR Compliance Information"""
    gdpr_info = {
        'title': 'General Data Protection Regulation (GDPR) Compliance',
        'effective_date': '2025-01-01',
        'last_updated': '2025-09-09',
        'sections': [
            {
                'title': 'Data Controller Information',
                'content': 'AI Agents Platform operates as a data controller under GDPR regulations. We process personal data lawfully, fairly, and transparently.'
            },
            {
                'title': 'Lawful Basis for Processing',
                'items': [
                    'Consent - for marketing communications and optional features',
                    'Contract - for service delivery and account management',
                    'Legitimate Interest - for security, fraud prevention, and service improvement',
                    'Legal Obligation - for compliance with applicable laws'
                ]
            },
            {
                'title': 'Data Subject Rights',
                'items': [
                    'Right to Access - Request copies of your personal data',
                    'Right to Rectification - Correct inaccurate personal data',
                    'Right to Erasure - Request deletion of your personal data',
                    'Right to Restrict Processing - Limit how we process your data',
                    'Right to Data Portability - Receive your data in machine-readable format',
                    'Right to Object - Object to processing based on legitimate interests',
                    'Rights related to Automated Decision Making - Including profiling'
                ]
            },
            {
                'title': 'Data Protection Officer',
                'content': 'For GDPR-related inquiries, contact our Data Protection Officer at dpo@aiagentsplatform.com'
            },
            {
                'title': 'International Transfers',
                'content': 'When transferring data outside the EEA, we ensure adequate protection through Standard Contractual Clauses and adequacy decisions.'
            }
        ]
    }
    
    return render_template('pages/laws/gdpr.html', gdpr=gdpr_info, title='GDPR Compliance')

@compliance_bp.route('/ccpa')
def ccpa():
    """CCPA Compliance Information"""
    ccpa_info = {
        'title': 'California Consumer Privacy Act (CCPA) Compliance',
        'effective_date': '2025-01-01',
        'last_updated': '2025-09-09',
        'sections': [
            {
                'title': 'Consumer Rights Under CCPA',
                'items': [
                    'Right to Know - What personal information is collected and how it\'s used',
                    'Right to Delete - Request deletion of personal information',
                    'Right to Opt-Out - Opt-out of the sale of personal information',
                    'Right to Non-Discrimination - Equal service regardless of privacy choices'
                ]
            },
            {
                'title': 'Categories of Personal Information',
                'items': [
                    'Identifiers (name, email, IP address)',
                    'Commercial Information (transaction history, preferences)',
                    'Internet Activity (browsing behavior, interactions)',
                    'Geolocation Data (approximate location)',
                    'Professional Information (job title, company)',
                    'Inferences (preferences, characteristics, behavior)'
                ]
            },
            {
                'title': 'Sale of Personal Information',
                'content': 'We do not sell personal information to third parties. We may share data with service providers for business purposes under strict contractual protections.'
            },
            {
                'title': 'Exercising Your Rights',
                'content': 'California residents can exercise their rights by contacting privacy@aiagentsplatform.com or using our online request form.'
            }
        ]
    }
    
    return render_template('pages/laws/ccpa.html', ccpa=ccpa_info, title='CCPA Compliance')

@compliance_bp.route('/accessibility')
def accessibility():
    """Web Accessibility Compliance"""
    accessibility_info = {
        'title': 'Web Accessibility Compliance',
        'standards': 'WCAG 2.1 Level AA',
        'last_updated': '2025-09-09',
        'sections': [
            {
                'title': 'Our Commitment',
                'content': 'AI Agents Platform is committed to ensuring digital accessibility for people with disabilities. We continually improve the user experience for everyone.'
            },
            {
                'title': 'Accessibility Features',
                'items': [
                    'Keyboard navigation support',
                    'Screen reader compatibility',
                    'High contrast color schemes',
                    'Resizable text and zoom support',
                    'Alt text for images',
                    'Descriptive link text',
                    'Structured headings and landmarks',
                    'Focus indicators and skip links'
                ]
            },
            {
                'title': 'Testing and Validation',
                'items': [
                    'Automated accessibility testing tools',
                    'Manual testing with assistive technologies',
                    'User testing with people with disabilities',
                    'Regular third-party accessibility audits'
                ]
            },
            {
                'title': 'Feedback and Support',
                'content': 'If you encounter accessibility barriers, please contact accessibility@aiagentsplatform.com for assistance.'
            }
        ]
    }
    
    return render_template('pages/laws/accessibility.html', 
                         accessibility=accessibility_info, 
                         title='Accessibility Compliance')

@compliance_bp.route('/cookies')
def cookies():
    """Cookie Policy and Compliance"""
    cookie_info = {
        'title': 'Cookie Policy',
        'last_updated': '2025-09-09',
        'sections': [
            {
                'title': 'What Are Cookies',
                'content': 'Cookies are small text files stored on your device that help us provide and improve our services.'
            },
            {
                'title': 'Types of Cookies We Use',
                'categories': [
                    {
                        'name': 'Strictly Necessary Cookies',
                        'purpose': 'Essential for website functionality and security',
                        'examples': ['Session management', 'Authentication', 'CSRF protection'],
                        'opt_out': False
                    },
                    {
                        'name': 'Performance Cookies',
                        'purpose': 'Help us understand how visitors interact with our website',
                        'examples': ['Google Analytics', 'Page load metrics', 'Error tracking'],
                        'opt_out': True
                    },
                    {
                        'name': 'Functional Cookies',
                        'purpose': 'Remember your preferences and settings',
                        'examples': ['Language preferences', 'Theme settings', 'Agent preferences'],
                        'opt_out': True
                    },
                    {
                        'name': 'Marketing Cookies',
                        'purpose': 'Deliver relevant advertisements and measure effectiveness',
                        'examples': ['Ad targeting', 'Conversion tracking', 'Social media integration'],
                        'opt_out': True
                    }
                ]
            },
            {
                'title': 'Managing Your Cookie Preferences',
                'content': 'You can manage your cookie preferences through your browser settings or our cookie preference center.'
            }
        ]
    }
    
    return render_template('pages/laws/cookies.html', cookies=cookie_info, title='Cookie Policy')

@compliance_bp.route('/security')
def security():
    """Security Compliance and Measures"""
    security_info = {
        'title': 'Security Measures and Compliance',
        'last_updated': '2025-09-09',
        'certifications': ['SOC 2 Type II', 'ISO 27001', 'GDPR Compliant'],
        'sections': [
            {
                'title': 'Data Encryption',
                'items': [
                    'TLS 1.3 encryption for data in transit',
                    'AES-256 encryption for data at rest',
                    'End-to-end encryption for sensitive communications',
                    'Encrypted database connections and storage'
                ]
            },
            {
                'title': 'Access Controls',
                'items': [
                    'Multi-factor authentication (MFA)',
                    'Role-based access control (RBAC)',
                    'Principle of least privilege',
                    'Regular access reviews and audits'
                ]
            },
            {
                'title': 'Infrastructure Security',
                'items': [
                    'Cloud-native security architecture',
                    'Network segmentation and firewalls',
                    'Intrusion detection and prevention',
                    'Regular security assessments and penetration testing'
                ]
            },
            {
                'title': 'Incident Response',
                'items': [
                    '24/7 security monitoring',
                    'Automated threat detection',
                    'Incident response procedures',
                    'Regular security training for staff'
                ]
            },
            {
                'title': 'Compliance Frameworks',
                'items': [
                    'SOC 2 Type II compliance',
                    'GDPR and CCPA compliance',
                    'PCI DSS for payment processing',
                    'Regular third-party security audits'
                ]
            }
        ]
    }
    
    return render_template('pages/laws/security.html', security=security_info, title='Security Compliance')

@compliance_bp.route('/data-processing')
def data_processing():
    """Data Processing Agreement"""
    dpa_info = {
        'title': 'Data Processing Agreement (DPA)',
        'effective_date': '2025-01-01',
        'last_updated': '2025-09-09',
        'sections': [
            {
                'title': 'Processing Details',
                'items': [
                    'Subject Matter: AI conversation processing and user management',
                    'Duration: For the duration of the service agreement',
                    'Nature and Purpose: Providing AI agent services',
                    'Categories of Data: User account data, conversation logs, usage analytics'
                ]
            },
            {
                'title': 'Data Controller and Processor Obligations',
                'content': 'We act as both data controller and processor depending on the specific processing activity. Clear distinctions are maintained for compliance purposes.'
            },
            {
                'title': 'Sub-processors',
                'items': [
                    'Cloud infrastructure providers (AWS, Google Cloud)',
                    'Authentication services (Keycloak)',
                    'Payment processors (Stripe, PayPal)',
                    'Analytics providers (with data anonymization)'
                ]
            },
            {
                'title': 'International Transfers',
                'content': 'All international data transfers are conducted under appropriate safeguards including Standard Contractual Clauses.'
            }
        ]
    }
    
    return render_template('pages/laws/dpa.html', dpa=dpa_info, title='Data Processing Agreement')

@compliance_bp.route('/api/consent')
def api_consent():
    """API endpoint for consent management"""
    consent_options = {
        'required': [
            {'id': 'essential', 'name': 'Essential Cookies', 'required': True, 'description': 'Necessary for website functionality'},
            {'id': 'service', 'name': 'Service Agreement', 'required': True, 'description': 'Required to use our AI agents'}
        ],
        'optional': [
            {'id': 'analytics', 'name': 'Analytics', 'required': False, 'description': 'Help us improve our services'},
            {'id': 'marketing', 'name': 'Marketing', 'required': False, 'description': 'Receive personalized offers and updates'},
            {'id': 'personalization', 'name': 'Personalization', 'required': False, 'description': 'Customize your experience'}
        ]
    }
    
    return jsonify(consent_options)