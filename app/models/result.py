class CommonResult:
    def __init__(self, status =True, message="", data={}):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            'status': self.status,
            'message': self.message,
            'data': self.data
        }
    def to_http_result(self):
        return HTTPResult(self.status,self.message,self.data)

class HTTPResult():
    def __init__(self, success=True, message="", data={}):
        self.success = success
        self.message = message
        self.data = data
    def to_dict(self):
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data
        }
