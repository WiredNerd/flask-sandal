# lambda (input) https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
# wsgi (output) https://wsgi.readthedocs.io/en/latest/definitions.html

def map_headers(event: dict):
    environ = {}
    headers = event.get('headers', {})
    for name, value in headers.items():
        name = name.replace('-', '_').upper()
        if name in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            environ[name] = value
        else:
            environ[f'HTTP_{name}'] = value
    return environ


def build_wsgi_environ(event, context):
    return {}
