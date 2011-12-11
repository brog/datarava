from django.template import Context, loader
from accounts.models import UserProfile, UserProfileForm
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

import logging
logger = logging.getLogger('datarava')

@csrf_protect
@never_cache
@login_required
def index(request):
    user = request.user
    logger.error('GETTING REQUST %s', user)
    logger.error('GETTING UserProfile %s', UserProfile.objects)
    
    try:
        profile = UserProfile.objects.get(user=user)
    except:
        profile = UserProfile.objects.create(user=user)
        logger.error('there is no profile %s', profile)
    #user.get_profile()
    
    logger.error(profile.id)
    UserProfileFormSet = modelformset_factory(UserProfile)
    if request.method == "POST":
        formset = UserProfileForm(request.POST, instance=profile)
        if formset.is_valid():
            formset.save()
    else:
        formset = UserProfileForm(instance=profile)
    
    return render_to_response("accounts/index.html", {
        "formset": formset,
    },  context_instance=RequestContext(request))