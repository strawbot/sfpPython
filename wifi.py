"""
Search for a specific wifi ssid and connect to it.
written by kasramvd.
"""
import os


class Finder:
    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.password = kwargs['password']
        self.interface_name = kwargs['interface']
        self.main_dict = {}

    def run(self):
        command = """sudo iwlist wlp2s0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        result = os.popen(command.format(self.server_name))
        result = list(result)

        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print("Successfully get ssids {}".format(str(ssid_list)))

        for name in ssid_list:
            try:
                result = self.connection(name)
            except Exception as exp:
                print("Couldn't connect to name : {}. {}".format(name, exp))
            else:
                if result:
                    print("Successfully connected to {}".format(name))

    def connection(self, name):
        try:
            os.system("nmcli d wifi connect {} password {} iface {}".format(name,
       self.password,
       self.interface_name))
        except:
            raise
        else:
            return True

if __name__ == "__main__":
    # Server_name is a case insensitive string, and/or regex pattern which demonstrates
    # the name of targeted WIFI device or a unique part of it.
    server_name = "example_name"
    password = "your_password"
    interface_name = "your_interface_name" # i. e wlp2s0
    F = Finder(server_name=server_name,
               password=password,
               interface=interface_name)
    F.run()


'''

import subprocess

def method1():
    results = subprocess.check_output(["netsh", "wlan", "show", "network"])

    results = results.decode("ascii") # needed in python 3
    results = results.replace("\r","")
    ls = results.split("\n")
    ls = ls[4:]
    ssids = []
    x = 0
    while x < len(ls):
        if x % 5 == 0:
            ssids.append(ls[x])
        x += 1
    print(ssids)
'''

'''
from subprocess import Popen, call, PIPE
import errno
import logging
import time
import shlex


def run_program(rcmd):
    """
    Runs a program, and it's paramters (e.g. rcmd="ls -lh /var/www")
    Returns output if successful, or None and logs error if not.
    """

    cmd = shlex.split(rcmd)
    executable = cmd[0]
    executable_options=cmd[1:]

    try:
        proc  = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
        response = proc.communicate()
        response_stdout, response_stderr = response[0], response[1]
    except OSError, e:
        if e.errno == errno.ENOENT:
            logging.debug( "Unable to locate '%s' program. Is it in your path?" % executable )
        else:
            logging.error( "O/S error occured when trying to run '%s': \"%s\"" % (executable, str(e)) )
    except ValueError, e:
        logging.debug( "Value error occured. Check your parameters." )
    else:
        if proc.wait() != 0:
            logging.debug( "Executable '%s' returned with the error: \"%s\"" %(executable,response_stderr) )
            return response
        else:
            logging.debug( "Executable '%s' returned successfully. First line of response was \"%s\"" %(executable, response_stdout.split('\n')[0] ))
            return response_stdout

def get_networks(iface, retry=10):
    """
    Grab a list of wireless networks within range, and return a list of dicts describing them.
    """
    while retry > 0:
        if "OK" in run_program("wpa_cli -i %s scan" % iface):
            networks=[]
            r = run_program("wpa_cli -i %s scan_result" % iface).strip()
            if "bssid" in r and len ( r.split("\n") ) >1 :
                for line in r.split("\n")[1:]:
                    b, fr, s, f = line.split()[:4]
                    ss = " ".join(line.split()[4:]) #Hmm, dirty
                    networks.append( {"bssid":b, "freq":fr, "sig":s, "ssid":ss, "flag":f} )
                return networks
        retry-=1
        logging.debug("Couldn't retrieve networks, retrying")
        time.sleep(0.5)
        logging.debug("Failed to list networks")

def start_wpa(_iface):
    """
    Terminates any running wpa_supplicant process, and then starts a new one.
    """
    run_program("wpa_cli terminate")
    time.sleep(1)
    run_program("wpa_supplicant -B -Dwext -i %s -C /var/run/wpa_supplicant -f %s" %(_iface, SUPPLICANT_LOG_FILE))

def get_wnics():
    """
    Kludgey way to get wireless NICs, not sure if cross platform.
    """
    r = run_program("iwconfig")
    ifaces=[]
    for line in r.split("\n"):
        if "IEEE" in line:
            ifaces.append( line.split()[0] )
    return ifaces

# print get_wnics()
# iface = get_wnics()[0]
# start_wpa(iface)
# networks = get_networks(iface)
'''

'''
import io
import os
import pkgutil
import subprocess
import sys
import tempfile
import time
from typing import Callable, List, Optional


class WinWiFi:
    @classmethod
    def get_profile_template(cls) -> str:
        return pkgutil.get_data(__package__, 'data/profile-template.xml').decode()

    @classmethod
    def netsh(cls, args: List[str], timeout: int = 3, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(['netsh'] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=timeout, check=check, encoding=sys.stdout.encoding)

    @classmethod
    def get_profiles(cls, callback: Callable = lambda x: None) -> List[str]:
        profiles: List[str] = []

        raw_data: str = cls.netsh(['wlan', 'show', 'profiles'], check=False).stdout

        line: str
        for line in raw_data.splitlines():
            if ' : ' not in line:
                continue
            profiles.append(line.split(' : ', maxsplit=1)[1].strip())

        callback(raw_data)

        return profiles

    @classmethod
    def gen_profile(cls, ssid: str = '', auth: str = '', encrypt: str = '', passwd: str = '', remember: bool = True) \
            -> str:
        profile: str = cls.get_profile_template()

        profile = profile.replace('{ssid}', ssid)
        profile = profile.replace('{connmode}', 'auto' if remember else 'manual')

        if not passwd:
            profile = profile[:profile.index('<sharedKey>')] + \
                profile[profile.index('</sharedKey>')+len('</sharedKey>'):]
            profile = profile.replace('{auth}', 'open')
            profile = profile.replace('{encrypt}', 'none')

        return profile

    @classmethod
    def add_profile(cls, profile: str):
        fd: io.RawIOBase
        path: str
        fd, path = tempfile.mkstemp()

        os.write(fd, profile.encode())
        cls.netsh(['wlan', 'add', 'profile', 'filename={}'.format(path)])

        os.close(fd)
        os.remove(path)

    @classmethod
    def scan(cls, refresh: bool = False, callback: Callable = lambda x: None) -> List['WiFiAp']:
        if refresh:
            interface: 'WiFiInterface'
            for interface in cls.get_interfaces():
                cls.disable_interface(interface.name)
                cls.enable_interface(interface.name)
            time.sleep(5)
        cp: subprocess.CompletedProcess = cls.netsh(['wlan', 'show', 'networks', 'mode=bssid'])
        callback(cp.stdout)
        return list(map(WiFiAp.parse_netsh, [out for out in cp.stdout.split('\n\n') if out.startswith('SSID')]))

    @classmethod
    def get_interfaces(cls) -> List['WiFiInterface']:
        cp: subprocess.CompletedProcess = cls.netsh(['wlan', 'show', 'interfaces'])
        return list(map(WiFiInterface.parse_netsh,
                        [out for out in cp.stdout.split('\n\n') if out.startswith('    Name')]))

    @classmethod
    def get_connected_interfaces(cls) -> List['WiFiInterface']:
        return list(filter(lambda i: i.state == WiFiConstant.STATE_CONNECTED, cls.get_interfaces()))

    @classmethod
    def disable_interface(cls, interface: str):
        cls.netsh(['interface', 'set', 'interface', 'name={}'.format(interface), 'admin=disabled'], timeout=15)

    @classmethod
    def enable_interface(cls, interface: str):
        cls.netsh(['interface', 'set', 'interface', 'name={}'.format(interface), 'admin=enabled'], timeout=15)

    @classmethod
    def connect(cls, ssid: str, passwd: str = '', remember: bool = True):
        if not passwd:
            for i in range(3):
                aps: List['WiFiAp'] = cls.scan()
                ap: 'WiFiAp'
                if ssid in [ap.ssid for ap in aps]:
                    break
                time.sleep(5)
            else:
                raise RuntimeError('Cannot find Wi-Fi AP')

            if ssid not in cls.get_profiles():
                ap = [ap for ap in aps if ap.ssid == ssid][0]
                cls.add_profile(cls.gen_profile(
                    ssid=ssid, auth=ap.auth, encrypt=ap.encrypt, passwd=passwd, remember=remember))
            cls.netsh(['wlan', 'connect', 'name={}'.format(ssid)])

            for i in range(30):
                if list(filter(lambda it: it.ssid == ssid, WinWiFi.get_connected_interfaces())):
                    break
                time.sleep(1)
            else:
                raise RuntimeError('Cannot connect to Wi-Fi AP')

    @classmethod
    def disconnect(cls):
        cls.netsh(['wlan', 'disconnect'])

    @classmethod
    def forget(cls, *ssids: str):
        for ssid in ssids:
            cls.netsh(['wlan', 'delete', 'profile', ssid])


class WiFiAp:
    @classmethod
    def parse_netsh(cls, raw_data: str) -> 'WiFiAp':
        ssid: str = ''
        auth: str = ''
        encrypt: str = ''
        bssid: str = ''
        strength: int = 0

        line: str
        for line in raw_data.splitlines():
            if ' : ' not in line:
                continue
            value: str = line.split(' : ', maxsplit=1)[1].strip()
            if line.startswith('SSID'):
                ssid = value
            elif line.startswith('    Authentication'):
                auth = value
            elif line.startswith('    Encryption'):
                encrypt = value
            elif line.startswith('    BSSID'):
                bssid = value.lower()
            elif line.startswith('         Signal'):
                strength = int(value[:-1])
        return cls(ssid=ssid, auth=auth, encrypt=encrypt, bssid=bssid, strength=strength, raw_data=raw_data)

    def __init__(
            self,
            ssid: str = '',
            auth: str = '',
            encrypt: str = '',
            bssid: str = '',
            strength: int = 0,
            raw_data: str = '',
    ):
        self._ssid: str = ssid
        self._auth: str = auth
        self._encrypt: str = encrypt
        self._bssid: str = bssid
        self._strength: int = strength
        self._raw_data: str = raw_data

    @property
    def ssid(self) -> str:
        return self._ssid

    @property
    def auth(self) -> str:
        return self._auth

    @property
    def encrypt(self) -> str:
        return self._encrypt

    @property
    def bssid(self) -> str:
        return self._bssid

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def raw_data(self) -> str:
        return self._raw_data


class WiFiConstant:
    STATE_CONNECTED = 'connected'
    STATE_DISCONNECTED = 'disconnected'


class WiFiInterface:
    @classmethod
    def parse_netsh(cls, raw_data: str) -> 'WiFiInterface':
        name: str = ''
        state: str = ''
        ssid: str = ''
        bssid: str = ''

        line: str
        for line in raw_data.splitlines():
            if ' : ' not in line:
                continue
            value: str = line.split(' : ', maxsplit=1)[1].strip()
            if line.startswith('    Name'):
                name = value
            elif line.startswith('    State'):
                state = value
            elif line.startswith('    SSID'):
                ssid = value
            elif line.startswith('    BSSID'):
                bssid = value

        c: 'WiFiInterface' = cls(name=name, state=state)
        if ssid:
            c.ssid = ssid
        if bssid:
            c.bssid = bssid
        return c

    def __init__(
            self,
            name: str = '',
            state: str = '',
            ssid: Optional[str] = None,
            bssid: Optional[str] = None,
    ):
        self._name: str = name
        self._state: str = state
        self._ssid: Optional[str] = ssid
        self._bssid: Optional[str] = bssid

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def ssid(self) -> Optional[str]:
        return self._ssid

    @ssid.setter
    def ssid(self, value: str):
        self._ssid = value

    @property
    def bssid(self) -> Optional[str]:
        return self._bssid

    @bssid.setter
    def bssid(self, value: str):
        self._bssid = value
'''