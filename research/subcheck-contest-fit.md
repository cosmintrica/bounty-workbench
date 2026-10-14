# Subcheck: contest fit and nearby entries

Checked 2026-10-14. Public, read-only research. No login, account changes, publication, organizer contact, or submission. **DEV submission has not occurred**, in the project records; creating a public repository is a separate action and does not enter the contest.

## Assessment

**Subcheck plausibly fits the prompt, but it is neither unique in the market nor accepted by the organizers.** A close Week 2 entry already performs local Whisper audio-versus-text checking. That similarity does not itself establish copying or disqualification. It does weaken any claim that the general concept is new. The defensible distinction is the narrow workflow: review an existing English SRT against audio, inspect text and timing differences, and export evidence plus a proposed SRT for a person to review.

The separate product research found additional prior art outside this contest. This file does not duplicate that investigation or represent an exhaustive novelty search.

## Closest public entries found

Two meaningfully close entries were identified; padding the list to six with unrelated receipt or listing apps would not improve this assessment. Descriptions below summarize author claims, not independently reproduced capabilities.

| Entry | Challenge/date | Overlap and distinction |
|---|---|---|
| [Backlist — Kokoro read 'Chapter IV' as 'Chapter Roman Four'. So I gave it a proofreader with ears.](https://dev.to/vanshaj/kokoro-read-chapter-iv-as-chapter-roman-four-so-i-gave-it-a-proofreader-with-ears-9id) | **Week 2: Side Hustle**, October 13 | Closest current competitor. Kokoro creates audiobook narration; local Whisper checks the resulting audio against manuscript lines. Users inspect flagged omissions, repeated or substituted words and pronunciation concerns. The author describes a substantial synthetic-fault evaluation, false alarms, browser inference, and no first user. This overlaps with Subcheck's core checking and review workflow. Subcheck instead takes existing audio and SRT as inputs, evaluates caption timing and format constraints, and produces CLI reports/proposed subtitle output. Do not claim that Whisper proof-listening, local processing, or human review queues are unique. |
| [Whisper AI & FFmpeg Media Transcriber — I Built a Local AI Transcriber for a Friend Who Works With Too Much Audio and Video](https://dev.to/manish7107/i-built-a-local-ai-transcriber-for-a-friend-who-works-with-too-much-audio-and-video-1h2g) | **Weekend: Build for a Friend**, October 3; **not a Week 2 competitor** | Adjacent prior challenge entry, visible through the shared tag. Local Whisper/FFmpeg transcription with a browser media player, timestamps and SRT/VTT/JSON exports. It shows that local Whisper subtitle production is already represented in this challenge series. The post describes generating transcripts, not auditing an existing SRT against audio. Its different challenge must not be counted as current Week 2 competition. |

Search coverage: the user-supplied [official tag](https://dev.to/t/hf26challenge), [page 2](https://dev.to/t/hf26challenge/page/2), the beginning of [page 3](https://dev.to/t/hf26challenge/page/3), and targeted DEV searches for Whisper, subtitle, SRT, caption, and audio QA. Anonymous tag ordering and search indexing are incomplete evidence. **No identical audio-plus-existing-SRT Week 2 entry was found in this bounded pass; absence from these results does not prove none exists.** The tag includes multiple challenge weeks and generic captions can mean social-media copy.

## Rules and repository interpretation

The [contest-specific rules](https://dev.to/page/hacktoberfest-week2-2026-10-12-contest-rules) set the entry window to **October 12, 2026, 12:00 PM PDT through October 18, 2026, 11:59 PM PDT**. Required entry components include the DEV post, code repository link, demo/video and open-source AI central to the project. A paying user is useful evidence, not a prerequisite. The overall prize is competitive; no result or payment is implied by meeting entry requirements.

The [challenge FAQ](https://dev.to/challenges/hacktoberfest-week2-2026-10-12) says: **“all submissions and their respective repositories must be started and completed within the challenge window.”** It permits AI use and substantial contributions built upon open-source work, with attribution for nontrivial prior work. Agent-session sharing is optional; later commits must be identified in the README. Writing quality has the highest judging weight. We found no separate rule requiring exclusively human-written code or an explicit human-review prerequisite; that does not excuse inaccurate statements about who reviewed or tested the product.

The [general rules](https://dev.to/page/official-hackathon-rules) require the entrant's original creation and development starting during the entry period. Independent implementation of a similar idea is not expressly prohibited. Copying an existing implementation or merely repackaging old work as a new repository would not satisfy these requirements. Similarity alone cannot settle authorship or eligibility.

**Umbrella repository:** neither consulted rule document expressly requires a dedicated one-project repository or expressly authorizes monorepos. No visible [organizer launch comment](https://dev.to/devteam/join-the-hacktoberfest-open-source-ai-challenge-side-hustle-2550-in-prizes-across-18-winners-55ba/comments) resolved that question. **Inference:** a newly created umbrella repository containing clearly identified, newly developed Subcheck code could satisfy the stated repository requirement. Link directly to Subcheck's folder and README, identify its development dates and dependencies, preserve genuine commit history, and clearly separate unrelated projects. A new umbrella repo must not be presented as proof that previously existing code was developed during the window. **This interpretation is not organizer approval.**

## What can be stated honestly now

- Local project evidence records 18 tests and real Whisper inference with network access denied after dependencies/model were present. This supports a working prototype and its tested fixture, not general transcription accuracy.
- The demonstrated input is one original 14.98-second synthetic English clip. The reference subtitles still trigger a three/free substitution and low-probability word flags. No human listen-through, real-editor trial, customers or revenue are documented in current verification.
- Our plausible customer and pricing remain hypotheses. Keep the manuscript/SRT distinction clear, credit Whisper and other dependencies, and avoid claims of worldwide novelty, automatic correctness, real customer validation, contest acceptance or expected earnings.
- A public source repository is only one entry component. Until the correctly tagged English DEV post with accessible code/demo is actually published, the project is **not submitted**. After publication, eligibility and judging remain the organizers' decision.

Submission state in this research pass: **not submitted; no award; $0 received**.
