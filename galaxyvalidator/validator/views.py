from coffin import shortcuts
from django.template import RequestContext
from django.http import HttpResponse

from models import Result

def render_to_string(template, context, request=None):
    if request:
        context_instance = RequestContext(request)
    else:
        context_instance = None
    return shortcuts.render_to_string(template, context, context_instance)

def render_to_response(template, context={}, request=None, mimetype="text/html"):
    response = render_to_string(template, context, request)
    return HttpResponse(response, mimetype=mimetype)

from forms import *

def results(request, result_id=None):
    if result_id:
        result = Result.objects.get(pk=result_id)
    else:
        action = request.POST.get('action')
        if action == 'text':
            # process text
            form = ValidateTextForm(request.POST)
            if form.is_valid():
                result = Result(input=form.cleaned_data['text'])
                result.output = result.process()
                result.save()
        # elif action == 'upload':
        #     form = ValidateFileForm(request.POST, request.FILES)
        #     # process uploaded file
        #     # form.cleaned_data['file'].file
    return render_to_response('validator/results.html', locals(), request)

def index(request):
    if request.POST:
        return results(request)
    
    forms = {
        'text': ValidateTextForm(),
    }
    
    return render_to_response('validator/index.html', locals(), request)