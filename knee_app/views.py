from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pickle
import google.generativeai as genai
import os

region_model = pickle.load(open(os.path.join("","model.pkl"), 'rb'))


GEMINI_KEY = os.environ.get("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel('gemini-1.5-flash-latest',system_instruction=f"you are my json interpeter, extract {' '.join(list(dict_cor.keys()))} from the text and return a json format according to these categories: {dict_cor}")

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        response = generate_response(user_message)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def generate_response(message):
    response = model.generate_content(message)
    
    return f""

def chat(request):
    return render(request, 'deploy_app/home.html')