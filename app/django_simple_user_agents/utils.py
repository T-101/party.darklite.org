from user_agents import parse


def get_user_agent(request):
    if not hasattr(request, 'META'):
        return ''

    ua_string = request.META.get('HTTP_USER_AGENT', '')

    if not isinstance(ua_string, str):
        ua_string = ua_string.decode('utf-8', 'ignore')

    user_agent = parse(ua_string)
    return user_agent


def get_and_set_user_agent(request):
    if hasattr(request, 'user_agent'):
        return request.user_agent

    if not request:
        return parse('')

    request.user_agent = get_user_agent(request)
    return request.user_agent
