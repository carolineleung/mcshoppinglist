import logging


class LogFactory(object):
    LOGGER_TOP_LEVEL_NAME = 'mcshoppinglist'

    @staticmethod
    def get_logger_top():
        return logging.getLogger('{0}'.format(LogFactory.LOGGER_TOP_LEVEL_NAME))

    @staticmethod
    def get_logger(logger_name_suffix):
        return logging.getLogger('{0}.{1}'.format(LogFactory.LOGGER_TOP_LEVEL_NAME, logger_name_suffix))

class NullLogHandler(logging.Handler):
    """
    A log handler that does nothing.
    """
    def emit(self, record):
        pass

def _static_init():
    # Prevent this warning when no logging is configured: No handlers could be found for logger
    #    Per: http://docs.python.org/library/logging.html
    logging.getLogger(LogFactory.LOGGER_TOP_LEVEL_NAME).addHandler(NullLogHandler())

_static_init()
