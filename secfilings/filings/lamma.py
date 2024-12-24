from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.llms import BaseLLM
import pandas as pd

class LlamaLLM(BaseLLM):
    def __init__(self, model_name="facebook/llama-7b"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def _call(self, prompt: str) -> str:
        # Tokenize input prompt
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        # Generate text from the model
        outputs = self.model.generate(inputs["input_ids"], max_length=100)
        
        # Decode and return the output
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
