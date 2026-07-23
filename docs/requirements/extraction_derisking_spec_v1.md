# Extraction De-Risking Specification v1.0

**Verbatim carrier** — extracted from `docs/governance/registry_doctrine_v1.md` Part VII (source SHA-256 pre-D-12-amendment: `9dd1cc4bee310ad36780d182377ae8f3e25b7a681430c982dda18d76a408fbcf` · post-D-12-amendment: `b42317239067d303a7479246372423b7054f76b4c7f881e7bd6d9a490837524b` · Part VII byte-identical across both). Standing Rule v3: source untouched (extraction is a read; source preserved byte-identical); this file carries the same text as a standalone requirements-canon artifact.

**Landed:** 2026-07-15 per Owner-verbatim ITEM 4 (D) of the Gap-Closure + Sequence Ratification dispatch.

**Companion to:** Registry Doctrine v1.0 · Transformation Quality Specification v1.0 §5.1 (speech table is the §5.1 instantiation per TQ landing pointer, unchanged) · Operating Values v1.1 · Critic Seam Spec v1.0/v1.1.

---

# Part VII — Extraction quality: the de-risking specification

Premise, Owner-agreed: extraction quality on a specific estate is unmeasured until measured — but its weak surfaces are enumerable in advance, each has existing open art, and each maps to a designed lever in the platform. The gap is speccable, not fated. Governing principle, restating D-7: engineer the inputs relentlessly; never touch the test. Model choice, fine-tuning, augmentation, and corpus curation are legitimate curation of success; the validation verdict (the human-baseline benchmark, BM-V) is drawn from measured estate composition, post-census, uncurated — a rehearsed checkpoint is preparation; a curated verdict is worthless.

| Weak surface | Existing art (starting points) | Akki lever | Pre-verdict checkpoint |
|---|---|---|---|
| Swahili & Kenyan languages | Meta MMS (1,100+ languages); multilingual Whisper; Mozilla Common Voice Swahili; FLEURS; KenCorpus | Registry-pinned base models per language; language-routed model selection at job level | Per-language WER on a small real sample — measured in week one, not month three |
| Code-switching (Sheng, Swahili–English) | Code-switch fine-tuning recipes; East African community corpora (Masakhane ecosystem) | Census-curated code-switch corpus → in-perimeter fine-tune; improved model re-enters via registry bump | Code-switched-segment WER vs monolingual baseline, same speakers |
| Accented English | AfriSpeech-200 (pan-African accented English); accent-adaptation literature | Fine-tune or adapter on accented checkpoint; pinned provenance either way | Accent-stratified WER on real archive segments |
| Degraded / telephone / AM archival audio | Standard augmentation + domain-adaptation recipes for narrowband, noisy audio | Augmentation in the training loop; era- and quality-stratified census slices target hard bands | WER by decade and quality band — the census provides strata for free |
| Speaker overlap & call-in diarization | Open diarization stacks (pyannote-class); overlap-aware recipes | Diarization model swap via the registry; VAD/diarizer independently upgradable | DER on a multi-speaker call-in sample |

## §7.1 Sequencing — each rung cheap, each rung a real number

- 1 · Domain-transfer measurement (first). Run current registry models on a small genuine sample spanning the strata above. Output: baseline WER/DER per surface. Days of work; removes the largest unknown first.
- 2 · Targeted adaptation. Where a surface misses its working threshold, apply its lever — swap base model, fine-tune, augment — and re-measure the same checkpoint. The registry's additive versioning records every attempt with pinned provenance.
- 3 · Composition-scale validation. BM-V runs on a slice drawn from the censused estate's real composition. Whatever it says is published internally and stands as the claimable number. Its P9-E5 bindings are unchanged by this doctrine: verdict inside the phase; no production mining until PASS.
- 4 · Throughput & cost. Only after quality is known: hours-per-GPU-hour and cost per qualified unit on production hardware — planning-grade economics become quoted economics.

Claims discipline: until step 3 completes, collateral states the method, never a number; after step 3, the measured figure is the only accuracy claim in circulation — whatever it is.

---

*Extraction De-Risking Specification v1.0 · 2026-07-15 · verbatim carrier of Registry Doctrine v1.0 Part VII · Owner-ruled standalone landing per Gap-Closure + Sequence Ratification dispatch ITEM 4 (D). Under D-12: mechanics enumerated above are known and parameterized; every checkpoint deploys in force with its conditions of success strictly implemented; construction order carries no epistemic weight.*
