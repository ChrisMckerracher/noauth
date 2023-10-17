import unittest
from unittest.mock import patch, Mock

from noauth.db.es.es_cache_repository import EsCacheRepository
from tests.db.redis.mock_redis import MockRedisEntity
from tests.util.jsons import load_and_modify
from pathlib import Path

class TestEsCacheRepository(unittest.TestCase):

    def setUp(self):

        self.test_id = "test_id"
        self.expected_index = MockRedisEntity.model_fields['index'].default
        self.es = Mock()
        self.redis = Mock()
        self.sit: EsCacheRepository = EsCacheRepository[MockRedisEntity](self.es, self.redis, MockRedisEntity)
        self.path = str(Path(__file__).parent.absolute())

    def test_get_with_cached_value(self):

        expected = MockRedisEntity(id=self.test_id)
        query = Mock()

        with patch("tests.db.redis.mock_redis.MockRedisQuery") as class_mock:
            class_mock.return_value = query
            query.get = lambda x: expected if x is self.test_id else (_ for _ in ()).throw(Exception())

            # This causes a recursion depth exception if the test fails! wtf. ONLY if you throw exception from the generator in the lambda??? EVEN IF the exception doesnt get thrown??? maybe???
            self.assertEqual(self.sit.get(self.test_id), expected)

    def test_get_with_uncached_value(self):

        expected = MockRedisEntity(id=self.test_id)
        query = Mock()

        with patch("tests.db.redis.mock_redis.MockRedisQuery") as class_mock:
            class_mock.return_value = query
            query.get = lambda x: None

            self.es.get = lambda index=None, id=None: load_and_modify(
                f"{self.path}/jsons/found.json", {"_source": {
                    "index": index, "id": self.test_id}}) if index is self.expected_index and id is self.test_id else \
                (_ for _ in ()).throw(Exception())

            self.assertEqual(self.sit.get(self.test_id), expected)

    def test_get_with_uncached_value_not_in_es(self):
        test_id = "test_id"
        expected_index = MockRedisEntity.model_fields['index'].default
        expected = None
        query = Mock()

        with patch("tests.db.redis.mock_redis.MockRedisQuery") as class_mock:
            class_mock.return_value = query
            query.get = lambda x: None

            self.es.get = lambda index=None, id=None: load_and_modify(
                f"{self.path}/jsons/not_found.json") if index is expected_index and id is test_id else \
                (_ for _ in ()).throw(Exception())

            self.assertEqual(self.sit.get(test_id), expected)

    #ToDo: ES may throw an exception still and we don't ahndle this

