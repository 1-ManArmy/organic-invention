// Advanced David Agent Interface
class DavidAgent extends BaseAgent {
    constructor() {
        super();
        this.agentId = "david_finance";
        this.agentName = "David";
        this.personality = "analytical";
        this.voiceStyle = "authoritative";
        this.features = ['investment_analysis', 'budgeting', 'market_insights', 'financial_planning'];
        this.moods = ['analytical', 'confident', 'strategic', 'cautious', 'optimistic', 'realistic'];
        
        this.initDavid();
    }
    
    initDavid() {
        document.body.classList.add("david_finance-mode");
        this.setupPersonalityFeatures();
        this.loadAgentPreferences();
    }
    
    setupPersonalityFeatures() {
        // Personality-specific initialization
        
        this.defaultSettings = {
            responseStyle: 'data-driven',
            analysisDepth: 'thorough',
            precisionLevel: 'high'
        };
    }
    
    getAgentEmoji() {
        return "📈";
    }
    
    // Agent-specific methods
    
    async sendSpecializedMessage(message, context) {
        const response = await fetch('/agent/david_finance/chat', {
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
            case 'investment_analysis':
                this.investmentanalysis();
                break;
            case 'budgeting':
                this.budgeting();
                break;
            case 'market_insights':
                this.marketinsights();
                break;
            case 'financial_planning':
                this.financialplanning();
                break;
            default:
                this.showNotification('Feature coming soon!', 'info');
        }
    }

}

// Initialize agent
let agent;
document.addEventListener('DOMContentLoaded', function() {
    agent = new DavidAgent();
});

// Agent-specific functions

function investmentanalysis() {
    agent.handleSpecializedFeature('investment_analysis');
}

function budgeting() {
    agent.handleSpecializedFeature('budgeting');
}

function marketinsights() {
    agent.handleSpecializedFeature('market_insights');
}

function financialplanning() {
    agent.handleSpecializedFeature('financial_planning');
}
