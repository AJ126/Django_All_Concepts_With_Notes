from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def show(request):
    return HttpResponse('<h1>welcome to the django project...</h1>')

def showTime(request):
    # Get current date and time
    now = datetime.datetime.now()
    dateTimeFormat = '''<div>
        <h1>Show the time<h1><hr>
        <span>Show current time: {}</span><br>
        <span>Show date only: {}</span><br>
        <span>Show date in (dd/mm/yyyy) format: {}</span><br>
        <span>Show date in (mm/dd/yyyy) format: {}</span><br>
        <span>Show full time: {}</span><br>
        <span>Show time in (hh:mm AM/PM) format: {}</span><br>
        <span>Show time in (hh:mm:ss) format: {}</span><br>
    </div>'''.format(now, 
                     now.date(), 
                     now.strftime("%d/%m/%Y"),
                     now.strftime("%m/%d/%Y"),
                     now.time().strftime("%H:%M:%S"),
                     now.time().strftime("%I:%M:%p"),
                     now.time().strftime("%H:%M:%S"))
    return HttpResponse(dateTimeFormat)