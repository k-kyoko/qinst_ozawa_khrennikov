import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class SequentialProbabilities:
    """Sequential joint probabilities for two binary questions in both orders."""

    ay_by: float
    ay_bn: float
    an_by: float
    an_bn: float
    by_ay: float
    by_an: float
    bn_ay: float
    bn_an: float

    @classmethod
    def from_mapping(cls, values: Mapping[str, float]) -> Self:
        """Create probabilities from the paper's AyBy-style field names."""

        return cls(
            ay_by=values["AyBy"],
            ay_bn=values["AyBn"],
            an_by=values["AnBy"],
            an_bn=values["AnBn"],
            by_ay=values["ByAy"],
            by_an=values["ByAn"],
            bn_ay=values["BnAy"],
            bn_an=values["BnAn"],
        )

    def __post_init__(self) -> None:
        ordered_values = {
            "A-to-B": (
                self.ay_by,
                self.ay_bn,
                self.an_by,
                self.an_bn,
            ),
            "B-to-A": (
                self.by_ay,
                self.by_an,
                self.bn_ay,
                self.bn_an,
            ),
        }

        for order, values in ordered_values.items():
            for value in values:
                if not math.isfinite(value):
                    raise ValueError(f"{order} probabilities must be finite; received {value!r}.")
                if not 0.0 <= value <= 1.0:
                    raise ValueError(
                        f"{order} probabilities must be between 0 and 1; received {value!r}."
                    )

            total = sum(values)
            if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
                raise ValueError(
                    f"{order} probabilities must sum to 1; received a sum of {total!r}."
                )


def qq_residual(probs: SequentialProbabilities) -> float:
    """Calculate the QQ-equality residual in Eq. (157)."""

    return (probs.by_ay + probs.bn_an) - (probs.ay_by + probs.an_bn)


@dataclass(frozen=True)
class QQRenormalizationResult:
    """Store the input and output of the QQE renormalization."""

    original: SequentialProbabilities
    normalized: SequentialProbabilities
    qq_residual: float
    s1: float
    s2: float


def qqe_renormalize(p: SequentialProbabilities) -> QQRenormalizationResult:
    """Renormalize sequential probabilities using Eqs. (105)–(116)."""

    qq = qq_residual(p)

    ab_same = p.ay_by + p.an_bn
    ba_same = p.by_ay + p.bn_an
    ab_different = p.ay_bn + p.an_by
    ba_different = p.by_an + p.bn_ay
    denominators = {
        "p(AyBy) + p(AnBn)": ab_same,
        "p(ByAy) + p(BnAn)": ba_same,
        "p(AyBn) + p(AnBy)": ab_different,
        "p(ByAn) + p(BnAy)": ba_different,
    }

    for expression, denominator in denominators.items():
        if math.isclose(denominator, 0.0, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(
                "Cannot apply QQE renormalization because the denominator "
                f"{expression} is zero or too close to zero ({denominator!r})."
            )

    s1 = (ab_same + ba_same) / 2
    s2 = (ab_different + ba_different) / 2

    p_bar = SequentialProbabilities(
        ay_by=s1 * p.ay_by / ab_same,
        ay_bn=s2 * p.ay_bn / ab_different,
        an_by=s2 * p.an_by / ab_different,
        an_bn=s1 * p.an_bn / ab_same,
        by_ay=s1 * p.by_ay / ba_same,
        by_an=s2 * p.by_an / ba_different,
        bn_ay=s2 * p.bn_ay / ba_different,
        bn_an=s1 * p.bn_an / ba_same,
    )

    return QQRenormalizationResult(
        original=p,
        normalized=p_bar,
        qq_residual=qq,
        s1=s1,
        s2=s2,
    )
