# Mozilla client bounty: PDF.js policy qualification

Checked: 2026-10-14. Public policy research only; no testing, source investigation, accounts, contact, or submission. This assessment concerns the Firefox client program, not Mozilla's web bounty program or HackerOne.

## Decision

**Qualified paid-program lead, with a high impact threshold and a critical component caveat:** evaluate only an issue that affects PDF.js as used inside an eligible official Firefox build. A standalone PDF.js finding is not sufficient. There is no finding, award, or payment from our work yet.

## Authorization and researcher eligibility

[General policy and safe harbor](https://www.mozilla.org/en-US/security/bug-bounty/): Mozilla expressly authorizes compliant research and promises not to pursue legal action for good-faith compliance or accidental/good-faith violations. That promise does not authorize third-party systems. Use researcher-owned/test data, avoid service disruption, and prefer local instances. Give Mozilla reasonable remediation time before third-party disclosure.

The reporter must be legally eligible to participate/receive payment, not have contributed the buggy code, and have no employment, contractor, or other business relationship with Mozilla or its subsidiaries. Sanctioned persons/countries are excluded. Romania is not specifically excluded by the published policy, but this is not individual eligibility or payment-onboarding confirmation.

Originality matters: external duplicate reports within 48 hours may split a reward. Previously internally reported issues normally do not qualify unless external evidence materially enables a stalled fix; Mozilla also reserves seven days for its internal automated detection. Excessive invalid reports can reduce rewards or lead to account restrictions.

## Current monetary and report terms

[Client program](https://www.mozilla.org/en-US/security/client-bug-bounty/): current Firefox release, Beta and Nightly builds can qualify; end-of-life products do not. Typical eligibility requires high/critical severity, with exceptional moderate cases discretionary.

| Category | Published ceiling, USD |
|---|---:|
| High impact | $3,000 |
| UXSS | $10,000 |
| Highest impact, including qualifying sandbox escape | $20,000 |

These are ceilings, not minimums or guaranteed awards; the Bounty Committee decides. A qualifying mitigation bypass can receive a separate bonus under the published criteria.

Use a Bugzilla account and the linked client bounty form, one issue per submission. Supply a simple reproducible case plus a root-cause explanation or suitable crash/ASAN evidence; enough information must exist to diagnose and fix it. A complete exploit is unnecessary. Attach supporting material, keep the description concise, and omit reporter-assigned severity keywords/CVSS scores. If filed without the bounty form, notify `security@mozilla.org` with the bug number and bounty request, not vulnerability details. Continuing diagnostic cooperation can improve the award.

Unbundled third-party software and routine vendor patch gaps normally do not qualify.

## PDF.js caveat and low-value exclusions

[Official client FAQ](https://www.mozilla.org/en-US/security/bug-bounty/faq/): a third-party build finding must reproduce in an official Mozilla release. Nonstandard `about:config` or operating-system changes usually receive no or reduced reward. Latest supported Release/Beta/ESR findings can sometimes qualify even if Nightly changed incidentally. Mere denial of service generally does not qualify; minor information leaks and many spoofing cases do not reach the ordinary paid threshold.

**Direct component precedent:** [Bugzilla 2055885, comment 19](https://bugzilla.mozilla.org/show_bug.cgi?id=2055885#c19) explicitly denied a PDF.js bounty because the chain was already broken in Firefox and the standalone web-hosted PDF.js version was outside coverage. This is a policy decision about a known issue, not a new hypothesis to investigate. It makes official-Firefox reproduction a prerequisite before treating any PDF.js candidate as payment-eligible. Repository ownership alone does not establish bounty scope.

## AI-assisted reporting

[Bugzilla etiquette](https://bugzilla.mozilla.org/page.cgi?id=etiquette.html) explicitly permits AI-assisted preparation. The human submitter remains responsible for accurate, concise content reflecting their own understanding; assisted material must be reviewed and verified before submission. No explicit AI-label/disclosure requirement was found in the consulted client policy, general policy, FAQ, or etiquette. Record assistance honestly in our evidence and require actual human review before any account-based submission; do not claim that review already happened.

## Historical payment evidence

[Mozilla's April 23, 2020 Firefox bounty retrospective](https://blog.mozilla.org/security/2020/04/23/bug-bounty-2019-and-future/) reports **$965,750 paid for 348 bugs during 2017–2019**. This is first-party evidence of historical aggregate payments, not merely advertised maximums. It does not establish individual bank receipt or our payment. Historical rules in that article do not replace current terms.

The [current Firefox bounty hall of fame](https://www.mozilla.org/en-US/security/bug-bounty/hall-of-fame/) reports over $4 million paid across Mozilla's bounties and lists recipients through Q3 2026. The total spans programs and the names do not show individual amounts, release dates, or receipts.

## Practical gaps before submission or income counting

- User-specific age/legal eligibility, Mozilla relationships, and sanctions status are not established by public policy research.
- Current client payment provider, accepted payout methods, fees, tax/identity documents, currency conversion and processing time were not specified in the consulted official client sources. Do not invent a Romanian payout route or promise a net amount.
- Actual supported-build impact, duplicate status, severity, and reward eligibility remain unproven until there is a validated finding and Mozilla assesses it. Public searches cannot reveal private duplicates.
- Bugzilla identity/authentication and the submitter's own review are concrete later dependencies. No account or report has been created.
- Track report submission, awarded amount, released payment and confirmed receipt separately. Current contribution to the $1,000 received-cash goal: **$0**.
