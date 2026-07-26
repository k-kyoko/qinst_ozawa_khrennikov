import pytest

from qinst_ozawa import (
    CLINTON_GORE,
    SequentialProbabilities,
    fit_independent_model,
    qqe_renormalize,
    reconstruct_jointprobdists,
)


def test_section11_workflow_through_public_api() -> None:
    observed = SequentialProbabilities.from_mapping(CLINTON_GORE)
    p_bar = qqe_renormalize(observed).normalized
    parameters = fit_independent_model(p_bar)
    reconstructed = reconstruct_jointprobdists(parameters)

    assert reconstructed.ay_by == pytest.approx(p_bar.ay_by)
    assert reconstructed.bn_an == pytest.approx(p_bar.bn_an)
