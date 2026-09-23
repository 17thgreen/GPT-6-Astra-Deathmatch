# S5 KXMVECROSSCATEGORY settled-resolution join packet

Byte copies of the attached freeze, scout reget, seed summary, panel
stub, settled reget, accept, frozen experiment, empty results, examiner
hold, maximize pin, and digest list live in this directory.
`SOURCE_PINS.json` lists digests and does not contain those file bytes
once the harness source lands. `admitted_at` stays null. `results`,
`pnl`, and `settled_join_n` stay null. Scout nonempty N=20 is a pin and
is not copied into `settled_join_n`. This packet does not run `admit.py`.
