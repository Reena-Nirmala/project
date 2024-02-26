# views.py
import pyttsx3
import requests
from PyPDF2 import PdfReader
from googletrans import Translator
from .models import PdfDocument


def summarize_pdf_api(pdf_path, pages_to_summarize, api_url, api_token):
    # API call for summarization
    headers = {"Authorization": f"Bearer {api_token}"}

    # Extract text only from the specified page
    # with open(pdf_path, 'rb') as file:
    #     pdf_reader = PdfReader(file)
    #     text = pdf_reader.pages[int(pages_to_summarize) - 1].extract_text()
    pages_range = [int(page) for page in pages_to_summarize.split('-')] if '-' in pages_to_summarize else [int(pages_to_summarize)]

    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        extracted_text = []

        for page_number in pages_range:
            page_index = page_number - 1  # Adjust for 0-based index in PyPDF2
            if 0 <= page_index < len(pdf_reader.pages):
                text = pdf_reader.pages[page_index].extract_text()
                if not text.strip() :
                    return "Empty page"
                else:
                    extracted_text.append(text.strip())
            else:
                # Page not available, handle accordingly
                return "Page not found"
        text= "\n".join(extracted_text)

    max_length = 700  # Adjust as needed

    response = requests.post(api_url, headers=headers, json={
        "inputs": text,
        "parameters": {"min_length": max_length // 4, "max_length": max_length},
    })

    if response.status_code == 200:
        return response.json()[0]["summary_text"]
    else:
        raise Exception(f"Error in API response: {response.text}")

# views.py

from django.http import JsonResponse
from django.shortcuts import render
from .models import PdfDocument

def summarize(request):
    if request.method == 'POST' and request.FILES.get('file-input'):
        pdf_file = request.FILES['file-input']
        pages_to_summarize = request.POST.get('maxL', None)

        try:
            api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            api_token = "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"

            user_id = request.session.get('user_id')

            pdf_document = PdfDocument(user1=user_id,pdf_file=pdf_file, pages_to_summarize=pages_to_summarize)


            pdf_document.save()   

            pdf_path = pdf_document.pdf_file.path

            summarized_text = summarize_pdf_api(pdf_path, pages_to_summarize, api_url, api_token)

            if summarized_text=="Page not found":
                return render(request, 'input.html',{'result':summarized_text})


            # pdf_document = PdfDocument(user1=user_id,pdf_file=pdf_file, pages_to_summarize=pages_to_summarize,summarized_text = summarized_text)
            # # pdf_document.
            # pdf_document.save()
            # Update existing pdf_document object with summarized_text
            pdf_document.summarized_text = summarized_text
            pdf_document.save()

            request.session['text_for_speech'] = summarized_text
            request.session['summarized_text'] = summarized_text

            return render(request, 'input.html', {'result': summarized_text})

        except Exception as e:
            error_message = f"Error processing PDF: {str(e)}"
            return render(request, 'input.html', {'error_message': error_message})

    return render(request, 'input.html')

def texttospeech1(request):
    rate = 150
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    text = request.session.get('text_for_speech', '')
    engine.say(text)
    engine.runAndWait()
    return render(request, 'input.html', {"result": text})


def language_translator1(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language, src='en')
    return translation.text

def translate_summary1(request):
    summarized_text = request.session.get('summarized_text', '')

    if summarized_text:
        target_language = request.GET.get('target_language', 'hi')

        translated_text = language_translator1(summarized_text, target_language)

        request.session['translated_text'] = translated_text

        return render(request, 'input.html', {"input": summarized_text, "result": translated_text})
    else:
        return render(request, 'input.html', {"result": "Summarized text not found in session"})




