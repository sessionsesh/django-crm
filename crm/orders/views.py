from django.shortcuts import render
from accounts.models import Role

from django.http import HttpResponse
# Create your views here.


def orders(request):
    user = request.user

    # try-catch for AnonymousUser handling
    args = {}
    try:
        args['role'] = user.role
        return render(request, 'orders.html', args)
    except:
        html = '<html><body>20 dollar bill</body></html>'
        return HttpResponse(html)
