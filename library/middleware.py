from django.http import HttpResponseForbidden
from .tools import Protection


class IPBanMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR')
        protection = Protection(request, user_ip)
        try:
            protection.table_set()
            protection.insert()
        except:
            pass

        banned_ips = protection.select_ban_ip()

        if user_ip in banned_ips:
            return HttpResponseForbidden('ban :>')
        response = self.get_response(request)
        return response
