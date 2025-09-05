# Veil Simulation Prototype – Chinese Mom Personas

## Overview
This repository contains a prototype of Veil’s simulation engine, focused on modeling **Chinese mom personas**.  
We use **Reddit posts on Asian identity and parenting** as training data, fine-tune a **Falcon-7B model with LoRA adapters**, and generate emotionally rich, culturally specific responses.

## Dataset
- **Source**: Reddit posts and comment threads from r/AsianParentStories, r/AsianAmerican, r/Parenting etc.  
- **Why Reddit**: Authentic, first-person, emotionally nuanced reflections.  
- **Limitations**: Overrepresents diaspora children’s voices, underrepresents mothers themselves; primarily English-language.  

## Modeling
- **Base Model**: [Falcon-7B](https://huggingface.co/tiiuae/falcon-7b)  
- **Fine-Tuning**: LoRA adapters for efficiency and scalability. (https://huggingface.co/SahilAdiv/falcon7b-chinese-mom-lora)
- **Output**: Personas that simulate tone, contradiction, and emotional traits (for example: protective, stern, pragmatic).  

## Personas
We define personas through:
- **Identity**: cultural/immigrant context (for example: Cantonese working-class).  
- **Emotional Traits**: protective, critical, warm-through-food.  
- **Contradiction Style**: affection hidden behind critique.  

## Ethical Considerations
- Avoid caricature and stereotypes.  
- Document cultural assumptions explicitly.  
- Supplement Reddit-derived data with bilingual sources for balance.  

## Future Work:
1. **Data Expansion**: Weibo, WeChat, bilingual corpora, oral histories.  
2. **Persona Scaling**: From 5–10 personas to **500+ global personas**.  
3. **Interactive Tools**: Playback, heatmaps, contradiction maps, prescriptive rewrites.  
