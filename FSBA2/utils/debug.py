import sys
import inspect
import linecache
from logging import *


basicConfig(
    level=DEBUG,
    format="%(asctime)s - [%(levelname)s] %(filename)s:%(lineno)d:%(funcName)s: %(message)s",
    datefmt="%F %T", stream=sys.stdout)


def get_src_line(frame):
    """
    Getting the source line from stack frame
    """
    line = str(linecache.getline(frame.filename, frame.lineno)).strip()
    return line

def debug_outer_stack_frame(context = 1):
    """debug_outer_stack_frame
    Get information from outer stack frame

    :param context: number of stackframe to be queried
    :type context: int

    """
    f = inspect.stack()[2]
    return "caller backtrace : %15s: line %3d: %s()  |  src expr ` %s `" %(f.filename, f.lineno, f.function, get_src_line(f))
