# Third-party components

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper), copyright 2023
  SYSTRAN, MIT. Runtime dependency installed from PyPI.
- [CTranslate2](https://github.com/OpenNMT/CTranslate2), SYSTRAN/OpenNMT authors,
  MIT. Inference runtime installed as a dependency.
- [SYSTRAN faster-whisper-tiny.en](https://huggingface.co/Systran/faster-whisper-tiny.en),
  revision `0d3d19a32d3338f10357c0889762bd8d64bbdeba`. Model card identifies MIT
  and a conversion of OpenAI Whisper. Downloaded independently; not redistributed.
- [OpenAI Whisper](https://github.com/openai/whisper), copyright 2022 OpenAI,
  source README licenses code and weights under MIT. The original Hugging Face
  tiny.en metadata displays Apache-2.0; the exact SYSTRAN artifact above is used.
- [PyAV](https://github.com/PyAV-Org/PyAV), BSD 3-clause. Bundled FFmpeg libraries
  have their own LGPL/GPL configurations. Do not describe the whole stack as MIT.
- Optional demo generation uses [espeakng-loader](https://pypi.org/project/espeakng-loader/)
  0.2.4 (MIT loader) and the separately installed [eSpeak NG](https://github.com/espeak-ng/espeak-ng)
  speech engine (GPL-3.0-or-later). No engine library or voice data is bundled
  in this project's source distribution. The original short script was written
  for this demonstration; the audio is synthetic, with no human voice recording.

The source project uses dependency installation instructions. If distributing
standalone binaries or model bundles, retain all applicable license notices and
review transitive redistribution requirements separately.
