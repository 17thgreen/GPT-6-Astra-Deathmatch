# AMS-013: missing-depth reward capacity and $5,000 comparison

User requests the same $5,000 sensitivity as AMS-012 for the original strategy:
complete deficient depth with one-cent orders, including a 10% target buffer.
This descriptive reanalysis reuses known data, not an independent experiment.

Before aggregation, declare the existing AMS-010 example: $11 quote principal,
$1.10 chosen fee reserve, $16.36 conditional remaining reward, about 57 minutes
left and 50% future qualifying time. Do not replace it with a better case found
by aggregation. This preserves the older capped-score stress as a conservative
comparison; published scoring includes the full boundary level (see source note).

Apply the frozen reward_scanner/policy.py evaluate function to every admitted
observation supplied by the AMS-011 readers for retained AMS-005, 007, 009 and 010.
Use model.admitted for the existing short-duration/high-rate screen; do not
retroactively apply AMS-010's future START date or five-minute discovery gate to
older data. This is a harmonized economic replay, not a rerun of prospective
admission. Original scanner results remain intact.

Count positive buffered plans by distinct program, hourly event, source/cycle and
exact book receipt timestamp. Aggregate only separate market/program pools in the
same response. Never sum repeated snapshots or separate hourly campaigns as
simultaneous capacity. Count order sets as well as side orders if any plan needs
both sides. Preserve all failures and the older midnight campaign's late capture.

Use floor(5000/12.10)=413 illustrative order sets for the strict $5,000 total
budget, retaining unallocated cash. Compute reward, net after full principal loss
and fee reserve consumption, and return on the whole $5,000 account. Fixed failed
fractions: 0%,10%,20%,25%,30%,50%,100%. Failed quotes earn zero; the others earn
$16.36; all consume principal and reserve. These are sensitivity weights, not
observed order outcomes, probabilities or a guaranteed lower bound. Also show
5000/11 quote-only capacity rounded down, with the reserve funded separately.

Do not extrapolate 24 hourly campaigns/day, infer an observed fill rate, assume
capital immediately recycles, or duplicate reward pools across bots. Explain
capacity relative to the smaller strategy. No fresh captures, orders or real risk
limits. Freeze source and focused tests before aggregation; publish results,
input hashes and existing archive restoration pointers in this new directory.
