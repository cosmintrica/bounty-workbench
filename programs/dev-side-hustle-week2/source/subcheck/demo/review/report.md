# Subcheck — local subtitle review

**Human review required.**

3 cues · 32 recognized words · 7 review items

Audio duration: 14.98s. Processing: 1.36s.

[Audio](audio.wav) · [Model subtitle draft](proposed.srt) · [Full evidence](report.json)

## Cue 1: text difference

2.00–5.85s · review

This caption fragment differs from speech recognition. Listen before editing; the model may be wrong.

Caption:

> three

Model comparison:

> free

## Cue 1: timing difference

2.00–5.85s · review

Aligned speech is about 0.11–4.41s; caption is 2.00–5.85s. Review synchronization.

Caption:

> Welcome to the studio. Today we are packing three orders.

Model comparison:

> Welcome to the studio. Today we are packing orders.

## Cue 2: overlap

5.05–7.36s · check

This cue begins before an earlier cue has ended.

## Cue 2: text difference

5.05–7.36s · review

This caption fragment differs from speech recognition. Listen before editing; the model may be wrong.

Caption:

> red

Model comparison:

> blue

## Cue 2: uncertain recognition

5.05–7.36s · review

Some aligned words have low model probability. This score is not calibrated accuracy.

Caption:

> Put the red notebook beside the camera.

Model comparison:

> Put

## Audio span: uncovered speech

8.25–10.37s · review

The model recognized words absent from the captions. Check for an omission or recognition error.

Caption:

> No matching caption text

Model comparison:

> the delivery leaves on friday morning

## Cue 3: uncertain recognition

11.06–14.28s · review

Some aligned words have low model probability. This score is not calibrated accuracy.

Caption:

> Please check every label before you close the box.

Model comparison:

> box.

## Limits

- AI differences are review suggestions. Listen to the audio before changing captions.
- The included tiny.en model is English-only and can miss or invent speech, especially in noise or silence.
- Word timestamps are approximate. Repeated phrases can align to the wrong occurrence.
- Numbers, names, contractions, paraphrases and non-speech captions can produce false positives.
- Reading speed is a configurable editorial threshold, not an accessibility certification.
- proposed.srt is an unreviewed model transcription; it does not preserve editorial formatting or speaker labels.

Model: Systran/faster-whisper-tiny.en @ 0d3d19a32d3338f10357c0889762bd8d64bbdeba
