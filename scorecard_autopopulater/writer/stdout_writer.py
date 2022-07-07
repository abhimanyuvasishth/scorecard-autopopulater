import logging

from scorecard_autopopulater.writer.writer import Writer


class StdoutWriter(Writer):
    def write_data_item(self, data: dict):
        logging.info(data)
