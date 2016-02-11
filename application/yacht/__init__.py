import re
from docker import Client


class Host(object):
    """
    Object that contains the hosts file data
    is only a fragment of the final host file content.
    """
    def __init__(self, alias):
        """
        only alphanumeric with dash dots or underscores alias names allowed.
        :param alias: string
        :return:
        """
        if not re.match(r'^[a-z0-9-_.]+$', alias):
            raise ValueError('Alias must follow the "^[a-z0-9-_.]+$" format.')
        self.alias = alias
        self.hosts = {}

    def add(self, ip, name):
        """
        adds host entry with the ip as key, if already set concatenates with space in the entry
        :param ip:
        :param name:
        :return:
        """
        if ip in self.hosts.keys():
            hosts = self.hosts[ip].split(' ')
            hosts += name,
            self.hosts[ip] = ' '.join(set(hosts))
            return

        self.hosts[ip] = name

    def __str__(self):
        """
        string representation of all the complete host entries
        :return:
        """
        return "\n".join(k + " " + v for k,v in self.hosts.iteritems())

    def save(self):
        """
        saves to a file the string representation of all the entries
        :return:
        """
        with open('/hosts.d/' + self.alias, 'w+') as f:
            f.write(str(self))


class Watcher(object):
    """
    The watcher that will be observing the docker events
    """
    def __init__(self):
        """
        the watcher will be created with a docker-py client
        and a set of filters for event watching
        :return:
        """
        self.client = Client()
        self.filters = {
            'event': ['start', 'restart', 'die', 'stop'],
            'type': 'container'
        }
        self.host = Host('docker')

    def process_event(self, event):
        """
        the processing of the event, the event will be a json encoded raw string
        representation of the event
        :param event:
        :return:
        """
        self.host_entries()
        self.host.save()
        self.create_host_file()

    def create_host_file(self):
        """

        :return:
        """
        f = open('/hosts', 'w+')
        f.write(self.base + "\n" + str(self.host))
        f.close()

    def start(self):
        """
        starts the observer and the event stream for processing
        :return:
        """
        with open('/hosts.d/base', 'r+') as fl:
            self.base = fl.read()
        self.host_entries()
        self.host.save()
        self.create_host_file()
        for event in self.client.events(filters=self.filters):
            self.process_event(event)

    def process_container_host(self, container):
        """

        :param container:
        :return:
        """
        details = self.client.inspect_container(container['Id'])
        names = [name.split('/').pop() for name in container['Names']]
        for ip in map(lambda (k, v): v['IPAddress'], details['NetworkSettings']['Networks'].iteritems()):
            for name in names:
                self.host.add(ip, name)

    def host_entries(self):
        """

        :return:
        """
        for container in self.client.containers():
            self.process_container_host(container)
        return str(self.host)