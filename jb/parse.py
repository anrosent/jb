import json
from collections import defaultdict

class JBNode:
    def __init__(self, o):
        self.stamp = make_stamp(o)
        self.kvs = defaultdict(JBValSet)

    def addKV(self, k, v):
        if k not in self.kvs:
            self.kvs[k] = JBValSet()
        self.kvs[k].add(v)

    def merge(self, node):
        diff = set(self.kvs.keys()) ^ set(node.kvs.keys())
        for k, vs in node.kvs.items():
            self.kvs[k].merge(vs)
            self.kvs[k].maybe = (k in diff)

    def __str__(self):
        return "<%s>" % dict(self.kvs)

    def __repr__(self):
        return str(self)

class JBValSet:

    def __init__(self):
        self.valset = set()
        self.maybe = False

    def add(self, val):
        self.valset.add(make_stamp(val))

    def merge(self, vs):
        self.valset |= vs.valset

    def __str__(self):
        return "[%s]<%s>" % ("maybe" if self.maybe else "required", self.valset)

    def __repr__(self):
        return str(self)

def _parse(o, nodeAcc=None): 
    root = False
    if nodeAcc is None:
        root = True
        nodeAcc = {}

    if isinstance(o, dict):
        node = JBNode(o)
        for k, v in o.items():
            node.addKV(k,v)
            _parse(v, nodeAcc)
        stamp = make_stamp(o)
        if stamp in nodeAcc:
            nodeAcc[stamp].merge(node)
        else:
            nodeAcc[stamp] = node
    elif isinstance(o, list):
        for el in o:
            _parse(el, nodeAcc)
    else:
        # Don't scan scalar vals
        pass

    if root:
        return {"root": nodeAcc}


def make_stamp(o):
    if isinstance(o, dict):
        return tuple(sorted(o.keys()))
    elif isinstance(o, list):
        return frozenset(map(make_stamp, o))
    else:
        return type(o)

def browse(s):
    p = _parse(json.loads(s))
    print(str(p))

