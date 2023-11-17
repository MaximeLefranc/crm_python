from django.shortcuts import render

from api.crm import User, get_all_users


def index(request):
    test = get_all_users()
    print(test)
    return render(request, 'contacts/index.html', {
        'users': get_all_users()
    })
