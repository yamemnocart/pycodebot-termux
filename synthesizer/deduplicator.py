class Deduplicator:
    def __init__(self, threshold=0.7, num_hashes=32):
        self.t = threshold
        self.n = num_hashes
        # 32 số nguyên tố lớn cho hàm hash
        self.primes = [
            1000003, 1000033, 1000037, 1000039, 1000081, 1000099,
            1000117, 1000121, 1000133, 1000151, 1000159, 1000171,
            1000183, 1000187, 1000193, 1000211, 1000213, 1000229,
            1000231, 1000249, 1000253, 1000273, 1000279, 1000291,
            1000303, 1000333, 1000357, 1000369, 1000379, 1000393,
            1000409, 1000423
        ]
        self.big = 2**61 - 1

    def _shingle(self, text: str):
        t = text.lower()
        return set(t[i:i+3] for i in range(max(0, len(t)-2)))

    def _minhash(self, shingles: set) -> tuple:
        sig = []
        for p in self.primes:
            m = self.big
            for s in shingles:
                h = (hash(s) * p) % self.big
                if h < m: m = h
            sig.append(m)
        return tuple(sig)

    def _sim(self, a, b):
        return sum(1 for x,y in zip(a,b) if x==y) / self.n

    def filter(self, items: list) -> list:
        sigs = [self._minhash(self._shingle(it["content"])) for it in items]
        keep = []
        for i in range(len(items)):
            dup = False
            for j in keep:
                if self._sim(sigs[i], sigs[j]) >= self.t:
                    dup = True; break
            if not dup:
                keep.append(i)
        return [items[i] for i in keep]
