
## relm.log
import datetime, os

def func_log(self, kind, msg):
    self.debug()

    print(kind.upper() + ": " + msg)

    path = self.config['LOGGING']['path']
    if not os.path.exists(path):
        os.makedirs(path)

    path = os.path.join(path, kind + ".log")

    msg = str(datetime.datetime.now()) + "   " + msg + "\n"

    if (
        (kind == 'error' and self.config['LOGGING'].getboolean('log_errors')) or
        (kind == 'event' and self.config['LOGGING'].getboolean('log_events')) or
        (kind == 'warn' and self.config['LOGGING'].getboolean('log_warnings'))
    ):
        with open(path, 'a') as logfile:
            logfile.write(msg)
