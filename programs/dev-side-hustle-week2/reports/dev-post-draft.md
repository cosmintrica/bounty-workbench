---
title: "Subcheck: A local listening checklist for subtitle editors"
published: false
tags: devchallenge, hf26challenge
---

<!-- DRAFT ON HOLD: project and video are public, but differentiation and usefulness need reassessment before DEV submission. No submission or acceptance is claimed. -->

A project for the [Hacktoberfest Week 2: Side Hustle challenge](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).

## What I Built

Subcheck turns an English audio file and its SRT captions into a focused listening checklist. It compares the captions with a local speech recognizer, points to possible missing dialogue and timing drift, and flags straightforward formatting problems such as overlapping cues. An editor can inspect the evidence, listen, and decide what to change. The original files stay unchanged.

The intended customer is a freelance video editor delivering captioned tutorials, product clips, or interviews. The proposed paid offering is a convenient local caption-review tool with setup and support. Its value would depend on whether the checklist saves more review time than its false positives consume. That is a business hypothesis: there are **zero customers and $0 revenue**, and no editor trial has taken place.

Existing projects such as [Crowbarr](https://github.com/amanofvaly/crowbarr) and [Subtitle Edit](https://nikse.dk/SubtitleEdit/) already cover related subtitle review and synchronization workflows. Subcheck is an experimental implementation; a meaningful advantage for editors has not been demonstrated. The working name is also used by unrelated software.

## Demo

**Video:** [View the evidence walkthrough](https://github.com/cosmintrica/bounty-workbench/blob/main/programs/dev-side-hustle-week2/source/subcheck/demo/subcheck-demo.mp4)

The demonstration uses an original, 14.98-second synthetic recording made with [eSpeak NG](https://github.com/espeak-ng/espeak-ng), through [espeakng-loader](https://github.com/thewh1teagle/espeakng-loader). It is not a client recording or a human usability test.

The script describes packing orders. A reference SRT follows the scripted sentences. A second SRT contains three deliberate changes:

| Deliberate change | Observed result |
|---|---|
| Delay the first cue by 1.5 seconds | A timing review item; the delay also causes a cue overlap |
| Change “blue notebook” to “red notebook” | A text comparison showing red versus blue |
| Remove the delivery sentence | An uncovered-speech item for the missing sentence |

All three changes were surfaced. The altered captions produced seven items in total. Running the reference captions through the same process still produced three items: the model transcribed the scripted **“three” as “free”**, and assigned low probabilities to “Put” and “box.” Those results remain in the demonstration. They explain why the output is a listening checklist and why it requires human judgment.

Each run exports a Markdown report, JSON evidence, a listening WAV, and `proposed.srt`. That SRT is an **unreviewed model transcript**, not a verified correction; it may lose speaker labels and other editorial formatting.

## Code

**Public repository:** [Source folder in the shared workbench](https://github.com/cosmintrica/bounty-workbench/tree/main/programs/dev-side-hustle-week2/source/subcheck)

The project started on October 14, 2026. Its source includes the CLI, alignment logic, tests, and synthetic-fixture generator. The delivery evidence records the environment, model revision, input hashes, and comparison results. Dependencies and model weights are downloaded separately.

The local workflow is:

```sh
python -m subcheck.cli prepare-model .models/tiny.en
python -m subcheck.cli audit audio.wav captions.srt \
  --model-dir .models/tiny.en --output review
```

Package installation comes first; the repository README contains the setup steps. Preparation needs internet access. After preparation, the review uses local model files.

## How I Built It

[OpenAI Whisper](https://github.com/openai/whisper) supplies the recognized words and approximate word times. Subcheck runs the pinned [SYSTRAN tiny.en conversion](https://huggingface.co/Systran/faster-whisper-tiny.en) through [faster-whisper](https://github.com/SYSTRAN/faster-whisper) and [CTranslate2](https://github.com/OpenNMT/CTranslate2) on the CPU. The model is central to the comparison; it is not used to decorate an otherwise unrelated feature.

The comparison logic normalizes text for matching, carries differences back to caption fragments, and keeps uncertain speech evidence separate from deterministic checks. Development review uncovered missed single-word omissions, ambiguous repeated phrases, misleading fragments across cue boundaries, and a draft-timing edge case. Those cases were corrected and added to the checks. The current suite passes **18 tests**.

Both the altered-caption and reference runs completed under a macOS profile that denied network access. A socket negative control failed with `PermissionError` under the same profile. This tests offline execution more directly than relying on an environment flag alone.

On the tested ARM64 Mac with Python 3.11.4, the first execution took 10.45 seconds; cached follow-ups took 1.362 and 1.03 seconds. These are measurements for one short synthetic fixture, not a general performance claim. The model used `int8_float32` computation.

**AI disclosure:** OpenAI Codex produced the implementation, tests, research, demonstration preparation, and this draft. Verification was automated and local. No human listen-through or real-editor evaluation has been completed, and no human review is claimed.

## Why Does Open Innovation Matter?

The open model and inference runtime let this workflow run on a laptop after preparation, with no transcription API account or per-minute API bill. Local execution was tested with networking denied, so this demo's audio did not need a remote transcription service. Hardware, electricity, setup, and editorial review still have costs.

The model revision is pinned and the weight checksum recorded. The comparison logic and evidence can be inspected, and a future version could evaluate a different model against the same fixtures. OpenAI Whisper, SYSTRAN's conversion, faster-whisper, and CTranslate2 make that possible; their licenses and the separate PyAV/FFmpeg dependency terms are credited in `THIRD_PARTY.md`.

The small English model also sets the present limit. Noise, accents, names, numbers, and repeated phrases need broader evaluation. Before treating Subcheck as a paid product, the next useful test is with an editor and consented real recordings: measure time saved, missed caption errors, and unnecessary review items. The “three/free” result is a concrete reason to do that evaluation before promising accuracy.
