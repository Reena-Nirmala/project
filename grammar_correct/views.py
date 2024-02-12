from django.shortcuts import render
from language_tool_python import LanguageTool
from django.http import JsonResponse

def grammar_checker(request):
    if request.method == 'POST':
        input_text = request.POST.get('text_to_check', '')

        # Check grammar in the given text
        tool = LanguageTool('en-US')
        matches = tool.check(input_text)

        # Apply the corrections
        corrected_text = tool.correct(input_text)

        # Return the results as JSON
        response_data = {
            'input_text': input_text,
            'corrections': [{'ruleId': match.ruleId, 'message': match.message, 'replacements': match.replacements} for match in matches],
            'corrected_text': corrected_text,
        }
        user_id = request.session.get('user_id')

        gram_check = GrammarCheck(user1=user_id, input_text=input_text, corrected_text=corrected_text)
        gram_check.save()
        # return JsonResponse(response_data)
        return render(request,'grammar.html',{'result':corrected_text,'input':input_text})

    return render(request, 'grammar.html')
