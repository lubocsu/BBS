# 存放一些基类
from wtforms import Form

class BoseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        # message = self.errors
        return message