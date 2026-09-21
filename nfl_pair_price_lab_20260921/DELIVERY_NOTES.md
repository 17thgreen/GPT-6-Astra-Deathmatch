# Q7 artifact delivery

Code, frozen specifications, tests, JSON summaries and reports are committed on
`research/q7-paired-price` in `17thgreen/GPT-6-Astra-Deathmatch`.

The separate Q7 data archive preserves normalized event data and compressed
fill/order/decision/pair ledgers omitted from routine Git commits. It is a data
archive, not a duplicate repository. Its checksum inventory is committed as
EXTERNAL_ARTIFACTS.json. Extract it at the repository root after checking the
archive's recorded SHA-256, then run the documented verification commands.

This delivery route supersedes the frozen README's prospective statement that
a standalone kit would duplicate the inherited code modules. Those modules are
instead supplied by the same Git checkout and checked by BASELINE_HASHES.json.
No experimental source, policy, input, threshold or analysis changed for this
packaging decision. The frozen README is preserved to retain its original hash.

Q6 references in Q7 contain the original summaries and uncompressed ledger
hashes. They support exact baseline verification without requiring the prior
Q6 compressed result files. The raw Q2 captures remain in the original kits;
normalized replay data do not claim to replace raw acquisition provenance.
