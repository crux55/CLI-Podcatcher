import logging


class Logger:

    def __index__(self):
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def log(self, message):
        print(message.encode('utf-8'))
        logging.info(message)
