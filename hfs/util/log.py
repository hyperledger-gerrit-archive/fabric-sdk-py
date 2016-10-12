import logging
import sys
from .common import Singleton

OUTPUT = 25

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'output': OUTPUT,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

LOGLEVELDEFAULT = 'debug'

# default: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGMSGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class SDKLogger(logging.Logger, object):
    __metaclass__ = Singleton

    def __init__(self):

        logging.Logger.__init__(self, "EasyOVS")

        # create console handler
        ch = logging.StreamHandler(sys.stdout)
        # create formatter
        formatter = logging.Formatter(LOGMSGFORMAT)
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to lg
        self.addHandler(ch)

        self.set_log_level()

    def set_log_level(self, levelname=LOGLEVELDEFAULT):
        level = LEVELS.get(levelname)

        self.setLevel(level)
        self.handlers[0].setLevel(level)

    def output(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'OUTPUT'.

           To pass exception information, use the keyword argument exc_info
           with a true value, e.g.

           logger.warning("Houston, we have a %s", "cli output", exc_info=1)
        """
        if self.isEnabledFor(OUTPUT):
            self._log(OUTPUT, msg, args, kwargs)


def make_list_compatible(fn):
    """Return a new function allowing fn( 'a 1 b' ) to be called as
       newfn( 'a', 1, 'b' )"""

    def newfn(*args):
        """
        Generated function. Closure-ish.
        """
        if len(args) == 1:
            return fn(*args)
        args = ' '.join([str(arg) for arg in args])
        return fn(args)

    # Fix newfn's name and docstring
    setattr(newfn, '__name__', fn.__name__)
    setattr(newfn, '__doc__', fn.__doc__)
    return newfn

lg = SDKLogger()

debug, info, output, warn, error = (
    lg.debug, lg.info, lg.output, lg.warn, lg.error) = \
    [make_list_compatible(f) for f in
     [lg.debug, lg.info, lg.output, lg.warning, lg.error]]

setLogLevel = lg.set_log_level

if __name__ == "__main__":
    setLogLevel("output")
    output("This is an output")
    warn("This is a warning")
    error("This is an error")
