import time

try:
    import redis

    REDIS_2 = redis.__version__.startswith("2.")
except:
    REDIS_2 = False


class Rede(object):
    def __init__(self, redis, name):
        """
        The rede is an effective 'snooze button' for events,
        you push an event into it along (for future referance) and in how many seconds you want it back,
        and poll whenever you want the elements back. only expired elements would pop out.

        :param redis: a Redis client object
        :type redis: object
        :param name: Set the collection of elements to name
        :type name: str
        """
        redis_version = redis.info()['redis_version']  # 'redis_version': '5.0.11'
        if redis_version < '5.0.0':
            raise ValueError("Redis version must be >= 5.0.0")
        self._redis = redis
        self._name = name

    def push(self, element, ttl):
        """
        Push an element into the dehydrator for ttl seconds, marking it with element_id
        Note: if the key does not exist this command will create a Dehydrator on it.

        :param element: Push an element into the dehydrator
        :type element: str
        :param ttl: Push an element into the dehydrator for ttl seconds
        :type ttl: int
        :return: The return value of ZADD varies based on the mode specified. With no options, ZADD returns the number of new elements added to the sorted set.
        :rtype: int
        """

        expire_timestamp = time.time() + ttl
        if REDIS_2:
            return self._redis.zadd(self._name, element, expire_timestamp)
        return self._redis.zadd(self._name, {element: expire_timestamp})

    def pull(self, *elements):
        """
        Pull the element, remove it from the dehydrator before it expires.

        :param elements:
        :type elements:
        :return: The number of elements removed from the sorted set, not including non existing elements.
        :rtype: list
        """

        return self._redis.zrem(self._name, *elements)

    def poll(self):
        """
        POLL dehydrator_name
        Pull and return all the expired elements in dehydrator_name.

        :return: List of all expired elements on success, or an empty list if no elements are expired, the key is empty or the key contains something other the a dehydrator.
        :rtype: list
        """
        elements = []
        while True:
            if REDIS_2:
                pop_result: list = self._redis.execute_command("ZPOPMIN", self._name, count=1)  # [] or ['a', '1.0']
            else:
                pop_result: list = self._redis.zpopmin(self._name, count=1)  # [] or [('a', 1.0)]
            if not pop_result:
                break

            if REDIS_2:
                element, expire_timestmap = pop_result
                if isinstance(expire_timestmap, bytes):
                    expire_timestmap = expire_timestmap.decode()
                expire_timestmap = float(expire_timestmap)
            else:
                element, expire_timestmap = pop_result[0]

            if time.time() < expire_timestmap:
                if REDIS_2:
                    self._redis.zadd(self._name, element, expire_timestmap)
                else:
                    self._redis.zadd(self._name, {element: expire_timestmap})
                break
            elements.append(element)
        return elements

    def look(self, element):
        """
        LOOK dehydrator_name element
        Show the ttl corresponding with element and without removing it from the dehydrator.

        :param element: element
        :type element: str
        :return: The ttl represented by element on success, None if key is empty or not a dehydrator, or element does not exist.
        :rtype: float
        """
        expire_timestamp = self._redis.zscore(self._name, element)  # None or float
        if expire_timestamp is None:
            return None
        return max(0, expire_timestamp - time.time())

    def ttn(self):
        """
        Show the time left (in seconds) until the next element will expire.

        :return: int representing the number of seconds until next element will expire. Null if dehydrator_name does not contain a dehydrator.
        :rtype: float
        """
        result = self._redis.zrange(self._name, 0, 0, withscores=True)  # [] or [('a', 1.0)]
        if result is []:
            return None
        _, expire_timestamp = result[0]
        return max(0, expire_timestamp - time.time())
