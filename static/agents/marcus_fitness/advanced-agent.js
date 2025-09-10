// Advanced Marcus Agent Interface
class MarcusAgent extends BaseAgent {
    constructor() {
        super();
        this.agentId = "marcus_fitness";
        this.agentName = "Marcus";
        this.personality = "energetic";
        this.voiceStyle = "energetic";
        this.features = ['workout_plans', 'nutrition', 'progress_tracking', 'motivation'];
        this.moods = ['energetic', 'motivational', 'challenging', 'supportive', 'intense', 'encouraging'];
        
        this.initMarcus();
    }
    
    initMarcus() {
        document.body.classList.add("marcus_fitness-mode");
        this.setupPersonalityFeatures();
        this.loadAgentPreferences();
    }
    
    setupPersonalityFeatures() {
        // Personality-specific initialization
        
        this.defaultSettings = {
            responseStyle: 'motivational',
            energyLevel: 'high',
            encouragementFrequency: 'frequent'
        };
    }
    
    getAgentEmoji() {
        return "💪";
    }
    
    // Agent-specific methods
    
    async sendSpecializedMessage(message, context) {
        const response = await fetch('/agent/marcus_fitness/chat', {
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
            case 'workout_plans':
                this.workoutplans();
                break;
            case 'nutrition':
                this.nutrition();
                break;
            case 'progress_tracking':
                this.progresstracking();
                break;
            case 'motivation':
                this.motivation();
                break;
            default:
                this.showNotification('Feature coming soon!', 'info');
        }
    }

}

// Initialize agent
let agent;
document.addEventListener('DOMContentLoaded', function() {
    agent = new MarcusAgent();
});

// Agent-specific functions

function workoutplans() {
    agent.handleSpecializedFeature('workout_plans');
}

function nutrition() {
    agent.handleSpecializedFeature('nutrition');
}

function progresstracking() {
    agent.handleSpecializedFeature('progress_tracking');
}

function motivation() {
    agent.handleSpecializedFeature('motivation');
}
