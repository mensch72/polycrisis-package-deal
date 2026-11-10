"""Heuristic search by constraint generation (WP6, stages 3 and 4).

Master: multi-start local search for the profile that maximises the product of
normalised gains among profiles that are individually rational, acceptable to every
actor, and not excluded by a cut found so far.
Oracle: for a family of coalitions, local search for a blocking profile; a block
becomes a cut. The loop ends when the oracle finds no block.

Utilities are read from the precomputed table only for speed; the search touches a
profile only through lookups, and the number of distinct profiles looked up is counted.
"""
import numpy as np
from itertools import combinations
from instance import N, D, SHAPE, OWNER, DIMS, TOP, LEVERS, ISSUES, ISSUE_OF

STRIDE = np.array([int(np.prod(SHAPE[d + 1:])) for d in range(D)])
T = 1e-9


class Search:
    def __init__(self, U, acc, scale, rng, starts=12, oracle_starts=5, random_coalitions=12, weights=None):
        self.Uf = U.reshape(N, -1)
        self.U0 = self.Uf[:, 0].copy()
        self.G = (self.Uf - self.U0[:, None]) / scale[:, None]        # normalised gains
        ok = np.all(self.G >= -T, axis=0) & acc.reshape(N, -1).all(0)
        pen = 20 * np.maximum(0, -self.G).sum(0) + 10 * (~acc.reshape(N, -1)).sum(0)
        w = np.ones(N) if weights is None else np.asarray(weights, float)
        self.base = (w[:, None] * np.log(np.maximum(self.G, 1e-3))).sum(0) - pen
        self.ok = ok
        self.rng = rng
        self.cuts = []
        self.seen = np.zeros(self.Uf.shape[1], bool)
        self.excl = np.zeros(self.Uf.shape[1], bool)
        self._cache = {}
        self.starts, self.oracle_starts, self.random_coalitions = starts, oracle_starts, random_coalitions
        clubs = [tuple(sorted({int(OWNER[d]) for d in range(D) if ISSUE_OF[d] == iss})) for iss in ISSUES]
        fam = [tuple(range(N))] + [tuple(j for j in range(N) if j != i) for i in range(N)]
        fam += clubs + [tuple(sorted(set(a) | set(b))) for a, b in combinations(clubs, 2)]
        fam += [(i,) for i in range(N)] + list(combinations(range(N), 2))
        self.family = list(dict.fromkeys(fam))

    def flat(self, a):
        return int(np.dot(a, STRIDE))

    def add_cut(self, g, pt):
        """Exclude every profile whose member utilities are weakly dominated by pt, strictly in one coordinate.
        The exclusion table is filled for all profiles at once only for speed."""
        self.cuts.append((g, pt))
        ug = self.Uf[g]
        self.excl |= np.all(ug <= pt[:, None] + T, axis=0) & np.any(ug < pt[:, None] - T, axis=0)

    def cut_violations(self, f):
        return int(self.excl[f])

    def phi(self, f):
        self.seen[f] = True
        return self.base[f] - 10 * self.cut_violations(f)

    def climb(self, a, dims, score):
        """Best-improvement local search over single-lever moves, then double-lever moves."""
        a = a.copy()
        f = self.flat(a)
        best = score(f)
        while True:
            move = None
            for d in dims:
                for v in range(SHAPE[d]):
                    if v != a[d]:
                        s = score(f + (v - a[d]) * STRIDE[d])
                        if s > best:
                            best, move = s, ((d, v),)
            if move is None:
                for d1, d2 in combinations(dims, 2):
                    for v1 in range(SHAPE[d1]):
                        if v1 == a[d1]:
                            continue
                        for v2 in range(SHAPE[d2]):
                            if v2 == a[d2]:
                                continue
                            s = score(f + (v1 - a[d1]) * STRIDE[d1] + (v2 - a[d2]) * STRIDE[d2])
                            if s > best:
                                best, move = s, ((d1, v1), (d2, v2))
            if move is None:
                return a, best
            for d, v in move:
                a[d] = v
            f = self.flat(a)

    def master(self):
        starts = [np.zeros(D, int), np.minimum(1, TOP), TOP.copy()]
        starts += [np.array([self.rng.integers(0, n) for n in SHAPE]) for _ in range(self.starts)]
        best_a, best_s = None, -np.inf
        for s0 in starts:
            a, s = self.climb(s0, range(D), self.phi)
            f = self.flat(a)
            if self.ok[f] and self.cut_violations(f) == 0 and s > best_s:
                best_a, best_s = a, s
        return best_a, best_s

    def oracle_v1(self, a):
        fa = self.flat(a)
        ga = self.G[:, fa]
        fam = list(self.family)
        for _ in range(self.random_coalitions):
            k = int(self.rng.integers(3, N))
            fam.append(tuple(sorted(self.rng.choice(N, k, replace=False).tolist())))
        for Gc in fam:
            g = list(Gc)
            dims = [d for d in range(D) if OWNER[d] in Gc]

            def score(f, g=g):
                self.seen[f] = True
                delta = self.G[g, f] - ga[g]
                return (float(delta.min()), float(delta.sum()))
            base = np.zeros(D, int)
            s_own = base.copy()
            s_own[dims] = a[dims]
            s_top = base.copy()
            s_top[dims] = TOP[dims]
            starts = [s_own, base, s_top]
            for _ in range(self.oracle_starts):
                r = base.copy()
                r[dims] = [self.rng.integers(0, SHAPE[d]) for d in dims]
                starts.append(r)
            for s0 in starts:
                b, (mn, sm) = self.climb(s0, dims, score)
                delta = self.G[g, self.flat(b)] - ga[g]
                if mn >= -T and delta.max() > T:
                    return Gc, b
        return None

    # ---- oracle, version 2: exact for small coalitions, local search over coalitions AND levers otherwise
    def _sub_flats(self, Gc):
        if Gc not in self._cache:
            dims = [d for d in range(D) if OWNER[d] in Gc]
            fl = np.zeros(int(np.prod([SHAPE[d] for d in dims])) if dims else 1, dtype=np.int64)
            if dims:
                for d, gr in zip(dims, np.meshgrid(*[np.arange(SHAPE[d]) for d in dims], indexing='ij')):
                    fl += gr.reshape(-1) * STRIDE[d]
            self._cache[Gc] = fl
        return self._cache[Gc]

    def exact_small(self, a, max_members=3):
        """Full enumeration of the deviations of every coalition with at most max_members members."""
        ga = self.G[:, self.flat(a)]
        for r in range(1, max_members + 1):
            for Gc in combinations(range(N), r):
                fl = self._sub_flats(Gc)
                self.seen[fl] = True
                g = list(Gc)
                delta = self.G[np.ix_(g, fl)] - ga[g][:, None]
                okb = (delta.min(0) >= -T) & (delta.max(0) > T)
                if okb.any():
                    j = int(np.argmax(np.where(okb, delta.sum(0), -np.inf)))
                    return Gc, np.array(np.unravel_index(int(fl[j]), SHAPE))
        return None

    def coalition_climb(self, a, members, b):
        """Local search over membership and levers. Moves: change one lever of a member, drop a member
        (its levers go to 0), add an outsider at its levels in a; double-lever moves if nothing else helps."""
        ga = self.G[:, self.flat(a)]

        def score(mem, f):
            self.seen[f] = True
            dl = self.G[mem, f] - ga[mem]
            return (float(dl.min()), float(dl.sum()))
        mem = sorted(members)
        b = b.copy()
        f = self.flat(b)
        best = score(mem, f)
        while True:
            move = None
            dims = [d for d in range(D) if OWNER[d] in mem]
            for d in dims:
                for v in range(SHAPE[d]):
                    if v != b[d]:
                        sc = score(mem, f + (v - b[d]) * STRIDE[d])
                        if sc > best:
                            best, move = sc, ('lev', ((d, v),))
            if len(mem) > 1:
                for j in mem:
                    sc = score([i for i in mem if i != j], f - sum(int(b[d]) * STRIDE[d] for d in DIMS[j]))
                    if sc > best:
                        best, move = sc, ('drop', j)
            for j in range(N):
                if j not in mem:
                    sc = score(sorted(mem + [j]), f + sum(int(a[d]) * STRIDE[d] for d in DIMS[j]))
                    if sc > best:
                        best, move = sc, ('add', j)
            if move is None:
                for d1, d2 in combinations(dims, 2):
                    for v1 in range(SHAPE[d1]):
                        if v1 == b[d1]:
                            continue
                        for v2 in range(SHAPE[d2]):
                            if v2 == b[d2]:
                                continue
                            sc = score(mem, f + (v1 - b[d1]) * STRIDE[d1] + (v2 - b[d2]) * STRIDE[d2])
                            if sc > best:
                                best, move = sc, ('lev', ((d1, v1), (d2, v2)))
            if move is None:
                return mem, b, best
            if move[0] == 'lev':
                for d, v in move[1]:
                    b[d] = v
            elif move[0] == 'drop':
                mem = [i for i in mem if i != move[1]]
                b[DIMS[move[1]]] = 0
            else:
                mem = sorted(mem + [move[1]])
                b[DIMS[move[1]]] = a[DIMS[move[1]]]
            f = self.flat(b)

    def oracle(self, a):
        blk = self.exact_small(a)
        if blk is not None:
            return blk
        ga = self.G[:, self.flat(a)]
        fam = [Gc for Gc in self.family if len(Gc) > 3]
        for _ in range(self.random_coalitions):
            k = int(self.rng.integers(4, N))
            fam.append(tuple(sorted(self.rng.choice(N, k, replace=False).tolist())))
        for Gc in fam:
            dims = [d for d in range(D) if OWNER[d] in Gc]
            starts = []
            for src in (a, TOP):
                s0 = np.zeros(D, int)
                s0[dims] = src[dims]
                starts.append(s0)
            for _ in range(self.oracle_starts):
                r = np.zeros(D, int)
                r[dims] = [self.rng.integers(0, SHAPE[d]) for d in dims]
                starts.append(r)
            for s0 in starts:
                mem, b, (mn, sm) = self.coalition_climb(a, list(Gc), s0)
                dl = self.G[mem, self.flat(b)] - ga[mem]
                if mn >= -T and dl.max() > T:
                    return tuple(mem), b
        return None

    def run(self, max_rounds=60, log=None):
        for r in range(max_rounds):
            a, s = self.master()
            if a is None:
                return dict(profile=None, rounds=r + 1, cuts=len(self.cuts), evals=int(self.seen.sum()))
            blk = self.oracle(a)
            if blk is None:
                return dict(profile=a, score=float(s), rounds=r + 1, cuts=len(self.cuts),
                            evals=int(self.seen.sum()))
            Gc, b = blk
            self.add_cut(list(Gc), self.Uf[list(Gc), self.flat(b)].copy())
            if log:
                log(f'    round {r + 1}: blocked by {Gc}')
        return dict(profile=None, rounds=max_rounds, cuts=len(self.cuts), evals=int(self.seen.sum()))
