from paramikolab import makeConnection

def test_makeConnection():
    assert makeConnection("172.31.134.1") == "Run success"
    assert makeConnection("172.31.134.2") == "Run success"
    assert makeConnection("172.31.134.3") == "Run success"
    assert makeConnection("172.31.134.4") == "Run success"
    assert makeConnection("172.31.134.5") == "Run success"
    assert makeConnection("172.31.134.1", "172.31.134.2", "172.31.134.3", "172.31.134.4", "172.31.134.5") == "Run success"
    assert makeConnection("172.31.134.6") == "Can't connect to host"

print("hello world");