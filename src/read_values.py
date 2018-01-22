import argparse
from dao_flower import FlowerDAO, FlowerEntry
from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

hostname='LHOTA File'

parser = argparse.ArgumentParser()
parser.add_argument('mac')
parser.add_argument('--load', action='store_true')
parser.add_argument('--show')
parser.add_argument('--zabbix', action='store_true')
args = parser.parse_args()

poller = MiFloraPoller(args.mac)
dao = FlowerDAO()

def load_and_store():
    temperature = int(poller.parameter_value(MI_TEMPERATURE))
    moisture = int(poller.parameter_value(MI_MOISTURE))
    light = int(poller.parameter_value(MI_LIGHT))
    conductivity = int(poller.parameter_value(MI_CONDUCTIVITY))
    battery = int(poller.parameter_value(MI_BATTERY))

    data_entry = FlowerEntry(temperature, moisture, conductivity, light, battery)
    dao.store(data_entry)
    dao.close()

def read_last(param):
    entries = dao.load();
    if len(entries) > 0:
        entry = entries[0]
    
    if (param == 'temperature'):
        print(entry.temperature)
    if (param == 'moisture'):
        print(entry.moisture)
    if (param == 'light'):
        print(entry.light)
    if (param == 'conductivity'):
        print(entry.conductivity)
    if (param == 'battery'):
        print(entry.battery)

def export_zabbix():
    with open('input_file_zabbix.txt', 'w') as f:
        entries = dao.load(count=None)
        for entry in entries:
            f.write('"{0}" miflora[temperature] {1} {2}\n'.format(hostname, entry.time, entry.temperature))
            f.write('"{0}" miflora[moisture] {1} {2}\n'.format(hostname, entry.time, entry.moisture))
            f.write('"{0}" miflora[light] {1} {2}\n'.format(hostname, entry.time, entry.light))
            f.write('"{0}" miflora[conductivity] {1} {2}\n'.format(hostname, entry.time, entry.conductivity))
            f.write('"{0}" miflora[battery] {1} {2}\n'.format(hostname, entry.time, entry.battery))

if args.load:
    load_and_store()
elif args.show is not None:
    read_last(args.show)
elif args.zabbix:
    export_zabbix()
