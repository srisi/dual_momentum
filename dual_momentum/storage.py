import pyarrow as pa
import redis
import pandas as pd
from copy import deepcopy

from IPython import embed

"""
Timing Notes:

%timeit r = redis.Redis(host='localhost', port=6379, db=0)
168 µs ± 12.9 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit pa.default_serialization_context()
16 µs ± 1.14 µs per loop (mean ± std. dev. of 7 runs, 100000 loops each)

"""

# Sometimes, in particular when running dual-momentum in docker for backtesting,
# redis is not available
# in that case, cache all of the ticker and index values and discard everything else
CACHE = {}

def write_to_redis(key: str, value, expiration: int = 3600):
    """
    Writes to local redis instance

    value is usually a dataframe

    :param key: str
    :param value:
    :param expiration: int, time until value expires in seconds
    :return:
    """

    try:
        redis_con = redis.Redis(host='localhost', port=6379, db=0)
        context = pa.default_serialization_context()
        val_serialized = context.serialize(value).to_buffer().to_pybytes()
        redis_con.set(name=key, value=val_serialized, ex=expiration)

    except redis.exceptions.ConnectionError:
        if key.startswith('cache'):
            # is df.copy(deep=True) equivalent to deepcopy()? Presumably...
            if isinstance(value, pd.DataFrame):
                val_copy = value.copy(deep=True)
            else:
                val_copy = deepcopy(value)
            CACHE[key] = val_copy

def read_from_redis(key: str):
    """
    Read key from local redis instance.
    Returns None if the key does not exist

    :param key:
    :return:
    """


    try:
        redis_con = redis.Redis(host='localhost', port=6379, db=0)
        val_serialized = redis_con.get(name=key)
        if val_serialized:
            context = pa.default_serialization_context()
            return context.deserialize(val_serialized)
        else:
            return None
    except redis.exceptions.ConnectionError:
        if key in CACHE:
            if isinstance(CACHE[key], pd.DataFrame):
                return CACHE[key].copy(deep=True)
            else:
                return deepcopy(CACHE[key])
        else:

            print("cache miss", key)
            return None
