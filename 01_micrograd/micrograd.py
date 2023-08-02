# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import math
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline


# %%
def f(x):
    return 3*x**2 - 4*x +5


# %%
f(3.0)

# %%
# plotting the function
xs = np.arange(-5, 5, 0.25)
ys = f(xs)
plt.plot(xs, ys)


# %%
# derivative calculation

h = 0.001
x = 2/3
(f(x + h) - f(x))/h

# %%
# more complex
a = 2.0
b = -3.0
c = 10.0
d = a*b + c
print(d)


# %%
# get derivatives with respect to a
h = 0.001

#inputs
a = 2.0
b = -3.0
c = 10.0
d = a*b + c

d1 = a*b + c
# derivative w.r.t a/b/c
# a += h
# b += h
c += h
d2 = a*b + c

print('d1', d1)
print('d2', d2)
print('slope', (d2 - d1)/h)



# %%
class Value:
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __repr__(self):
        return f"Value(data={self.data})"

    def __add__(self, other):
        out = Value(self.data + other.data, (self, other), '+') 
        return out
        
    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), '*')
        return out


# a*b +c is Equivalent to a.__mul__(b).__add(c)
a = Value(2.0, label='a')
b = Value(-3.0, label='b')
c = Value(10.0, label='c')
e = a*b; e.label = 'e'
d = e + c; d.label = 'd'
f = Value(-2.0, label='f')
L = d*f; L.label = 'L'
L
# d
# d._prev
# d._op
# d

# %%
#visualization of the nodes
from graphviz import Digraph

def trace(root):
    # builds a set of all nodes and edges in a graph
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges
def draw_dot(root):
    # create a Digraph object
    dot = Digraph(format = 'svg', graph_attr = {'rankdir': 'LR'}) #LR - Left to Right

    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        # for any value in the graph create a rectangular ('record') node for it
        dot.node(name = uid, label = "{ %s | data %0.4f}" % (n.label, n.data), shape = 'record')
        if n._op:
            # if the value is result of an op create a op node for it
            dot.node(name = uid + n._op, label = n._op)
            # and connect this node to it
            dot.edge(uid + n._op, uid)
            
    for n1, n2 in edges:
        # connect n1 to the op node of n2
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)

    return dot
            


# %%
draw_dot(L)

# %%
