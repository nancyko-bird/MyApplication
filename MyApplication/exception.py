class CustomError(Exception):
    """自定义异常类，可以接收一条错误信息"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
