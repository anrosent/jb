from jb.parse import make_stamp

f = open

def stampTest():
    assert make_stamp(3) == int
    assert make_stamp([1,2,3]) == set(int)
    assert make_stamp([1,"2",3]) == set(int, str)
    assert make_stamp({"4":4}) == ("4")
    assert make_stamp({"4":4, "5": [1,2]}) == ("4", "5")
