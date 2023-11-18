from logging import Formatter, LogRecord

from flask import has_request_context, request


class RequestFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        record.endpoint = None
        record.method = None
        if has_request_context():
            record.endpoint = request.endpoint
            record.method = request.method.upper()
        return super().format(record)
