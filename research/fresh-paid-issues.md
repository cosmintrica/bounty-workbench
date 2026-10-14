# Fresh paid OSS issue checks — 2026-10-14

**Result: no issue in this six-candidate pass is ready for us to implement.** Three were discovered through September/October 2026 GitHub searches, and three were checked against Algora's current public open listings. This is a bounded availability review, not a claim that all opportunities are exhausted. No claims, comments, account actions, source implementations, pull requests or payments were made.

Previously rejected JHipster, Tenstorrent #8621, Coolify, Tailcall website/gargantua, Gitpay, ZIO and Expensify issues were not revisited. Search results and third-party bounty-watch repositories were only discovery leads; decisions below use original project sources and the reward platform itself.

| Candidate | Verified monetary offer | Current availability / competition | Decision |
|---|---|---|---|
| [Tenstorrent tt-metal #59732](https://github.com/tenstorrent/tt-metal/issues/59732), created October 7, 2026 | Issue advertises **$3,000 USD** for correcting sampling distribution bias. This is an advertised award, not funding or received-payment evidence. | Open, but the issue body and GitHub assignee field explicitly reserve it for **samiyadev786**. Seven comments include other contributors requesting assignment/reassignment. Requires validation on both Wormhole and Blackhole hardware. | **Reject for current work: already assigned.** Do not duplicate the assignee's implementation or interpret public requests for reassignment as actual reassignment. |
| [Sybil local-ai-registry #223](https://github.com/sybil-solutions/local-ai-registry/issues/223), created October 12, 2026 | **$50** after an accepted, merged recipe; official [bounty policy](https://github.com/sybil-solutions/.github/blob/main/BOUNTIES.md) specifies PayPal or GitHub Sponsors within seven days. | Open, no assignee and no `claimed` label when fetched. Two comments: a proposed untested patch and a [separate `/attempt` request](https://github.com/sybil-solutions/local-ai-registry/issues/223#issuecomment-6145213090) awaiting maintainer confirmation. Searches of PRs for issue 223 and of the open PR list for 223/890M found no matching PR. A matching target machine is required; known current host is ARM64 macOS, not Ryzen AI 890M. | **Conditional future lead, not implementation-ready.** Needs access to the exact hardware, confirmed claim availability and payout eligibility. No spending or equipment acquisition proposed for a $50 task. |
| [VARUN3WARE/textkit-bounty #5](https://github.com/VARUN3WARE/textkit-bounty/issues/5), created October 12, 2026 | **No real money.** Its [README](https://github.com/VARUN3WARE/textkit-bounty#readme) explicitly identifies this as a simulation/demo with no actual payments. | Open and unassigned, but demo PRs already exist for intentionally seeded issues. | **Reject: simulated bounty pool.** The `bounty` label is not a monetary opportunity. |
| [Forgecode #389](https://github.com/tailcallhq/forgecode/issues/389), formerly under antinomyhq | [Algora](https://algora.io/antinomyhq/bounties?status=open) still advertises **$50** and lists it as open. | GitHub API resolves the repository redirect and reports **closed / completed**, July 28, 2025, assignee jayantpranjal0. | **Reject: completed underlying issue; stale reward listing.** |
| [D2 #1578](https://github.com/d2lang/d2/issues/1578), formerly under terrastruct | [Algora](https://algora.io/terrastruct/bounties?status=open) still advertises **$50** and lists it as open. | GitHub API resolves the redirect and reports **closed / not_planned**, September 15, 2026, assignee loop-index. | **Reject: declined/closed underlying task; stale reward listing.** |
| [node-seeli #135](https://github.com/esatterwhite/node-seeli/issues/135) | [CloudGakkai's Algora board](https://algora.io/cloudgakkai/bounties?status=open) and the original Algora bot comment advertise **$50**. | **Closed / completed** May 8, 2026 via PR #146; released in v18.1.0. Prior competing PRs #144 and #145 are in the thread. A contributor asked about payout after merge and release; no receipt or completed payment was established. | **Reject: completed implementation.** The open Algora entry and payout questions do not make it available again. |

## Conditions worth retaining for future candidates

### Sybil recipe bounties

The [official policy](https://github.com/sybil-solutions/.github/blob/main/BOUNTIES.md) explicitly directs contributors to use a coding agent in the recipe kit, so AI assistance is part of the published workflow. A contributor comments `/attempt`, a maintainer applies `claimed`, and the exclusive reservation lasts seven days. A PR opened while someone else holds the claim does not qualify.

Issue #223 requires an actual Ryzen AI 890M run with at least 64K context and six passing checks: loading, answering, reasoning, tool calls, near-full-context recall and at least 15 tokens/second. Estimates, different hardware, changed clocks or output caps do not qualify. The submission must carry real run evidence; a maintainer reproduces rentable hardware runs, otherwise machine/probe and memory logs are required.

The policy names two payment methods but does not establish this user's payment-account eligibility, tax/KYC requirements or past completed cash payouts. Those remain unverified. A pending `/attempt` is also not the same as a maintainer-approved claim. This lead may be reconsidered only if compatible hardware is already available and the maintainer confirms an eligible claim; no need to fabricate a recipe or benchmark on the Mac.

### Tenstorrent

[Terms](https://docs.tenstorrent.com/bounty_terms.html) require the contributor to hold the GitHub assignment when submitting, satisfy the issue acceptance criteria, release under the repository license and provide requested eligibility/payment information. Age of majority, legal capacity, non-conflicting obligations and program exclusions apply. This user's age/country alone do not prove full eligibility.

The issue's $3,000 advertised award is paired with a `bounty_difficulty/medium` label, while the current generic terms list $501–1,999 for medium. This discrepancy would require clarification before relying on the amount if the issue ever reopened; current assignment already rules it out.

[Contribution policy](https://github.com/tenstorrent/tt-metal/blob/main/CONTRIBUTING.md#bug-bounty-program---ai-tool-restrictions) permits offline AI development assistance only with personal human review, understanding and responsibility. It prohibits automated/AI-agent claim or assignment posts and requires human posting. Therefore no agent should claim a future issue on the user's behalf. The unassigned status of another issue would not override this rule.

For the three closed Algora tasks and the textkit simulation, the decisive unavailability evidence was sufficient to stop; current AI/payout eligibility was not inferred or fully audited for those unsuitable tasks.

## Evidence method and accounting

GitHub API issue metadata, original bodies/comments, public README/contribution policies and live official Algora listings were fetched on October 14, 2026. GitHub searches included `created:>=2026-10-01` and a broader `created:>=2026-09-01 label:bounty`, excluding previously screened/high-noise repositories. Queries of railwayapp open issues mentioning bounties returned zero; this is only a search result, not a statement about all Railway reward programs.

**Pass totals: 6 checked candidates, 0 selected implementations, 0 submissions, $0 awarded, $0 received.**
