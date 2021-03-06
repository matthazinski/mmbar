#!/usr/bin/python3
###############################################################################
# status.py - python i3bar status line generator
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
###############################################################################

import importlib
import json
import os.path
import sys
import time
import widgets
import yaml

if len(sys.argv) > 1:
    configpath = sys.argv[1]
else:
    try:
        import xdg.BaseDirectory
        configpath = xdg.BaseDirectory.load_first_config('mmbar/config.yml')
    except:
        configpath = os.path.expanduser('~/.config/mmbar/config.yml')

config = yaml.safe_load(open(configpath))
interval = config['interval']
icon_path = os.path.dirname(os.path.abspath(__file__))
widgets = []

# load widgets from config
for item in config['widgets']:
    if isinstance(item, dict):
        # grab the first dict from the list of widgets
        components, args = item.popitem()
    else:
        # if the item is not a dict, then it is a widget with no args
        # for backwards compatibility, we split on spaces
        splat = item.split(' ')
        components = splat[0]
        if len(splat) > 1:
            args = splat[1:]
        else:
            args = []

    components = components.split('.')
    path = '.'.join(components[:-1])
    module = importlib.import_module(path)

    class_ = getattr(module, components[-1])

    if isinstance(args, dict):
        # keyword arguments
        instance = class_(**args)
    elif isinstance(args, list):
        # positional arguments
        instance = class_(*args)
    else:
        # single argument
        instance = class_(args)

    widgets.append(instance)

print(json.dumps({'version': 1}) + '[[]')
while True:
    output = []
    for widget in widgets:
        wout = widget.output()

        if wout is not None:
            wout['icon'] = os.path.join(icon_path, 'icons', wout['icon'])
            wout['full_text'] = ' {}'.format(wout['full_text'])
            output.append(wout)
    print(',' + json.dumps(output), flush=True)
    time.sleep(interval)
print(']')
