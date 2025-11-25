from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


class RememberMeMiddleware:
    """
    Middleware para salvar o nome de usuário em cookie quando "Lembrar meu usuário" está marcado
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Se é um POST para login e tem remember_me
        if request.path == '/accounts/login/' and request.method == 'POST':
            remember_me = request.POST.get('remember_me')
            username = request.POST.get('username')
            
            if remember_me and username and request.user.is_authenticated:
                # Salvar username em cookie por 30 dias
                response.set_cookie('username', username, max_age=30*24*60*60)
            elif not remember_me and request.user.is_authenticated:
                # Remover cookie se não marcou remember_me
                response.delete_cookie('username')
        
        return response
