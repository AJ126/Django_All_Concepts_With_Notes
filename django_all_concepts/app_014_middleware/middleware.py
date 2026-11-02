class ExecutionFlowMiddleware(object):
    def __init__(self, get_response):
        print('get_response...............', get_response)
        self.get_response=get_response

    def __call__(self, request):
        print('before request............')
        response = self.get_response(request)
        print("after request............")
        return response
