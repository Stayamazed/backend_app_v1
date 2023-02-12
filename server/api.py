from .auth_token import auth_token
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

# import torch
# from torch import autocast
# from diffusers import StableDiffusionPipeline
# from io import BytesIO
# import base64 

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

"""device = "cuda"
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)
pipe.to(device)

@app.get("/")
def generate(prompt: str): 
    with autocast(device): 
        image = pipe(prompt, guidance_scale=8.5).images[0]

    image.save("testimage.png")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())

    return Response(content=imgstr, media_type="image/png")"""

@app.get("/")
def generate_image(prompt:str):
    api_url = 'https://stablediffusionapi.com/api/v3/text2img'
    param = {
        "key":auth_token,
        "prompt":prompt,
        "width":"512",
        "height":"512",
        "samples":"1",
        "num_inference_steps":"20",
        "guidance_scale":7.5,
        "safety_checker":"yes"
    }
    headers = {"Content-Type":"application/json"}
    response = requests.post(api_url,data = json.dumps(param),headers=headers)
    # image = response.text.output[0]
    # print(image)
    response_json = response.json()
    image = response_json['output']
    print(image)
    # image = response_json.output[0]
    # print(image)
    return response_json

@app.get("/hello")
def hello_world():
    return "Hello world"
