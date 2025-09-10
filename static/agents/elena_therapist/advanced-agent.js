// Advanced Elena Agent Interface
class ElenaAgent extends BaseAgent {
    constructor() {
        super();
        this.agentId = "elena_therapist";
        this.agentName = "Elena";
        this.personality = "empathetic";
        this.voiceStyle = "soothing";
        this.features = ['therapy_sessions', 'mood_tracking', 'meditation', 'wellness_plans'];
        this.moods = ['calming', 'empathetic', 'supportive', 'understanding', 'gentle', 'wise'];
        
        this.initElena();
    }
    
    initElena() {
        document.body.classList.add("elena_therapist-mode");
        this.setupPersonalityFeatures();
        this.loadAgentPreferences();
    }
    
    setupPersonalityFeatures() {
        // Personality-specific initialization
        
        this.defaultSettings = {
            responseStyle: 'caring',
            emotionalSupport: 'high',
            listeningMode: 'active'
        };
    }
    
    getAgentEmoji() {
        return "🌱";
    }
    
    // Agent-specific methods
    
    async sendSpecializedMessage(message, context) {
        const response = await fetch('/agent/elena_therapist/chat', {
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
            case 'therapy_sessions':
                this.therapysessions();
                break;
            case 'mood_tracking':
                this.moodtracking();
                break;
            case 'meditation':
                this.meditation();
                break;
            case 'wellness_plans':
                this.wellnessplans();
                break;
            default:
                this.showNotification('Feature coming soon!', 'info');
        }
    }

}

// Initialize agent
let agent;
document.addEventListener('DOMContentLoaded', function() {
    agent = new ElenaAgent();
});

// Agent-specific functions

function therapysessions() {
    agent.handleSpecializedFeature('therapy_sessions');
}

function moodtracking() {
    agent.handleSpecializedFeature('mood_tracking');
}

function meditation() {
    agent.handleSpecializedFeature('meditation');
}

function wellnessplans() {
    agent.handleSpecializedFeature('wellness_plans');
}
