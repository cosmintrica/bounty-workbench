# Subcheck

Local subtitle review for freelance video editors. Compare an English audio file
with existing SRT captions and receive a listening checklist, word-level evidence,
and an editable model transcription. Original files are never changed.

Whisper is central: it supplies the spoken words and approximate timestamps used
to identify possible omitted dialogue, text differences, and timing drift. Local
checks also flag overlapping cues, cues past the audio end and reading speed above
your threshold. **Speech recognition is fallible; every suggestion needs review.**

## Run

Python 3.10+ is required. The tested environment and exact versions are recorded
in the accompanying evidence. Initial package and model downloads need internet;
review uses the pinned local model and no cloud API key.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m subcheck.cli prepare-model .models/tiny.en
.venv/bin/python -m subcheck.cli audit audio.wav captions.srt \
  --model-dir .models/tiny.en --output review
```

Open `review/report.md`, listen to `review/audio.wav`, and inspect the original
caption against the recognition result. `review/proposed.srt` is an **unreviewed
ASR draft**, not a verified correction. `review/report.json` includes input hashes,
model revision, word probabilities, thresholds and timing evidence. The output
directory must be empty so an existing editorial review cannot be overwritten.

Use `--max-cps 20` to adjust characters per second and `--drift 0.6` for the timing
comparison threshold. These are editorial choices, not standards certification.

## Try the included fixture

The `demo/` directory includes a 14.98-second original synthetic voice clip,
reference captions, deliberately altered captions and actual saved reports.
After installing and downloading the model, run:

```sh
.venv/bin/subcheck audit demo/packing-orders.wav demo/needs-review.srt \
  --model-dir .models/tiny.en --output my-demo-review
```

The altered captions contain a 1.5-second delay, "red" in place of "blue", and
an omitted delivery sentence. All three changes generated suggestions in the
tested run. The correct reference captions still produced a "three"/"free"
recognition difference and two low-probability flags. See both saved reports;
the fixture is an illustration, not a reliability benchmark.

Tested on macOS 27.0.1, Apple silicon, Python 3.11.4. Both fixture audits also
completed with network access denied by the operating system. This establishes
offline inference in that tested configuration after dependencies/model download.
The exact installed dependency versions are in `requirements-tested.txt`.

## Limits

- Tiny.en is English-only and trades accuracy for a small CPU footprint.
- Noise, silence, accents, names and numbers can produce incorrect recognition.
- Repeated phrases may align to the wrong occurrence; times are estimates.
- Word probabilities are not calibrated accuracy scores.
- Draft SRT does not preserve speaker labels, sounds or editorial formatting.
- Synthetic demo results do not establish real-client reliability or demand.

## Development

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Optional fixture regeneration (use a new, empty output directory):

```sh
.venv/bin/python -m pip install espeakng-loader==0.2.4
.venv/bin/python make_demo.py regenerated-demo
```

This optional speech generator is not needed to review existing audio or run
the included fixture. Its engine has a separate GPL license; see the notices.

New project started October 14, 2026 for the DEV/MLH Week 2 Side Hustle challenge.
No customers, revenue, contest acceptance or prize are claimed. AI assistance was
used for implementation, research and testing. Human review is required before
publication or submission. No entry has been submitted.

## Open-source components

faster-whisper 1.2.1 and CTranslate2 run the pinned SYSTRAN conversion of OpenAI's
Whisper tiny.en on the CPU. See `THIRD_PARTY.md` for attribution. Model weights and
dependencies are downloaded separately and are not bundled in this source tree.
