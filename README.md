![](https://img.shields.io/github/release/fanjindong/pyrede.svg)
![](https://img.shields.io/github/issues/fanjindong/pyrede.svg)
![](https://img.shields.io/pypi/pyversions/pyrede.svg)
![](https://img.shields.io/travis/com/fanjindong/pyrede/master.svg)
![](https://img.shields.io/github/last-commit/fanjindong/pyrede.svg)

<h1>  pyrede - The <img src="https://upload.wikimedia.org/wikipedia/en/6/6b/Redis_Logo.svg" alt="redis" height="47" align="top"/> Element Snooze Python Module</h1>

:rocket:**A Rede is a fancy snooze delayed queue**


**Usage**

The Rede is an effective 'snooze button' for events,
you push an event into it along (for future referance) and in how many seconds you want it back,
and poll whenever you want the elements back. only expired elements would pop out.


```
   import pyrede
   import redis

   rede = pyrede.Rede(redis.Redis(decode_responses=True), "demo")

   rede.push("123", 1)
   rede.push("456", 1)
   rede.push("789", 3)

   time.sleep(1)

   list(rede.poll())
```
output-> ["123", "456"]