# Task board

Format: `- [ ] (owner lane) task  ~estimate`. Tick with `[x]`. Requests to another lane start with `REQUEST:`.
Times are Cairo time. Submission window: Sat 14 Nov 09:00 to Sun 15 Nov 23:59 (confirm the Cairo local deadline at kickoff, it may be earlier).

## Phase 0: Friday night (tonight, max 2 hours, then SLEEP)
- [ ] (all) Clone repo, `python run.py setup`, `python run.py mock`, open http://localhost:8000 and see the demo map
- [ ] (all) Log in to Claude Code with your account, run `/sync` once to test
- [ ] (A) Push skeleton to a private GitHub repo, add teammates, create the 3 lane branches
- [ ] (C) Read the full statements of the 4 shortlisted challenges in `docs/DECISION_MATRIX.md`, note the official datasets and download size of each
- [ ] (B) Pick the app look: dark space theme, one hero view, confirm map + chart work offline from fixtures

## Phase 1: Sat 09:00 to 11:00 (decide, do not code)
- [ ] (all) Kickoff: confirm Cairo schedule, local judging time, pitch format
- [ ] (all) Score challenges in `docs/DECISION_MATRIX.md`, pick ONE by 10:30
- [ ] (C) Fill `docs/CHALLENGE.md`
- [ ] (A) Adapt `contracts/prediction.schema.json` to the challenge, regenerate fixtures, bump to v1
- [ ] (all) Write the one sentence pitch at top of `docs/PITCH.md`

## Phase 2: Sat 11:00 to 20:00 (walking skeleton: real data end to end, ugly is fine)
- [ ] (C) `data/fetch.py` downloads a SMALL real slice and caches it
- [ ] (A) Baseline model in `ml/train.py` with an honest validation metric
- [ ] (A) `ml/predict.py` writes `ml/outputs/predictions.json` that passes the contract
- [ ] (B) App shows real predictions when `MOCK=0`
- [ ] (A) 20:00 integration: merge all lanes to main, `python run.py check` green

## Phase 3: Sat 20:00 to Sun 02:00 (make it good)
- [ ] (A) Better model, error analysis, feature importance or explanation per item
- [ ] (B) Polish hero view, explanation panel, loading states
- [ ] (C) Science validation: compare against a known event or published result

## Night: Sun 02:00 to 08:00 (sleep in shifts, long jobs run unattended)

## Phase 4: Sun 08:00 to 14:00 (last features, FEATURE FREEZE 14:00)
- [ ] (A) Final model + metrics frozen into `ml/model_card.md`
- [ ] (B) Deploy (Render / HF Spaces / GitHub Pages with static JSON)

## Phase 5: Sun 14:00 to 23:59 (story + submission)
- [ ] (C) Demo video (max length per submission guide, English subtitles)
- [ ] (C) Slides from `docs/PITCH.md`
- [ ] (all) Fill submission page, references, public repo link
- [ ] (all) SUBMIT a first version by 20:00, then improve until deadline

## Lane A inbox

## Lane B inbox

## Lane C inbox
