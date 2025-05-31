import logging
import contextlib


class NestedLogger:
    @staticmethod
    def default():
        return default

    def __init__(
        self, logger: logging.Logger = logging, initial_indent=0, indent_increment=2
    ):
        self.logger = logger
        self._indent = initial_indent
        self.indent_increment = indent_increment

    @contextlib.contextmanager
    def action_logging(self, message: str, level=logging.DEBUG):
        self._indent += self.indent_increment
        indent = " " * self._indent

        self.logger.log(level, indent + "start;    " + message)

        yield

        self.logger.log(level, indent + "complete;    " + message)

        self._indent -= self.indent_increment

    def to_new(self):
        return NestedLogger(
            logger=self.logger,
            initial_indent=self._indent,
            indent_increment=self.indent_increment,
        )


default = NestedLogger()
