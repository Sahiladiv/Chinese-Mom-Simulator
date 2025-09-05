from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from prompt_handling import build_mom_prompt, extract_single, make_prompt_for_emotion
import pandas as pd
from prompt_handling import build_mom_prompt, extract_single, make_prompt_for_emotion

import openai
import time
from tqdm import tqdm

import os
from openai import OpenAI

def falcon_fine_tuned_model():
    # Load base model (i.e. falcon-7b)
    base_model = AutoModelForCausalLM.from_pretrained(
        "tiiuae/falcon-7b",
        torch_dtype="auto",
        device_map="auto"
    )
    # Loading adapter + tokenizer
    model = PeftModel.from_pretrained(base_model, "SahilAdiv/falcon7b-chinese-mom-lora")
    tokenizer = AutoTokenizer.from_pretrained("SahilAdiv/falcon7b-chinese-mom-lora")
    return model, tokenizer


import streamlit as st
st.write("Model loading")
model, tokenizer = falcon_fine_tuned_model()
st.title("Hello Team Veil AI")
user_input = st.text_input("Type some policy:")
if user_input:
    st.success(f"You typed: {user_input}")



import json
my_prompt = "Every school should have chinese learning center"
with open("dataset/chinese_mom_personas.json", "r", encoding="utf-8") as f:
    personas = json.load(f)
focus_group_answer = {} 
for persona in personas:
    prompt_text = build_mom_prompt(persona, my_prompt)
    inputs = tokenizer(prompt_text, return_tensors="pt").to("cuda")
    output = model.generate(
    **inputs,
    max_new_tokens=150,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.2   # >1 discourages repetition
    )

    focus_group_answer[persona['label']] = tokenizer.decode(output[0], skip_special_tokens=True)

rows = []
for persona, text in focus_group_answer.items():
    extracted = extract_single(text)
    rows.append({"persona": persona, "post": extracted["post"], "assistant": extracted["assistant"]})
import pandas as pd
focus_group_df = pd.DataFrame(rows)


OPENAI_API_KEY = "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"
# ---- CONFIG ----
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=openai.api_key)
MODEL = "gpt-4"
DELAY = 1.2 


annotations = []
for i, row in tqdm(focus_group_df.iterrows(), total=len(focus_group_df)):
    try:
        prompt = make_prompt_for_emotion(row['persona'], row['post'], row['assistant'])
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in labeling social emotions and tone."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=500
        )
        result = response.choices[0].message.content
        annotations.append(result)
        time.sleep(DELAY)
    except Exception as e:
        print(f"Error on row {i}: {e}")
        annotations.append("")

focus_group_df['annotations'] = annotations



st.write(focus_group_df)

