# Demonstration evidence

The original eSpeak NG fixture is 14.98 seconds. The deliberately altered SRT
contains a 1.5-second delay, red/blue substitution and omitted sentence. All three
changes generated review suggestions; the delayed cue also overlaps the next cue.
The changed-caption report has seven items. The reference report has three:
three/free recognition error and low model probabilities for Put and box.

18 tests passed; see unit-tests.txt. verification.json records source hashes,
versions and actual timings. Inference completed for both SRT inputs under the
macOS profile `(version 1)(allow default)(deny network*)`. A socket negative
control under the same profile failed with PermissionError (network denied).
Dependencies and the pinned model had already been downloaded before these runs.

subcheck-demo.mp4 is a generated evidence walkthrough, not a recording of a
separate graphical interface. It contains the actual synthetic fixture and
summarizes the saved results. Its provenance records input and output hashes.

There has been no human listen-through or real-editor evaluation. No customer,
revenue, contest entry, award or payment is claimed.
