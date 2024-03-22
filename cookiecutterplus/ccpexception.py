class CookieCutterPlusError(Exception):
    def __init__(self, message="Error in cc+", *args):
        super().__init__(message, *args)
