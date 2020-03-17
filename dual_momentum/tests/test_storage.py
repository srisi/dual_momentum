import unittest
import redis
from dual_momentum.ticker_data import TickerData
from dual_momentum.storage import write_to_redis, read_from_redis
import time

class TestRedisReadWrite(unittest.TestCase):
    """
    Test if reading and writing to redis works and if dataframes remain the same after
    getting put in redis

    """

    def setUp(self):
        self.ticker_data = TickerData('SPY')

    def test_write_and_read(self):
        write_to_redis(key='spy_monthly', value=self.ticker_data.data_monthly, expiration=10)
        write_to_redis(key='spy_daily', value=self.ticker_data.data_daily, expiration=10)

        spy_daily = read_from_redis('spy_daily')
        spy_monthly = read_from_redis('spy_monthly')
        self.assertTrue(spy_daily.equals(self.ticker_data.data_daily))
        self.assertTrue(spy_monthly.equals(self.ticker_data.data_monthly))

class TestRedisExpiration(unittest.TestCase):
    """
    Test if values properly expire from redis

    """

    def setUp(self):
        self.redis_con = redis.Redis(host='localhost', port=6379, db=1)
        self.redis_con.flushall()

    def tearDown(self):
        self.redis_con.flushall()

    def test_expiration(self):
        self.redis_con.set(name='test_exp', value='t', ex=3)
        self.assertEqual(self.redis_con.get('test_exp'), b't')
        time.sleep(4)
        self.assertEqual(self.redis_con.get('test_exp'), None)


if __name__ == '__main__':
    unittest.main()




