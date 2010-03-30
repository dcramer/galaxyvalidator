from django.forms.forms import BoundField
from django.template.defaultfilters import escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from jinja2 import Markup

from coffin.shortcuts import render_to_string
from coffin import template
register = template.Library()

def render_form(form, include=None, exclude=None, ordering=None):
    """
    Renders a form using easily stylable, valid XHTML.
    
    Can accept inclusion fields, exclusion fields, and field ordering arguments.
    
    <code>
    {{ myform|render_form(('my', 'fields', 'to', 'include')) }}
    </code>
    """
    kwargs = dict(include=include, exclude=exclude, ordering=ordering)
    normal_row = u'<div id="%(row_id)s" class="formRow %(class_names)s">%(label)s <span class="formField">%(field)s</span>%(help_text_wrapped)s%(errors)s</div>'        
    inline_row = u'<div id="%(row_id)s" class="formRow %(class_names)s"><label><span class="formField">%(field)s</span> %(help_text)s</label>%(errors)s</div>'
    error_row = u'<div class="formRow fInputErrorRow">%s</div>'
    class_prefix = 'f'
    row_ender = '</div>'

    top_errors = form.non_field_errors() # Errors that should be displayed above all fields.
    output, hidden_fields = [], []
    if kwargs['include']:
        if exclude:
            _fields = ((name, field) for name, field in form.fields.iteritems() if name in kwargs['include'] and name not in kwargs['exclude'])
        else:
            _fields = ((name, field) for name, field in form.fields.iteritems() if name in kwargs['include'])
    elif kwargs['exclude']:
        _fields = ((name, field) for name, field in form.fields.iteritems() if name not in kwargs['exclude'])
    else:
        _fields = form.fields.iteritems()
    # Set ordering to include fields if it doesn't exist.
    if not kwargs['ordering'] and include:
        kwargs['ordering'] = include
    if kwargs['ordering']:
        _fields = tuple(_fields)
        _fields_dict = dict(_fields)
        _fields = ((f, _fields_dict[f]) for f in kwargs['ordering'] if f in _fields_dict)

    for name, field in _fields:
        bf = BoundField(form, field, name)
        bf_errors = form.error_class(bf.errors) # Escape and cache in local variable.
        if bf.is_hidden:
            if bf_errors:
                top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
            hidden_fields.append(unicode(bf))
        else:
            if bf.label:
                label_text = escape(force_unicode(bf.label))
                # Only add the suffix if the label does not end in
                # punctuation.
                if form.label_suffix:
                    if label_text[-1] not in ':?.!':
                        label_text += form.label_suffix
            else:
                label_text = ''

            params = {
                'errors': force_unicode(bf_errors),
                'row_id': 'id_%s_wrap' % (name),
                'label': force_unicode(bf.label_tag(label_text) or ''),
                'field': bf,
                'help_text': force_unicode(field.help_text or ''),
                'help_text_wrapped': field.help_text and '<small class="helptext">%s</small>' % field.help_text or '',
            }

            widget = unicode(bf.field.widget.__class__.__name__)
            class_names = [class_prefix + widget + 'Row']
            if field.required:
                class_names.append(class_prefix + 'Required')
            if bf.errors:
                class_names.append(class_prefix + 'Errors')
            params['class_names'] = ' '.join(class_names)

            # XXX: Bad Hack
            if widget in ('CheckboxInput', 'RadioInput') and params['help_text']:
                output.append(inline_row % params)
            else:
                output.append(normal_row % params)
    if top_errors:
        output.insert(0, error_row % force_unicode(top_errors))
    if hidden_fields: # Insert any hidden fields in the last row.
        str_hidden = u''.join(hidden_fields)
        if output:
            last_row = output[-1]
            # Chop off the trailing row_ender (e.g. '</td></tr>') and
            # insert the hidden fields.
            output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
        else:
            # If there aren't any rows in the output, just append the
            # hidden fields.
            output.append(str_hidden)
    return Markup(u'\n'.join(output))
register.filter(render_form, jinja2_only=True)

from django.conf import settings
import os, os.path
def mediaversion(value):
    """Returns the modified time (as a string) for the media"""
    try:
        fname = os.path.abspath(os.path.join(settings.MEDIA_ROOT, value))
        if not fname.startswith(settings.PROJECT_ROOT):
            raise ValueError("Media must be located within MEDIA_ROOT.")
        return unicode(int(os.stat(fname).st_mtime))
    except OSError:
        return 0
register.object(mediaversion)

def mediaurl(value, arg=None):
    return "%s%s?%s" % (settings.MEDIA_URL, value, mediaversion(value))
register.object(mediaurl)

import subprocess
def get_lapin_version():
    args = [settings.LAPIN_BINARY_PATH, '-v']
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    
    results = p.communicate()
    if results[1]:
        return
    return results[0]