from django.http import HttpResponseRedirect


def redirect_to_form(*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and \
                    kwargs.get('user') is None:
        return HttpResponseRedirect('/form/')


def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        username = request.session.get('saved_username')
    return {'username': username}


def redirect_to_form2(*args, **kwargs):
    user = kwargs['user']
    if (not user.group) and (not kwargs['request'].session.get('saved_group')):
        return HttpResponseRedirect('/form2/')


def group(request, *args, **kwargs):
    if 'saved_group' in request.session:
        user = kwargs['user']
        user.group = request.session.get('saved_group')
        user.save()