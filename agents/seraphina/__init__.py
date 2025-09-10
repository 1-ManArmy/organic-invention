# Seraphina - AI Girlfriend Agent
# Advanced romantic AI companion with emotion engine and memory system
# Powered by specialized models for intimate and flirty interactions

from .routes import seraphina_bp
from .logic import SerafinaEngine
from .engine.romantic_ai import RomanticPersonality
from .memory.emotional_memory import EmotionalMemory

__all__ = ['seraphina_bp', 'SerafinaEngine', 'RomanticPersonality', 'EmotionalMemory']