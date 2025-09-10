// Advanced Base Agent Interface JavaScript

class BaseAgent {
    constructor() {
        this.currentMood = 'focused';
        this.currentMode = 'text';
        this.isRecording = false;
        this.isConnected = true;
        this.messageHistory = [];
        this.userSettings = this.loadUserSettings();
        this.voiceRecognition = null;
        this.speechSynthesis = window.speechSynthesis;
        this.recordingTimer = null;
        this.recordingStartTime = null;
        
        this.initializeInterface();
        this.setupEventListeners();
        this.setupVoiceRecognition();
    }

    initializeInterface() {
        // Initialize UI components
        this.updateConnectionStatus();
        this.updateMoodDisplay();
        this.setupFloatingActionButton();
        this.setupSettings();
    }

    setupEventListeners() {
        // Send button
        const sendBtn = document.getElementById('send-btn');
        const messageInput = document.getElementById('message-input');
        
        sendBtn?.addEventListener('click', () => this.sendMessage());
        messageInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Character counter
        messageInput?.addEventListener('input', this.updateCharacterCounter.bind(this));

        // Mode buttons
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchMode(e.target.dataset.mode);
            });
        });

        // Mood buttons
        document.querySelectorAll('.mood-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchMood(e.target.dataset.mood);
            });
        });

        // Voice controls
        document.getElementById('voice-toggle')?.addEventListener('click', this.toggleVoiceMode.bind(this));
        document.getElementById('start-recording')?.addEventListener('click', this.startRecording.bind(this));
        document.getElementById('stop-recording')?.addEventListener('click', this.stopRecording.bind(this));

        // Feature buttons
        document.getElementById('text-mode-btn')?.addEventListener('click', () => this.switchInputMode('text'));
        document.getElementById('voice-mode-btn')?.addEventListener('click', () => this.switchInputMode('voice'));
        document.getElementById('upload-btn')?.addEventListener('click', () => this.switchInputMode('upload'));
        document.getElementById('camera-btn')?.addEventListener('click', () => this.openCamera());

        // Settings
        document.getElementById('settings-btn')?.addEventListener('click', this.toggleSettings.bind(this));
        
        // Export and share
        document.getElementById('export-chat')?.addEventListener('click', this.exportChat.bind(this));
        document.getElementById('clear-chat')?.addEventListener('click', this.clearChat.bind(this));
        document.getElementById('save-session')?.addEventListener('click', this.saveSession.bind(this));
        document.getElementById('share-chat')?.addEventListener('click', this.shareChat.bind(this));

        // File upload
        const fileInput = document.getElementById('file-input');
        const uploadArea = document.getElementById('upload-area');
        
        fileInput?.addEventListener('change', this.handleFileSelect.bind(this));
        uploadArea?.addEventListener('click', () => fileInput?.click());

        // Fullscreen
        document.getElementById('fullscreen-btn')?.addEventListener('click', this.toggleFullscreen.bind(this));

        // Auto-resize textarea
        messageInput?.addEventListener('input', this.autoResizeTextarea.bind(this));
    }

    setupVoiceRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.voiceRecognition = new webkitSpeechRecognition();
            this.voiceRecognition.continuous = false;
            this.voiceRecognition.interimResults = false;
            this.voiceRecognition.lang = 'en-US';

            this.voiceRecognition.onstart = () => {
                this.isRecording = true;
                this.updateRecordingUI();
            };

            this.voiceRecognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('message-input').value = transcript;
                this.updateCharacterCounter();
            };

            this.voiceRecognition.onend = () => {
                this.isRecording = false;
                this.updateRecordingUI();
            };

            this.voiceRecognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.showNotification('Voice recognition error: ' + event.error, 'error');
            };
        }
    }

    setupFloatingActionButton() {
        const mainFab = document.getElementById('main-fab');
        const fabMenu = document.getElementById('fab-menu');

        mainFab?.addEventListener('click', () => {
            fabMenu?.classList.toggle('active');
        });

        // Close FAB menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.floating-actions')) {
                fabMenu?.classList.remove('active');
            }
        });
    }

    setupSettings() {
        // Load saved settings
        const settings = this.loadUserSettings();
        
        // Apply settings to UI
        const responseStyle = document.getElementById('response-style');
        const expertiseLevel = document.getElementById('expertise-level');
        const voiceSpeed = document.getElementById('voice-speed');
        const autoSave = document.getElementById('auto-save');

        if (responseStyle) responseStyle.value = settings.responseStyle || 'detailed';
        if (expertiseLevel) expertiseLevel.value = settings.expertiseLevel || 'intermediate';
        if (voiceSpeed) voiceSpeed.value = settings.voiceSpeed || '1';
        if (autoSave) autoSave.checked = settings.autoSave !== false;

        // Save settings on change
        [responseStyle, expertiseLevel, voiceSpeed, autoSave].forEach(element => {
            element?.addEventListener('change', this.saveUserSettings.bind(this));
        });
    }

    async sendMessage() {
        const input = document.getElementById('message-input');
        const message = input?.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessageToChat(message, 'user');
        input.value = '';
        this.updateCharacterCounter();
        this.autoResizeTextarea();

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send to backend
            const response = await this.sendToAgent(message);
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            // Add AI response
            this.addMessageToChat(response.message, 'ai', response.mood);
            
            // Update mood if changed
            if (response.mood && response.mood !== this.currentMood) {
                this.switchMood(response.mood);
            }

            // Auto-save if enabled
            if (this.userSettings.autoSave) {
                this.saveSession();
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.removeTypingIndicator();
            this.showNotification('Failed to send message. Please try again.', 'error');
        }
    }

    async sendToAgent(message) {
        const response = await fetch(`/agent/${this.agentId}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                mood: this.currentMood,
                mode: this.currentMode,
                settings: this.getUserSettings(),
                history: this.messageHistory.slice(-5) // Last 5 messages for context
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    }

    addMessageToChat(message, sender, mood = null) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message-container ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="message-bubble user-bubble">
                    <p>${this.escapeHtml(message)}</p>
                </div>
                <div class="message-meta">
                    <span class="message-time">${timestamp}</span>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-wrapper">
                    <div class="message-avatar">
                        <img src="/static/agents/${this.agentId}/avatar.jpg" alt="${this.agentName}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                        <div class="avatar-indicator">${this.getAgentEmoji()}</div>
                    </div>
                    <div class="message-content">
                        <div class="message-bubble ai-bubble">
                            <p>${this.parseMessageContent(message)}</p>
                            <div class="message-actions">
                                <button class="action-btn" onclick="agent.playMessage(this)" title="Play Audio">
                                    <i class="fas fa-play"></i>
                                </button>
                                <button class="action-btn" onclick="agent.saveMessage(this)" title="Save Message">
                                    <i class="fas fa-bookmark"></i>
                                </button>
                                <button class="action-btn" onclick="agent.copyMessage(this)" title="Copy">
                                    <i class="fas fa-copy"></i>
                                </button>
                                <button class="action-btn" onclick="agent.analyzeMessage(this)" title="Analyze">
                                    <i class="fas fa-chart-line"></i>
                                </button>
                            </div>
                        </div>
                        <div class="message-meta">
                            <span class="message-time">${timestamp}</span>
                            ${mood ? `<span class="message-mood">${mood}</span>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }

        chatMessages.appendChild(messageDiv);
        
        // Store in history
        this.messageHistory.push({
            message: message,
            sender: sender,
            timestamp: Date.now(),
            mood: mood
        });

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Animate in
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        requestAnimationFrame(() => {
            messageDiv.style.transition = 'all 0.3s ease';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        });
    }

    switchMode(mode) {
        this.currentMode = mode;
        
        // Update UI
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });

        // Show/hide relevant panels
        this.updateModeInterface();
        
        this.showNotification(`Switched to ${mode} mode`, 'success');
    }

    switchMood(mood) {
        this.currentMood = mood;
        
        // Update UI
        document.querySelectorAll('.mood-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mood === mood);
        });

        // Update mood display
        const moodIndicator = document.getElementById('current-mood');
        const moodEmoji = document.getElementById('mood-emoji');
        
        if (moodIndicator) moodIndicator.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
        if (moodEmoji) moodEmoji.textContent = this.getMoodEmoji(mood);

        this.showNotification(`Mood changed to ${mood}`, 'info');
    }

    switchInputMode(inputMode) {
        // Hide all input panels
        document.getElementById('voice-panel')?.style.setProperty('display', 'none');
        document.getElementById('upload-area')?.style.setProperty('display', 'none');
        
        // Update feature buttons
        document.querySelectorAll('.feature-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        switch (inputMode) {
            case 'voice':
                document.getElementById('voice-panel')?.style.setProperty('display', 'block');
                document.getElementById('voice-mode-btn')?.classList.add('active');
                break;
            case 'upload':
                document.getElementById('upload-area')?.style.setProperty('display', 'block');
                document.getElementById('upload-btn')?.classList.add('active');
                break;
            default:
                document.getElementById('text-mode-btn')?.classList.add('active');
        }
    }

    startRecording() {
        if (this.voiceRecognition && !this.isRecording) {
            this.voiceRecognition.start();
            this.recordingStartTime = Date.now();
            this.recordingTimer = setInterval(this.updateRecordingTimer.bind(this), 1000);
        }
    }

    stopRecording() {
        if (this.voiceRecognition && this.isRecording) {
            this.voiceRecognition.stop();
            if (this.recordingTimer) {
                clearInterval(this.recordingTimer);
                this.recordingTimer = null;
            }
        }
    }

    updateRecordingTimer() {
        if (this.recordingStartTime) {
            const elapsed = Math.floor((Date.now() - this.recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            const timerElement = document.getElementById('recording-timer');
            if (timerElement) {
                timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
        }
    }

    updateRecordingUI() {
        const startBtn = document.getElementById('start-recording');
        const stopBtn = document.getElementById('stop-recording');
        const voiceWave = document.getElementById('voice-wave');

        if (this.isRecording) {
            startBtn?.style.setProperty('display', 'none');
            stopBtn?.style.setProperty('display', 'flex');
            voiceWave?.style.setProperty('display', 'flex');
        } else {
            startBtn?.style.setProperty('display', 'flex');
            stopBtn?.style.setProperty('display', 'none');
            voiceWave?.style.setProperty('display', 'none');
        }
    }

    toggleVoiceMode() {
        if (this.currentMode === 'voice') {
            this.switchMode('text');
        } else {
            this.switchMode('voice');
        }
    }

    toggleSettings() {
        const settingsPanel = document.getElementById('settings-panel');
        if (settingsPanel) {
            const isVisible = settingsPanel.style.display !== 'none';
            settingsPanel.style.display = isVisible ? 'none' : 'block';
        }
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    updateCharacterCounter() {
        const input = document.getElementById('message-input');
        const counter = document.getElementById('char-counter');
        
        if (input && counter) {
            const length = input.value.length;
            counter.textContent = length;
            
            // Color code based on length
            if (length > 1800) {
                counter.style.color = '#dc2626';
            } else if (length > 1500) {
                counter.style.color = '#f59e0b';
            } else {
                counter.style.color = '#64748b';
            }
        }
    }

    autoResizeTextarea() {
        const textarea = document.getElementById('message-input');
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
        }
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;

        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'message-container ai-message typing';
        typingDiv.innerHTML = `
            <div class="message-wrapper">
                <div class="message-avatar">
                    <div class="avatar-indicator">${this.getAgentEmoji()}</div>
                </div>
                <div class="message-content">
                    <div class="typing-bubble">
                        <div class="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async exportChat() {
        const exportData = {
            agent: this.agentName,
            agentId: this.agentId,
            timestamp: new Date().toISOString(),
            messages: this.messageHistory,
            settings: this.userSettings
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.agentId}_chat_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showNotification('Chat exported successfully!', 'success');
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history? This action cannot be undone.')) {
            const chatMessages = document.getElementById('chat-messages');
            if (chatMessages) {
                // Keep only welcome message
                const welcomeMessage = chatMessages.querySelector('.welcome-message');
                chatMessages.innerHTML = '';
                if (welcomeMessage) {
                    chatMessages.appendChild(welcomeMessage);
                }
            }
            this.messageHistory = [];
            this.showNotification('Chat cleared', 'info');
        }
    }

    async saveSession() {
        try {
            const sessionData = {
                messages: this.messageHistory,
                settings: this.userSettings,
                mood: this.currentMood,
                mode: this.currentMode,
                timestamp: Date.now()
            };

            const response = await fetch(`/agent/${this.agentId}/save-session`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(sessionData)
            });

            if (response.ok) {
                this.showNotification('Session saved successfully!', 'success');
            } else {
                throw new Error('Failed to save session');
            }
        } catch (error) {
            console.error('Error saving session:', error);
            this.showNotification('Failed to save session', 'error');
        }
    }

    async shareChat() {
        if (navigator.share && this.messageHistory.length > 0) {
            try {
                const chatSummary = `Chat with ${this.agentName} - ${this.messageHistory.length} messages`;
                await navigator.share({
                    title: chatSummary,
                    text: 'Check out my conversation with an AI agent!',
                    url: window.location.href
                });
            } catch (error) {
                console.error('Error sharing:', error);
            }
        } else {
            // Fallback: copy URL
            navigator.clipboard.writeText(window.location.href);
            this.showNotification('Chat URL copied to clipboard!', 'info');
        }
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        if (files.length > 0) {
            this.processFiles(files);
        }
    }

    async processFiles(files) {
        for (const file of files) {
            try {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('agent_id', this.agentId);

                this.showNotification(`Uploading ${file.name}...`, 'info');

                const response = await fetch('/upload-file', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const result = await response.json();
                    this.addMessageToChat(`📎 Uploaded: ${file.name}`, 'user');
                    this.addMessageToChat(result.message, 'ai');
                    this.showNotification(`${file.name} processed successfully!`, 'success');
                } else {
                    throw new Error('Upload failed');
                }
            } catch (error) {
                console.error('File upload error:', error);
                this.showNotification(`Failed to upload ${file.name}`, 'error');
            }
        }
    }

    async openCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            // Implementation for camera functionality
            this.showNotification('Camera access granted', 'success');
            // TODO: Implement camera capture interface
        } catch (error) {
            console.error('Camera access error:', error);
            this.showNotification('Camera access denied', 'error');
        }
    }

    playMessage(button) {
        const messageText = button.closest('.message-bubble').querySelector('p').textContent;
        if (this.speechSynthesis) {
            const utterance = new SpeechSynthesisUtterance(messageText);
            utterance.rate = parseFloat(this.userSettings.voiceSpeed || 1);
            utterance.voice = this.speechSynthesis.getVoices().find(voice => 
                voice.name.includes(this.voiceStyle || 'Google')
            ) || this.speechSynthesis.getVoices()[0];
            
            this.speechSynthesis.speak(utterance);
            
            // Visual feedback
            button.innerHTML = '<i class="fas fa-pause"></i>';
            utterance.onend = () => {
                button.innerHTML = '<i class="fas fa-play"></i>';
            };
        }
    }

    saveMessage(button) {
        const messageText = button.closest('.message-bubble').querySelector('p').textContent;
        const savedMessages = JSON.parse(localStorage.getItem('savedMessages') || '[]');
        savedMessages.push({
            agent: this.agentName,
            message: messageText,
            timestamp: Date.now()
        });
        localStorage.setItem('savedMessages', JSON.stringify(savedMessages));
        this.showNotification('Message saved!', 'success');
    }

    copyMessage(button) {
        const messageText = button.closest('.message-bubble').querySelector('p').textContent;
        navigator.clipboard.writeText(messageText).then(() => {
            this.showNotification('Message copied to clipboard!', 'success');
        });
    }

    analyzeMessage(button) {
        // Implementation for message analysis
        this.showNotification('Analysis feature coming soon!', 'info');
    }

    quickAction(action) {
        switch (action) {
            case 'voice':
                this.toggleVoiceMode();
                break;
            case 'help':
                this.showHelp();
                break;
            case 'settings':
                this.toggleSettings();
                break;
        }
    }

    showHelp() {
        const helpContent = `
            <h3>Quick Help</h3>
            <ul>
                <li><strong>Voice Mode:</strong> Click the microphone to speak</li>
                <li><strong>File Upload:</strong> Drag & drop or click to upload files</li>
                <li><strong>Mood Changes:</strong> Select different moods to change responses</li>
                <li><strong>Export Chat:</strong> Save your conversation as JSON</li>
            </ul>
        `;
        this.showNotification(helpContent, 'info', 5000);
    }

    updateConnectionStatus() {
        // Simulate connection status updates
        setInterval(() => {
            const signalBars = document.querySelectorAll('.signal-bars .bar');
            const strength = Math.floor(Math.random() * 4) + 1;
            
            signalBars.forEach((bar, index) => {
                bar.classList.toggle('active', index < strength);
            });
        }, 5000);
    }

    updateMoodDisplay() {
        const moodIndicator = document.getElementById('current-mood');
        const moodEmoji = document.getElementById('mood-emoji');
        
        if (moodIndicator) moodIndicator.textContent = this.currentMood.charAt(0).toUpperCase() + this.currentMood.slice(1);
        if (moodEmoji) moodEmoji.textContent = this.getMoodEmoji(this.currentMood);
    }

    getUserSettings() {
        return {
            responseStyle: document.getElementById('response-style')?.value || 'detailed',
            expertiseLevel: document.getElementById('expertise-level')?.value || 'intermediate',
            voiceSpeed: document.getElementById('voice-speed')?.value || '1',
            autoSave: document.getElementById('auto-save')?.checked !== false
        };
    }

    loadUserSettings() {
        const saved = localStorage.getItem(`${this.agentId}_settings`);
        return saved ? JSON.parse(saved) : {
            responseStyle: 'detailed',
            expertiseLevel: 'intermediate',
            voiceSpeed: '1',
            autoSave: true
        };
    }

    saveUserSettings() {
        const settings = this.getUserSettings();
        localStorage.setItem(`${this.agentId}_settings`, JSON.stringify(settings));
        this.userSettings = settings;
    }

    showNotification(message, type = 'info', duration = 3000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                ${typeof message === 'string' ? `<p>${message}</p>` : message}
            </div>
            <button class="notification-close">&times;</button>
        `;

        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 1.5rem',
            background: type === 'error' ? '#fee2e2' : type === 'success' ? '#dcfce7' : type === 'warning' ? '#fef3c7' : '#eff6ff',
            border: `1px solid ${type === 'error' ? '#fecaca' : type === 'success' ? '#bbf7d0' : type === 'warning' ? '#fde68a' : '#dbeafe'}`,
            borderRadius: '8px',
            color: type === 'error' ? '#991b1b' : type === 'success' ? '#166534' : type === 'warning' ? '#92400e' : '#1e40af',
            zIndex: '10000',
            maxWidth: '400px',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });

        document.body.appendChild(notification);

        // Animate in
        requestAnimationFrame(() => {
            notification.style.transform = 'translateX(0)';
        });

        // Close button handler
        notification.querySelector('.notification-close').addEventListener('click', () => {
            this.closeNotification(notification);
        });

        // Auto close
        if (duration > 0) {
            setTimeout(() => {
                this.closeNotification(notification);
            }, duration);
        }
    }

    closeNotification(notification) {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    parseMessageContent(message) {
        // Basic markdown-like parsing
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    getMoodEmoji(mood) {
        const moodEmojis = {
            focused: '🎯', helpful: '🤝', analytical: '📊', creative: '💡', detailed: '🔍',
            energetic: '⚡', motivational: '🔥', supportive: '🤗', intense: '💪',
            calming: '🧘', empathetic: '💙', gentle: '🌸', wise: '🦉',
            inspiring: '✨', imaginative: '🌟', artistic: '🎨', whimsical: '🦋',
            confident: '💼', strategic: '♟️', optimistic: '📈', realistic: '💡',
            mystical: '🔮', intuitive: '👁️', peaceful: '☮️', enlightened: '🌟',
            competitive: '🏆', excited: '🎉', playful: '🎮', collaborative: '🤝',
            passionate: '🔥', enthusiastic: '🌟', warm: '🤗'
        };
        return moodEmojis[mood] || '😊';
    }

    getAgentEmoji() {
        // Override in subclasses
        return '🤖';
    }

    updateModeInterface() {
        // Override in subclasses for mode-specific UI changes
    }
}

// Utility functions for drag and drop
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0 && window.agent) {
        window.agent.processFiles(files);
    }
}

// Add drag and drop styles
const dragStyles = `
.upload-zone.drag-over {
    border-color: #3b82f6 !important;
    background: #eff6ff !important;
}

.typing-bubble {
    background: #f1f5f9;
    border-radius: 18px;
    padding: 0.75rem 1rem;
    display: inline-block;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #94a3b8;
    animation: typing-pulse 1.5s infinite;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing-pulse {
    0%, 60%, 100% { opacity: 0.4; transform: scale(1); }
    30% { opacity: 1; transform: scale(1.2); }
}

.notification-content ul {
    margin: 0.5rem 0;
    padding-left: 1rem;
}

.notification-close {
    position: absolute;
    top: 0.5rem;
    right: 0.75rem;
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    color: inherit;
    opacity: 0.7;
}

.notification-close:hover {
    opacity: 1;
}
`;

// Inject drag styles
const styleSheet = document.createElement('style');
styleSheet.textContent = dragStyles;
document.head.appendChild(styleSheet);