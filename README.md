# qinst-ozawa-khrennikov


This library reproduces the calculations in Section 11 of Ozawa and Khrennikov
(2021), “Modeling combination of question order effect, response replicability
effect, and QQ-equality with quantum instruments.”

The current implementation uses the Clinton–Gore data to:

1. calculate the QQ residual of the observed sequential joint probabilities;
2. renormalize the probabilities so that they satisfy the QQ equality;
3. estimate the personality and belief distributions of the independent-personality
   model; and
4. reconstruct the sequential joint probabilities from the estimated distributions.

```python
from qinst_ozawa import (
    CLINTON_GORE,
    SequentialProbabilities,
    fit_independent_model,
    qqe_renormalize,
    reconstruct_jointprobdists,
)

observed = SequentialProbabilities.from_mapping(CLINTON_GORE)
renormalized = qqe_renormalize(observed)
parameters = fit_independent_model(renormalized.normalized)
reconstructed = reconstruct_jointprobdists(parameters)
```

### Model hypothesis

Following Eq. (118) of the paper, the implementation assumes that the belief
state `(alpha, beta)` and the personality state `gamma` are independent:

```text
mu(alpha, beta, gamma) = p(alpha, beta) q(gamma)
```

Here, `p` is a distribution over four belief states and `q` is a distribution
over three personality states.

### Applicable data

- Questions A and B both have binary yes/no responses.
- Four sequential joint probabilities are available for each question order,
  A→B and B→A.
- The four probabilities for each order are finite values in `[0, 1]` and sum
  to `1`.
- Probabilities passed to `fit_independent_model()` satisfy the QQ equality.
  Apply `qqe_renormalize()` first when the observed data do not satisfy it.
- Estimation using Eqs. (137)–(138) requires both `p(Ay) != p(By)` and
  `p(Ay) != p(Bn)`.
- Estimation of the belief distribution using Eqs. (141)–(144) requires
  `q(0) != 0`.
- All inferred values in `p` and `q` must be nonnegative, and each distribution
  must sum to `1`.

If these conditions are not met, the data may not be representable by the
independent-personality model, or the parameters may not be uniquely identifiable
from these equations.

Ozawa and Khrennikov (2021), “Modeling combination of question order effect,
response replicability effect, and QQ-equality with quantum instruments” の
Section 11にある計算をPythonで再現するためのライブラリです。

現在の実装は、Clinton–Goreデータを用いて次の計算を行います。

1. 観測された逐次同時確率のQQ残差を計算する。
2. QQ equalityを満たすように確率を再正規化する。
3. 独立人格モデルの人格分布と信念分布を推定する。
4. 推定した分布から逐次同時確率を再構成する。

```python
from qinst_ozawa import (
    CLINTON_GORE,
    SequentialProbabilities,
    fit_independent_model,
    qqe_renormalize,
    reconstruct_jointprobdists,
)

observed = SequentialProbabilities.from_mapping(CLINTON_GORE)
renormalized = qqe_renormalize(observed)
parameters = fit_independent_model(renormalized.normalized)
reconstructed = reconstruct_jointprobdists(parameters)
```

### モデルの仮説

この実装では、論文のEq. (118)に従い、信念状態
`(alpha, beta)` と人格状態 `gamma` が独立であると仮定します。

```text
mu(alpha, beta, gamma) = p(alpha, beta) q(gamma)
```

ここで、`p`は4 (2x2)状態の信念分布、`q`は3状態の人格分布です。

### 適用できるデータ

- 質問Aと質問Bがともに二値回答（yes/no）である。
- A→B順とB→A順について、それぞれ4つの逐次同時確率が与えられる。
- 各質問順の4確率は有限な`0`以上`1`以下の値で、合計が`1`である。
- `fit_independent_model()`へ渡す確率はQQ equalityを満たす。観測データが
  満たさない場合は、先に`qqe_renormalize()`を適用する。
- Eqs. (137)–(138)による推定には、`p(Ay) != p(By)`かつ
  `p(Ay) != p(Bn)`が必要である。
- Eqs. (141)–(144)による信念分布の推定には、`q(0) != 0`が必要である。
- 推定された`p`と`q`は、すべて非負で、それぞれ合計が`1`になる必要がある。

これらの条件を満たさないデータは、独立人格モデルでは表現できないか、
この推定式だけからはパラメータを一意に決定できません。
