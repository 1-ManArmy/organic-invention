// Advanced Alex Agent Interface
class AlexAgent extends BaseAgent {
    constructor() {
        super();
        this.agentId = "alex_creative";
        this.agentName = "Alex";
        this.personality = "creative";
        this.voiceStyle = "expressive";
        this.features = ['writing_assistance', 'art_generation', 'brainstorming', 'story_creation'];
        this.moods = ['inspiring', 'imaginative', 'artistic', 'whimsical', 'experimental', 'expressive'];
        
        this.initAlex();
    }
    
    initAlex() {
        document.body.classList.add("alex_creative-mode");
        this.setupPersonalityFeatures();
        this.loadAgentPreferences();
    }
    
    setupPersonalityFeatures() {
        // Personality-specific initialization
        
        this.defaultSettings = {
            responseStyle: 'imaginative',
            creativityLevel: 'high',
            inspirationMode: 'continuous'
        };
    }
    
    getAgentEmoji() {
        return "🎨";
    }
    
    // Agent-specific methods
    
    async sendSpecializedMessage(message, context) {
        const response = await fetch('/agent/alex_creative/chat', {
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
            case 'writing_assistance':
                this.writingassistance();
                break;
            case 'art_generation':
                this.artgeneration();
                break;
            case 'brainstorming':
                this.brainstorming();
                break;
            case 'story_creation':
                this.storycreation();
                break;
            default:
                this.showNotification('Feature coming soon!', 'info');
        }
    }

}

// Initialize agent
let agent;
document.addEventListener('DOMContentLoaded', function() {
    agent = new AlexAgent();
});

// Agent-specific functions

function writingassistance() {
    agent.handleSpecializedFeature('writing_assistance');
}

function artgeneration() {
    agent.handleSpecializedFeature('art_generation');
}

function brainstorming() {
    agent.handleSpecializedFeature('brainstorming');
}

function storycreation() {
    agent.handleSpecializedFeature('story_creation');
}
