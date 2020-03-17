import pandas as pd
import pyarrow as pa
import redis

"""
Timing Notes:

%timeit r = redis.Redis(host='localhost', port=6379, db=0)
168 µs ± 12.9 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit pa.default_serialization_context()
16 µs ± 1.14 µs per loop (mean ± std. dev. of 7 runs, 100000 loops each)

"""


def write_to_redis(key: str, value, expiration: int = 3600):
    """
    Writes to local redis instance

    value is usually a dataframe

    :param key: str
    :param value:
    :param expiration: int, time until value expires in seconds
    :return:
    """

    print(f'Writing to redis. {key}. {expiration}. {value}')

    redis_con = redis.Redis(host='localhost', port=6379, db=0)
    context = pa.default_serialization_context()
    val_serialized = context.serialize(value).to_buffer().to_pybytes()
    redis_con.set(name=key, value=val_serialized, ex=expiration)


def read_from_redis(key: str):
    """
    Read key from local redis instance.
    Returns None if the key does not exist

    :param key:
    :return:
    """

    redis_con = redis.Redis(host='localhost', port=6379, db=0)
    val_serialized = redis_con.get(name=key)
    if val_serialized:
        context = pa.default_serialization_context()
        return context.deserialize(val_serialized)
    else:
        return None




