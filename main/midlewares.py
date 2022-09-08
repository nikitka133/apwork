from main.models import SubCategory


def category_context_processor(request):
    if request.method == 'GET' or request.POST['category']:
        context = {'category': SubCategory.objects.all(),
                   "keyword": "",
                   'all': ""}

        return context
    else:
        # обязательно вернуть словарь
        return {'nothing': 'OK'}
