# NH-001A: archive-availability amendment, before outcome scoring

The original October 29 16:00 UTC and November 4 16:00 UTC analyses remain frozen.
CDX shows House latest-probability captures on October 9, October 10 and November 3;
Senate has November 3 in the inspected October 1-November 3 range. Captured HTML
from October 23/24 and November 1 is a display shell, not proof of the uncaptured
JSON probabilities at that date. No probabilities or returns have been scored.

Add a separately labeled NH-001A primary decision at **2024-11-04 22:00 UTC**.
This exceeds the 24-hour lag after the November 3 20:38 UTC archived probability
files. Add a secondary sensitivity at **2024-11-05 16:00 UTC**, before ordinary
election-night results. Use the same forecast-age, model weights, cost assumptions,
selection reserve and scoring rules. Do not describe these as the original horizons
or as a new independent election. House remains the primary family, Senate the
separate replication. Do not pool both horizons into extra independent samples.

Availability is bounded conservatively by the exact archive capture time. Original
publication dates, if present in JSON, cannot move availability earlier than the
archived evidence supports. A later-captured historical time series is not admitted
as evidence that its unchanged contents were public on every earlier date.

## Acquisition implementation adjustment

The original GET-only collector is preserved as acquire.py. Its first bounded run
was interrupted after valid metadata receipts because each remote request takes
roughly 7-10 seconds and two workers would take unnecessarily long. No scoring had
occurred. acquire_v2.py resumes the exact metadata panel and verified cache, uses
eight workers, retains all failures, and adds the two stated quote windows.
This changes acquisition throughput, not the family definition or outcome filter.

## Contract interpretation

538 forecasts the election winner. The selected Kalshi contracts generally pay
on the party of the member sworn in for the 2025 term. Party/seat joins must match,
but these are related rather than literally identical propositions. Death,
replacement or party change creates residual settlement-definition risk. Record
actual Kalshi resolutions and carry that limitation into the verdict; never call
this a rule-identical arbitrage or claim a model explicitly covers those risks.
