from configparser import ConfigParser
import requests

# Need to use this when running from pytest
CONFIG_FILE = './config.ini'
# Use this when running scripts by themselves
# CONFIG_FILE = '../config.ini'


class LoggerAPI:
    ip_address = ''
    uri = 'dl:'

    def __init__(self, table):
        self.uri = self.uri + table
        config = ConfigParser()
        config.optionxform = str
        config.read(CONFIG_FILE)
        self.ip_address = 'http://' + config['logger'].get('ip') + '/'

    def set_var(self, var, value):
        payload = {'command': 'setvalueex', 'uri': self.uri + '.' + var, 'value': str(value), 'format': 'json'}
        r = requests.post(self.ip_address, params=payload)
        print("Sending request: " + r.url)
        resp = r.json()
        if resp['outcome'] == 1:
            return True
        return False

    def get_var_most_recent(self, var):
        payload = {'command': 'dataquery', 'uri': self.uri + '.' + var, 'format': 'json',
                   'mode': 'most-recent', 'p1': '1'}
        r = requests.post(self.ip_address, params=payload)
        resp = r.json()
        return resp['data'][0]['vals'][0]

    def get_var_recent_number(self, var, num):
        payload = {'command': 'dataquery', 'uri': self.uri + '.' + var, 'format': 'json',
                   'mode': 'most-recent', 'p1': str(num)}
        r = requests.post(self.ip_address, params=payload)
        resp = r.json()
        return [x['vals'][0] for x in resp['data']]


if __name__ == '__main__':
    logger = LoggerAPI('Public')
    success = logger.set_var('mvOut', 3600)
    # data = logger.get_var_most_recent('pulse_interval')
    data_list = logger.get_var_recent_number('PTemp', 10)
    print(data_list)
