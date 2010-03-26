from coffin import shortcuts
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from models import Result, LapinError

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
                try:
                    result.process()
                except LapinError, exception:
                    return render_to_response('validator/error.html', locals(), request)
                result.save()
                return HttpResponseRedirect(result.get_absolute_url())
            else:
                return index(request)
        else:
            return index(request)
        # elif action == 'upload':
        #     form = ValidateFileForm(request.POST, request.FILES)
        #     # process uploaded file
        #     # form.cleaned_data['file'].file
        
    form = ValidateTextForm(initial={'text': result.input})
    
    return render_to_response('validator/results.html', locals(), request)

def index(request):
    if request.POST:
        return results(request)
    
    forms = {
        'text': ValidateTextForm(),
    }
    
    return render_to_response('validator/index.html', locals(), request)