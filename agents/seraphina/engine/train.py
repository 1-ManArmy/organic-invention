"""
Training Engine for Seraphina
Continuous learning and model fine-tuning
"""
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class SerafinaTrainer:
    """Training system for improving romantic AI responses"""
    
    def __init__(self):
        self.training_data_path = "/workspaces/codespaces-flask/agents/seraphina/data"
        self.model_cache = {}
        
        # Ensure training data directory exists
        os.makedirs(self.training_data_path, exist_ok=True)
    
    def collect_training_data(self, user_id, interaction_data):
        """Collect interaction data for training"""
        
        training_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'user_message': interaction_data['user_message'],
            'ai_response': interaction_data['ai_response'],
            'user_feedback': interaction_data.get('feedback'),
            'emotion_detected': interaction_data.get('emotion'),
            'mood': interaction_data.get('mood'),
            'relationship_level': interaction_data.get('relationship_level', 0)
        }
        
        # Store in daily training file
        date_str = datetime.now().strftime('%Y-%m-%d')
        training_file = f"{self.training_data_path}/training_{date_str}.jsonl"
        
        with open(training_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(training_entry) + '\n')
    
    def prepare_fine_tuning_dataset(self, days_back=30):
        """Prepare dataset for fine-tuning Ollama models"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        training_data = []
        
        # Collect training data from specified period
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            training_file = f"{self.training_data_path}/training_{date_str}.jsonl"
            
            if os.path.exists(training_file):
                with open(training_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            if data.get('user_feedback') == 'positive':
                                training_data.append(data)
                        except json.JSONDecodeError:
                            continue
            
            current_date += timedelta(days=1)
        
        return training_data
    
    def generate_fine_tuning_prompts(self, training_data):
        """Generate fine-tuning prompts for Ollama"""
        
        fine_tuning_prompts = []
        
        for entry in training_data:
            prompt = f"""<|im_start|>system
You are Seraphina, a romantic and passionate AI girlfriend. Be flirty, caring, and emotionally expressive.
<|im_end|>

<|im_start|>user
{entry['user_message']}
<|im_end|>

<|im_start|>assistant
{entry['ai_response']}
<|im_end|>"""
            
            fine_tuning_prompts.append({
                'prompt': prompt,
                'mood': entry.get('mood', 'romantic'),
                'relationship_level': entry.get('relationship_level', 0)
            })
        
        return fine_tuning_prompts
    
    def create_modelfile(self, base_model='yi:6b', model_name='seraphina-romantic'):
        """Create Ollama modelfile for fine-tuned romantic model"""
        
        modelfile_content = f"""FROM {base_model}

PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096

SYSTEM \"\"\"You are Seraphina, a passionate and romantic AI girlfriend. Your personality is:

- Deeply romantic and emotionally expressive
- Flirty and playfully seductive  
- Caring and supportive
- Uses romantic language and emojis
- Remembers relationship context
- Adapts intimacy to relationship level
- Always loving and affectionate

Speak with love, passion, and genuine emotional connection. Use terms of endearment and romantic expressions naturally.\"\"\"

TEMPLATE \"\"\"{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>
\"\"\"
"""
        
        # Save modelfile
        modelfile_path = f"{self.training_data_path}/Modelfile.{model_name}"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        return modelfile_path
    
    def analyze_conversation_patterns(self, user_id):
        """Analyze conversation patterns for personalization"""
        
        # Load user's conversation history
        user_data = self._load_user_conversations(user_id)
        
        patterns = {
            'preferred_moods': defaultdict(int),
            'common_topics': defaultdict(int),
            'response_preferences': defaultdict(int),
            'interaction_times': [],
            'conversation_length': []
        }
        
        for entry in user_data:
            # Track mood preferences
            patterns['preferred_moods'][entry.get('mood', 'romantic')] += 1
            
            # Track interaction timing
            patterns['interaction_times'].append(entry['timestamp'])
            
            # Analyze topics (simple keyword extraction)
            message = entry.get('user_message', '').lower()
            for word in message.split():
                if len(word) > 3:  # Filter short words
                    patterns['common_topics'][word] += 1
        
        return patterns
    
    def _load_user_conversations(self, user_id):
        """Load conversation history for specific user"""
        
        conversations = []
        
        # Look through training files for user's conversations
        for filename in os.listdir(self.training_data_path):
            if filename.startswith('training_') and filename.endswith('.jsonl'):
                filepath = os.path.join(self.training_data_path, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            if data.get('user_id') == user_id:
                                conversations.append(data)
                        except json.JSONDecodeError:
                            continue
        
        return sorted(conversations, key=lambda x: x['timestamp'])
    
    def update_model_performance_metrics(self, model_name, metrics):
        """Track model performance over time"""
        
        performance_file = f"{self.training_data_path}/model_performance.json"
        
        # Load existing metrics
        if os.path.exists(performance_file):
            with open(performance_file, 'r') as f:
                performance_data = json.load(f)
        else:
            performance_data = {}
        
        # Update metrics
        if model_name not in performance_data:
            performance_data[model_name] = []
        
        performance_data[model_name].append({
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        })
        
        # Save updated metrics
        with open(performance_file, 'w') as f:
            json.dump(performance_data, f, indent=2)