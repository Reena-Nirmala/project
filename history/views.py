# from django.http import HttpResponse
# from django.shortcuts import render
# from text.models import TextSummary
# from pdf_to_summary.models import PdfDocument

# def history(request):
#     history = TextSummary.objects.filter(user1=request.session.get('user_id'))
#     # print(history[0].input_text)
#     # return HttpResponse("<h1>dfgergv</h1>")
#     pdf_documents = PdfDocument.objects.filter(user1=request.session.get('user_id'))
#     if history:
#         return render(request, 'history.html', {'history': history,'pdf_documents': pdf_documents})
#     else:
#         return render(request,'empty.html')
#     # return TextSummary(history[0].input_text)

from django.shortcuts import render
from text.models import TextSummary
from pdf_to_summary.models import PdfDocument
from grammar_correct.models import GrammarCheck


def history(request):
    # Retrieve TextSummary objects
    text_summaries = TextSummary.objects.filter(user1=request.session.get('user_id'))

    # Retrieve PdfDocument objects
    pdf_documents = PdfDocument.objects.filter(user1=request.session.get('user_id'))

    # Return both types of objects to the template
    grammars = GrammarCheck.objects.filter(user1=request.session.get('user_id'))

    return render(request, 'history.html', {'text_summaries': text_summaries, 'pdf_documents': pdf_documents, 'grammars':grammars})