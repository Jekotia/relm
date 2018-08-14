##
## relm.notification.email.config
import configparser

def func_config(self, config):
    config["NOTIFICATIONS"] = {
        "type": "email",
        "email_host": "smtp.domain.com",
        "email_port": "587",
        "email_secure": False,
        "email_to": "example@domain.com",
        "email_from": "example@domain.com",
        "email_password": "BadPassword"
    }

    return config