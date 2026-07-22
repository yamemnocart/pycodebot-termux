class Ranker:
    def sort(self, items: list) -> list:
        def score(it):
            vote = max(0, it.get("vote", 0))
            w = it.get("weight", 1)
            # Công thức: điểm = (vote + 1) * trọng số nguồn
            return (vote + 1) * w
        return sorted(items, key=score, reverse=True)
