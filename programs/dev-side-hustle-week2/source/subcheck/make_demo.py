"""Generate original synthetic test speech with eSpeak NG; no human voice data.

Optional dev dependency: espeakng-loader==0.2.4 (GPL speech engine, separately
installed). Uses the documented eSpeak synchronous callback API.
"""
import ctypes as c
import json
from pathlib import Path
import sys
import tempfile
import wave

import espeakng_loader
from subcheck.core import timestamp


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('demo')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('Demo destination must be empty.')
    lib = espeakng_loader.load_library()
    if lib is None:
        raise SystemExit('Unable to load eSpeak NG.')
    lib.espeak_Initialize.argtypes = [c.c_int, c.c_int, c.c_char_p, c.c_int]
    lib.espeak_Initialize.restype = c.c_int
    # The bundled engine truncates long data-directory paths. A temporary short
    # link keeps it usable from deep workspaces without changing installed files.
    short_path = tempfile.TemporaryDirectory(prefix='subcheck-voice-')
    data_link = Path(short_path.name) / 'espeak-ng-data'
    data_link.symlink_to(espeakng_loader.get_data_path(), target_is_directory=True)
    rate = lib.espeak_Initialize(2, 0, str(data_link.parent).encode(), 0x8000)
    if rate <= 0:
        raise SystemExit('Unable to initialize eSpeak data.')
    callback_type = c.CFUNCTYPE(c.c_int, c.POINTER(c.c_short), c.c_int, c.c_void_p)
    chunks = []

    @callback_type
    def receive(samples, count, events):
        if samples and count:
            chunks.append(c.string_at(samples, count * 2))
        return 0

    lib.espeak_SetSynthCallback.argtypes = [callback_type]
    lib.espeak_SetSynthCallback(receive)
    lib.espeak_SetVoiceByName.argtypes = [c.c_char_p]
    if lib.espeak_SetVoiceByName(b'en-us') != 0:
        raise SystemExit('English voice unavailable.')
    lib.espeak_SetParameter(1, 145, 0)
    lib.espeak_Synth.argtypes = [c.c_char_p, c.c_size_t, c.c_uint, c.c_int,
                                c.c_uint, c.c_uint, c.c_void_p, c.c_void_p]
    sentences = [
        'Welcome to the studio. Today we are packing three orders.',
        'Put the blue notebook beside the camera.',
        'The delivery leaves on Friday morning.',
        'Please check every label before you close the box.',
    ]
    audio = bytearray(b'\0' * (rate // 2 * 2))
    truth = []
    for text in sentences:
        chunks.clear()
        data = text.encode() + b'\0'
        if lib.espeak_Synth(data, len(data), 0, 1, 0, 1, None, None) != 0:
            raise SystemExit('Synthesis failed.')
        start = len(audio) / (rate * 2)
        audio.extend(b''.join(chunks))
        end = len(audio) / (rate * 2)
        truth.append(dict(start=start, end=end, text=text))
        audio.extend(b'\0' * (round(rate * .7) * 2))
    lib.espeak_Terminate()
    short_path.cleanup()
    out.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out / 'packing-orders.wav'), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(audio)

    def srt(rows):
        return '\n\n'.join(f"{i}\n{timestamp(r['start'])} --> {timestamp(r['end'])}\n{r['text']}"
                            for i, r in enumerate(rows, 1)) + '\n'
    (out / 'reference.srt').write_text(srt(truth))
    changed = [dict(row) for row in truth]
    changed[0]['start'] += 1.5
    changed[0]['end'] += 1.5
    changed[1]['text'] = changed[1]['text'].replace('blue', 'red')
    changed.pop(2)
    (out / 'needs-review.srt').write_text(srt(changed))
    (out / 'fixture.json').write_text(json.dumps(dict(
        source='Original text synthesized by eSpeak NG via espeakng-loader 0.2.4',
        voice='en-us', words_per_minute=145, sample_rate=rate, sentences=truth,
        intentional_changes=['First cue delayed by 1.5 seconds', 'blue replaced by red in cue 2',
                             'Delivery sentence omitted']), indent=2) + '\n')
    print(f'Created synthetic demo in {out}; {len(audio)/(rate*2):.2f}s.')


if __name__ == '__main__':
    main()
