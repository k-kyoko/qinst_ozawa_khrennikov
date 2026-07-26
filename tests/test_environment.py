import sys

import numpy as np

import qinst_ozawa
from qinst_ozawa import CLINTON_GORE


def test_python_environment() -> None:
    assert sys.version_info[:2] == (3, 12)
    assert np.__version__
    assert qinst_ozawa.__version__ == "0.1.0"


def test_clinton_gore_data() -> None:
    assert set(CLINTON_GORE) == {
        "AyBy",
        "AyBn",
        "AnBy",
        "AnBn",
        "ByAy",
        "ByAn",
        "BnAy",
        "BnAn",
    }
    assert np.isclose(
        sum(CLINTON_GORE[key] for key in ("AyBy", "AyBn", "AnBy", "AnBn")),
        1.0,
    )
    assert np.isclose(
        sum(CLINTON_GORE[key] for key in ("ByAy", "ByAn", "BnAy", "BnAn")),
        1.0,
    )
