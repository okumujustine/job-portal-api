from rest_framework.views import exception_handler


def error_template(key, error):
    return {
        key: error
    }


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_generic_error,
        "Http404": _handle_generic_error,
        "PermissionDenied": _handle_generic_error,
        "NotAuthenticated": _handle_authentication_error,
    }

    response = exception_handler(exc, context)

    if response is not None:
        if "RegisterView" in str(context['view']):
            if response.data.get("email", None):
                response.data = {
                    "error": response.data.get("email")
                }

            return response

        if "SetNewPasswordAPIView" in str(context['view']):

            if response.data.get("password", None):
                response.data = error_template("password",
                                               response.data.get("password")[0])

            if response.data.get("token", None):
                response.data = error_template("token",
                                               response.data.get("token")[0])

            if response.data.get("uidb64", None):
                response.data = error_template("uidb64",
                                               response.data.get("uidb64")[0])
            return response

        if "LoginAPIView" in str(context['view']) and exc.status_code == 401:
            response.status_code = 400
            response.data = {
                "error": response.data['detail']
            }
            return response

        if exc.status_code == 500:
            response.status_code = 500
            response.data = {
                "error": "internal server error!"
            }
            return response

        if exc.status_code == 530:
            response.status_code = 530
            response.data = {
                "error": "failed to send verification email, try again later!"
            }
            return response

        if exc.status_code == 403:
            response.status_code = 403
            response.data = {
                "error": "forbidden, login please!"
            }
            return response

        if exc.status_code == 401:
            response.status_code = 401
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
