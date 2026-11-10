"""Fallbacks for an empty core (WP6), exact by enumeration, for utilities on a full lever grid.

Fallback 1: the candidate with the smallest blocking margin, max over G of e(G, a) as in docs/plan.md.
Fallback 3: the core of every sub-package, that is, of every non-empty subset of the issues.
(Fallback 2, far-sighted stability, belongs to WP8 and is not implemented here.)
"""
from itertools import combinations
import numpy as np
import core

TOL = core.TOL


def margin_table(U, owner, cand, scale):
    """e(G, a) for every candidate a (flat indices) and every coalition G: array (len(cand), n_coalitions),
    and the list of coalitions. e(G, a) = max over a' with outsiders at 0 of the smallest normalised gain
    of a member of G over a. It is positive iff G can make all its members strictly better off."""
    n = U.shape[0]
    Uf = U.reshape(n, -1)
    Gs = core.coalitions(n)
    E = np.empty((len(cand), len(Gs)))
    for j, G in enumerate(Gs):
        g = list(G)
        rows = core.rows_for(U, G, owner) / scale[g][None, :]            # (m, |G|)
        ua = (Uf[np.ix_(g, cand)] / scale[g][:, None]).T                 # (c, |G|)
        chunk = max(1, int(2e7 // (rows.shape[0] * len(g))))
        for s in range(0, len(cand), chunk):
            E[s:s + chunk, j] = (rows[None, :, :] - ua[s:s + chunk, None, :]).min(-1).max(-1)
    return E, Gs


def least_margin(U, owner, cand, scale):
    """Fallback 1. Returns dict with the margins of all candidates, the minimum, and the minimisers."""
    E, Gs = margin_table(U, owner, cand, scale)
    worst = E.max(1)
    eps = float(worst.min())
    arg = np.flatnonzero(worst <= eps + 1e-12)
    return dict(E=E, coalitions=Gs, worst=worst, eps=eps, minimisers=cand[arg], minimiser_rows=arg)


def strict_blockers(U, owner, a_flat):
    """All coalitions that block a in the strict-core sense (all members weakly, one strictly better)."""
    n = U.shape[0]
    Uf = U.reshape(n, -1)
    out = []
    for G in core.coalitions(n):
        g = list(G)
        rows = core.rows_for(U, G, owner)
        u = Uf[g, a_flat]
        ge = np.all(rows >= u - TOL, axis=1)
        if ge.any() and np.any(rows[ge] > u + TOL):
            out.append(G)
    return out


def subpackage_cores(U, owner, issue_of, issues, acc=None):
    """Fallback 3. For every non-empty subset of the issues: the game in which only the levers of these
    issues move (all others at 0). Returns per subset the counts of individually rational, efficient and
    strict-core profiles, without aspiration filter and, if acc is given, inside the acceptable region."""
    n = U.shape[0]
    D = len(owner)
    res = {}
    for r in range(1, len(issues) + 1):
        for S in combinations(issues, r):
            dims = [d for d in range(D) if issue_of[d] in S]
            idx = tuple(slice(None) if issue_of[d] in S else 0 for d in range(D))
            Uk = U[(slice(None),) + idx]
            ow = np.asarray(owner)[dims]
            ck, info = core.strict_core(Uk, ow, np.ones(Uk.shape[1:], bool))
            entry = dict(n_profiles=int(np.prod(Uk.shape[1:])), n_ir=info['n_ir'],
                         n_efficient=info.get('n_efficient', 0), n_core=int(len(ck)), core_flat=ck, dims=dims)
            if acc is not None:
                Ck = acc[(slice(None),) + idx].all(0)
                ckC, infoC = core.strict_core(Uk, ow, Ck)
                entry.update(n_acceptable=int(Ck.sum()), n_candidates_in_C=infoC['n_candidates'],
                             n_core_in_C=int(len(ckC)), core_in_C_flat=ckC)
            res['+'.join(S)] = entry
    return res
