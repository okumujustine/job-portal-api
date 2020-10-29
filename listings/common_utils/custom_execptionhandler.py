from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_generic_error,
        "Http404": _handle_generic_error,
        "PermissionDenied": _handle_generic_error,
        "NotAuthenticated": _handle_authentication_error,
        # "AuthenticationFailed": _handle_generic_error
    }

    response = exception_handler(exc, context)

    if response is not None:
        # import pdb
        # pdb.set_trace()

        if "LoginAPIView" in str(context['view']) and exc.status_code == 401:
            response.status_code = 400
            response.data = {
                "error": response.data['detail']
            }
            return response

        # if exc.status_code == 400:
        #     response.data = {
        #         "error": "Bad request!"
        #     }
        #     return response

        if exc.status_code == 500:
            response.data = {
                "error": "interna server error!"
            }
            return response

        if exc.status_code == 403:
            response.data = {
                "error": "forbidden, login please!"
            }
            return response

        if exc.status_code == 401:
            response.data = {
                "error": "login please!"
            }
            return response

        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers(exception_class)(exc, context, response)
    return response


def _handle_authentication_error(exc, context, response):
    response.data = {
        "error": "Please login to proceed!",
        "status_code": response.status_code
    }
    return response


def _handle_generic_error(exc, context, response):
    return response
