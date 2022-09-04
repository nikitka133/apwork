from main.models import SubCategory


def category_context_processor(request):
    if request.method == 'GET':
        context = {'category': SubCategory.objects.all(), "keyword": "", 'all': ""}
        return context
    else:
        # обязательно что-то словарь
        return {'nothing': 'OK'}