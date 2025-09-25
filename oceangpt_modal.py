import modal
from pydantic import BaseModel

# ---- Modal Setup ----
app = modal.App("oceangpt-7b-app")

# Using an A100 GPU (40GB is enough)
image = modal.Image.debian_slim().pip_install(
    "transformers", "torch", "accelerate", "bitsandbytes", "fastapi", "pydantic"
)


class PromptRequest(BaseModel):
    prompt: str


@app.function(image=image, gpu="A100", timeout=600)
@modal.fastapi_endpoint(method="POST")
def api_endpoint(request: PromptRequest):
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    # Cache model globally so it's not reloaded every call
    global pipe
    if "pipe" not in globals():
        model_name = "zjunlp/OceanGPT-basic-7B-v0.1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            load_in_8bit=True,  # quantized to save GPU memory
        )
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    # Run inference
    out = pipe(request.prompt, max_new_tokens=1000, do_sample=True, temperature=0.7)
    return {"response": out[0]["generated_text"]}
