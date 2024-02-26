from .cookiecutterplus import CookieCutterPlus
from api.app import CookieCutterPlusAPI

class CookieCutterPlusBuilder:
    def __init__(self):
        self.args = None

    def withArgs(self, args):
        self.args = args
        return self

    def build(self):
        if self.args.get('api_mode', None) is None:
            return CookieCutterPlus(self.args)
        else:
            return CookieCutterPlusAPI()