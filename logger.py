import logging
import inspect


class Logger:

    def __index__(self):
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def log(self, message):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__
        the_method = stack[1][0].f_code.co_name
        logging.log("[{0}::{1}] ".format(the_class, the_method) + message)

    def debug(self, message):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__
        the_method = stack[1][0].f_code.co_name
        logging.debug("[{0}::{1}] ".format(the_class, the_method) + message)

    def info(self, message):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__
        the_method = stack[1][0].f_code.co_name
        logging.info("[{0}::{1}] ".format(the_class, the_method) + message)

    def warn(self, message):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__
        the_method = stack[1][0].f_code.co_name
        logging.warning("[{0}::{1}] ".format(the_class, the_method) + message)
