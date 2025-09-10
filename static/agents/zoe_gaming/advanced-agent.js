// Advanced Zoe Agent Interface
class ZoeAgent extends BaseAgent {
    constructor() {
        super();
        this.agentId = "zoe_gaming";
        this.agentName = "Zoe";
        this.personality = "competitive";
        this.voiceStyle = "energetic";
        this.features = ['game_strategy', 'skill_improvement', 'team_coordination', 'tournament_prep'];
        this.moods = ['competitive', 'excited', 'strategic', 'playful', 'intense', 'collaborative'];
        
        this.initZoe();
    }
    
    initZoe() {
        document.body.classList.add("zoe_gaming-mode");
        this.setupPersonalityFeatures();
        this.loadAgentPreferences();
    }
    
    setupPersonalityFeatures() {
        // Personality-specific initialization
        
        this.defaultSettings = {
            responseStyle: 'strategic',
            competitiveLevel: 'high',
            trainingIntensity: 'maximum'
        };
    }
    
    getAgentEmoji() {
        return "🎮";
    }
    
    // Agent-specific methods
    
    async sendSpecializedMessage(message, context) {
        const response = await fetch('/agent/zoe_gaming/chat', {
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
            case 'game_strategy':
                this.gamestrategy();
                break;
            case 'skill_improvement':
                this.skillimprovement();
                break;
            case 'team_coordination':
                this.teamcoordination();
                break;
            case 'tournament_prep':
                this.tournamentprep();
                break;
            default:
                this.showNotification('Feature coming soon!', 'info');
        }
    }

}

// Initialize agent
let agent;
document.addEventListener('DOMContentLoaded', function() {
    agent = new ZoeAgent();
});

// Agent-specific functions

function gamestrategy() {
    agent.handleSpecializedFeature('game_strategy');
}

function skillimprovement() {
    agent.handleSpecializedFeature('skill_improvement');
}

function teamcoordination() {
    agent.handleSpecializedFeature('team_coordination');
}

function tournamentprep() {
    agent.handleSpecializedFeature('tournament_prep');
}
