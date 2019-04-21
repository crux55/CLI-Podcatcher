import logging


class Logger:

    def __index__(self):
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def log(self, message):
        print(message)
        logging.info(message)
