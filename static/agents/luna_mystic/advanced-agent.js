// Advanced Luna Agent Interface
class LunaAgent extends BaseAgent {
    constructor() {
        super();
        this.agentId = "luna_mystic";
        this.agentName = "Luna";
        this.personality = "mystical";
        this.voiceStyle = "mystical";
        this.features = ['tarot_reading', 'astrology', 'meditation_guidance', 'spiritual_advice'];
        this.moods = ['mystical', 'intuitive', 'wise', 'ethereal', 'peaceful', 'enlightened'];
        
        this.initLuna();
    }
    
    initLuna() {
        document.body.classList.add("luna_mystic-mode");
        this.setupPersonalityFeatures();
        this.loadAgentPreferences();
    }
    
    setupPersonalityFeatures() {
        // Personality-specific initialization
        
        this.defaultSettings = {
            responseStyle: 'mystical',
            wisdomLevel: 'deep',
            spiritualGuidance: 'intuitive'
        };
    }
    
    getAgentEmoji() {
        return "🌙";
    }
    
    // Agent-specific methods
    
    async sendSpecializedMessage(message, context) {
        const response = await fetch('/agent/luna_mystic/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                mood: this.currentMood,
                context: context,
                personality: this.personality,
                settings: this.getUserSettings()
            })
        });
        return response.json();
    }
    
    handleSpecializedFeature(featureName) {
        switch(featureName) {
            case 'tarot_reading':
                this.tarotreading();
                break;
            case 'astrology':
                this.astrology();
                break;
            case 'meditation_guidance':
                this.meditationguidance();
                break;
            case 'spiritual_advice':
                this.spiritualadvice();
                break;
            default:
                this.showNotification('Feature coming soon!', 'info');
        }
    }

}

// Initialize agent
let agent;
document.addEventListener('DOMContentLoaded', function() {
    agent = new LunaAgent();
});

// Agent-specific functions

function tarotreading() {
    agent.handleSpecializedFeature('tarot_reading');
}

function astrology() {
    agent.handleSpecializedFeature('astrology');
}

function meditationguidance() {
    agent.handleSpecializedFeature('meditation_guidance');
}

function spiritualadvice() {
    agent.handleSpecializedFeature('spiritual_advice');
}
