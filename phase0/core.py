"""Exact checks by enumeration, for utilities given on a full lever grid.

U has shape (n_actors, *shape); owner[d] is the actor who owns lever d.
The reference (no-deal) profile is the all-zero profile.
"""
import numpy as np
from itertools import combinations

TOL = 1e-9


def coalitions(n):
    return [G for r in range(1, n + 1) for G in combinations(range(n), r)]


def coalition_slice(G, owner):
    Gs = set(G)
    return tuple(slice(None) if owner[d] in Gs else 0 for d in range(len(owner)))


def rows_for(U, G, owner):
    """Member utilities over all profiles in which outsiders play level 0: array (m, |G|)."""
    idx = coalition_slice(G, owner)
    return np.stack([np.asarray(U[i][idx]).reshape(-1) for i in G], axis=1)


def cull(cu, rows):
    """alive[j] is False iff candidate cu[j] is weakly dominated by some row,
    strictly in at least one coordinate."""
    alive = np.ones(len(cu), bool)
    m, k = rows.shape
    if m == 0 or len(cu) == 0:
        return alive
    chunk = max(1, int(3e7 // (m * k)))
    for s in range(0, len(cu), chunk):
        c = cu[s:s + chunk]
        ge = (rows[None, :, :] >= c[:, None, :] - TOL).all(-1)
        gt = (rows[None, :, :] > c[:, None, :] + TOL).any(-1)
        alive[s:s + chunk] = ~(ge & gt).any(1)
    return alive


def orientation(U, owner):
    """Orientation test: along every lever the owner's utility must be weakly decreasing
    and every other actor's weakly increasing. Returns the list of violations
    (lever, actor, number of violating steps, largest violation)."""
    viol = []
    for d in range(len(owner)):
        for i in range(U.shape[0]):
            dU = np.diff(U[i], axis=d)
            bad = dU > TOL if i == owner[d] else dU < -TOL
            if bad.any():
                viol.append((d, i, int(bad.sum()), float(np.abs(dU[bad]).max())))
    return viol


def strict_core(U, owner, cand_mask, log=None):
    """Strict core among the candidates in cand_mask (boolean over the grid).
    A candidate a is kept iff it is individually rational and no coalition G has a
    profile a' with outsiders at level 0 that all members weakly prefer and one
    strictly prefers. Blocking profiles are NOT restricted to the candidate set.
    Returns (flat indices of core profiles, info)."""
    n = U.shape[0]
    Uf = U.reshape(n, -1)
    U0 = Uf[:, 0].copy()
    ir = np.all(Uf >= U0[:, None] - TOL, axis=0)
    cand = np.flatnonzero(cand_mask.reshape(-1) & ir)
    info = dict(n_ir=int(ir.sum()), n_candidates=int(len(cand)), blocked={})
    if len(cand) == 0:
        return cand, info
    # grand coalition = efficiency; dominators of IR profiles are IR themselves
    rowsN = Uf[:, ir].T
    top = rowsN[np.argsort(-rowsN.sum(1))[:3000]]      # ordering is only a speed heuristic
    top = top[cull(top, top)]
    alive = cull(Uf[:, cand].T, top)
    n0 = len(cand)
    cand = cand[alive]
    alive = cull(Uf[:, cand].T, rowsN)
    cand = cand[alive]
    info['blocked'][tuple(range(n))] = n0 - len(cand)
    info['n_efficient'] = int(len(cand))
    info['efficient_idx'] = cand.copy()
    if log:
        log(f'  efficient and IR candidates: {len(cand)}')
    for G in sorted(coalitions(n)[:-1], key=len):
        if len(cand) == 0:
            break
        g = list(G)
        rows = rows_for(U, G, owner)
        cu = Uf[np.ix_(g, cand)].T
        rows = rows[np.all(rows >= np.maximum(U0[g], cu.min(0)) - TOL, axis=1)]
        alive = cull(cu, rows)
        if (~alive).any():
            info['blocked'][G] = int((~alive).sum())
        cand = cand[alive]
    return cand, info


def margins(U, owner, a_flat, scale):
    """Blocking margin e(G, a) = max over a' (outsiders at 0) of the smallest normalised
    gain of a member, for every coalition G. Zero for G = N iff a is weakly efficient."""
    n = U.shape[0]
    Uf = U.reshape(n, -1)
    out = {}
    for G in coalitions(n):
        g = list(G)
        rows = rows_for(U, G, owner)
        delta = (rows - Uf[g, a_flat][None, :]) / scale[g][None, :]
        out[G] = float(delta.min(1).max())
    return out


def in_strict_core(U, owner, a_flat):
    """Direct test of one profile against every coalition. Returns (True, None) or (False, G)."""
    n = U.shape[0]
    Uf = U.reshape(n, -1)
    for G in sorted(coalitions(n), key=len):
        g = list(G)
        rows = rows_for(U, G, owner)
        u = Uf[g, a_flat]
        ge = np.all(rows >= u - TOL, axis=1)
        if ge.any() and np.any(rows[ge] > u + TOL):
            return False, G
    return True, None


def sufficient_groups(indicator, owner, lever_dims, target, n):
    """Minimal groups that can reach indicator >= target with everyone else at level 0.
    indicator must be weakly increasing in every lever. lever_dims: levers that move it."""
    shape = indicator.shape
    owners = sorted(set(int(owner[d]) for d in lever_dims))
    suff = []
    for r in range(1, len(owners) + 1):
        for S in combinations(owners, r):
            idx = tuple((shape[d] - 1) if (owner[d] in S) else 0 for d in range(len(shape)))
            if indicator[idx] >= target - TOL:
                suff.append(set(S))
    minimal = [S for S in suff if not any(T < S for T in suff)]
    veto = set(owners)
    for S in suff:
        veto &= S
    return minimal, (veto if suff else set())


def over_fulfilment(U, owner, a_star):
    """Number of coalitions whose members all weakly gain, one strictly, when they raise their own
    levers above a_star while everyone else stays at a_star. Zero whenever every lever is costly
    to its owner; checked separately because the orientation test can fail elsewhere on the grid."""
    n = U.shape[0]
    a_flat = int(np.ravel_multi_index(tuple(int(x) for x in a_star), U.shape[1:]))
    ua = U.reshape(n, -1)[:, a_flat]
    count = 0
    for G in coalitions(n):
        idx = tuple(slice(int(a_star[d]), None) if owner[d] in G else int(a_star[d]) for d in range(len(owner)))
        rows = np.stack([np.asarray(U[i][idx]).reshape(-1) for i in G], axis=1)
        u = ua[list(G)]
        ge = np.all(rows >= u - TOL, axis=1)
        if ge.any() and np.any(rows[ge] > u + TOL):
            count += 1
    return count
