from datetime import datetime
import inspect

class Logger:
    # todo: add more logging options
    def log(message, mode = "stdout"):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        if (mode == "stdout"):
            print('[', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '] ', filename, ': ', message, sep='')
