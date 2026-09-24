# Why the reward budget alone cannot establish profitability

The scanner's positive budget cushion is an admission screen. It assumes the
quote remains eligible for enough time. An immediate full losing fill can remove
the quote before it earns much. Empty-side public trade history cannot identify
the response to a bid that was never placed.

To make that dependency concrete, survival.py defines an explicitly hypothetical
single-order model. Let r be the constant effective reward per hour after assumed
competition and qualifying-time discount; C the full losing purchase plus a fee
stress; H the remaining reward horizon; and m the assumed mean time to a full
losing fill, exponentially distributed. No replenishment is allowed. An unfilled
order is assumed cancelled without cost at H. All inventory bought in the full
fill is assumed worthless. Then:

    expected net = (r*m - C) * (1 - exp(-H/m))

The sign changes at m=C/r. This follows directly from expected time resting and
the probability of one full fill; it is not a fitted trading result. A positive
remaining-budget screen does not measure m. Shorter cancellation delays or a
different fill distribution cannot be inferred from this model either.

The example uses the prior AMS-009 $100, roughly 57.7-minute campaign, a 1100 at
one-cent quote, a $1.10 fee stress, one-third reward share after competition,
and 50% qualifying time. Evaluate assumed means of 5, 15, 30, 45, 60 and 120
minutes plus the no-fill limit. These values are scenarios, not estimates. The
late-window and opening-window observations must not be used to fit this model.

Partial fills, changing fill hazard near resolution, correlated strikes, price
changes, payout floors, account eligibility and actual cash credits are omitted.
The purpose is to quantify what favorable inventory behavior would be required,
not to convert an unverified reward quote into a profit forecast.
