import unittest
from unittest.mock import patch

from noauth.db.redis.client_builder import get_client


class TestClientBuilder(unittest.TestCase):

    @patch("noauth.db.redis.client_builder.Redis")
    @patch("noauth.db.redis.client_builder.os")
    def test_client_builder_used_localhost_in_dev_mode(self, os_mock, redis_mock):
        os_mock.getenv.side_effect = lambda val, default: "DEV"

        get_client()
        redis_mock.assert_called_with(host="localhost", port=6379, decode_responses=True)

    @patch("noauth.db.redis.client_builder.ZKCache")
    @patch("noauth.db.redis.client_builder.Redis")
    @patch("noauth.db.redis.client_builder.os")
    def test_client_builder_calls_zk_node_in_Prod(self, os_mock, redis_mock, zk_cache_mock):
        expected_value = "http://not_local_host.com"

        zk_cache_obj = zk_cache_mock.return_value

        zk_cache_obj.get.return_value = expected_value

        os_mock.getenv.side_effect = lambda val, default: "PROD"

        get_client()
        redis_mock.assert_called_with(host=expected_value, port=6379, decode_responses=True)
