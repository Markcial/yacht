import re

class Host(object):
    def __init__(self, alias):
        if not re.match(r'^[a-z0-9-_.]+$', alias):
            raise ValueError('Alias must follow the "^[a-z0-9-_.]+$" format.')
        self.alias = alias
        self.hosts = {}

    def add(ip, name):
        self.hosts[ip] = name

    def __str__(self):
        return "\n".join(k + " " + v for k,v in self.hosts.iteritems())

    def save(self):
        with open('/hosts.d/' + self.alias, 'w+') as f:
            f.write(str(self))
