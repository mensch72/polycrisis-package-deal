"""Towers of coalitions and CCF profiles in a pre-CPEP (Jobst's proposal of 10 November 2026).

A CPEP is a costly positive externality problem (Heitzig, 2025): every lever costs its owner and is
weakly welcome to everyone else. A pre-CPEP drops the second half: a lever may harm other actors.

A tower is a weakly ascending chain of coalitions I_1, ..., I_m = I with CCF profiles c_1 <= ... <= c_m = c
such that for every k
  (i)  c_k is constantly zero for actors outside I_k and, for actors in I_k, ignores actors outside I_k;
  (ii) the game restricted to I_k, with everyone outside at a0 = 0 and the members of I_(k-1) restricted to
       actions at or above the outcome b(c_(k-1)), is a proper CPEP in which c_k is a strong equilibrium.

Readings chosen here, to be confirmed by Jobst [assumption]:
  - "proper CPEP for I_k" is tested on the utilities of the members of I_k only. Outsiders may be harmed.
  - the stage reference is the bottom of the stage box, b(c_(k-1)); gains at stage k are measured from it.
  - the canonical tower filing is a nested step function: actor i in I_k is liable for b_k,i if every other
    member of I_k is at or above b_k, for the largest such k, and for 0 if there is none.
Strong equilibria of a CPEP have exactly the strict-core outcomes, and step functions sustain them
[proved: Heitzig, 2025, Theorems 2 and A1]. The code does not rely on this: it tests deviations directly.

Everything is exact, by enumeration over a full lever grid U (n_actors, *shape); owner[d] owns lever d.
"""
from itertools import product
import numpy as np
import core

TOL = core.TOL


def violation_steps(U, owner):
    """For every (lever d, actor i) that violates the orientation test somewhere: boolean array over the
    steps along d (shape with axis d shortened by one), True where the step violates."""
    out = {}
    for d in range(len(owner)):
        for i in range(U.shape[0]):
            dU = np.diff(U[i], axis=d)
            bad = dU > TOL if i == owner[d] else dU < -TOL
            if bad.any():
                out[(d, i)] = bad
    return out


def box_is_cpep(viol, owner, members, lower):
    """Is the stage game a proper CPEP? Members' levers range from lower upwards, all other levers are 0.
    Only violations in which both the owner of the lever and the affected actor are members count."""
    members = set(members)
    for (d, i), bad in viol.items():
        if owner[d] not in members or i not in members:
            continue
        idx = tuple(slice(int(lower[q]), None) if owner[q] in members else slice(0, 1) for q in range(len(owner)))
        if bad[idx].any():
            return False
    return True


def stage_game(U, owner, members, lower):
    """Utilities of the members over the stage box. Returns (Uk, dims, owner_k, sub_shape)."""
    members = list(members)
    idx = tuple(slice(int(lower[d]), None) if owner[d] in members else 0 for d in range(len(owner)))
    Uk = U[members][(slice(None),) + idx]
    dims = [d for d in range(len(owner)) if owner[d] in members]
    owner_k = np.array([members.index(int(owner[d])) for d in dims])
    return Uk, dims, owner_k, Uk.shape[1:]


def to_full(sub_flat, dims, sub_shape, lower, D):
    """Stage-box flat index -> full profile (length D)."""
    a = np.zeros(D, int)
    a[dims] = np.array(np.unravel_index(int(sub_flat), sub_shape)) + np.asarray(lower)[dims]
    return a


def registry(stages, shape, owner, G, devs):
    """Registry rule for the nested step filing of a tower, vectorised over deviations.
    stages: list of (members, b_k) with b_k ascending full profiles. The actors in G file the constants
    devs (m x D; only their own levers are read). Greatest fixed point by iteration from the top."""
    D = len(shape)
    n = int(max(owner)) + 1
    a = np.tile(np.array(shape) - 1, (len(devs), 1))
    inG = np.array([owner[d] in G for d in range(D)])
    mine = {i: np.array([owner[d] == i for d in range(D)]) for i in range(n)}
    for _ in range(100):
        new = a.copy()
        if inG.any():
            new[:, inG] = np.minimum(a[:, inG], devs[:, inG])
        for i in range(n):
            if i in G:
                continue
            lim = np.zeros((len(devs), int(mine[i].sum())), int)
            for members, b in stages:                       # ascending, so later stages overwrite
                if i not in members:
                    continue
                oth = np.array([owner[d] in members and owner[d] != i for d in range(D)])
                ok = np.all(a[:, oth] >= b[oth], axis=1) if oth.any() else np.ones(len(devs), bool)
                lim = np.where(ok[:, None], b[mine[i]][None, :], lim)
            new[:, mine[i]] = np.minimum(a[:, mine[i]], lim)
        if np.array_equal(new, a):
            return a
        a = new
    raise RuntimeError('no fixed point')


def all_devs(shape, owner, G, lower=None):
    rng = [range(int(lower[d]) if lower is not None else 0, shape[d]) if owner[d] in G else (0,)
           for d in range(len(shape))]
    return np.array(list(product(*rng)), dtype=np.int64)


def profitable(U, shape, G, outcomes, ref_flat):
    """Mask over outcomes (m x D): all members of G weakly better than at ref, one strictly."""
    Uf = U.reshape(U.shape[0], -1)
    fl = np.ravel_multi_index(outcomes.T, shape)
    d = Uf[np.ix_(list(G), fl)] - Uf[list(G), ref_flat][:, None]
    return np.all(d >= -TOL, axis=0) & np.any(d > TOL, axis=0)


def stage_deviations(U, shape, owner, members, lower, b):
    """Test (ii) directly for one stage: every group G inside the coalition, every constant deviation
    inside the stage box; the others answer with the step through b, else fall to the box bottom;
    outsiders stay at 0. Returns the number of profitable deviations per group."""
    members = sorted(members)
    D = len(shape)
    ref = int(np.ravel_multi_index(tuple(b), shape))
    res = {}
    for G in core.coalitions(len(members)):
        G = tuple(members[j] for j in G)
        dv = all_devs(shape, owner, G, lower)
        inG = np.array([owner[d] in G for d in range(D)])
        inM = np.array([owner[d] in members for d in range(D)])
        ok = np.all(dv[:, inG] >= b[inG], axis=1)
        out = np.where(ok[:, None], b[None, :], np.asarray(lower)[None, :])
        out[:, inG] = dv[:, inG]
        out[:, ~inM] = 0
        n = int(profitable(U, shape, G, out, ref).sum())
        if n:
            res[G] = n
    return res
