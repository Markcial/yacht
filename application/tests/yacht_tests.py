# --.-- encoding: utf-8 --.--
import unittest
from StringIO import StringIO

from mock import MagicMock, mock_open, patch
from ..yacht import Host


class MockedFileHandle(object):
    def __init__(self):
        self.content = ''

    def write(self, content):
        self.content = content

    def read(self):
        return self.content


class HostTestSuite(unittest.TestCase):
    def setUp(self):
        self.host = Host('demo')

    def test_create_host_without_alias(self):
        self.assertRaises(TypeError, Host)

    def test_create_host_with_invalid_nonascii_name(self):
        self.assertRaises(ValueError, Host, 'loñaeoçae')

    def test_create_host_with_invalid_chars(self):
        self.assertRaises(ValueError, Host, 'host^file{name}')

    def test_add_host_to_a_host_object_instance(self):
        ip = '192.172.162.21'
        host = 'www.yadda.com'
        self.host.add(ip, host)
        self.assertEqual(ip + ' ' + host, str(self.host))

    def test_add_already_added_host_to_a_host_object_instance(self):
        ip = '192.172.162.21'
        host1 = 'www.yadda.com'
        host2 = 'www.foobar.com'
        self.host.add(ip, host1)
        self.host.add(ip, host2)
        self.assertEqual(ip + ' ' + host1 + ' ' + host2, str(self.host))

    def test_add_multiple_hosts_to_a_hosts_object_file(self):
        ip1 = '213.93.12.32'
        host1 = 'host1'
        ip2 = '213.93.12.35'
        host2 = 'host2'
        self.host.add(ip1, host1)
        self.host.add(ip2, host2)
        self.assertEqual("""%s %s\n%s %s"""%(ip1, host1, ip2, host2), str(self.host))

    def test_writing_host_object_contents_to_file(self):
        m = mock_open(read_data=StringIO('foo bar baz'))
        self.host.add('127.0.0.1', 'localhost')
        with patch('application.yacht.open', m, create=True):
            self.host.save()
        m.assert_called_once_with('/hosts.d/' + self.host.alias, 'w+')
        handle = m()
        handle.write.assert_called_once_with('127.0.0.1 localhost')