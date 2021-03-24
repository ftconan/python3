from django.http import HttpResponse


def index(request):
    """
    index
    @param request:
    @return:
    """
    return HttpResponse("Hello, world. You're at the polls index.")
