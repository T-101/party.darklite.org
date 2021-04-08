class UserIPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        real_ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if not real_ip:
            real_ip = request.META.get("REMOTE_ADDR")
        request.session['x_real_ip'] = real_ip
        response = self.get_response(request)
        return response
