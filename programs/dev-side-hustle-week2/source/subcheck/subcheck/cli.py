"""Explicit model preparation, followed by local-only subtitle review."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.request
import wave

from .core import Word, analyze, parse_srt, proposed_srt, serialize

MODEL_ID = "Systran/faster-whisper-tiny.en"
REVISION = "0d3d19a32d3338f10357c0889762bd8d64bbdeba"
WEIGHT_SHA256 = "1a5afae06a4db91c975c9a9d78be5cc110ee4ea022ad57d55492e4550e936b2a"
MODEL_FILES = ("config.json", "model.bin", "tokenizer.json", "vocabulary.txt", "README.md")
LIMITATIONS = [
    "AI differences are review suggestions. Listen to the audio before changing captions.",
    "The included tiny.en model is English-only and can miss or invent speech, especially in noise or silence.",
    "Word timestamps are approximate. Repeated phrases can align to the wrong occurrence.",
    "Numbers, names, contractions, paraphrases and non-speech captions can produce false positives.",
    "Reading speed is a configurable editorial threshold, not an accessibility certification.",
    "proposed.srt is an unreviewed model transcription; it does not preserve editorial formatting or speaker labels.",
]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_model(destination: Path):
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("Model destination must be empty; existing files will not be replaced.")
    destination.mkdir(parents=True, exist_ok=True)
    entries = []
    for name in MODEL_FILES:
        url = f"https://huggingface.co/{MODEL_ID}/resolve/{REVISION}/{name}"
        target = destination / name
        print(f"Downloading {name} from the pinned public model revision…", flush=True)
        with urllib.request.urlopen(url, timeout=120) as response, target.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        checksum = sha256(target)
        if name == "model.bin" and checksum != WEIGHT_SHA256:
            raise ValueError("Downloaded model weight checksum differs from the publisher record.")
        entries.append({"name": name, "bytes": target.stat().st_size, "sha256": checksum, "url": url})
    manifest = dict(name=MODEL_ID, revision=REVISION, files=entries,
                    downloaded_at=datetime.now(timezone.utc).isoformat())
    (destination / "subcheck-model.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Model saved to {destination}. Audits can now run offline.")


def load_model_metadata(model_dir):
    for name in MODEL_FILES[:4]:
        if not (model_dir / name).is_file():
            raise ValueError(f"Missing local model file: {name}. Run prepare-model first.")
    manifest_path = model_dir / "subcheck-model.json"
    if not manifest_path.is_file():
        raise ValueError("The local model needs a subcheck-model.json provenance manifest.")
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("name") != MODEL_ID or manifest.get("revision") != REVISION:
        raise ValueError("This release expects its pinned English model revision.")
    if sha256(model_dir / "model.bin") != WEIGHT_SHA256:
        raise ValueError("Model weight checksum differs from the publisher record.")
    for item in manifest["files"]:
        if item["name"] not in MODEL_FILES:
            raise ValueError("Unexpected file in model manifest.")
        if sha256(model_dir / item["name"]) != item["sha256"]:
            raise ValueError(f"Model checksum mismatch: {item['name']}")
    return {key: manifest[key] for key in ("name", "revision")}


def markdown_report(report):
    def quote(value):
        return "\n".join("> " + line.replace("<", "&lt;").replace(">", "&gt;")
                         for line in str(value).splitlines())
    lines = ["# Subcheck — local subtitle review", "", "**Human review required.**", "",
             f"{report['summary']['cues']} cues · {report['summary']['words']} recognized words · "
             f"{report['summary']['issues']} review items", "",
             f"Audio duration: {report['duration_seconds']:.2f}s. Processing: {report['elapsed_seconds']:.2f}s.",
             "", "[Audio](audio.wav) · [Model subtitle draft](proposed.srt) · [Full evidence](report.json)", ""]
    for issue in report["issues"]:
        cue = f"Cue {issue['cue_id']}" if issue["cue_id"] is not None else "Audio span"
        lines.extend([f"## {cue}: {issue['kind'].replace('_', ' ')}", "",
                      f"{issue['start']:.2f}–{issue['end']:.2f}s · {issue['severity']}", "",
                      issue["message"], ""])
        if issue["expected"]:
            lines.extend(["Caption:", "", quote(issue["expected"]), ""])
        if issue["observed"]:
            lines.extend(["Model comparison:", "", quote(issue["observed"]), ""])
    if not report["issues"]:
        lines.extend(["No differences exceeded the selected checks. This is not a guarantee of accuracy.", ""])
    lines.extend(["## Limits", ""] + [f"- {line}" for line in report["limitations"]])
    lines.extend(["", f"Model: {report['model']['name']} @ {report['model']['revision']}", ""])
    return "\n".join(lines)


def audit(args):
    # Set before importing any model/hub library. Only local paths are passed.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    if not args.audio.is_file() or not args.captions.is_file():
        raise ValueError("Audio and captions must both be existing local files.")
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("Output directory must be empty; previous reviews will not be overwritten.")
    cues = parse_srt(args.captions.read_text(encoding="utf-8-sig"))
    metadata = load_model_metadata(args.model_dir)
    started = time.monotonic()
    from faster_whisper import WhisperModel, decode_audio
    audio = decode_audio(str(args.audio), sampling_rate=16000)
    duration = len(audio) / 16000
    if duration <= 0:
        raise ValueError("Audio has no samples.")
    model = WhisperModel(str(args.model_dir), device="cpu", compute_type="int8",
                         cpu_threads=args.threads, local_files_only=True)
    segments, info = model.transcribe(audio, language="en", beam_size=5, word_timestamps=True,
                                      vad_filter=True, condition_on_previous_text=False)
    words = [Word(w.start, w.end, w.word, w.probability) for s in segments for w in (s.words or [])]
    issues = analyze(cues, words, duration, max_cps=args.max_cps, drift=args.drift)
    metadata["compute_type"] = model.model.compute_type
    report = dict(audio_name=args.audio.name, captions_name=args.captions.name, model=metadata,
                  generated_at=datetime.now(timezone.utc).isoformat(), duration_seconds=duration,
                  elapsed_seconds=round(time.monotonic() - started, 3),
                  summary=dict(cues=len(cues), words=len(words), issues=len(issues)),
                  issues=issues, cues=serialize(cues), transcript=serialize(words),
                  settings=dict(max_cps=args.max_cps, drift=args.drift, threads=args.threads,
                                language=info.language, vad=True), limitations=LIMITATIONS,
                  inputs=dict(audio_sha256=sha256(args.audio), captions_sha256=sha256(args.captions)))
    args.output.mkdir(parents=True, exist_ok=True)
    with wave.open(str(args.output / "audio.wav"), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes((audio.clip(-1, 1) * 32767).astype("<i2").tobytes())
    (args.output / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    (args.output / "report.md").write_text(markdown_report(report))
    (args.output / "proposed.srt").write_text(proposed_srt(words))
    print(f"Reviewed {len(cues)} cues against {len(words)} locally recognized words.")
    print(f"{len(issues)} review items. Listen before editing. Report: {args.output / 'report.md'}")


def main():
    parser = argparse.ArgumentParser(description="Local subtitle review for freelance editors")
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare-model", help="Download the pinned ~78 MB English model")
    prep.add_argument("destination", type=Path)
    run = sub.add_parser("audit", help="Compare local audio and SRT; never uploads either input")
    run.add_argument("audio", type=Path)
    run.add_argument("captions", type=Path)
    run.add_argument("--model-dir", required=True, type=Path)
    run.add_argument("--output", required=True, type=Path)
    run.add_argument("--threads", type=int, default=4, choices=range(1, 17), metavar="1..16")
    run.add_argument("--max-cps", type=float, default=20)
    run.add_argument("--drift", type=float, default=.6)
    args = parser.parse_args()
    try:
        prepare_model(args.destination) if args.command == "prepare-model" else audit(args)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f"subcheck: {error}\n")


if __name__ == "__main__":
    main()
