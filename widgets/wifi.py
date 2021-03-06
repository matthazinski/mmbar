import re
import subprocess


class WifiWidget(object):
    def __init__(self, interface='wlan0'):
        self.interface = interface

    def output(self):
        try:
            out = subprocess.check_output(['iwgetid'])
            out = out.decode('utf-8')
        except subprocess.CalledProcessError:
            return

        m = re.match(r'{interface}\s+ESSID:"(.+?)"\n'.format(
            interface=self.interface), out)

        if m:
            return {
                'name': "wifi",
                'instance': self.interface,
                'full_text': m.group(1),
                'color': '#dfaf8f',
                'icon': 'wifi_02.xbm',
            }
