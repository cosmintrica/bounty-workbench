# Subcheck — prior art and readiness reassessment

Checked October 14, 2026 after implementation. This comparison should have been
performed before investing in a contest entry. It changes the next action: keep
Subcheck as an experimental project and hold the DEV submission pending a stronger,
evidence-backed reason for an editor to choose it.

- [Crowbarr](https://github.com/amanofvaly/crowbarr) is an MIT project created
  September 8, 2026. Its official README describes Whisper-based subtitle auditing,
  timing repair while preserving authored text, and separate output files. This
  overlaps materially with the premise; it targets self-hosted media libraries.
- [Subtitle Edit](https://nikse.dk/SubtitleEdit/) already provides speech recognition,
  subtitle comparison, timing tools and editorial checks. Its broader GUI has a
  substantial existing feature set. No direct benchmark against it was performed.
- The [subcheck package on PyPI](https://pypi.org/project/subcheck/) is an unrelated
  GitHub OIDC checker. Our distribution is named subcheck-local and is not published
  to PyPI; the display/console name is provisional and not unique.

Our work is a small audio-plus-existing-SRT CLI with an inspectable review report,
not evidence that the idea is new or that customers will pay. The current checks
prove bounded local behavior: 18 unit tests and two inference runs on one original
synthetic clip. They do not establish human-speech reliability or market demand.

The user asked about a current contest entry with an overlapping workflow; see
subcheck-contest-fit.md for the separate current-tag and official-rule review.
No DEV entry, organizer eligibility decision, award or payment has occurred.
