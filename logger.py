import logging
import inspect


class Logger:

    @staticmethod
    def error(message):
        Logger.handleLogging(logging.ERROR, Logger.assembleMessage(message))

    @staticmethod
    def loadConfig():
        logging.basicConfig(filename='example.log', level=logging.INFO)

    @staticmethod
    def debug(message):
        Logger.handleLogging(logging.DEBUG, Logger.assembleMessage(message))

    @staticmethod
    def info(message):
        Logger.handleLogging(logging.INFO, Logger.assembleMessage(message))

    @staticmethod
    def warn(message):
        Logger.handleLogging(logging.WARNING, Logger.assembleMessage(message))

    @staticmethod
    def handleLogging(level, message):
        logging.log(level, message)
        print(message)

    @staticmethod
    def assembleMessage(message):
        stack = inspect.stack()
        try:
            the_class = stack[2][0].f_locals['self'].__class__
        except KeyError:
            the_class = 'No instance'
        the_method = stack[2][0].f_code.co_name
        prefix = "[{0}::{1}] ".format(the_class, the_method)
        postfix = ""
        return prefix + message + postfix
