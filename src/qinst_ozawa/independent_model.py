"""Independent-personality model from Sections 10 and 11 of the paper."""

import math
from dataclasses import dataclass

from .probabilities import SequentialProbabilities, qq_residual


@dataclass(frozen=True)
class PersonalityDistribution:
    """Probability distribution over personality states gamma = 0, 1, 2."""

    q0: float
    q1: float
    q2: float

    def __post_init__(self) -> None:
        values = (self.q0, self.q1, self.q2)

        for value in values:
            if not math.isfinite(value):
                raise ValueError(f"Personality probabilities must be finite; received {value!r}.")
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Personality probabilities must be between 0 and 1; received {value!r}."
                )

        total = sum(values)
        if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(
                f"Personality probabilities must sum to 1; received a sum of {total!r}."
            )


@dataclass(frozen=True)
class BeliefDistribution:
    """Probability distribution over belief states (alpha, beta)."""

    p00: float
    p01: float
    p10: float
    p11: float

    def __post_init__(self) -> None:
        values = (self.p00, self.p01, self.p10, self.p11)

        for value in values:
            if not math.isfinite(value):
                raise ValueError(f"Belief probabilities must be finite; received {value!r}.")
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Belief probabilities must be between 0 and 1; received {value!r}."
                )

        total = sum(values)
        if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(f"Belief probabilities must sum to 1; received a sum of {total!r}.")


@dataclass(frozen=True)
class IndependentModelParameters:
    """Personality and belief distributions for the independent model."""

    personality: PersonalityDistribution
    belief: BeliefDistribution


def fit_independent_model(
    p_bar: SequentialProbabilities,
) -> IndependentModelParameters:
    """Estimate independent-model parameters using Eqs. (137)–(144)."""

    if not math.isclose(qq_residual(p_bar), 0.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError(
            "Cannot fit the independent-personality model because the QQ residual "
            "is not zero. Apply qqe_renormalize() before fitting."
        )

    # Marginal distributions
    p_ay = p_bar.ay_by + p_bar.ay_bn
    p_an = p_bar.an_by + p_bar.an_bn
    p_by = p_bar.by_ay + p_bar.by_an
    p_bn = p_bar.bn_ay + p_bar.bn_an

    denominator_q2 = p_ay - p_by  # Eq. (137)
    denominator_q1 = p_ay - p_bn  # Eq. (138)

    if math.isclose(denominator_q2, 0.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(
            "Cannot infer q(2) using Eq. (137): p(Ay) - p(By) is zero or too "
            f"close to zero ({denominator_q2!r}). The model requires p(Ay) != p(By)."
        )

    if math.isclose(denominator_q1, 0.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(
            "Cannot infer q(1) using Eq. (138): p(Ay) - p(Bn) is zero or too "
            f"close to zero ({denominator_q1!r}). The model requires p(Ay) != p(Bn)."
        )

    q2 = (p_bar.ay_by - p_bar.by_ay) / denominator_q2
    q1 = (p_bar.ay_bn - p_bar.bn_ay) / denominator_q1
    q0 = 1 - q1 - q2

    if math.isclose(q0, 0.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(
            "Cannot infer the belief distribution using Eqs. (141)–(144): "
            f"q(0) is zero or too close to zero ({q0!r}). The model requires q(0) != 0."
        )

    try:
        personality = PersonalityDistribution(q0=q0, q1=q1, q2=q2)
    except ValueError as error:
        raise ValueError(
            "The data are not representable by the independent-personality model: "
            f"the inferred personality distribution is invalid ({error})."
        ) from error

    # Belief distribution: Eqs. (141)–(144)
    p11 = (p_bar.ay_by - p_ay * q2) / q0
    p10 = (p_bar.ay_bn - p_ay * q1) / q0
    p01 = (p_bar.an_by - p_an * q1) / q0
    p00 = (p_bar.an_bn - p_an * q2) / q0

    try:
        belief = BeliefDistribution(p00=p00, p01=p01, p10=p10, p11=p11)
    except ValueError as error:
        raise ValueError(
            "The data are not representable by the independent-personality model: "
            f"the inferred belief distribution is invalid ({error})."
        ) from error

    return IndependentModelParameters(
        personality=personality,
        belief=belief,
    )


def reconstruct_jointprobdists(
    prms: IndependentModelParameters,
) -> SequentialProbabilities:
    """Reconstruct sequential joint probabilities using Eqs. (129)–(136)."""

    psn = prms.personality
    blf = prms.belief

    # Marginal distributions
    p_ay = blf.p11 + blf.p10
    p_an = blf.p01 + blf.p00
    p_by = blf.p11 + blf.p01
    p_bn = blf.p10 + blf.p00

    # Sequential joint probabilities: Eqs. (129)–(136)
    return SequentialProbabilities(
        ay_by=blf.p11 * psn.q0 + p_ay * psn.q2,
        ay_bn=blf.p10 * psn.q0 + p_ay * psn.q1,
        an_by=blf.p01 * psn.q0 + p_an * psn.q1,
        an_bn=blf.p00 * psn.q0 + p_an * psn.q2,
        by_ay=blf.p11 * psn.q0 + p_by * psn.q2,
        by_an=blf.p01 * psn.q0 + p_by * psn.q1,
        bn_ay=blf.p10 * psn.q0 + p_bn * psn.q1,
        bn_an=blf.p00 * psn.q0 + p_bn * psn.q2,
    )
