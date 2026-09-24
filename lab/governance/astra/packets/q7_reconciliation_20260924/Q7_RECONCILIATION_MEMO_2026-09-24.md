# Q7 reconciliation memo — 2026-09-24

Status: `RECONCILIATION_MEMO_READY_NOT_SCORED`. `examiner_stamp`: null.

This packet is documentation. It does not retune a knob, does not run a replay, does not choose a P&L, and does not edit any frozen lab. Q6-000 (`nfl_factorial_lab_20260921`) was read and hashed only.

Governance packets already live at `lab/governance/astra/packets/`. This memo is placed there. Refiner diagnosis packets stay at `packets/refiner/` and were not moved.

Numbers below are copied from the cited blob or recomputed from those copied fields by `reconcile_extract.py`. A figure that is not in a blob is `NOT_FOUND`.

## a. Pins

| Pin | Value |
|---|---|
| `origin/main` HEAD | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` |
| Main commit Logan's research reviewed | `a281adc944e4dacffcdb5677a140fabaed675a81` |
| Reviewed commit is an ancestor of `origin/main` | true (`git merge-base --is-ancestor`) |
| Commits after the reviewed pin | one: `34a2720218b4f4f2d6dd0cbde6334ee672a3684b`, "C1-RJ KXUFCFIGHT settled-join harness (authentic pins, NOT_SCORED) (#49)" |
| Files changed in that commit | 75 |
| Q7-relevant paths changed since `a281adc944e4dacffcdb5677a140fabaed675a81` | none. `git diff --name-only` filtered on `q7`, `Q7`, `paircheck`, `pair_price`, `refiner`, and `nfl_factorial` is empty |
| Research branch `research/q7-paired-price` | `01c726ae9244d801d359e00df67d6a71f4012669` ("Record verified Q7 results and freeze simpler guarded router") |

The post-review commit adds the C1-RJ harness. Its registry row says "No Arm B." It does not change the Q7 pair-check lab, the rehab labs, the Refiner packets, or `nfl_factorial_lab_20260921`.

Inherited engine blobs are identical on the two pins (recomputed sha256):

| File | sha256 |
|---|---|
| `nfl_factorial_lab_20260921/adaptive_policy.py` | `fdd4294fcac8490f156130c0c6dc0e4e1c1f1b20214cd923c3cc18d0dcb466db` |
| `nfl_factorial_lab_20260921/factorial_policy.py` | `4f1f870242431537599a9e22222f181f919347d1095e276c89d41fa23a4e9870` |
| `nfl_factorial_lab_20260921/queue_policies.py` | `641d0df3913f4a66fb926c84d170fe1fe61347a2fad16959b6824abb0c135fc2` |
| `nfl_factorial_lab_20260921/replay_v2.py` | `5aba1bf36385d9defeb032040dd6560d3eb1a192fc0203e984a47d9e7c3f37c3` |

Every compared file, recomputed with sha256 of the git blob:

| Path | Commit | sha256 | Bytes |
|---|---|---|---:|
| `nfl_paircheck_lab_20260922/paircheck_policy.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `ae0a19e03acebd359e711fb13b5b47ca807d72632f3a2cd1c1c282ad5916d7a9` | 9513 |
| `nfl_paircheck_lab_20260922/EXPERIMENT_SPEC.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `cdfba7817a4a13c51b3aec3dc2256e7de1cd61386d9e1b359d85b2b65a78344f` | 10419 |
| `nfl_paircheck_lab_20260922/FROZEN_EXPERIMENT.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `b0dd91699d2170e42c3a0ae9e27769a80f64f8121b116da030f253ac0d8a7f2b` | 8884 |
| `nfl_paircheck_lab_20260922/README.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `595deb359891e5eeb11cb02243340988dac57f0bd295ef1439345d1515cbac87` | 3106 |
| `nfl_paircheck_lab_20260922/run_experiment.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `55d6fafe860d68e8b84e59b37c8cd641b4ec835712632867eaebcd809ff626b6` | 7248 |
| `nfl_paircheck_lab_20260922/analyze.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `2fcc5262197ccf1e1dd3eb241649c57581e7353046945427b6e01e8f14fa16d6` | 4720 |
| `nfl_paircheck_lab_20260922/results/NOT_RUN.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `e9cb7084b71aa4cde64cdfd791ed6b3b138aadd425c925df3b35bdd60cf1c7b2` | 1141 |
| `nfl_paircheck_lab_20260922/results/analysis_status.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `8acec3c77b86abce43b6eb01a941de317f1603a5a30c7ee4bc4582800c119ebb` | 189 |
| `nfl_paircheck_lab_20260922/results/verification.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `9cde03dc3d52eb3ab9d18024155c341451de9e1e8836356cdcf3cf1d0ac006e4` | 208 |
| `nfl_q7_rehab_p1_cadence_20260923/cadence_policy.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `e9e0a7a12dc7218208c116f378c56d57ae530a3eac9986201dcf57c443bd4091` | 7405 |
| `nfl_q7_rehab_p1_cadence_20260923/EXPERIMENT_SPEC.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `4ea892d235a9ce3fd545cfba595b237e55df20b10f0e296de22b27731d39802b` | 7856 |
| `nfl_q7_rehab_p1_cadence_20260923/FROZEN_EXPERIMENT.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `3183754c6880b20ad16b51b4595549409a24508ece6e3b21d507d51142ce3174` | 9194 |
| `nfl_q7_rehab_p1_cadence_20260923/results/NOT_RUN.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `ff043ad08171e7d207507f44484bf2194eec3c476f4f94922bcc0fe9b26b1fd5` | 538 |
| `nfl_q7_rehab_p1_cadence_20260923/results/UNIT_RESULTS.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `e04aec7f4deed276400c1f36f8e2cd66e3a1c5f960b5355830da1455bbef5d7f` | 1670 |
| `nfl_q7_rehab_p2_rank_sizing_20260923/rank_sizing_policy.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `2447fc4f777855270f2037be94aeae2367f1990c595678cc9bcc9a9872deb360` | 8501 |
| `nfl_q7_rehab_p2_rank_sizing_20260923/EXPERIMENT_SPEC.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `a114caf497382689ca5227b6b0307403861313049ad2d641c7690978af2b8885` | 9607 |
| `nfl_q7_rehab_p2_rank_sizing_20260923/FROZEN_EXPERIMENT.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `e3e4814abcbb92b5142c1e4783fed53b50372783aeb58f664361966d719bd7d7` | 10919 |
| `nfl_q7_rehab_p2_rank_sizing_20260923/selection.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `247a064d41895c29b837fbf454235d9f8b7b56261e532edbc8baead2e65519d6` | 3155 |
| `nfl_q7_rehab_p2_rank_sizing_20260923/results/NOT_RUN.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `5f52851b741619ee82ae1fbd70f92d5dcbb527cc16d3212f4295377e064d49b8` | 539 |
| `nfl_q7_rehab_p2_rank_sizing_20260923/results/UNIT_RESULTS.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `b8282d077048ccaf76be9312294b717323ae206f93eb83c2eb0a4be2d66b7232` | 2253 |
| `packets/refiner/CONDUCTOR_ACCEPT_Q7_B_REHAB_P1_CADENCE_600_2026-09-23.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `6ff909e9e07c136a0b47d866ab54179e91080d514692c7bff9cb588e847dc1b9` | 663 |
| `packets/refiner/CONDUCTOR_DECISION_Q7_B_P1_PARENT_LEDGERS_2026-09-23.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `78c4cf447d13c922540601d41ea11b12e5c90011622dcf92f25af4b8e1a580cf` | 1446 |
| `packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `5ee602ba5d6537956c87eca0d5af5bf4443b80e935e85d1c7c61279f4fed432a` | 5060 |
| `packets/refiner/REFINER_HAND_SIMULATOR_Q7_B_PASS2_RANK_SIZING_2026-09-23.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `8acc6811a880df96c943b53481743f14ca9240996b59e073f2ee2aacd81d3118` | 1977 |
| `packets/refiner/REFINER_PASS1_DIAGNOSIS_Q7_ARM_B_2026-09-23.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `2f5beac53925ed9452c8cda05825c6da5b51593b183877a63770bbb0df9f584e` | 3518 |
| `packets/refiner/REFINER_PASS1_FREEZE_Q7_B_CADENCE_600_2026-09-23.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `91506143c2f75e27dd8a2593e9b484457b61e5b1a8537002bf2b4f4be435ec97` | 3470 |
| `packets/refiner/REFINER_PASS2_DIAGNOSIS_Q7_ARM_B_2026-09-23.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `a9539677db0c775534f3b15c07bf572d3d8877844867561e49b059716f1af292` | 3911 |
| `packets/refiner/REFINER_PASS2_FREEZE_Q7_B_PORTFOLIO_RANK_SIZING_2026-09-23.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `5f70d83abe5f45f01a29f5bf4bf10484f934715990aed4759630ee6f90392bfd` | 4344 |
| `nfl_factorial_lab_20260921/adaptive_policy.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `fdd4294fcac8490f156130c0c6dc0e4e1c1f1b20214cd923c3cc18d0dcb466db` | 11000 |
| `nfl_factorial_lab_20260921/factorial_policy.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `4f1f870242431537599a9e22222f181f919347d1095e276c89d41fa23a4e9870` | 3624 |
| `nfl_factorial_lab_20260921/queue_policies.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `641d0df3913f4a66fb926c84d170fe1fe61347a2fad16959b6824abb0c135fc2` | 11366 |
| `nfl_factorial_lab_20260921/replay_v2.py` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `5aba1bf36385d9defeb032040dd6560d3eb1a192fc0203e984a47d9e7c3f37c3` | 18973 |
| `nfl_factorial_lab_20260921/inputs/manifest.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` | 50950 |
| `nfl_factorial_lab_20260921/inputs/markets.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `66cc07e9e9e1543b3fdcbcded30ff50af0abae87bb2aa3d5fcb3d0be7925632f` | 9697 |
| `nfl_factorial_lab_20260921/inputs/week_membership.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `a47d0e0dc5a64d79335bc5588f8aa5e1d937503d36ebcbaaf219965a68adf88c` | 1166 |
| `kalshi_capital_structure_lab_20260922/FROZEN_EXPERIMENT.json` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `cb9816d4dec5aa992958aeadec02f4bc7efd7ae77f6eb0a94bfa40051f1a204c` | 4858 |
| `docs/EXPERIMENT_REGISTRY.md` | `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | `f8e24c19b2299587603b784f33bdc037cea828eb57acd1e5acc9581aff265787` | 81160 |
| `nfl_pair_price_lab_20260921/pair_policy.py` | `01c726ae9244d801d359e00df67d6a71f4012669` | `5b0c2b4438dbf016686fca82293f1825febce38799315ac14708b5a41a394abc` | 5618 |
| `nfl_pair_price_lab_20260921/Q7_RESULTS.md` | `01c726ae9244d801d359e00df67d6a71f4012669` | `0b75b48fdb302dd86869e1516bade13f42a1611e5ab150889d1bb6420c8c38e9` | 3504 |
| `nfl_pair_price_lab_20260921/EXPERIMENT_SPEC.md` | `01c726ae9244d801d359e00df67d6a71f4012669` | `fe978c80a00dfad52a5ea27ff734c8a26224fe708e5b52a31fb8d4701b533df0` | 5695 |
| `nfl_pair_price_lab_20260921/FROZEN_EXPERIMENT.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `0a503c3ed0b6e7734ddb236fae687bce3c2cf3cf7138dc10b821262af11ce9a8` | 1393 |
| `nfl_pair_price_lab_20260921/README.md` | `01c726ae9244d801d359e00df67d6a71f4012669` | `ef03704e996658771f0bffe7bfd39b5dbb695eeb2cc9659810505c1278ac4ead` | 1545 |
| `nfl_pair_price_lab_20260921/run_experiment.py` | `01c726ae9244d801d359e00df67d6a71f4012669` | `9829f078f68d5ac38ec0b816fb38caffb895682e8aebdc9070804325d1fc8bd0` | 4916 |
| `nfl_pair_price_lab_20260921/q7_analysis.py` | `01c726ae9244d801d359e00df67d6a71f4012669` | `7e8139179c74ddefc08d3d089327dad12e68016564907321ec0a0dd872e88342` | 9679 |
| `nfl_pair_price_lab_20260921/EXTERNAL_ARTIFACTS.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `420a1d5ca5033bd0dd99239249891058a08d146a51224e238cf3814560c5f929` | 13856 |
| `nfl_pair_price_lab_20260921/results/effects.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `90c9a2c95c59c03003fdb0653fc1a7f03dc56951f34f19fefa84e655404d57c0` | 1799 |
| `nfl_pair_price_lab_20260921/results/selection.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `c88164646a7fc35962f90d32d496af211ec402c24dd0cbcc988ccc33b0b20587` | 898 |
| `nfl_pair_price_lab_20260921/results/experiment_summary.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `c22a9ddec133820e23d29a21410cc7d88010faae336cd179cc9b851851cb653f` | 206059 |
| `nfl_pair_price_lab_20260921/results/verification.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `4d5971ed28ade1d10bf24f701362389cc35fbbf161e5671ada4177c1803382e3` | 12148 |
| `nfl_pair_price_lab_20260921/inputs/manifest.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` | 50950 |
| `nfl_pair_price_lab_20260921/inputs/markets.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `66cc07e9e9e1543b3fdcbcded30ff50af0abae87bb2aa3d5fcb3d0be7925632f` | 9697 |
| `nfl_pair_price_lab_20260921/inputs/week_membership.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `a47d0e0dc5a64d79335bc5588f8aa5e1d937503d36ebcbaaf219965a68adf88c` | 1166 |
| `nfl_factorial_lab_20260921/adaptive_policy.py` | `01c726ae9244d801d359e00df67d6a71f4012669` | `fdd4294fcac8490f156130c0c6dc0e4e1c1f1b20214cd923c3cc18d0dcb466db` | 11000 |
| `nfl_factorial_lab_20260921/factorial_policy.py` | `01c726ae9244d801d359e00df67d6a71f4012669` | `4f1f870242431537599a9e22222f181f919347d1095e276c89d41fa23a4e9870` | 3624 |
| `nfl_factorial_lab_20260921/queue_policies.py` | `01c726ae9244d801d359e00df67d6a71f4012669` | `641d0df3913f4a66fb926c84d170fe1fe61347a2fad16959b6824abb0c135fc2` | 11366 |
| `nfl_factorial_lab_20260921/replay_v2.py` | `01c726ae9244d801d359e00df67d6a71f4012669` | `5aba1bf36385d9defeb032040dd6560d3eb1a192fc0203e984a47d9e7c3f37c3` | 18973 |
| `nfl_pair_price_lab_20260921/results/q3300_d0.25_router_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `9c38520c3f74ba885b0ec62f296187c907c2f5a1b10e7028e36d61ee8a420661` | 11314 |
| `nfl_pair_price_lab_20260921/results/q3300_d0.25_router_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `8e4785ab3390eca4e3f6e217acaacb2839b5a3079a6f91decfdcd233140c7fb2` | 11303 |
| `nfl_pair_price_lab_20260921/results/q3300_d0.25_allocator_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `c84e5ba6256ec19927f617e8cea73be725d10c6f9de543b9f8fbaeac46e8d0f8` | 11434 |
| `nfl_pair_price_lab_20260921/results/q3300_d0.25_allocator_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `04a7c22b5e09a45b17630346ecbb69efa1c91aeceb1df638d44af2bfb313a81f` | 11419 |
| `nfl_pair_price_lab_20260921/results/q3300_d5_router_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `9b08f766c746c912fe4722d37d1441d73a0c7a8f4e2c5b75aaf449a09634687b` | 11331 |
| `nfl_pair_price_lab_20260921/results/q3300_d5_router_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `695faf97e395aa344818bf30ddb4e4f98c7fa6d742b2cc7b39dc3ade8d2c9a75` | 11314 |
| `nfl_pair_price_lab_20260921/results/q3300_d5_allocator_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `06bf0df0d0b2f53de73f96b114cdee3beb7cc9f1657a8f300aa1711da5fb9802` | 11459 |
| `nfl_pair_price_lab_20260921/results/q3300_d5_allocator_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `f23cfb865ff22e6ba091d44aa75951398511ff9c1e3ec719627545cc45b4538b` | 11439 |
| `nfl_pair_price_lab_20260921/results/q10000_d0.25_router_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `c5d9aa44ed894090565ac86de607ebb93b62f785e47ad6552ec0aa23d6aac7f8` | 11324 |
| `nfl_pair_price_lab_20260921/results/q10000_d0.25_router_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `904806f25d84dbf1368b70e12ec89f58284395bd2fe37e26444ea17b98f68694` | 11211 |
| `nfl_pair_price_lab_20260921/results/q10000_d0.25_allocator_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `a213b86a9d72b07c41e4d19dc43d92ebff1a5a5ed83b0dcbb3a850a893132902` | 11415 |
| `nfl_pair_price_lab_20260921/results/q10000_d0.25_allocator_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `495a1dc9b61c83092b1f724ce028bb312b764ba04b119dcdae924c8320fb7e06` | 11283 |
| `nfl_pair_price_lab_20260921/results/q10000_d5_router_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `60cb503583ce2967bf4c965c905682d3a9ffb62e9bc1d35196aee7d49599d4b8` | 11309 |
| `nfl_pair_price_lab_20260921/results/q10000_d5_router_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `080e8f8e5fd3182a5f459e7d649c9410a653dca5033c029dca93239674c2bd66` | 11179 |
| `nfl_pair_price_lab_20260921/results/q10000_d5_allocator_off.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `d7c6626fdbd02f3faa42a9a9af0e5f0674a5f8259259a893aa07d5cfbc119fdc` | 11419 |
| `nfl_pair_price_lab_20260921/results/q10000_d5_allocator_on.json` | `01c726ae9244d801d359e00df67d6a71f4012669` | `47ffb39863dc0651371c25f539510b159b6e9f4df7703c8b02263b31162aaf1f` | 11313 |

## b. Policy diff, line level

Both sides import the same Q6 modules and add a chosen-pair margin:

`margin = 1 - sum(chosen leg costs) - 0.0002 - 2 * balance_precision / order_size`

with `cost = price + maker_coefficient * price * (1 - price)` from `queue_policies.py` `candidate` lines 145–148. The cushion quantity is configured `order_size` (250), not a joint fill. Route choice itself stays `queue_policies.py` `choose` lines 150–170: per direction, keep routes with `pair_margin > 0` against the cheapest counterleg, then incumbent `switch_ratio`. That per-leg screen is not the combined-cost check.

Shared order creation, after a policy has decided to call `quote`: `replay_v2.py` `quote` lines 161–183. An existing order at a different price is cancelled with `cancel_delay_seconds` (lines 165–166) and is not replaced in that call. A same-price working order is kept, and a smaller `wanted` only schedules a delayed resize (lines 167–172). A new `Order` is constructed only when no working order exists (lines 180–182). Fills are `match` lines 217–228: the public print consumes queue ahead, then size is `floor(min(remaining, volume * fill_participation))`. Inventory pairing cash is `account_fill` lines 203–215. Completed P&L is `finish` lines 325–334: `completed_strategy_pnl` is cash minus starting cash only when every game window is complete and `unresolved_contracts < 0.009`; otherwise it is null. Null is not zero.

### Main (`34a2720218b4f4f2d6dd0cbde6334ee672a3684b`)

Frozen study: `nfl_paircheck_lab_20260922/paircheck_policy.py` (sha256 `ae0a19e03acebd359e711fb13b5b47ca807d72632f3a2cd1c1c282ad5916d7a9`).

| Decision | Function | Lines |
|---|---|---|
| (ii) which routes are selected | inherited `QueueReplay.choose`, called from `plan_admission` and from `AdaptiveReplay.refresh` → `QueueReplay.refresh` | `paircheck_policy.py` 80; `queue_policies.py` 150–170 and 185 |
| (i) whether a new quote is created | `OriginalPairCheck.plan_admission` and `refresh` | `paircheck_policy.py` 76–113 |
| (iii) size per order | not changed by the pair check. Baseline refresh passes `candidate['wanted']`. `quote` then applies cash and exposure caps | `queue_policies.py` 123 and 197; `replay_v2.py` 174–179 |
| (iv) working orders, inventory, completion | `split_offset`; gated `quote`; inherited cancel/resize/fill | `paircheck_policy.py` 48–51 and 102–107; `replay_v2.py` 151–183 and 203–228 |

Arm B (`pair_check` true) builds the blocked set in `plan_admission` lines 80–89. The check runs only when `choose` returned two legs. If `margin > 0`, the blocked set is empty and `refresh` calls the inherited refresh (lines 86–87 and 98–99). If `margin <= 0`, keys with `direction * inventory < 0` stay offset and are not blocked; the other chosen keys are blocked (lines 88–89). `refresh` then wraps `quote` (lines 102–107): if the key is blocked and `self.orders.get(key) is None`, the function returns without submitting. If a working order exists, the wrapper calls inherited `quote`, so a same-price order stays up and a price change still waits out `cancel_delay_seconds`. The blocked key remains inside the set `choose` returned, so `QueueReplay.refresh` lines 186–188 do not cancel it for `route/eligibility`.

If `choose` did not return two legs, `plan_admission` lines 82–83 return an empty blocked set. A one-leg selection is not treated as a failed pair.

Arm A skips the check (`refresh` lines 92–93). Arms C and D are `AllocatorPairCheck`. Arm D calls frozen `FactorialReplay.portfolio_rank` (`factorial_policy.py` lines 20–40), which returns `None` when `margin <= 0` (line 27). Arm C uses `_rank_without_combined_cost_filter` (lines 156–180), the same rank math without that return. Allocator admission and size stay on the inherited allocation path: `rebalance` sets `next_allocation = now + 600` (`factorial_policy.py` lines 42–44) and `AdaptiveReplay.refresh` sizes by `allocations[event] / total`, with an offset floor (`adaptive_policy.py` lines 159–168). The pair check does not add a faster cancel loop.

Later rehab labs, also on this pin, are frozen and not run. They do not replace the parent Arm B code.

- Pass 1, `nfl_q7_rehab_p1_cadence_20260923/cadence_policy.py`. B0 is `OriginalPairCheck(..., True)` (lines 110–114). B1 `RehabCadenceReplay.refresh` lines 83–97 adds a second gate: new-exposure keys are admitted only when `now >= next_allocation`, and that attempt sets `next_allocation = now + 600` (constant at line 23). Between ticks, `_gated_refresh` lines 72–75 uses the same "no working order means skip submit" wrapper. D is imported Arm D (lines 117–122).
- Pass 2, `nfl_q7_rehab_p2_rank_sizing_20260923/rank_sizing_policy.py`. B0 is again imported Arm B (lines 101–107). B2 `refresh` lines 81–88 sets `experiment = 'allocation'` around `OriginalPairCheck.refresh`, so the inherited capital-budget sizer runs, while the pair-check quote gate still wraps `quote`. `rebalance` lines 73–79 calls `FactorialReplay.rebalance` and then forces `next_allocation = -inf` so the 600-second clock is not an admission gate. Size is `floor_qty(wanted * min(1, allocation / total))` (lines 35–46) with the inherited offset floor. `make_replay` line 108 refuses arm B1.

### Branch (`01c726ae9244d801d359e00df67d6a71f4012669`)

`nfl_pair_price_lab_20260921/pair_policy.py` (sha256 `5b0c2b4438dbf016686fca82293f1825febce38799315ac14708b5a41a394abc`).

| Decision | Function | Lines |
|---|---|---|
| (ii) route selection before the guard | `QueueReplay.choose` via `GuardedRouter.choose` → `super().choose` | `pair_policy.py` 42–43; `queue_policies.py` 150–170 |
| (ii) set actually quoted after a failed margin | `GuardedRouter.choose` replaces `chosen` | `pair_policy.py` 47–63 |
| (i) whether a new quote is created | inherited `QueueReplay.refresh` quotes only keys still in `chosen`, and cancels the rest | `queue_policies.py` 185–198 |
| (iii) size on a failed margin | `bounded_quantity(c, 0)` written into `c['wanted']` | `pair_policy.py` 54–59; `adaptive_policy.py` 37–42 |
| (iii) size when the margin passes | inherited `candidate['wanted']`, then `quote` caps | `pair_policy.py` 64–65; `queue_policies.py` 197 |
| (iv) working orders and offsets | cancel path above; offset test `direction * holdings < 0`; room is `0 - direction * holdings - other pending` | `pair_policy.py` 51–59; `adaptive_policy.py` 37–42 |

`chosen_margin` lines 8–12 returns `None` unless there are two legs with directions `{-1, 1}`. `GuardedRouter.choose` lines 47–63 treats `margin is None` and `margin <= 0` the same: only legs with `direction * holdings < 0` stay in `chosen`, and only when `bounded_quantity` returns at least 0.01. Because those keys are removed from `chosen`, `QueueReplay.refresh` lines 186–188 cancel any working order on a dropped key. The cancel still waits `cancel_delay_seconds` (`replay_v2.py` lines 151–155). A flat inventory has no offset leg, so a failed or missing pair clears `chosen`.

`router_off` is `AdaptiveReplay(..., 'baseline')` (`pair_policy.py` line 114), the same baseline refresh Arm A uses.

`allocator_on` / `allocator_off` are `PairAllocator` lines 70–110. Guard true delegates to `FactorialReplay.portfolio_rank` (the `margin <= 0` return). Guard false uses `rank_without_margin_rejection`, which keeps neutral `adjusted = 1` when ranking is off. `portfolio_rank` also calls `choose` again to fill a pair log (lines 85–88). `choose` writes `pair_margin` and `score` on candidate dicts (`queue_policies.py` lines 157–159) and does not change `wanted` or engine order state. Allocator size and the 600-second budget clock stay on the inherited allocation path. There is no quote-creation wrapper and no `bounded_quantity` resize inside the allocator guard.

### Behavioral differences

| Where | Main behavior | Branch behavior | Consequence for fills and inventory |
|---|---|---|---|
| Combined-cost predicate | `margin <= 0` on two chosen legs blocks new exposure (`paircheck_policy.py` 84–89) | `margin is None` or `margin <= 0` drops non-offset keys from `chosen` (`pair_policy.py` 47–63) | A selection that is not a two-leg opposite pair is left alone on main and is reduced to inventory offsets on the branch |
| New order on a failing pair | Gated `quote` returns immediately when the key is blocked and no working order exists (`paircheck_policy.py` 105–106) | The key is absent from `chosen`, so `refresh` never calls `quote` for it (`queue_policies.py` 189–190) | That key is not newly submitted on either side |
| Existing working order on a failing non-offset leg | The key stays in `chosen`. Inherited `quote` keeps a same-price order and delay-cancels a price change (`paircheck_policy.py` 102–107; `replay_v2.py` 165–172) | The key is not in `chosen`, so `refresh` calls `cancel` (`queue_policies.py` 186–188) | A resting non-offset order can remain on main for the rest of the cancel/keep rules and is sent down the cancel path on the branch. Later tape prints can still fill an order until cancel acknowledgment (`replay_v2.py` `match` 217–228, including fills while cancel is pending) |
| Offset size when the check fails | The check does not rewrite `wanted`. The offset leg keeps candidate size, then `quote` applies cash and exposure (`queue_policies.py` 123, 197) | `wanted` becomes `bounded_quantity(c, 0)`, capped by absolute inventory minus other same-direction pending size (`pair_policy.py` 54–59; `adaptive_policy.py` 37–42) | Offset resting size can differ. Fills are the later tape match against whatever size is live |
| Passing margin, router | Empty blocked set; full inherited refresh (`paircheck_policy.py` 86–87, 98–99) | `choose` returns the superclass set unchanged (`pair_policy.py` 64–65) | Both leave route choice and candidate `wanted` to the inherited router |
| Allocator check on | `FactorialReplay.portfolio_rank` returns `None` on `margin <= 0`; side rejection row only (`paircheck_policy.py` 135–154) | Same `portfolio_rank` return, plus a second `choose` that logs (`pair_policy.py` 78–89) | Budget withholding is the inherited 600-second allocation path on both. This memo does not treat the decision-gzip pin hashes as equal; see section e |
| Allocator check off | `_rank_without_combined_cost_filter` (`paircheck_policy.py` 156–180) | `rank_without_margin_rejection` (`pair_policy.py` 91–110) | Both remove only the `margin <= 0` rank return and keep neutral adjusted score 1 with factors `000` |
| Rehab B1 cadence | Extra 600-second gate on new exposure, same quote wrapper (`cadence_policy.py` 83–97) | No B1 arm | No branch fill stream exists for this gate. Main rehab result files are `NOT_RUN` |
| Rehab B2 sizing | Allocation-fraction size on top of the Arm B quote gate (`rank_sizing_policy.py` 81–88) | No B2 arm. Branch offset sizing is `bounded_quantity`, not the allocation fraction | Different sizing functions. No scored B2 ledger is in the tree |

Pair completion is the inherited engine on both sides. Neither guard waits for the other leg or sets `assumed_simultaneous_fills`. Spec text: main `EXPERIMENT_SPEC.md` "Do not assume simultaneous fills"; branch `EXPERIMENT_SPEC.md` "A passing margin does not assure simultaneous fills". Unresolved contracts stay out of `completed_strategy_pnl` (`replay_v2.py` 334).

## c. Fixtures and inputs

Declared tape identity is the same file hash. The tape bytes are in neither commit. The in-tree main study did not replay them.

| Item | Main `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` | Branch `01c726ae9244d801d359e00df67d6a71f4012669` |
|---|---|---|
| Cohort | 31 development games, 16 week 1 and 15 week 2. `nfl_paircheck_lab_20260922/FROZEN_EXPERIMENT.json` `fixed.development_games` 31. `results/NOT_RUN.json` status `NOT_RUN_INPUTS_MISSING` | Same counts in `inputs/manifest.json` `cohort` and `inputs/week_membership.json` (16 / 15) |
| Manifest file | `nfl_factorial_lab_20260921/inputs/manifest.json` sha256 `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` | `nfl_pair_price_lab_20260921/inputs/manifest.json`, same sha256, byte-identical |
| `markets.json` and `week_membership.json` | factorial input paths | pair-price input paths; byte-identical to the factorial blobs |
| `events.jsonl.gz` declared sha256 | `cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4` inside the manifest | same field |
| `events.jsonl.gz` blob | `NOT_FOUND` in the commit. `NOT_RUN.json` `missing_inputs` is `["events.jsonl.gz"]`, `scenarios_executed` 0 | `NOT_FOUND` in the commit. `EXTERNAL_ARTIFACTS.json` stores bytes `22967126` and the same sha256. Those gzip bytes were not re-hashed here |
| Quote source | candles, specified in the frozen JSON and in the runner | `quote_source: "candles"` stored on every scenario `config` |
| Fee model | `replay_v2.py` `Config` lines 48–50: maker coefficient `0.0175`, taker coefficient `0.07`, `balance_precision` `".0001"`. Charge is `account_fill` lines 203–206 | Same `Config` blob. Each stored scenario `config` copies `maker_coefficient` 0.0175 and `taker_coefficient` 0.07 |
| Early queue | Scenario grid is 3300 and 10000 only (`FROZEN_EXPERIMENT.json` `early_queues`) | Stored `config.queue_early` is 3300 or 10000 on all 16 summaries |
| Queue `290.595` | `Config.queue_early` default at `replay_v2.py` line 41. Not a Q7 scenario. The runner overrides `queue_early` | Same default line, same override. Not present in the 16 stored configs |
| Last-12-hour queue | default `1327847.005` (`replay_v2.py` line 42), used when kickoff minus now is under 43200 seconds (line 117) | stored `config.queue_last12h` `1327847.005` on every summary |
| Delays | submit and cancel move together: 0.25 and 5 (`FROZEN_EXPERIMENT.json` `submit_cancel_delays`) | stored `order_delay_seconds` equals `cancel_delay_seconds`, values 0.25 or 5 |
| Other stored config | order size 250, exposure cap 250, assumed exit depth 250, participation 0.5, requote 60, proxy max age 300, liquidation lead 300, starting cash 5000, `event_netting` true, `inventory_reduce_only` false | same fields on every scenario `config` |
| Fill model | inherited `match`, participation 0.5 | same function; participation stored as 0.5 |
| Seeds | `NOT_FOUND`. The substring `seed` is absent from the Q7 spec, frozen JSON, runner, and `replay_v2.py` on this pin | `NOT_FOUND` on the same search of the branch spec, frozen JSON, and runner |

Do the two sides replay the same inputs? They declare the same manifest, including the same `events.jsonl.gz` sha256, and the market and week files in git are byte-identical. The tape object itself is not in either commit, so this memo did not re-hash it. The main pair-check tree's own result file says the replay did not run. The branch summaries are present and record that cohort. Section e shows the desk B/D pins are different objects from the branch external pins. Declared inputs match. The stored outputs that were hashed are not one replay sitting in both commits.

## d. Arm label map

| Label | Side | Definition in the frozen file | Counterpart | Relation |
|---|---|---|---|---|
| A | main pair-check | Original router, `pair_check` false. Untouched reference | `router_off` | Code-path counterpart: both are `AdaptiveReplay` baseline. Output equality is not scored; main scenario JSON is `NOT_FOUND` |
| B | main pair-check | Original router, `pair_check` true. Admission of new exposure only, by gating `quote` | `router_on` is the role analog only | **Label collision if B is read as `router_on`.** Same 2×2 slot (router plus check). Different admission and sizing code, section b |
| C | main pair-check | Allocator `000`, combined-cost filter removed | `allocator_off` | Code-path counterpart plus the branch's extra pair log. Main scenario JSON is `NOT_FOUND` |
| D | main pair-check | Allocator `000`, check on. Untouched Q6 reference | `allocator_on` | Code-path counterpart plus the branch's extra `choose` log. Decision-gzip pin hashes differ (section e). P&L equality is `NOT_FOUND` |
| B0 | main rehab pass 1 and pass 2 | Alias of Q7 Arm B | none | No branch label. Mapping B0 to `router_on` repeats the B collision |
| B1 | main rehab pass 1 | Arm B plus 600-second new-exposure cadence | none | No counterpart. Pass 2 `make_replay` refuses B1 |
| B2 | main rehab pass 2 | Arm B plus portfolio-rank capital-budget sizing, cadence gate disarmed | none | No counterpart. Not the branch `bounded_quantity` resize |
| `router_off` | branch | Untouched baseline | A | See A |
| `router_on` | branch | `GuardedRouter`: filter inside `choose`, bounded offset size | B as role analog only | Not equivalent to B |
| `allocator_off` | branch | `PairAllocator(guard=False)` | C | See C |
| `allocator_on` | branch | `PairAllocator(guard=True)`, Q6 `000` | D | See D |

The branch arm set has no letters A/B/C/D. The main pair-check arm set has no `router_on` / `router_off` / `allocator_on` / `allocator_off` names. Rehab reuses the letter B as B0/B1/B2 for different knobs. B1 and B2 are not aliases of parent B.

Both selection rules use a 95 percent engineering bar, on different numerators. Main `analyze.py` lines 49–50: B is at least `0.95 * D` on every stress. Branch `q7_analysis.py` lines 21–22: `router_on` is at least `0.95 * allocator_on` on every stress. Those are stored rule texts, not a ranking of the two P&Ls.

## e. Full ledgers

### Main, in the commit

`nfl_paircheck_lab_20260922/results/` contains `NOT_RUN.json`, `analysis_status.json`, and `verification.json` only.

- `NOT_RUN.json` sha256 `e9cb7084b71aa4cde64cdfd791ed6b3b138aadd425c925df3b35bdd60cf1c7b2`: `status` `NOT_RUN_INPUTS_MISSING`, `scenarios_executed` 0, `pnl` null, `results` null. The note says this file is not a profit result.
- `verification.json`: `all_checks_passed` null, `scenarios_executed` 0, `pnl` null.
- `analysis_status.json`: `effects` null, `selection` null, `pnl` null.
- `FROZEN_EXPERIMENT.json`: `results` null, `pnl` null, `status` `IMPLEMENTED_FROZEN_NOT_RUN`.

Per-scenario completed P&L, unresolved contracts, fees, fills, and `all_flat` for arms A, B, C, and D are `NOT_FOUND` in this commit. A and C are also absent from the parent pin list.

Rehab pass 1 and pass 2 `results/NOT_RUN.json` each have `scenarios_executed` 0, `pnl` null, `results` null, `score_run_in_this_freeze` false. Their scenario grids name B0/B1/D and B0/B2/D. No scenario ledger is in the tree. `nfl_q7_rehab_p1_cadence_20260923/results/experiment_summary.json` is `NOT_FOUND`. The pass 2 diagnosis cites that summary; the bytes are not in the commit.

### Main, pin records whose bytes are absent

`packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json` (sha256 `5ee602ba5d6537956c87eca0d5af5bf4443b80e935e85d1c7c61279f4fed432a`) lists B and D artifacts for the four stresses. Every listed path is absent from `34a2720218b4f4f2d6dd0cbde6334ee672a3684b` (`present_in_main_commit` false). Stored pin sha256 values were copied; they were not recomputed.

`paircheck_effects.json` pin: sha256 `5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf`, bytes 2237. The file is `NOT_FOUND`. `kalshi_capital_structure_lab_20260922/FROZEN_EXPERIMENT.json` `q7_checkout_observation.paircheck_effects_present` is false, and `q7_packet_pins.note` says those blobs are not the files in that checkout. The same object stores `q7_packet_pins.selection` `NO_NEW_SELECTION` and `paircheck_effects_status` `COMPLETE` as citations of the absent blob.

Pinned decision-gzip sizes, copied from that pin file, show a split the memo cannot open:

| Artifact | Stored bytes | Stored sha256 |
|---|---:|---|
| `q3300_d0.25_B.json` | 56907767 | `370ccbcf342db59aa1697d448d3274791cf17c015d8e9eead17d788fbe79ffb5` |
| `q3300_d0.25_B_decisions.jsonl.gz` | 66 | `c0bad55ee32de8ffcd51f6143cdec377c0e93c4730fc4a9297a83f8f8aa9eeea` |
| `q3300_d0.25_D.json` | 2356708 | `fc38cfbc134ca313a6cd2b8763ef49c3a56f6b5cc763c50f82e2b4545cda898f` |
| `q3300_d0.25_D_decisions.jsonl.gz` | 838293 | `c26827d0dbe1d9426343deeecc0d8b3e389ccf60f9dd24b683ff1ca1839066e4` |
| `q3300_d5_B_decisions.jsonl.gz` | 63 | `90a3afd9fd508a5d4f7ed548286aed64fbd1fa2d97e86f84581953a1ef882367` |
| `q3300_d5_D_decisions.jsonl.gz` | 837745 | `af14f73e241d6b7dfebf90fa6e7a15729632c2fd6956bed1f8f6d8e391570d6e` |
| `q10000_d0.25_B_decisions.jsonl.gz` | 67 | `034ec66d980a1e7e18159a40bd12746a3754d593429454c18ca968b31b7d068b` |
| `q10000_d0.25_D_decisions.jsonl.gz` | 827009 | `27e164f61889d261b072aa5b49aed3675b4daa04dbccf93c6ff6b05568862687` |
| `q10000_d5_B_decisions.jsonl.gz` | 64 | `dbde156309f57b8a7735bfd7c1abd7d7f2d423ef51451f7e9b0fa74c06ef1260` |
| `q10000_d5_D_decisions.jsonl.gz` | 826245 | `0c3c55742242d5a2cb13e569884d2eff3ff4c33de5e2aba10e84701f01f25ee2` |

The same pin file records the other summary JSON byte sizes: `q3300_d5_B.json` 56896894, `q10000_d0.25_B.json` 56496246, `q10000_d5_B.json` 56496255, `q3300_d5_D.json` 2356849, `q10000_d0.25_D.json` 2342036, `q10000_d5_D.json` 2342066. The gzip bytes are not in the commit, so this memo does not call them truncated. It also does not decompress them. Decision counts inside the main B gzip files are `NOT_FOUND`.

### Branch summaries that are in the commit

Each `nfl_pair_price_lab_20260921/results/q*_*.json` is an aggregate result, not a fill ledger. Byte sizes of those 16 files are in section a (11179 through 11459). `fills` is an integer count (`fills_field_type` `int` on every row). `fees` is `metrics.fees`. `per_game` has 31 rows on every file. `decision_records` is a count (`adaptive_policy.py` `finish` line 193). Standalone `completed_strategy_pnl` matches `results/experiment_summary.json` on all 16 scenarios (`branch_summary_pnl_matches_standalone` true). Summary sha256 `c22a9ddec133820e23d29a21410cc7d88010faae336cd179cc9b851851cb653f`, 206059 bytes.

Unresolved inventory is 0.0 and `all_flat` is true on every row below, so the stored completed P&L is the flat-window cash result from `replay_v2.py` line 334. These figures are hypothetical historical replay results stored in the branch commit. They are not a ranking.

| Scenario | `completed_strategy_pnl` | `unresolved_contracts` | `metrics.fees` | `fills` | `all_flat` |
|---|---:|---:|---:|---:|---|
| `q3300_d0.25_router_off` | 201.52149999992344 | 0.0 | 1437.4750999999899 | 14331 | True |
| `q3300_d0.25_router_on` | 354.33099999998285 | 0.0 | 1313.7027999999939 | 13001 | True |
| `q3300_d0.25_allocator_off` | 205.94219999993493 | 0.0 | 1429.0538999999892 | 14209 | True |
| `q3300_d0.25_allocator_on` | 345.24439999997867 | 0.0 | 1309.016999999992 | 12853 | True |
| `q3300_d5_router_off` | 198.4082999999182 | 0.0 | 1437.8165999999912 | 14045 | True |
| `q3300_d5_router_on` | 353.8933999999563 | 0.0 | 1311.8981999999944 | 12716 | True |
| `q3300_d5_allocator_off` | 203.26209999991897 | 0.0 | 1430.646099999991 | 13917 | True |
| `q3300_d5_allocator_on` | 345.417399999943 | 0.0 | 1306.7423999999926 | 12594 | True |
| `q10000_d0.25_router_off` | 10.354599999961465 | 0.0 | 561.3920999999967 | 4696 | True |
| `q10000_d0.25_router_on` | 90.44509999996444 | 0.0 | 504.94709999999776 | 4204 | True |
| `q10000_d0.25_allocator_off` | 14.292899999959445 | 0.0 | 562.5955999999968 | 4754 | True |
| `q10000_d0.25_allocator_on` | 75.9048999999668 | 0.0 | 509.4154999999978 | 4224 | True |
| `q10000_d5_router_off` | 0.3238999999530279 | 0.0 | 565.116299999998 | 4675 | True |
| `q10000_d5_router_on` | 79.0757999999596 | 0.0 | 508.2775999999982 | 4184 | True |
| `q10000_d5_allocator_off` | 6.690399999954934 | 0.0 | 566.0138999999978 | 4744 | True |
| `q10000_d5_allocator_on` | 69.05739999996058 | 0.0 | 510.58159999999833 | 4204 | True |

Fill, order, decision, and pair `jsonl.gz` files are listed in `EXTERNAL_ARTIFACTS.json` and are `NOT_FOUND` as blobs in `01c726ae9244d801d359e00df67d6a71f4012669`. `results/verification.json` (sha256 `4d5971ed28ade1d10bf24f701362389cc35fbbf161e5671ada4177c1803382e3`) records `decisions: 0` for every `router_off` and `router_on` case, and `all_checks_passed` true. The external pin for `q3300_d0.25_router_on_decisions.jsonl.gz` is 74 bytes, sha256 `bf0ce358d6e8ccdf2bcc60380a8601cab7ffc7560ba572a1e0a0dcbad0fa9134`, absent from the commit. Router-off pair gz pins are 71, 68, 72, and 69 bytes for `q3300_d0.25`, `q3300_d5`, `q10000_d0.25`, and `q10000_d5`, and those blobs are also absent. The zero decision count is the verification JSON field, not a decompression of those gzip bytes.

`q3300_d0.25_allocator_on_decisions.jsonl.gz` external pin: 838304 bytes, sha256 `dba3d5b26c31a1f4da90b17297be5b097d01b60298ae3414a21351a5b0a476fa`, absent. The main pin for `q3300_d0.25_D_decisions.jsonl.gz` is 838293 bytes, sha256 `c26827d0dbe1d9426343deeecc0d8b3e389ccf60f9dd24b683ff1ca1839066e4`, also absent. The stored pin hashes differ.

### Recomputed branch router gap

Formula, the same float subtraction as `q7_analysis.py` `differences`: `completed_strategy_pnl(router_on) - completed_strategy_pnl(router_off)`.

Display formula is `q7_analysis.py` `money`: `f"${x:+,.2f}"`.

| Stress | Recomputed gap | `effects.json` `guard_effect_router` | Equal | `router_on / allocator_on` | `router_on >= 0.95 * allocator_on` |
|---|---:|---:|---|---:|---|
| `q3300_d0.25` | 152.80950000005942 | 152.80950000005942 | True | 1.0263193262512142 | True |
| `q3300_d5` | 155.48510000003807 | 155.48510000003807 | True | 1.024538428000485 | True |
| `q10000_d0.25` | 80.09050000000298 | 80.09050000000298 | True | 1.1915581207537853 | True |
| `q10000_d5` | 78.75190000000657 | 78.75190000000657 | True | 1.1450735185513028 | True |

`effects.json` sha256 `90c9a2c95c59c03003fdb0653fc1a7f03dc56951f34f19fefa84e655404d57c0`. The recomputed gap equals the stored effects field on all four stresses. `Q7_RESULTS.md` (sha256 `0b75b48fdb302dd86869e1516bade13f42a1611e5ab150889d1bb6420c8c38e9`) prints those gaps as `$+152.81`, `$+155.49`, `$+80.09`, and `$+78.75`, and prints the router completed P&Ls as `$+354.33` / `$+201.52`, `$+353.89` / `$+198.41`, `$+90.45` / `$+10.35`, and `$+79.08` / `$+0.32`. Each of those display strings matches `money()` of the scenario JSON fields. `selection.json` `retains_allocator` checks match `router_on >= 0.95 * allocator_on` on all four stresses. The branch headline gap reproduces from its own in-tree scenario JSON.

The retention ratio above is router-on over allocator-on. It is not a B/D ratio.

### Recomputed main 0.843

Stored sentence in `packets/refiner/REFINER_PASS1_DIAGNOSIS_Q7_ARM_B_2026-09-23.md` (sha256 `2f5beac53925ed9452c8cda05825c6da5b51593b183877a63770bbb0df9f584e`), line 9:

> primary B/D = **0.843**; harsh queues 0.600 / 0.548

The same paragraph stores `retains_95pct_of_D=false` on every stress. Line 11 stores `D−B ≈ +$54.25` and `C−A ≈ +$4.42` and says those contrasts are "from scored effects; not re-derived."

Formula that would apply, from `analyze.py` lines 49–50 together with a ratio: `completed_strategy_pnl(B) / completed_strategy_pnl(D)`.

Numerator, denominator, and recomputed ratio: `NOT_FOUND`. The scenario ledgers and `paircheck_effects.json` are not in the commit. The stored headline **does not reproduce from a ledger in this commit**. The diagnosis does not say which harsh stress is 0.600 and which is 0.548. That assignment is `NOT_FOUND`.

`REFINER_PASS2_DIAGNOSIS_Q7_ARM_B_2026-09-23.md` stores approximate prose, not ledger fields: `q3300_d0.25: B0≈291 · B1≈176 · D≈345; B1≈51% of D`, and `q10000_d0.25` `≈88%`. Recomputation from a ledger is `NOT_FOUND`. The cited `experiment_summary.json` is `NOT_FOUND`. `packets/Q7_EXAMINER_SCORECARD_2026-09-22.md` and `reports/RPT-Q7.md`, named as diagnosis sources, are `NOT_FOUND` in `34a2720218b4f4f2d6dd0cbde6334ee672a3684b`.

## f. Why the two headline claims are not the same comparison

1. **Policy.** Main Arm B gates `quote` and leaves a working non-offset order on the inherited keep/cancel-delay path. Branch `router_on` removes failed keys inside `choose`, which cancels a working order on that key, and it resizes offsets with `bounded_quantity`. A non-two-leg selection is blocked only on the branch.
2. **What the headline divides.** The 0.843 sentence is B/D on the main pair-check. The branch gap that reproduces is `router_on - router_off`, and the branch 95 percent check divides `router_on` by `allocator_on`. Section d says B and `router_on` share a role slot and not an implementation.
3. **Labels.** A/B/C/D versus `router_*` / `allocator_*`, plus rehab B0/B1/B2. Reading "B" as `router_on` is the collision in section d.
4. **Inputs actually replayed in-tree.** The manifest hash matches, and the tape blob is missing on both sides. Main's in-tree pair-check status is `NOT_RUN_INPUTS_MISSING` with `pnl` null. The branch summaries are present. Desk B/D pins are a third set of absent bytes whose decision-gzip sha256 values differ from the branch external pins.
5. **Accounting objects.** Branch in-tree scenario files are the aggregates in section e (`q3300_d0.25_router_on.json` is 11303 bytes) with `fills` as a count, `unresolved_contracts` 0.0, and `all_flat` true. The main pin for `q3300_d0.25_B.json` is 56907767 bytes and the file is not in the tree, so its fee, fill, flatness, and unresolved fields are `NOT_FOUND`. Rehab ledgers are `NOT_RUN`.
6. **Stored status strings, copied, not rescored.** Branch `selection.json` stores `selected` `router_on` and `status` `DEVELOPMENT_SHADOW_CANDIDATE_ONLY`. The capital-structure pin stores `q7_packet_pins.selection` `NO_NEW_SELECTION` for the absent pair-check effects blob. This memo does not pick either status as the better P&L.

## g. Open items for a controlled reconciliation run

Proposal only. This packet does not run it.

1. Restore `events.jsonl.gz` whose sha256 is `cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4`, using the existing manifest. Do not commit the gzip.
2. If the desk B/D files are restored, check them against `PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json` before they are treated as the main-side score. A mismatch stays a failed pin, not a new P&L.
3. Freeze both policies as they are: `OriginalPairCheck` arm B and `GuardedRouter` `router_on`, plus the allocator counterparts if the question includes C/D. No new knob, no cushion change, no order-size change, no edit to `nfl_factorial_lab_20260921`.
4. Use one config: queues 3300 and 10000, delays 0.25 and 5 moving together, candles, liquidation lead 300, participation 0.5, last-12-hour queue `1327847.005`, the fee coefficients on `Config`. Leave `290.595` as the unused engine default unless a new freeze adds that stress.
5. Write per-scenario aggregates and the fill/order ledgers, and hash them. Keep `completed_strategy_pnl` null when the book is not flat. Do not count unresolved contracts as profit.
6. Recompute B/D and `router_on - router_off` from those new files. This memo's status is not that score.
7. No live orders.

## NOT_FOUND

- `events.jsonl.gz` bytes on both pins (declared sha256 is present; the blob is not).
- `nfl_paircheck_lab_20260922/results/paircheck_effects.json`.
- In-tree scenario JSON for main arms A, B, C, D, and therefore their completed P&L, unresolved contracts, fees, fills, and `all_flat`.
- Parent pin bytes for B and D JSON and gzip artifacts (hashes are stored; files are absent). A and C are not in that pin list.
- Decision counts inside the main B `*_decisions.jsonl.gz` pins.
- Which harsh stress is 0.600 and which is 0.548.
- Numerator and denominator of 0.843, and any recomputation of that ratio from a ledger.
- `nfl_q7_rehab_p1_cadence_20260923/results/experiment_summary.json` and every rehab B0/B1/B2/D scenario ledger.
- Exact ledger values behind the pass 2 prose `B0≈291`, `B1≈176`, `D≈345`, `≈51%`, and `≈88%`.
- `packets/Q7_EXAMINER_SCORECARD_2026-09-22.md` and `reports/RPT-Q7.md`.
- Branch `*_fills.jsonl.gz`, `*_orders.jsonl.gz`, `*_decisions.jsonl.gz`, and `*_pairs.jsonl.gz` bytes (pins exist in `EXTERNAL_ARTIFACTS.json`).
- An RNG seed on either Q7 runner.
