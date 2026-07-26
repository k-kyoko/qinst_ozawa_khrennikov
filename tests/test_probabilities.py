import pytest

from qinst_ozawa.data import CLINTON_GORE
from qinst_ozawa.probabilities import (
    SequentialProbabilities,
    qq_residual,
    qqe_renormalize,
)


def test_clinton_gore_qq_residual() -> None:
    prob = SequentialProbabilities.from_mapping(CLINTON_GORE)
    assert qq_residual(prob) == pytest.approx(-0.0032)


def test_rejects_nan() -> None:
    invalid = CLINTON_GORE | {"AyBy": float("nan")}
    with pytest.raises(ValueError):
        SequentialProbabilities.from_mapping(invalid)


def test_rejects_lessthanzero() -> None:
    invalid = CLINTON_GORE | {"AyBy": -1.0}
    with pytest.raises(ValueError):
        SequentialProbabilities.from_mapping(invalid)


def test_rejects_greaterthanone() -> None:
    invalid = CLINTON_GORE | {"AyBy": 1.2}
    with pytest.raises(ValueError):
        SequentialProbabilities.from_mapping(invalid)


def test_rejects_sum() -> None:
    invalid = CLINTON_GORE | {"AyBy": 0.2, "AnBn": 0.9}
    with pytest.raises(ValueError):
        SequentialProbabilities.from_mapping(invalid)


def test_qq_residual_alternate_expression() -> None:
    probs = SequentialProbabilities.from_mapping(CLINTON_GORE)
    alternate = probs.ay_bn + probs.an_by - probs.by_an - probs.bn_ay
    assert alternate == pytest.approx(qq_residual(probs))


def test_rejects_zero_denominator() -> None:
    probabilities = SequentialProbabilities(
        ay_by=0.0,
        ay_bn=0.5,
        an_by=0.5,
        an_bn=0.0,
        by_ay=0.5,
        by_an=0.0,
        bn_ay=0.0,
        bn_an=0.5,
    )
    with pytest.raises(ValueError):
        qqe_renormalize(probabilities)


def test_clinton_gore_S1() -> None:
    prob = SequentialProbabilities.from_mapping(CLINTON_GORE)
    result = qqe_renormalize(prob)
    assert result.s1 == pytest.approx(0.7770, abs=1e-4)


def test_clinton_gore_S2() -> None:
    prob = SequentialProbabilities.from_mapping(CLINTON_GORE)
    result = qqe_renormalize(prob)
    assert result.s2 == pytest.approx(0.2230, abs=1e-4)


def test_qq_residual_after_normalize() -> None:
    prob = SequentialProbabilities.from_mapping(CLINTON_GORE)
    result = qqe_renormalize(prob)
    qq = qq_residual(result.normalized)
    assert qq == pytest.approx(0.0, abs=1e-9)


def test_renormalization_stores_original_residual() -> None:
    probabilities = SequentialProbabilities.from_mapping(CLINTON_GORE)
    result = qqe_renormalize(probabilities)
    assert result.qq_residual == pytest.approx(-0.0032)


@pytest.mark.parametrize(
    ("field_name", "expected"),
    [
        ("ay_by", 0.4889),
        ("ay_bn", 0.0450),
        ("an_by", 0.1780),
        ("an_bn", 0.2881),
        ("by_ay", 0.5637),
        ("by_an", 0.1977),
        ("bn_ay", 0.0253),
        ("bn_an", 0.2133),
    ],
)
def test_clinton_gore_normalized_probability(
    field_name: str,
    expected: float,
) -> None:
    probs = SequentialProbabilities.from_mapping(CLINTON_GORE)
    result = qqe_renormalize(probs)
    actual = getattr(result.normalized, field_name)

    assert actual == pytest.approx(expected, abs=1e-4)
