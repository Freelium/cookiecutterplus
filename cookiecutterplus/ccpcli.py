from .ccpstate import CCPStateManager
from .ccpbuilder import CookieCutterPlusBuilder


def cli(args=None):
    parsed_args = CCPStateManager().parse_args(args)
    # if parsed_args.api_mode is enabled then run the API, else instantiate CookieCutterPlus
    CookieCutterPlusBuilder().with_args(parsed_args).build().run()
