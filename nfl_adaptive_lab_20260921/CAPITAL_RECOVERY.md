# Capital-control recovery before any completed capital-control outcome

The original $1,000 baseline control stopped on the inherited reservation guard:
cash114.55130000000185; reservation114.55132385499999. Difference approximately
$0.000023855. No complete P&L was produced. Retain the original runner, freeze
and full stack trace. This is not a loss and not a successful run.

For the capital-only comparison, add an explicit $0.02 idle cash buffer when
sizing every new order. Do not relax the assertion, alter fee accounting, clip
fills, or change shared depth. Apply the same buffer to $1,000, $4,000 AND $5,000
controls. This is a bounded workaround for tight reservation headroom, not a
claim that the old engine's rounding/reservation implementation is fully audited.
It reduces capacity slightly; report the buffer and compare its $5k result to
the untouched primary baseline. The main 16-case matrix and diagnostic policies
remain frozen and unchanged. No capital-control outcomes were available when
this recovery was frozen. This still does not simulate several wallets.
