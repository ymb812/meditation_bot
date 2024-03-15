from django.shortcuts import redirect


def handler404(request, exception):
    return redirect(to='redirect_to_admin')
