from django.core.exceptions import ImproperlyConfigured

def get_client_ip(request):
    """
    get client ip address
    """
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        ip = xff.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_secret(setting, secrets):
    """
    using secrets.json for hiding private key
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment varible".format(setting)
        raise ImproperlyConfigured(error_msg)