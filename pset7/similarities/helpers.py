from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    lines_a = a.splitlines()
    lines_b = b.splitlines()

    return list(make_common_set(lines_a, lines_b))


def sentences(a, b):
    """Return sentences in both a and b"""

    lines_a = sent_tokenize(a)
    lines_b = sent_tokenize(b)

    return list(make_common_set(lines_a, lines_b))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    lines_a = substrings_from_one(a, n)
    lines_b = substrings_from_one(b, n)

    # Return list of common strings
    return list(make_common_set(lines_a, lines_b))


def make_common_set(strs_a, strs_b):
    """Return set of common strings in 2 lists"""

    return {str_a for str_a in strs_a if str_a in strs_b}


def substrings_from_one(s, n):
    """Return substrings of length n from given s (string)"""

    substrs = []
    for i in range(len(s)):
        substr = s[i: (i+n)]
        if len(substr) == n:
            substrs.append(substr)

    return substrs