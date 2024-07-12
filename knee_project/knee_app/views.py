from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
from PIL import Image
import tensorflow as tf

GEMINI_KEY = os.environ.get("GEMINI_KEY")
#genai.configure(api_key=GEMINI_KEY)
img_model = tf.keras.models.load_model('modelo.keras')
#model = genai.GenerativeModel('gemini-1.5-flash-latest',system_instruction=f"you are my json interpeter, extract {' '.join(list(dict_cor.keys()))} from the text and return a json format according to these categories: {dict_cor}")

@csrf_exempt
def chatbot_response(request):
    
    
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image = Image.open(image_file)
            tensor = tf.convert_to_tensor(image)
            prediction = img_model.predict(tensor)
            print(prediction)
        # Process the image here
            return JsonResponse({'response': "Image received"}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def generate_response(message):
    #response = model.generate_content(message)
    
    return f""

def chat(request):
    return render(request, 'knee_app/home.html')