from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

def falcon_fine_tuned_model()
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