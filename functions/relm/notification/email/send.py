#                       _       _                       _          _     _             _                                    _   
#                      | |     | |                     | |        | |   | |           | |                                  | |  
#  _ __ ___   __ _ _ __| | ____| | _____      ___ __   | |_ ___   | |__ | |_ _ __ ___ | |  ___ _   _ _ __  _ __   ___  _ __| |_ 
# | '_ ` _ \ / _` | '__| |/ / _` |/ _ \ \ /\ / / '_ \  | __/ _ \  | '_ \| __| '_ ` _ \| | / __| | | | '_ \| '_ \ / _ \| '__| __|
# | | | | | | (_| | |  |   < (_| | (_) \ V  V /| | | | | || (_) | | | | | |_| | | | | | | \__ \ |_| | |_) | |_) | (_) | |  | |_ 
# |_| |_| |_|\__,_|_|  |_|\_\__,_|\___/ \_/\_/ |_| |_|  \__\___/  |_| |_|\__|_| |_| |_|_| |___/\__,_| .__/| .__/ \___/|_|   \__|
#                                                                                                   | |   | |                   
#                                                                                                   |_|   |_|                   
#  _     _             _                   _       _     _         __             _                       _       _                        
# | |   | |           | |                 (_)     | |   | |       / _|           | |                     | |     | |                       
# | |__ | |_ _ __ ___ | | __   ____ _ _ __ _  __ _| |__ | | ___  | |_ ___  _ __  | |_ ___ _ __ ___  _ __ | | __ _| |_ ___   _   _ ___  ___ 
# | '_ \| __| '_ ` _ \| | \ \ / / _` | '__| |/ _` | '_ \| |/ _ \ |  _/ _ \| '__| | __/ _ \ '_ ` _ \| '_ \| |/ _` | __/ _ \ | | | / __|/ _ \
# | | | | |_| | | | | | |  \ V / (_| | |  | | (_| | |_) | |  __/ | || (_) | |    | ||  __/ | | | | | |_) | | (_| | ||  __/ | |_| \__ \  __/
# |_| |_|\__|_| |_| |_|_|   \_/ \__,_|_|  |_|\__,_|_.__/|_|\___| |_| \___/|_|     \__\___|_| |_| |_| .__/|_|\__,_|\__\___|  \__,_|___/\___|
#                                                                                                           | |                                     
#                                                                                                           |_|                                     


## relm.notify
import smtplib, string

def func_send(self, jsonNew, jsonOld):
    self.debug()

    self.debug("NOTIFYING ABOUT NEW RELEASE")
    fromaddr = self.config['NOTIFICATIONS']['email_from']
    toaddrs  = self.config['NOTIFICATIONS']['email_to']

    with open('./email.template', 'r') as tpl:
        tpl = tpl.read()

    template = string.Template(tpl).safe_substitute(sender=fromaddr, to=toaddrs, name=jsonNew['software'], version_old=jsonOld['version'], version_new=jsonNew['version'], url=jsonNew['url'])

    msg = template


    try:
        email_host = self.config['NOTIFICATIONS']['email_host']
        email_port = self.config['NOTIFICATIONS']['email_port']
        email_user = self.config['NOTIFICATIONS']['email_from']
        email_pass = self.config['NOTIFICATIONS']['email_password']
        email_secure = self.config['NOTIFICATIONS']['email_secure']

        if email_secure == True:
            server_ssl = smtplib.SMTP_SSL(email_host, email_port)
            server_ssl.ehlo()
            server_ssl.login(email_user, email_pass)
            server_ssl.sendmail(fromaddr, toaddrs, msg)
            server_ssl.close()
        else:
            server = smtplib.SMTP(email_host, email_port)
            server.ehlo() #server.set_debuglevel(1)
            server.login(email_user, email_pass)
            server.sendmail(fromaddr, toaddrs, msg)
            server.close()
    except smtplib.SMTPAuthenticationError:
        pass
        self.log("error", "Failed to send email notification for " + jsonNew['developer'] + " " + jsonNew['software'])
        status = False
    else:
        self.log("event", "Successfully sent email notification for " + jsonNew['developer'] + " " + jsonNew['software'])
        status = True
    #server.quit()
    return status
