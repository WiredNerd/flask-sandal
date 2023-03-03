from flask import Request, Flask

from flask_sandal.mapping import build_wsgi_environ


class LambdaRequest(Request):
    """Wrapper for :py:obj:`flask.request` that exposes properties aws_event and aws_context"""

    @property
    def aws_event(self):
        return self.environ.get('aws.event')

    @property
    def aws_context(self):
        return self.environ.get('aws.context')


class LambdaResponse:
    """Receiver for response from :py:meth:`~.Flask.wsgi_app` call"""
    status: int
    response_headers: dict
    exc_info: any

    def start_response(self, status, response_headers, exc_info=None):
        self.status = int(status[:3])
        self.response_headers = dict(response_headers)
        self.exc_info = exc_info


class FlaskLambda(Flask):
    """Wrapper class for a Flask application

    To use, add the following line to your app::

        app = FlaskLambda(__name__)

    Direct AWS Lambda to call ``app`` as the handler function

    Note: :py:obj:`flask.request` will contain additional properties from :py:class:`LambdaRequest`
    """
    request_class = LambdaRequest

    def __call__(self, event, context):
        try:
            if 'httpMethod' not in event:
                # Called as Flask, not Lambda
                # event = environ, context = start_response
                return super(FlaskLambda, self).__call__(event, context)

            self.logger.debug('aws_event: %r', event)

            response = LambdaResponse()

            body = next(
                self.wsgi_app(
                    build_wsgi_environ(event, context),
                    response.start_response
                )
            )

            return {
                'isBase64Encoded': False,
                'statusCode': response.status,
                'headers': response.response_headers,
                'body': body.decode('utf-8'),
            }
        except Exception as ex:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/text'},
                'body': f'Internal Server Error: {ex}'
            }
