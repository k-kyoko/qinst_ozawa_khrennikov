"""Published data used by the project."""

# Paper Eqs. 149--156.
CLINTON_GORE: dict[str, float] = {
    "AyBy": 0.4899,
    "AyBn": 0.0447,
    "AnBy": 0.1767,
    "AnBn": 0.2887,
    "ByAy": 0.5625,
    "ByAn": 0.1991,
    "BnAy": 0.0255,
    "BnAn": 0.2129,
}

# Data from paper
# Z. Wang, T. Solloway, R.M. Shiffrin, & J.R. Busemeyer, Context effects produced by question orders reveal quantum nature of human judgments, Proc. Natl. Acad. Sci. U.S.A. 111 (26) 9431-9436, https://doi.org/10.1073/pnas.1407756111 (2014).
    
BLACK_WHITE: dict[str, float] = {
    "AyBy": 0.3987,
    "AyBn": 0.0174,
    "AnBy": 0.1612,
    "AnBn": 0.4227,
    "ByAy": 0.4012,
    "ByAn": 0.0597,
    "BnAy": 0.1379,
    "BnAn": 0.4012,
}

# high QQE violation
ROSE_JACKSON: dict[str, float] = {
    "AyBy": 0.3379,
    "AyBn": 0.3241,
    "AnBy": 0.0178,
    "AnBn": 0.3202,
    "ByAy": 0.4156,
    "ByAn": 0.0671,
    "BnAy": 0.1234,
    "BnAn": 0.3939,
}