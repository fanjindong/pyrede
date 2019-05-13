import time

from redis import Redis

from pyrede import Rede

rds = Redis()
rde = Rede(rds, "demo")


def test_Rede():
    rde.push("a", 1)
    rde.push("b", 2)
    rde.push("c", 3)

    assert 0 < rde.ttn() < 1

    assert 0 < rde.look("a") < 1
    assert 1 < rde.look("b") < 2
    assert 2 < rde.look("c") < 3

    rde.pull("a")
    assert rde.look("a") is None
    assert 1 < rde.ttn() < 2

    rde.push("c", 2)
    time.sleep(2)
    assert rde.poll() == [b"b", b"c"]
