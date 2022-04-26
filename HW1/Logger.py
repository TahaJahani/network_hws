from datetime import datetime
import inspect

class Logger:
    # todo: add more logging options
    def log(message, mode = "stdout"):
        filename = inspect.stack()[1][1]
        if (mode == "stdout"):
            print('[', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '] ', filename, ': ', message, sep='')
