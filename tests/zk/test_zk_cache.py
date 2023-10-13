import datetime
import unittest
from datetime import timedelta
from unittest.mock import patch

from noauth.zk import ZKCache


class TestZKCache(unittest.TestCase):
    @patch('noauth.zk.zk_cache.KazooClient', autospec=True)
    def test_get_method(self, mock_class):
        node = "/test/node"

        expected_val = "value"

        mock_client = mock_class.return_value
        mock_client.get.side_effect = {node: (str.encode(expected_val), "stuff")}.get

        zk_cache = ZKCache(zk_node=node)
        self.assertEqual(zk_cache.get(), expected_val)

    @patch('noauth.zk.zk_cache.KazooClient', autospec=True)
    def test_get_method_returns_None_on_ZK_Exception(self, mock_class):
        node = "/test/node"

        mock_client = mock_class.return_value
        mock_client.get.side_effect = Exception()

        zk_cache = ZKCache(zk_node=node)
        self.assertEqual(zk_cache.get(), None)

    @patch('noauth.zk.zk_cache.KazooClient', autospec=True)
    def test_get_method_does_not_call_zk_when_timedelta_does_not_change(self, mock_class):
        node = "/test/node"
        original_val = "value"
        new_val = "new_value"

        mock_client = mock_class.return_value
        mock_client.get.side_effect = {node: (str.encode(original_val), "stuff")}.get

        zk_cache = ZKCache(zk_node=node)
        self.assertEqual(zk_cache.get(), original_val)

        # Change the value of the node
        mock_client.get.side_effect = {node: (str.encode(new_val), "stuff")}.get

        # as the time is still within the time_delta, we dont make a call to the ZK client
        zk_cache.time = datetime.datetime.now()
        self.assertEqual(zk_cache.get(), original_val)

    @patch('noauth.zk.zk_cache.KazooClient', autospec=True)
    def test_get_method_calls_zk_on_timedelta_change(self, mock_class):
        node = "/test/node"
        original_val = "value"
        new_val = "new_value"

        mock_client = mock_class.return_value
        mock_client.get.side_effect = {node: (str.encode(original_val), "stuff")}.get

        zk_cache = ZKCache(zk_node=node)
        self.assertEqual(zk_cache.get(), original_val)

        # Change the value of the node
        mock_client.get.side_effect = {node: (str.encode(new_val), "stuff")}.get

        # as the time is no longer within the time delta, we make a call to the ZK client
        zk_cache.time = zk_cache.time - timedelta(seconds=zk_cache.cache_time_seconds)
        self.assertEqual(zk_cache.get(), new_val)


if __name__ == '__main__':
    unittest.main()
