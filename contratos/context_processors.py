def username_cookie(request):
    """
    Context processor para disponibilizar username do cookie nos templates
    """
    return {
        'username_cookie': request.COOKIES.get('username', '')
    }
