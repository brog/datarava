# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from sleeprecord.models import Sleeprecord

def index(request):
    sleep_records = Sleeprecord.objects.all()
    t = loader.get_template('sleeprecord/index.html')
    c = Context({
        'sleep_records' : sleep_records, 
    })

    return HttpResponse(t.render(c))