# Source checkpoint correction before outcomes

The first local source checkpoint e036dac retained both early generic module
names and their m4_-prefixed replacements. Generic names could collide with
imports from the preserved M2/M3 directories. Remove the redundant prototypes;
only m4_run.py, m4_policy.py, m4_data.py and the other m4_ modules are supported.
This correction and a replacement source/input hash freeze precede all M4
historical outcomes. The specification, policy matrix and captured data do not
change. Sixteen focused tests pass. No prior M4 profit run exists to replace.
