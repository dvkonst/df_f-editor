from collections import Counter
from pprint import pprint


ANCHOR = 12
MIN_LENGTH = 4
THRESHOLD = 0.005


def _main():
    with open(r'D:\Downloads\kinetics_C.fa') as f:
        lines = [l.strip() for l in (l for l in f if not l.startswith('>'))]

    threshold_n = len(lines) * THRESHOLD

    assert len(set(l[ANCHOR] for l in lines)) == 1
    assert len(set(len(l) for l in lines)) == 1

    length = len(lines[0])

    result = set()
    for start in range(ANCHOR + 1):
        for end in range(length, max(start + MIN_LENGTH, ANCHOR + 1) - 1, -1):
            print('Checking motifs from', start, 'to', end, end - start)
            c = Counter(l[start:end] for l in lines)
            for motif, number in c.most_common():
                if number >= threshold_n:
                    print('Adding', motif)
                    result.add(('{:.3f}'.format(number / len(lines)), ' ' * start + motif + ' ' * (length - end)))
    pprint(result)


if __name__ == '__main__':
    _main()
