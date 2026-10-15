# 2013 HW2

[Original prompt](../assignments/homework2.pdf), [standalone LaTeX](solution.tex),
and [compiled solution](solution.pdf).

All four analytical questions are answered. The printed clock-tree C buffer is
`2*tau_g`; wire delay is negligible under the original `4*tau_g` criterion.
The critical path is A to C, with delay **0.6 ns**. The intended mobility ratio
is 2 under matched threshold magnitudes; the general relation is also given.
For larger high noise margin, choose `beta_n > beta_p` under the same symmetric
threshold convention.

Run `python verify.py`. It checks all three clock paths and five illustrative
ideal noise-margin examples using the formal slope boundaries. Evidence:
[clock_tree.csv](clock_tree.csv), [noise_margin.csv](noise_margin.csv),
[verification.json](verification.json). The original prompt does not request
an electrical simulation for this homework.

Both supplied handwritten answer photographs were reviewed. Their main answers
are retained, with explicit unit, threshold and noise-margin definitions.
