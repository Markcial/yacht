# --.-- encoding: utf-8 --.--
import unittest
from yacht import Host
from mock import mock_open, patch

class HostTestSuite(unittest.TestCase):
    def setUp(self):
        self.host = Host('demo')

    def test_create_host_without_alias(self):
        self.assertRaises(TypeError, Host)

    def test_create_host_with_invalid_nonascii_name(self):
        self.assertRaises(ValueError, Host, 'loñaeoçae')

    def test_create_host_with_invalid_chars(self):
        self.assertRaises(ValueError, Host, 'host^file{name}')

    def test_save_host_file(self):
        with patch.object(builtins, 'open', mock_open(read_data='bibble')):
            self.host.save()
