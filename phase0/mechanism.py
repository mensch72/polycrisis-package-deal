"""The registry rule and conditional commitment functions (CCFs) on the lever lattice.

A CCF of actor i maps a full profile a (only the others' levers are read) to an upper
limit on i's own levers. The registry returns the largest profile a with
a_i <= c_i(a_-i) for all i. For weakly increasing CCFs this is the greatest fixed point
of a -> min(a, c(a)), reached by iterating downwards from the top of the lattice.
"""
import numpy as np
from instance import N, D, OWNER, DIMS, TOP


def canonical(i, a_star):
    """Step CCF through a_star: own listed levels iff every other lever is at or above its listed level."""
    dims = DIMS[i]
    others = [d for d in range(D) if OWNER[d] != i]
    a_star = np.asarray(a_star)

    def c(a):
        return a_star[dims] if np.all(a[others] >= a_star[others]) else np.zeros(len(dims), int)
    return c


def constant(i, x):
    x = np.asarray(x)
    return lambda a: x


def outcome(ccfs, max_iter=10000):
    a = TOP.copy()
    for _ in range(max_iter):
        changed = False
        for i in range(N):
            new = np.minimum(a[DIMS[i]], ccfs[i](a))
            if np.any(new != a[DIMS[i]]):
                a[DIMS[i]] = new
                changed = True
        if not changed:
            return a
    raise RuntimeError('no fixed point reached')


def closed_form_deviation(a_star, G, x):
    """Outcome when the members of G switch to unconditional actions x (dict actor -> levels)
    and everyone else keeps the canonical CCF through a_star."""
    a_star = np.asarray(a_star)
    a = np.zeros(D, int)
    ok = all(np.all(np.asarray(x[i]) >= a_star[DIMS[i]]) for i in G)
    for i in range(N):
        if i in G:
            a[DIMS[i]] = x[i]
        elif ok:
            a[DIMS[i]] = a_star[DIMS[i]]
    return a
