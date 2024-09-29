import heapq
import re

def alignText(d1, d2):
    start = Node(0, 0, 0, [])
    heap = [(0, start)]
    seen = set()

    while heap:
        _, state = heapq.heappop(heap)

        if state.p1 == len(d1) and state.p2 == len(d2):
            return state.route

        if (state.p1, state.p2) in seen:
            continue

        seen.add((state.p1, state.p2))

        if state.p1 < len(d1) and state.p2 < len(d2):
            dist = levDist(d1[state.p1], d2[state.p2])
            newNode = Node(state.p1 + 1, state.p2 + 1, state.cost + dist, state.route + [(state.p1, state.p2, dist)])
            heapq.heappush(heap, (newNode.cost + calcHeur(newNode, d1, d2), newNode))

        if state.p1 < len(d1):
            newNode = Node(state.p1 + 1, state.p2, state.cost + 1, state.route + [(state.p1, None, 1)])
            heapq.heappush(heap, (newNode.cost + calcHeur(newNode, d1, d2), newNode))

        if state.p2 < len(d2):
            newNode = Node(state.p1, state.p2 + 1, state.cost + 1, state.route + [(None, state.p2, 1)])
            heapq.heappush(heap, (newNode.cost + calcHeur(newNode, d1, d2), newNode))

def checkPlag(d1, d2, thresh=0.8):
    doc1 = splitText(d1)
    doc2 = splitText(d2)

    alignment = alignText(doc1, doc2)
    plagCases = []

    for i, j, dist in alignment:
        if i is not None and j is not None:
            maxLen = max(len(doc1[i]), len(doc2[j]))
            sim = 1 - (dist / maxLen)
            if sim >= thresh:
                plagCases.append((i, j, sim))

    return plagCases

def calcHeur(currState, d1, d2):
    rem1 = len(d1) - currState.p1
    rem2 = len(d2) - currState.p2
    return min(rem1, rem2)

def runTests():
    tests = [
        ("Same Docs", "This is a test. It has multiple sentences. We want to detect plagiarism.",
         "This is a test. It has multiple sentences. We want to detect plagiarism."),

        ("Small Changes", "This is a test. It has multiple sentences. We want to detect plagiarism.",
         "This is an exam. It contains several phrases. We aim to identify copying."),

        ("Diff Docs", "This is about cats. Cats are furry animals. They make good pets.",
         "Python is a programming language. It is widely used in data science."),

        ("Partial Match", "This is a test. It has multiple sentences. We want to detect plagiarism.",
         "This is different. We want to detect plagiarism. This is unique.")
    ]

    for name, d1, d2 in tests:
        print(f"\nTest: {name}")
        result = checkPlag(d1, d2)
        print(f"Found {len(result)} cases:")

        for i, j, sim in result:
            print(f"  Sent {i + 1} in doc1 matches sent {j + 1} in doc2 with {sim:.2%} similarity")

def splitText(txt):
    sents = re.split(r'(?<=[.!?])\s+', txt)
    return [s.lower().strip() for s in sents]

def levDist(s1, s2):
    if len(s1) < len(s2):
        return levDist(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prevRow = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        currRow = [i + 1]
        for j, c2 in enumerate(s2):
            insert = prevRow[j + 1] + 1
            delete = currRow[j] + 1
            sub = prevRow[j] + (c1 != c2)
            currRow.append(min(insert, delete, sub))
        prevRow = currRow
    return prevRow[-1]

class Node:
    def __init__(self, p1, p2, cost, route):
        self.p1 = p1
        self.p2 = p2
        self.cost = cost
        self.route = route

    def __lt__(self, other):
        return self.cost < other.cost

if __name__ == "__main__":
    runTests()
