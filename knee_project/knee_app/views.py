from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
from PIL import Image
import tensorflow as tf
import numpy as np
import json
from dotenv import load_dotenv
load_dotenv()

print(os.getcwd())
recomendations = json.load(open('recomendations.json',"r", encoding="utf8"))
GEMINI_KEY = os.getenv("GEMINI_KEY")

categories = ["doubtful", "mild", "moderate","normal", "severe"]
genai.configure(api_key=GEMINI_KEY)
img_model = tf.keras.applications.ResNet50(weights='imagenet')
text_model = genai.GenerativeModel('gemini-1.5-flash-latest',system_instruction=f"You are a doctor assistant to knee arthritis detection, you receive a diagnostic that can be ['doubtful', 'mild', 'moderate', 'severe','normal'] and a probability of the diagnostic. Redact a message indicating the possible diagnostic according to the given categories, the probability and the next steps to follow in spanish without bold font.")

@csrf_exempt
def chatbot_response(request):
    
    
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image = Image.open(image_file)
            res_image = image.resize((224, 224))
            
            tensor = tf.convert_to_tensor(res_image)
            prediction = img_model.predict(tensor[tf.newaxis, ...],verbose=0).flatten()[:5]
            relevant_information = generate_response({"prediction":categories[np.argmax(prediction)],"probability":np.max(prediction),"recomendations":recomendations[categories[np.argmax(prediction)]]["recomendations"]})
            message = generate_response(relevant_information)
            return JsonResponse({'response': f"{message}"}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def generate_response(information):
    prompt = f"{information}"
    response = text_model.generate_content(prompt).to_dict()["candidates"][0]["content"]["parts"][0]["text"]
    
    return response

def chat(request):
    return render(request, 'knee_app/home.html')