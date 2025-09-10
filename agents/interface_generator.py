"""
Advanced AI Agent Template Generator
Creates personalized agent interfaces based on agent personality and features
"""

class AgentInterfaceGenerator:
    def __init__(self):
        self.agent_themes = {
            'sophia_assistant': {
                'name': 'Sophia',
                'role': 'Professional AI Assistant',
                'primary_color': '#4f46e5',
                'secondary_color': '#7c3aed',
                'accent_color': '#06b6d4',
                'gradient': 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #06b6d4 100%)',
                'personality': 'professional',
                'features': ['document_analysis', 'scheduling', 'research', 'productivity'],
                'moods': ['focused', 'helpful', 'analytical', 'creative', 'detailed', 'efficient'],
                'avatar_icon': '🧠',
                'background_pattern': 'tech',
                'voice_style': 'professional'
            },
            'marcus_fitness': {
                'name': 'Marcus',
                'role': 'Fitness Coach & Trainer',
                'primary_color': '#ef4444',
                'secondary_color': '#f97316',
                'accent_color': '#eab308',
                'gradient': 'linear-gradient(135deg, #ef4444 0%, #f97316 50%, #eab308 100%)',
                'personality': 'energetic',
                'features': ['workout_plans', 'nutrition', 'progress_tracking', 'motivation'],
                'moods': ['energetic', 'motivational', 'challenging', 'supportive', 'intense', 'encouraging'],
                'avatar_icon': '💪',
                'background_pattern': 'fitness',
                'voice_style': 'energetic'
            },
            'elena_therapist': {
                'name': 'Elena',
                'role': 'Mental Health & Wellness Therapist',
                'primary_color': '#10b981',
                'secondary_color': '#06b6d4',
                'accent_color': '#8b5cf6',
                'gradient': 'linear-gradient(135deg, #10b981 0%, #06b6d4 50%, #8b5cf6 100%)',
                'personality': 'empathetic',
                'features': ['therapy_sessions', 'mood_tracking', 'meditation', 'wellness_plans'],
                'moods': ['calming', 'empathetic', 'supportive', 'understanding', 'gentle', 'wise'],
                'avatar_icon': '🌱',
                'background_pattern': 'nature',
                'voice_style': 'soothing'
            },
            'alex_creative': {
                'name': 'Alex',
                'role': 'Creative Writing & Art Assistant',
                'primary_color': '#8b5cf6',
                'secondary_color': '#ec4899',
                'accent_color': '#f59e0b',
                'gradient': 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 50%, #f59e0b 100%)',
                'personality': 'creative',
                'features': ['writing_assistance', 'art_generation', 'brainstorming', 'story_creation'],
                'moods': ['inspiring', 'imaginative', 'artistic', 'whimsical', 'experimental', 'expressive'],
                'avatar_icon': '🎨',
                'background_pattern': 'artistic',
                'voice_style': 'expressive'
            },
            'david_finance': {
                'name': 'David',
                'role': 'Financial Advisor & Investment Guide',
                'primary_color': '#059669',
                'secondary_color': '#0d9488',
                'accent_color': '#0891b2',
                'gradient': 'linear-gradient(135deg, #059669 0%, #0d9488 50%, #0891b2 100%)',
                'personality': 'analytical',
                'features': ['investment_analysis', 'budgeting', 'market_insights', 'financial_planning'],
                'moods': ['analytical', 'confident', 'strategic', 'cautious', 'optimistic', 'realistic'],
                'avatar_icon': '📈',
                'background_pattern': 'finance',
                'voice_style': 'authoritative'
            },
            'luna_mystic': {
                'name': 'Luna',
                'role': 'Mystical Guide & Spiritual Advisor',
                'primary_color': '#7c3aed',
                'secondary_color': '#a855f7',
                'accent_color': '#ec4899',
                'gradient': 'linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%)',
                'personality': 'mystical',
                'features': ['tarot_reading', 'astrology', 'meditation_guidance', 'spiritual_advice'],
                'moods': ['mystical', 'intuitive', 'wise', 'ethereal', 'peaceful', 'enlightened'],
                'avatar_icon': '🌙',
                'background_pattern': 'cosmic',
                'voice_style': 'mystical'
            },
            'zoe_gaming': {
                'name': 'Zoe',
                'role': 'Gaming Companion & Esports Coach',
                'primary_color': '#8b5cf6',
                'secondary_color': '#06b6d4',
                'accent_color': '#10b981',
                'gradient': 'linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #10b981 100%)',
                'personality': 'competitive',
                'features': ['game_strategy', 'skill_improvement', 'team_coordination', 'tournament_prep'],
                'moods': ['competitive', 'excited', 'strategic', 'playful', 'intense', 'collaborative'],
                'avatar_icon': '🎮',
                'background_pattern': 'gaming',
                'voice_style': 'energetic'
            },
            'chef_antonio': {
                'name': 'Chef Antonio',
                'role': 'Culinary Master & Cooking Instructor',
                'primary_color': '#f97316',
                'secondary_color': '#eab308',
                'accent_color': '#ef4444',
                'gradient': 'linear-gradient(135deg, #f97316 0%, #eab308 50%, #ef4444 100%)',
                'personality': 'passionate',
                'features': ['recipe_creation', 'cooking_techniques', 'ingredient_pairing', 'culinary_education'],
                'moods': ['passionate', 'enthusiastic', 'perfectionist', 'creative', 'warm', 'encouraging'],
                'avatar_icon': '👨‍🍳',
                'background_pattern': 'culinary',
                'voice_style': 'warm'
            }
        }

    def generate_agent_interface(self, agent_id):
        """Generate complete agent interface HTML, CSS, and JS"""
        if agent_id not in self.agent_themes:
            raise ValueError(f"Agent {agent_id} not found in themes")
        
        theme = self.agent_themes[agent_id]
        
        html_template = self._generate_html_template(agent_id, theme)
        css_template = self._generate_css_template(agent_id, theme)
        js_template = self._generate_js_template(agent_id, theme)
        
        return {
            'html': html_template,
            'css': css_template,
            'js': js_template
        }

    def _generate_html_template(self, agent_id, theme):
        """Generate HTML template for agent"""
        mood_buttons = self._generate_mood_buttons(theme['moods'])
        feature_cards = self._generate_feature_cards(theme['features'], theme)
        welcome_message = self._get_welcome_message(theme)
        input_interface = self._generate_input_interface(agent_id, theme)
        quick_actions = self._generate_quick_actions(theme)
        
        # Build template without f-strings to avoid Jinja conflicts
        template = '''{% extends "base.html" %}

{% block head %}
<link rel="stylesheet" href="/static/agents/''' + agent_id + '''/advanced-interface.css">
<style>
    body.''' + agent_id + '''-mode {
        background: linear-gradient(135deg, ''' + theme['primary_color'] + '''15, ''' + theme['secondary_color'] + '''10);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
</style>
{% endblock %}

{% block content %}
<!-- Advanced ''' + theme['name'] + ''' Agent Interface -->
<section class="''' + agent_id + '''-hero">
    <div class="container">
        <div class="agent-header">
            <div class="agent-avatar">
                <div class="avatar-container">
                    <div class="avatar-glow"></div>
                    <div class="avatar-image">
                        <img src="/static/agents/''' + agent_id + '''/avatar.jpg" alt="''' + theme['name'] + '''" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                        <i class="avatar-icon">''' + theme['avatar_icon'] + '''</i>
                    </div>
                    <div class="voice-wave-indicator" id="voice-wave" style="display: none;">
                        <span></span><span></span><span></span><span></span><span></span>
                    </div>
                </div>
                <div class="status-indicator online pulse"></div>
            </div>
            <div class="agent-info">
                <h1 class="agent-name">
                    <span class="gradient-text">''' + theme['name'] + '''</span>
                    <span class="agent-emoji">''' + theme['avatar_icon'] + '''</span>
                </h1>
                <p class="agent-role">''' + theme['role'] + '''</p>
                <div class="agent-stats">
                    <div class="stat-item">
                        <span class="stat-label">Sessions:</span>
                        <span class="stat-value" id="session-count">{{ user_profile.session_count or 0 }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Experience Level:</span>
                        <span class="stat-value">{{ user_profile.experience_level or "Beginner" }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Progress:</span>
                        <span class="stat-value">{{ user_profile.progress_level or 0 }}%</span>
                    </div>
                </div>
                <div class="agent-mood">
                    <span class="mood-label">Current Mode:</span>
                    <span class="mood-indicator" id="current-mood">''' + theme['moods'][0].title() + '''</span>
                    <span class="mood-emoji" id="mood-emoji">''' + theme['avatar_icon'] + '''</span>
                </div>
            </div>
            <div class="agent-controls">
                <button class="control-btn voice-toggle" id="voice-toggle" title="Toggle Voice Chat">
                    <i class="fas fa-microphone"></i>
                </button>
                <button class="control-btn settings-btn" id="settings-btn" title="Agent Settings">
                    <i class="fas fa-cog"></i>
                </button>
                <button class="control-btn fullscreen-btn" id="fullscreen-btn" title="Fullscreen Mode">
                    <i class="fas fa-expand"></i>
                </button>
            </div>
        </div>
    </div>
</section>

<section class="chat-interface">
    <div class="container">
        <div class="chat-container">
            <!-- Advanced Chat Header -->
            <div class="chat-header">
                <div class="header-top">
                    <div class="connection-status">
                        <div class="signal-bars">
                            <span class="bar active"></span>
                            <span class="bar active"></span>
                            <span class="bar active"></span>
                            <span class="bar active"></span>
                        </div>
                        <span class="connection-text">Connected</span>
                    </div>
                    
                    <div class="chat-tools">
                        <button class="tool-btn" id="export-chat" title="Export Chat History">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="tool-btn" id="clear-chat" title="Clear Chat">
                            <i class="fas fa-trash"></i>
                        </button>
                        <button class="tool-btn" id="save-session" title="Save Session">
                            <i class="fas fa-bookmark"></i>
                        </button>
                        <button class="tool-btn" id="share-chat" title="Share">
                            <i class="fas fa-share"></i>
                        </button>
                    </div>
                </div>
                
                <!-- Mode & Mood Selector -->
                <div class="mode-selector-container">
                    <div class="mood-selector">
                        <span class="selector-label">Mood:</span>
                        ''' + mood_buttons + '''
                    </div>
                    
                    <div class="mode-selector">
                        <span class="selector-label">Mode:</span>
                        <button class="mode-btn active" data-mode="text"><i class="fas fa-keyboard"></i> Text</button>
                        <button class="mode-btn" data-mode="voice"><i class="fas fa-microphone"></i> Voice</button>
                        <button class="mode-btn" data-mode="video"><i class="fas fa-video"></i> Video</button>
                        <button class="mode-btn" data-mode="analysis"><i class="fas fa-chart-line"></i> Analysis</button>
                    </div>
                </div>
                
                <!-- Settings Panel -->
                <div class="settings-panel" id="settings-panel" style="display: none;">
                    <div class="settings-grid">
                        <div class="setting-group">
                            <label>Response Style:</label>
                            <select id="response-style">
                                <option value="detailed" selected>Detailed</option>
                                <option value="concise">Concise</option>
                                <option value="creative">Creative</option>
                                <option value="analytical">Analytical</option>
                            </select>
                        </div>
                        <div class="setting-group">
                            <label>Expertise Level:</label>
                            <select id="expertise-level">
                                <option value="beginner">Beginner</option>
                                <option value="intermediate" selected>Intermediate</option>
                                <option value="advanced">Advanced</option>
                                <option value="expert">Expert</option>
                            </select>
                        </div>
                        <div class="setting-group">
                            <label>Voice Speed:</label>
                            <input type="range" min="0.5" max="2" step="0.1" value="1" id="voice-speed">
                        </div>
                        <div class="setting-group">
                            <label>Auto-save Sessions:</label>
                            <input type="checkbox" id="auto-save" checked>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Chat Messages -->
            <div class="chat-messages" id="chat-messages">
                <div class="welcome-message">
                    <div class="welcome-avatar">
                        <img src="/static/agents/''' + agent_id + '''/avatar.jpg" alt="''' + theme['name'] + '''" onerror="this.src='/static/agents/default-avatar.png'">
                        <div class="avatar-indicator">''' + theme['avatar_icon'] + '''</div>
                    </div>
                    <div class="welcome-content">
                        <div class="message-bubble ai-bubble">
                            <p>''' + welcome_message + '''</p>
                            <div class="message-actions">
                                <button class="action-btn" onclick="agent.playMessage(this)" title="Play Audio">
                                    <i class="fas fa-play"></i>
                                </button>
                                <button class="action-btn" onclick="agent.saveMessage(this)" title="Save Message">
                                    <i class="fas fa-bookmark"></i>
                                </button>
                                <button class="action-btn" onclick="agent.analyzeMessage(this)" title="Analyze">
                                    <i class="fas fa-chart-line"></i>
                                </button>
                            </div>
                        </div>
                        <div class="message-meta">
                            <span class="message-time">Just now</span>
                            <span class="message-mood">''' + theme['moods'][0].title() + '''</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Advanced Input Interface -->
            ''' + input_interface + '''
        </div>
    </div>
</section>

<!-- Advanced Features Showcase -->
<section class="''' + agent_id + '''-features">
    <div class="container">
        <h2 class="features-title">''' + theme['avatar_icon'] + ''' Advanced ''' + theme['name'] + ''' Features</h2>
        <div class="features-grid">
            ''' + feature_cards + '''
        </div>
        
        <!-- Quick Actions -->
        <div class="quick-access-panel">
            <h3>Quick Actions</h3>
            <div class="quick-actions">
                ''' + quick_actions + '''
            </div>
        </div>
    </div>
</section>

<!-- Floating Actions -->
<div class="floating-actions">
    <button class="fab main-fab" id="main-fab">
        <i class="fab-icon">''' + theme['avatar_icon'] + '''</i>
    </button>
    <div class="fab-menu" id="fab-menu">
        <button class="fab sub-fab" onclick="agent.quickAction('voice')">
            <i class="fas fa-microphone"></i>
        </button>
        <button class="fab sub-fab" onclick="agent.quickAction('help')">
            <i class="fas fa-question"></i>
        </button>
        <button class="fab sub-fab" onclick="agent.quickAction('settings')">
            <i class="fas fa-cog"></i>
        </button>
    </div>
</div>

<script src="/static/agents/''' + agent_id + '''/advanced-agent.js"></script>
{% endblock %}'''
        
        return template

    def _generate_mood_buttons(self, moods):
        """Generate mood selector buttons"""
        buttons = []
        for i, mood in enumerate(moods):
            emoji = self._get_mood_emoji(mood)
            active_class = 'active' if i == 0 else ''
            buttons.append(f'<button class="mood-btn {active_class}" data-mood="{mood}">{emoji} {mood.title()}</button>')
        return '\n                        '.join(buttons)

    def _generate_feature_cards(self, features, theme):
        """Generate feature cards for the agent"""
        feature_descriptions = {
            'document_analysis': 'Advanced document processing and analysis capabilities',
            'scheduling': 'Smart calendar and appointment management',
            'research': 'Deep web research and information gathering',
            'productivity': 'Workflow optimization and task management',
            'workout_plans': 'Personalized fitness routines and training programs',
            'nutrition': 'Meal planning and nutritional guidance',
            'progress_tracking': 'Detailed fitness progress monitoring',
            'motivation': 'Daily motivation and encouragement',
            'therapy_sessions': 'Professional therapy and counseling support',
            'mood_tracking': 'Emotional state monitoring and analysis',
            'meditation': 'Guided meditation and mindfulness practices',
            'wellness_plans': 'Comprehensive wellness and self-care programs',
            'writing_assistance': 'Creative writing support and editing',
            'art_generation': 'AI-powered art creation and inspiration',
            'brainstorming': 'Creative idea generation and development',
            'story_creation': 'Interactive storytelling and narrative building',
            'investment_analysis': 'Market analysis and investment recommendations',
            'budgeting': 'Personal finance management and budgeting',
            'market_insights': 'Real-time market data and trends',
            'financial_planning': 'Long-term financial strategy and planning',
            'tarot_reading': 'Mystical tarot card readings and interpretations',
            'astrology': 'Astrological insights and horoscope analysis',
            'meditation_guidance': 'Spiritual meditation and inner peace practices',
            'spiritual_advice': 'Life guidance and spiritual wisdom',
            'game_strategy': 'Advanced gaming strategies and tactics',
            'skill_improvement': 'Gaming skill development and training',
            'team_coordination': 'Team play optimization and communication',
            'tournament_prep': 'Competitive gaming preparation and coaching',
            'recipe_creation': 'Custom recipe development and cooking guidance',
            'cooking_techniques': 'Advanced culinary skills and methods',
            'ingredient_pairing': 'Food pairing and flavor combinations',
            'culinary_education': 'Cooking education and technique mastery'
        }
        
        cards = []
        for feature in features:
            emoji = self._get_feature_emoji(feature)
            description = feature_descriptions.get(feature, 'Advanced AI capabilities')
            cards.append(f'''
            <div class="feature-card premium">
                <div class="feature-icon animated">{emoji}</div>
                <h3>{feature.replace('_', ' ').title()}</h3>
                <p>{description}</p>
                <div class="feature-tech">
                    <span class="tech-badge">AI-Powered</span>
                    <span class="tech-badge">Real-time</span>
                </div>
            </div>''')
        
        return '\n            '.join(cards)

    def _generate_input_interface(self, agent_id, theme):
        """Generate input interface based on agent features"""
        placeholder = self._get_input_placeholder(theme)
        return '''
            <div class="chat-input-container">
                <!-- Voice Panel -->
                <div class="voice-panel" id="voice-panel" style="display: none;">
                    <div class="voice-controls">
                        <button class="voice-control-btn" id="start-recording">
                            <i class="fas fa-microphone"></i>
                            <span>Start Recording</span>
                        </button>
                        <button class="voice-control-btn" id="stop-recording" style="display: none;">
                            <i class="fas fa-stop"></i>
                            <span>Stop Recording</span>
                        </button>
                        <div class="recording-timer" id="recording-timer">00:00</div>
                    </div>
                    <div class="voice-visualizer">
                        <canvas id="voice-canvas" width="300" height="100"></canvas>
                    </div>
                </div>
                
                <!-- Upload Area -->
                <div class="upload-area" id="upload-area" style="display: none;">
                    <div class="upload-zone" ondrop="handleDrop(event)" ondragover="handleDragOver(event)">
                        <i class="fas fa-cloud-upload-alt"></i>
                        <p>Drop files here or click to upload</p>
                        <small>Supports: Images, Documents, Audio, Video files</small>
                        <input type="file" id="file-input" multiple accept="*" style="display: none;">
                    </div>
                </div>
                
                <!-- Main Input -->
                <div class="main-input-area">
                    <div class="input-wrapper">
                        <div class="text-input-container">
                            <textarea id="message-input" 
                                    placeholder="''' + placeholder + '''" 
                                    rows="1" 
                                    maxlength="2000"></textarea>
                            <div class="input-counter">
                                <span id="char-counter">0</span>/2000
                            </div>
                        </div>
                        <button id="send-btn" class="send-btn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
                
                <!-- Feature Toolbar -->
                <div class="feature-toolbar">
                    <div class="toolbar-section">
                        <button class="feature-btn active" id="text-mode-btn" title="Text Mode">
                            <i class="fas fa-keyboard"></i>
                        </button>
                        <button class="feature-btn" id="voice-mode-btn" title="Voice Mode">
                            <i class="fas fa-microphone"></i>
                        </button>
                        <button class="feature-btn" id="upload-btn" title="Upload Files">
                            <i class="fas fa-paperclip"></i>
                        </button>
                        <button class="feature-btn" id="camera-btn" title="Camera">
                            <i class="fas fa-camera"></i>
                        </button>
                    </div>
                    
                    <div class="toolbar-section">
                        <button class="feature-btn" id="emoji-btn" title="Emojis">
                            <i class="fas fa-smile"></i>
                        </button>
                        <button class="feature-btn" id="analysis-btn" title="Analysis Mode">
                            <i class="fas fa-chart-line"></i>
                        </button>
                        <button class="feature-btn" id="export-btn" title="Export">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
            </div>'''

    def _generate_quick_actions(self, theme):
        """Generate quick action buttons based on agent type"""
        actions = {
            'professional': [
                ('<i class="fas fa-file-alt"></i><span>Analyze Document</span>', 'analyzeDocument()'),
                ('<i class="fas fa-calendar"></i><span>Schedule Meeting</span>', 'scheduleMeeting()'),
                ('<i class="fas fa-search"></i><span>Research Topic</span>', 'researchTopic()'),
                ('<i class="fas fa-tasks"></i><span>Create Plan</span>', 'createPlan()')
            ],
            'energetic': [
                ('<i class="fas fa-dumbbell"></i><span>Start Workout</span>', 'startWorkout()'),
                ('<i class="fas fa-chart-line"></i><span>Track Progress</span>', 'trackProgress()'),
                ('<i class="fas fa-apple-alt"></i><span>Nutrition Plan</span>', 'nutritionPlan()'),
                ('<i class="fas fa-trophy"></i><span>Set Goals</span>', 'setGoals()')
            ],
            'empathetic': [
                ('<i class="fas fa-heart"></i><span>Mood Check</span>', 'moodCheck()'),
                ('<i class="fas fa-leaf"></i><span>Meditation</span>', 'startMeditation()'),
                ('<i class="fas fa-comments"></i><span>Talk Session</span>', 'talkSession()'),
                ('<i class="fas fa-spa"></i><span>Wellness Plan</span>', 'wellnessPlan()')
            ],
            'creative': [
                ('<i class="fas fa-pen"></i><span>Start Writing</span>', 'startWriting()'),
                ('<i class="fas fa-palette"></i><span>Generate Art</span>', 'generateArt()'),
                ('<i class="fas fa-lightbulb"></i><span>Brainstorm</span>', 'brainstorm()'),
                ('<i class="fas fa-book"></i><span>Create Story</span>', 'createStory()')
            ],
            'analytical': [
                ('<i class="fas fa-chart-pie"></i><span>Market Analysis</span>', 'marketAnalysis()'),
                ('<i class="fas fa-calculator"></i><span>Budget Plan</span>', 'budgetPlan()'),
                ('<i class="fas fa-coins"></i><span>Investment Advice</span>', 'investmentAdvice()'),
                ('<i class="fas fa-piggy-bank"></i><span>Save Money</span>', 'saveMoney()')
            ],
            'mystical': [
                ('<i class="fas fa-eye"></i><span>Tarot Reading</span>', 'tarotReading()'),
                ('<i class="fas fa-star"></i><span>Astrology</span>', 'astrology()'),
                ('<i class="fas fa-om"></i><span>Spiritual Guide</span>', 'spiritualGuide()'),
                ('<i class="fas fa-crystal-ball"></i><span>Divine Insight</span>', 'divineInsight()')
            ],
            'competitive': [
                ('<i class="fas fa-gamepad"></i><span>Game Strategy</span>', 'gameStrategy()'),
                ('<i class="fas fa-target"></i><span>Skill Training</span>', 'skillTraining()'),
                ('<i class="fas fa-users"></i><span>Team Tactics</span>', 'teamTactics()'),
                ('<i class="fas fa-medal"></i><span>Tournament Prep</span>', 'tournamentPrep()')
            ],
            'passionate': [
                ('<i class="fas fa-utensils"></i><span>Create Recipe</span>', 'createRecipe()'),
                ('<i class="fas fa-fire"></i><span>Cooking Tips</span>', 'cookingTips()'),
                ('<i class="fas fa-seedling"></i><span>Ingredient Guide</span>', 'ingredientGuide()'),
                ('<i class="fas fa-chef-hat"></i><span>Master Technique</span>', 'masterTechnique()')
            ]
        }
        
        personality_actions = actions.get(theme['personality'], actions['professional'])
        action_buttons = []
        
        for content, onclick in personality_actions:
            action_buttons.append(f'''
                <button class="quick-action-btn" onclick="{onclick}">
                    {content}
                </button>''')
        
        return '\n                '.join(action_buttons)

    def _get_welcome_message(self, theme):
        """Generate personalized welcome message"""
        messages = {
            'professional': f"Hello! I'm {theme['name']}, your professional AI assistant. I'm here to help you boost your productivity, analyze documents, and tackle complex tasks with precision and efficiency. What can I help you accomplish today?",
            'energetic': f"Hey there! I'm {theme['name']}, your personal fitness coach! 💪 Ready to crush your fitness goals? Whether you want to build muscle, lose weight, or improve your performance, I'm here to push you to your limits and beyond!",
            'empathetic': f"Welcome, dear soul. I'm {theme['name']}, your wellness therapist and emotional guide. 🌱 This is a safe space where you can share your thoughts, feelings, and experiences. I'm here to listen, support, and help you on your journey to mental wellness.",
            'creative': f"Greetings, creative spirit! I'm {theme['name']}, your artistic muse and writing companion. ✨ Together, we'll explore the boundless realms of imagination, craft compelling stories, and bring your creative visions to life!",
            'analytical': f"Good day! I'm {theme['name']}, your financial advisor and analytical expert. 📊 I'm here to help you make smart financial decisions, analyze market trends, and build a secure financial future. Let's discuss your financial goals!",
            'mystical': f"Blessed be, seeker of wisdom. I am {theme['name']}, your mystical guide through the ethereal realms. 🌙 The universe has aligned to bring us together. What spiritual insights or divine guidance do you seek today?",
            'competitive': f"What's up, gamer! I'm {theme['name']}, your esports coach and gaming strategist! 🎮 Ready to level up your skills and dominate the competition? Let's analyze your gameplay and develop winning strategies!",
            'passionate': f"Buongiorno! I'm {theme['name']}, your passionate culinary master! 👨‍🍳 Welcome to my kitchen where we'll create magnificent dishes, master cooking techniques, and explore the beautiful art of gastronomy together!"
        }
        
        return messages.get(theme['personality'], f"Hello! I'm {theme['name']}, ready to assist you with expertise and care.")

    def _get_input_placeholder(self, theme):
        """Generate placeholder text for input based on personality"""
        placeholders = {
            'professional': "What task can I help you with today?",
            'energetic': "Ready to get moving? Tell me your fitness goals! 💪",
            'empathetic': "Share what's on your heart... I'm here to listen 🌱",
            'creative': "What story shall we weave together today? ✨",
            'analytical': "What financial question can I analyze for you? 📊",
            'mystical': "What wisdom do you seek from the universe? 🌙",
            'competitive': "Ready to dominate? What game are we strategizing? 🎮",
            'passionate': "What delicious creation shall we cook up? 👨‍🍳"
        }
        
        return placeholders.get(theme['personality'], "How can I assist you today?")

    def _get_mood_emoji(self, mood):
        """Get emoji for mood"""
        mood_emojis = {
            'focused': '🎯', 'helpful': '🤝', 'analytical': '📊', 'creative': '💡', 'detailed': '🔍', 'efficient': '⚡',
            'energetic': '⚡', 'motivational': '🔥', 'challenging': '💪', 'supportive': '🤗', 'intense': '⚡', 'encouraging': '👏',
            'calming': '🧘', 'empathetic': '💙', 'understanding': '🤗', 'gentle': '🌸', 'wise': '🦉',
            'inspiring': '✨', 'imaginative': '🌟', 'artistic': '🎨', 'whimsical': '🦋', 'experimental': '🧪', 'expressive': '🎭',
            'confident': '💼', 'strategic': '♟️', 'cautious': '⚠️', 'optimistic': '📈', 'realistic': '💡',
            'mystical': '🔮', 'intuitive': '👁️', 'ethereal': '✨', 'peaceful': '☮️', 'enlightened': '🌟',
            'competitive': '🏆', 'excited': '🎉', 'playful': '🎮', 'collaborative': '🤝',
            'passionate': '🔥', 'enthusiastic': '🌟', 'perfectionist': '👨‍🍳', 'warm': '🤗'
        }
        return mood_emojis.get(mood, '😊')

    def _get_feature_emoji(self, feature):
        """Get emoji for feature"""
        feature_emojis = {
            'document_analysis': '📄', 'scheduling': '📅', 'research': '🔍', 'productivity': '⚡',
            'workout_plans': '💪', 'nutrition': '🥗', 'progress_tracking': '📈', 'motivation': '🔥',
            'therapy_sessions': '🛋️', 'mood_tracking': '📊', 'meditation': '🧘', 'wellness_plans': '🌱',
            'writing_assistance': '✍️', 'art_generation': '🎨', 'brainstorming': '💡', 'story_creation': '📚',
            'investment_analysis': '📊', 'budgeting': '💰', 'market_insights': '📈', 'financial_planning': '🏦',
            'tarot_reading': '🔮', 'astrology': '⭐', 'meditation_guidance': '🧘', 'spiritual_advice': '🌙',
            'game_strategy': '🎮', 'skill_improvement': '🎯', 'team_coordination': '👥', 'tournament_prep': '🏆',
            'recipe_creation': '📝', 'cooking_techniques': '👨‍🍳', 'ingredient_pairing': '🌿', 'culinary_education': '🍳'
        }
        return feature_emojis.get(feature, '⚡')

    def _generate_css_template(self, agent_id, theme):
        """Generate CSS template for agent"""
        background_pattern = self._get_background_pattern(theme['background_pattern'])
        agent_styles = self._get_agent_specific_styles(agent_id, theme)
        
        template = '''/* Advanced ''' + theme['name'] + ''' Agent Styles */
:root {
    --''' + agent_id + '''-primary: ''' + theme['primary_color'] + ''';
    --''' + agent_id + '''-secondary: ''' + theme['secondary_color'] + ''';
    --''' + agent_id + '''-accent: ''' + theme['accent_color'] + ''';
    --''' + agent_id + '''-gradient: ''' + theme['gradient'] + ''';
    --''' + agent_id + '''-shadow: 0 10px 30px ''' + theme['primary_color'] + '''30;
    --''' + agent_id + '''-glow: 0 0 20px ''' + theme['primary_color'] + '''50;
}

.''' + agent_id + '''-hero {
    background: var(--''' + agent_id + '''-gradient);
    padding: 60px 0 40px;
    color: white;
    position: relative;
    overflow: hidden;
    min-height: 200px;
}

.''' + agent_id + '''-hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: ''' + background_pattern + ''';
    animation: float 20s infinite linear;
    opacity: 0.1;
}

.''' + agent_id + '''-features {
    padding: 60px 0;
    background: linear-gradient(135deg, ''' + theme['primary_color'] + '''08, ''' + theme['secondary_color'] + '''05);
}

/* Agent-specific customizations */
''' + agent_styles + '''

/* Import common advanced styles */
@import url('/static/agents/common/advanced-base.css');
'''
        
        return template

    def _generate_js_template(self, agent_id, theme):
        """Generate JavaScript template for agent"""
        features_js = str(theme['features'])
        moods_js = str(theme['moods'])
        personality_js = self._get_personality_js(theme)
        agent_methods = self._get_agent_methods(agent_id, theme)
        agent_functions = self._get_agent_functions(agent_id, theme)
        
        template = '''// Advanced ''' + theme['name'] + ''' Agent Interface
class ''' + theme['name'] + '''Agent extends BaseAgent {
    constructor() {
        super();
        this.agentId = "''' + agent_id + '''";
        this.agentName = "''' + theme['name'] + '''";
        this.personality = "''' + theme['personality'] + '''";
        this.voiceStyle = "''' + theme['voice_style'] + '''";
        this.features = ''' + features_js + ''';
        this.moods = ''' + moods_js + ''';
        
        this.init''' + theme['name'] + '''();
    }
    
    init''' + theme['name'] + '''() {
        document.body.classList.add("''' + agent_id + '''-mode");
        this.setupPersonalityFeatures();
        this.loadAgentPreferences();
    }
    
    setupPersonalityFeatures() {
        // Personality-specific initialization
        ''' + personality_js + '''
    }
    
    getAgentEmoji() {
        return "''' + theme['avatar_icon'] + '''";
    }
    
    // Agent-specific methods
    ''' + agent_methods + '''
}

// Initialize agent
let agent;
document.addEventListener('DOMContentLoaded', function() {
    agent = new ''' + theme['name'] + '''Agent();
});

// Agent-specific functions
''' + agent_functions + '''
'''
        
        return template

    def _get_background_pattern(self, pattern_type):
        """Get background pattern based on type"""
        patterns = {
            'tech': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"20\" cy=\"30\" r=\"2\" fill=\"white\"/><circle cx=\"70\" cy=\"20\" r=\"1.5\" fill=\"white\"/></svg>')",
            'fitness': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><rect x=\"10\" y=\"40\" width=\"80\" height=\"20\" fill=\"white\" opacity=\"0.3\"/></svg>')",
            'nature': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><path d=\"M20,80 Q30,60 40,80 Q50,60 60,80\" stroke=\"white\" fill=\"none\"/></svg>')",
            'artistic': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><polygon points=\"50,20 60,40 40,40\" fill=\"white\" opacity=\"0.3\"/></svg>')",
            'finance': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><polyline points=\"20,80 40,60 60,70 80,40\" stroke=\"white\" fill=\"none\"/></svg>')",
            'cosmic': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"30\" cy=\"40\" r=\"3\" fill=\"white\" opacity=\"0.6\"/><circle cx=\"70\" cy=\"60\" r=\"2\" fill=\"white\" opacity=\"0.4\"/></svg>')",
            'gaming': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><rect x=\"30\" y=\"30\" width=\"40\" height=\"40\" fill=\"white\" opacity=\"0.2\"/></svg>')",
            'culinary': "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"15\" fill=\"none\" stroke=\"white\" opacity=\"0.3\"/></svg>')"
        }
        return patterns.get(pattern_type, patterns['tech'])

    def _get_agent_specific_styles(self, agent_id, theme):
        """Get agent-specific CSS styles"""
        return f'''
.{agent_id}-mode .feature-btn:hover {{
    border-color: var(--{agent_id}-primary);
    background: var(--{agent_id}-primary);
    color: white;
}}

.{agent_id}-mode .send-btn {{
    background: var(--{agent_id}-gradient);
}}

.{agent_id}-mode .mood-btn.active {{
    background: var(--{agent_id}-primary);
}}
'''

    def _get_personality_js(self, theme):
        """Get personality-specific JavaScript"""
        personality_configs = {
            'professional': '''
        this.defaultSettings = {
            responseStyle: 'detailed',
            formalityLevel: 'professional',
            analysisDepth: 'comprehensive'
        };''',
            'energetic': '''
        this.defaultSettings = {
            responseStyle: 'motivational',
            energyLevel: 'high',
            encouragementFrequency: 'frequent'
        };''',
            'empathetic': '''
        this.defaultSettings = {
            responseStyle: 'caring',
            emotionalSupport: 'high',
            listeningMode: 'active'
        };''',
            'creative': '''
        this.defaultSettings = {
            responseStyle: 'imaginative',
            creativityLevel: 'high',
            inspirationMode: 'continuous'
        };''',
            'analytical': '''
        this.defaultSettings = {
            responseStyle: 'data-driven',
            analysisDepth: 'thorough',
            precisionLevel: 'high'
        };''',
            'mystical': '''
        this.defaultSettings = {
            responseStyle: 'mystical',
            wisdomLevel: 'deep',
            spiritualGuidance: 'intuitive'
        };''',
            'competitive': '''
        this.defaultSettings = {
            responseStyle: 'strategic',
            competitiveLevel: 'high',
            trainingIntensity: 'maximum'
        };''',
            'passionate': '''
        this.defaultSettings = {
            responseStyle: 'enthusiastic',
            passionLevel: 'high',
            expertiseSharing: 'detailed'
        };'''
        }
        return personality_configs.get(theme['personality'], personality_configs['professional'])

    def _get_agent_methods(self, agent_id, theme):
        """Get agent-specific methods"""
        return f'''
    async sendSpecializedMessage(message, context) {{
        const response = await fetch('/agent/{agent_id}/chat', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                message: message,
                mood: this.currentMood,
                context: context,
                personality: this.personality,
                settings: this.getUserSettings()
            }})
        }});
        return response.json();
    }}
    
    handleSpecializedFeature(featureName) {{
        switch(featureName) {{
            {self._get_feature_cases(theme['features'])}
            default:
                this.showNotification('Feature coming soon!', 'info');
        }}
    }}
'''

    def _get_feature_cases(self, features):
        """Generate switch cases for features"""
        cases = []
        for feature in features:
            cases.append(f'''case '{feature}':
                this.{feature.replace('_', '')}();
                break;''')
        return '\n            '.join(cases)

    def _get_agent_functions(self, agent_id, theme):
        """Get agent-specific global functions"""
        functions = []
        for feature in theme['features']:
            function_name = feature.replace('_', '').lower()
            functions.append(f'''
function {function_name}() {{
    agent.handleSpecializedFeature('{feature}');
}}''')
        
        return '\n'.join(functions)

# Usage example:
generator = AgentInterfaceGenerator()

def create_agent_interface(agent_id):
    """Create complete agent interface files"""
    try:
        interface_data = generator.generate_agent_interface(agent_id)
        
        # Create directory structure
        import os
        agent_dir = f'/workspaces/codespaces-flask/agents/{agent_id}'
        os.makedirs(f'{agent_dir}/templates', exist_ok=True)
        os.makedirs(f'/workspaces/codespaces-flask/static/agents/{agent_id}', exist_ok=True)
        
        # Write HTML template
        with open(f'{agent_dir}/templates/{agent_id}.html', 'w') as f:
            f.write(interface_data['html'])
        
        # Write CSS file
        with open(f'/workspaces/codespaces-flask/static/agents/{agent_id}/advanced-interface.css', 'w') as f:
            f.write(interface_data['css'])
        
        # Write JS file  
        with open(f'/workspaces/codespaces-flask/static/agents/{agent_id}/advanced-agent.js', 'w') as f:
            f.write(interface_data['js'])
        
        print(f"✅ Created advanced interface for {agent_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating interface for {agent_id}: {str(e)}")
        return False