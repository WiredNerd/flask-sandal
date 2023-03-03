from flask_sandal import LambdaRequest, LambdaResponse


class TestLambdaRequest:
    def test_aws_event(self):
        req = LambdaRequest({
            'aws.event': {'httpMethod', 'GET'}
        })
        assert req.aws_event == {'httpMethod', 'GET'}

    def test_aws_context(self):
        req = LambdaRequest({
            'aws.context': {'key', 'value'}
        })
        assert req.aws_context == {'key', 'value'}


class TestLambdaResponse:
    def test_start_response(self):
        lambda_response = LambdaResponse()
        lambda_response.start_response("1234", [("header1", "value1"), ("header2", "value2")], "exec_information")
        assert lambda_response.status == 123
        assert lambda_response.response_headers == {
            "header1": "value1",
            "header2": "value2",
        }
        assert lambda_response.exc_info == "exec_information"
