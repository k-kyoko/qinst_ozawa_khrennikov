import pytest

from qinst_ozawa.data import CLINTON_GORE
from qinst_ozawa.independent_model import (
    BeliefDistribution,
    IndependentModelParameters,
    PersonalityDistribution,
    fit_independent_model,
    reconstruct_jointprobdists,
)
from qinst_ozawa.probabilities import SequentialProbabilities, qqe_renormalize


def test_accepts_valid_independentmodelParameters() -> None:
    personality = PersonalityDistribution(
        q0=0.6,
        q1=0.1,
        q2=0.3,
    )
    belief = BeliefDistribution(
        p00=0.2,
        p01=0.2,
        p10=0.3,
        p11=0.3,
    )
    fit = IndependentModelParameters(personality=personality, belief=belief)

    assert fit.personality == personality
    assert fit.belief == belief


def test_rejects_nan_personalitydist() -> None:
    with pytest.raises(ValueError):
        PersonalityDistribution(
            q0=float("nan"),
            q1=0.2,
            q2=0.8,
        )


def test_rejects_lessthanzero_personalitydist() -> None:
    with pytest.raises(ValueError):
        PersonalityDistribution(
            q0=0.2,
            q1=-0.1,
            q2=0.9,
        )


def test_rejects_greaterthanone_personalitydist() -> None:
    with pytest.raises(ValueError):
        PersonalityDistribution(
            q0=0.5,
            q1=0.3,
            q2=1.2,
        )


def test_rejects_sum_personalitydist() -> None:
    with pytest.raises(ValueError):
        PersonalityDistribution(
            q0=0.6,
            q1=0.5,
            q2=0.3,
        )


def test_rejects_nan_beliefdist() -> None:
    with pytest.raises(ValueError):
        BeliefDistribution(
            p00=float("nan"),
            p01=0.2,
            p10=0.7,
            p11=0.1,
        )


def test_rejects_lessthanzero_beliefdist() -> None:
    with pytest.raises(ValueError):
        BeliefDistribution(
            p00=0.2,
            p01=-0.1,
            p10=0.1,
            p11=0.8,
        )


def test_rejects_greaterthanone_beliefdist() -> None:
    with pytest.raises(ValueError):
        BeliefDistribution(
            p00=0.1,
            p01=0.3,
            p10=1.2,
            p11=0.1,
        )


def test_rejects_sum_beliefdist() -> None:
    with pytest.raises(ValueError):
        BeliefDistribution(
            p00=0.2,
            p01=0.2,
            p10=0.3,
            p11=0.41,
        )


def test_fit_clinton_gore() -> None:
    observed = SequentialProbabilities.from_mapping(CLINTON_GORE)
    p_bar = qqe_renormalize(observed).normalized
    fit = fit_independent_model(p_bar)

    assert fit.personality.q0 == pytest.approx(0.6045, abs=1e-4)
    assert fit.personality.q1 == pytest.approx(0.0668, abs=1e-4)
    assert fit.personality.q2 == pytest.approx(0.3288, abs=1e-4)

    assert fit.belief.p00 == pytest.approx(0.2231, abs=1e-4)
    assert fit.belief.p01 == pytest.approx(0.2429, abs=1e-4)
    assert fit.belief.p10 == pytest.approx(0.0155, abs=1e-4)
    assert fit.belief.p11 == pytest.approx(0.5184, abs=1e-4)


def test_fit_rejects_data_without_qqe() -> None:
    observed = SequentialProbabilities.from_mapping(CLINTON_GORE)

    with pytest.raises(ValueError):
        fit_independent_model(observed)


@pytest.mark.parametrize(
    "field_name",
    [
        "ay_by",
        "ay_bn",
        "an_by",
        "an_bn",
        "by_ay",
        "by_an",
        "bn_ay",
        "bn_an",
    ],
)
def test_reconst_clinton_gore_pbar(field_name: str) -> None:
    observed = SequentialProbabilities.from_mapping(CLINTON_GORE)
    p_bar = qqe_renormalize(observed).normalized
    params = fit_independent_model(p_bar)
    reconstructed = reconstruct_jointprobdists(params)

    assert getattr(reconstructed, field_name) == pytest.approx(
        getattr(p_bar, field_name),
        abs=1e-12,
    )


def test_round_trip_known_parameters() -> None:
    original = IndependentModelParameters(
        personality=PersonalityDistribution(
            q0=0.6,
            q1=0.1,
            q2=0.3,
        ),
        belief=BeliefDistribution(
            p00=0.1,
            p01=0.2,
            p10=0.3,
            p11=0.4,
        ),
    )

    generated = reconstruct_jointprobdists(original)
    recovered = fit_independent_model(generated)

    assert recovered.personality.q0 == pytest.approx(0.6)
    assert recovered.personality.q1 == pytest.approx(0.1)
    assert recovered.personality.q2 == pytest.approx(0.3)

    assert recovered.belief.p00 == pytest.approx(0.1)
    assert recovered.belief.p01 == pytest.approx(0.2)
    assert recovered.belief.p10 == pytest.approx(0.3)
    assert recovered.belief.p11 == pytest.approx(0.4)
