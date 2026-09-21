# Model specification and predictor provenance

Implementation choices below were coded before candidate scores were produced.
The original selection protocol remains in `ROUND2_PROTOCOL.md`.

## Clock-conditioned diffusion surrogate

Use linear hat functions B_j(log r) with knots .05, .10, .25, .50, .75, .97. The probit score is

`z = a(r) * margin / (13.7 sqrt(r)) + b(r) * spread_line * r / (13.7 sqrt(r)) + state_terms`,

where a(r)=sum(a_j B_j), b(r)=sum(b_j B_j); all a_j,b_j are nonnegative. The original nine
possession/field/down/distance/timeout terms remain. This gives 21 coefficients. The prior is
12 ones followed by nine zeros; the mean squared deviation penalty is .0001 or .001.
The model preserves team-swap symmetry and monotonicity in score and pregame strength.
It is a discriminative terminal-outcome forecast. Its clock curve is not automatically the variance
integral of a dynamically coherent diffusion process; do not advertise it as one.

## Stern residual learner

Start with the fitted V1 log odds. At each stage use gradient y-p and curvature max(p(1-p),.001).
Fit a least-squares tree to (y-p)/curvature with weights game_weight*curvature. Minimum leaf size
800 applies to augmented rows, not independent games. Clip terminal corrections to [-2,2], and
multiply by learning rate .05. Evaluate the fixed depth/checkpoint grid in the protocol.

Each game state is mirrored with half weight: reverse margin, strength and possession; exchange
timeouts; keep offense-relative field position, down, distance, clock and total. Final inference is
`0.5 * (p(raw_state) + 1 - p(mirrored_state))`. This enforces complementary team forecasts even
when an individual tree is asymmetric. It does not guarantee monotonicity in score.

Trees are serialized as JSON node arrays. Both training and inference split float32 feature values
so serialized predictions match the tree library's numeric convention. No pickle is needed.

## Inputs

| Feature source | Usage | Timing qualification |
|---|---|---|
| Pre-play home/away score | Current margin | nflverse pre-play fields, not final score |
| Remaining regulation seconds | r and score/strength coordinates | Archived game state; receipt time absent |
| Possession, yardline_100, down, ydstogo | Offense-relative state and signed interactions | Archived pre-play state; revisions possible |
| Home/away timeouts | Timeout difference and raw tree features | Archived state; receipt time absent |
| Remaining half seconds | Raw tree feature | Archived pre-play half-clock |
| spread_line | Pregame strength | Untimestamped historical line; availability not verified |
| total_line | Raw tree feature | Untimestamped historical total; availability not verified |
| Final scores | Outcome label and exclusion of ties only | Never included in predictor design |

The exact 21 residual features are ordered in `stern_round2.TREE_FEATURES`. Missing extra fields
are dropped after the original cadence selection, not replaced by a later play. Coverage changes
are recorded. All compared models use the same admitted rows. No EPA, wp, next-play state, final
margin or future quote enters the feature matrix.

## Interpretation

The target is home victory in a retrospectively selected non-tied-game cohort. It is not yet an
unconditional Kalshi expected payout. Restrict use to research; ties, overtime, final three minutes,
live availability, market calibration and executable liquidity remain separate admission work.
The market-anchor transport in V1 remains a hypothesis, not an independently validated signal.
