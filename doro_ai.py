"""
Dorothy Bot - AI Module
Handles Dorothy's AI responses and sentiment analysis
"""

import aiohttp
import random
from config import doro_patterns, doro_actions, NVIDIA_API_KEY, NVIDIA_API_URL

async def analyze_sentiment(message: str) -> str:
    """Analyze message sentiment using NVIDIA API or fallback"""
    try:
        # Try NVIDIA API first
        if NVIDIA_API_KEY:
            prompt = f"""Analyze sentiment of this message and return ONE word:
happy, sad, confused, angry, scared, excited, neutral, apologetic, sleepy, or curious.

Message: "{message}"

Return only the sentiment word."""

            headers = {
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "meta/llama-3.1-8b-instruct",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": 5
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(NVIDIA_API_URL, json=payload, headers=headers, timeout=2) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        sentiment = data['choices'][0]['message']['content'].strip().lower()
                        if sentiment in doro_patterns:
                            return sentiment
    except:
        pass
    
    # Fallback analysis
    return analyze_simple(message)

def analyze_simple(message: str) -> str:
    """Simple keyword-based sentiment analysis"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["chết", "đánh", "giết", "ngu", "fuck", "damn", "angry", "mad"]):
        return "angry"
    elif any(word in message_lower for word in ["buồn", "khóc", "sad", "cry", "tear"]):
        return "sad"
    elif any(word in message_lower for word in ["sợ", "ma", "scared", "afraid", "fear"]):
        return "scared"
    elif any(word in message_lower for word in ["xin lỗi", "sorry", "apologize"]):
        return "apologetic"
    elif any(word in message_lower for word in ["ngủ", "mệt", "sleep", "tired", "sleepy"]):
        return "sleepy"
    elif any(word in message_lower for word in ["vui", "happy", "haha", "yay", "great", "awesome"]):
        return "happy"
    elif any(word in message_lower for word in ["wow", "amazing", "tuyệt", "incredible", "fantastic"]):
        return "excited"
    elif "?" in message:
        return "curious"
    elif "!" in message:
        return "excited"
    else:
        return "neutral"

def generate_doro_response(sentiment: str, include_action: bool = True) -> str:
    """Generate Doro response based on sentiment"""
    sentiment = sentiment if sentiment in doro_patterns else "neutral"
    
    # Choose response pattern
    response = random.choice(doro_patterns[sentiment])
    
    # 20% chance to add action
    if include_action and random.random() < 0.2:
        action = random.choice(doro_actions[sentiment])
        response = f"{response}\n{action}"
    
    return response
