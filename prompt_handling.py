import json
import re
from typing import List, Dict

def build_mom_prompt(persona, child_post):
    """
    Build a roleplay prompt for a given Chinese mom persona (already loaded dict).
    """
    prompt = f"""
    <|system|>
    You are roleplaying as a Chinese mom with the following personality:

    {persona['identity_profile']}

    Emotional traits: {", ".join(persona['emotional_traits'])}
    Tone: {", ".join(persona['tone_tags'])}
    Contradiction style: {persona['contradiction_style']}

    Rules:
    - Always stay in character.
    - Respond as if speaking directly to your child.
    - Use the tone tags in your phrasing (e.g., blunt vs poetic).
    - Show affection, pride, or disappointment through the contradiction style.
    </|system|>

    <|user|> POST: {child_post}<|assistant|>
    """
    return prompt.strip()
    
    
def extract_single(text: str) -> Dict[str, str]:
    """
    Extract one POST and ASSISTANT from text.
    Raises ValueError if not found.
    """

    SINGLE_BLOCK_RE = re.compile(
    r"<\|user\|>\s*POST:\s*(?P<post>.*?)\s*<\|assistant\|>\s*(?P<assistant>.*)\Z",
    re.DOTALL
    )
    m = SINGLE_BLOCK_RE.search(text)
    if not m:
        raise ValueError("No single ChatML block found.")
    return {
        "post": m.group("post").strip(),
        "assistant": m.group("assistant").strip()
    }
    
    
def make_prompt_for_emotion(title, post, answer):
    return f"""
    You are a social simulation analyst. Given a Reddit post, label the following:
    
    1. Emotion scores (range 0.0 - 1.0) for: guilt, shame, love, anger, anxiety, pride, disappointment
    2. Tone tags (2 - 5 words, like: blunt, caring, sarcastic, evasive, guilt-tripping)
    3. Contradiction flag: true or false
    4. Reason for contradiction (if true)
    
    Return the output in this JSON format:
    
    {{
      "emotions": {{}},
      "tone": [],
      "contradiction": {{
        "flag": true/false,
        "reason": "..."
      }}
    }}
    
    POST:
    {post}
    
    TOP COMMENTS:
    {answer}
    """.strip()