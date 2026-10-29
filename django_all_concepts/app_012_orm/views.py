from django.shortcuts import render
from django.db.models import Q
from app_012_orm.models import *
# Create your views here.

def ormData(request):
    data = ormInfo.objects.all()
    singleRecord = ormInfo.objects.get(id=1)
    filterRecords = ormInfo.objects.filter(name__startswith='ma')
    exactRecord = ormInfo.objects.get(id__exact=2)
    containRecords = ormInfo.objects.filter(name__contains='sh')
    filter1 = ormInfo.objects.filter(id__in=[1, 2, 3])
    getCombineQueryData = ormInfo.objects.filter(Q(name__startswith='ma') | Q(id=4))
    getDataWithAnd = ormInfo.objects.filter(Q(name__startswith='sh') & Q(id=5))
    queryData = {'all': data, 'singleRecord': singleRecord, 'filterRecords': filterRecords, 'exactRecord': exactRecord,
                 'containRecords': containRecords, 'filter1': filter1, 'getCombineQueryData': getCombineQueryData,
                  'getDataWithAnd': getDataWithAnd}
    return render(request, 'app_012_orm/orm.html', {'queryData': queryData})
