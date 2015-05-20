import logging, traceback

class ReportBuilder:
    def __init__(self):
        self.str = ""

    def add_line(self, line, **kwargs):
        if len(kwargs) > 0: line = line.format(**kwargs)
        logging.info("[Report]: " + line)
        self.str += line + "\n"
        
    def add_error(self, error):
        text = traceback.format_exc()
        logging.error("[Report]: " + text)
        self.str += "------------------------" + "\n"
        self.str += text + "\n"
     
    def get_result(self):
        return self.str

    def get_html_result(self):
        return "<pre>" + self.str + "</pre>"