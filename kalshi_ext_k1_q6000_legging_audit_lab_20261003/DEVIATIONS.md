# EXT-K1 deviations

## Overround

The frozen box fixture `fixtures/CONSENSUS_FIXTURE.json`
(sha256 `9996b19888bf49cffdd9a35d1cc05d45f7bb28c77af06d9f85d977babfac3c38`)
defines overround as `q_away + q_home - 1`.

This lab records overround as `q_away + q_home` (`consensus.py`;
`overround_definition` in `results/CONSENSUS_FIXTURE.json`).

T11 compares the lab value minus 1.0 with the frozen fixture within 1e-6.
No committed metric reads overround, so this definitional difference does not
change any result number.
