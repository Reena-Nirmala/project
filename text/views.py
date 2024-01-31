import requests
import pyttsx3
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import TextSummary


def index(request):
    return render(request, 'index.html')


text = ''

@login_required()
def output(request):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    api_token = "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"
    headers = {"Authorization": f"Bearer {api_token}"}

    data = request.POST.get("data")
    max_length = int(request.POST.get("maxL"))
    min_length = max_length // 4

    def query(payload):
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": data,
        "parameters": {"min_length": min_length, "max_length": max_length},
    })[0]

    # return HttpResponse(f'<h1>{output["summary_text"]}</h1>')
    text = output["summary_text"]
    # user = request.user


    # Save the generated summary to the database
    # text_summary = TextSummary.objects.create(
    #     user_id=request.user,
    #     input_text=data,
    #     generated_summary=text
    # )

    user_id = request.session.get('user_id')

    summary = TextSummary(user1=user_id, input_text=data, generated_summary=text)
    summary.save()

    # Create a new summary associated with the user (if available)

    request.session['text_for_speech'] = text
    request.session['summarized_text'] = text

    return render(request, 'index.html', {"result": output["summary_text"],"input" : data})


def texttospeech(request):
    rate = 150
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    text = request.session.get('text_for_speech', '')
    # Use the engine to speak the given text audio
    engine.say(text)
    # Wait for the speech to finish
    engine.runAndWait()
    return render(request, 'index.html', {"result": text})




from django.shortcuts import render
from googletrans import Translator

def language_translator(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language, src='en')
    return translation.text



def translate_summary(request):
    # Ensure 'summarized_text' is present in the session
    summarized_text = request.session.get('summarized_text', '')

    if summarized_text:
        # Get the target language from the request parameters or use 'hi' as default
        target_language = request.GET.get('target_language', 'hi')

        # If summarized_text is not None, proceed with translation
        translated_text = language_translator(summarized_text, target_language)


        # Set the translated text to a new session key
        request.session['translated_text'] = translated_text


        return render(request, 'index.html', {"input": summarized_text, "result": translated_text})
    else:
        # If 'summarized_text' is not present, handle accordingly
        return render(request, 'index.html', {"result": "Summarized text not found in session"})

