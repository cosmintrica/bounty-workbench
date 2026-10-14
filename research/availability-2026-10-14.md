# Availability decisions — October 14, 2026

These are dated screening decisions, not submissions, awards or payments.

## Gitpay: no open publicly listed task carrying a bounty

The public catalogue was read through its normal listing endpoint, following the
pagination used by its public source. The two pages in `gitpay-public-catalog.json`
contain **189 unique tasks**, matching the reported total. All 189 have status
`closed`. The separate open-status query in `gitpay-open-funded-catalog.json`
reports zero results. This rules out selecting a currently available task from
that catalogue at the recorded check; it does not describe private tasks or future
listings, and does not establish that the platform is inactive.

- [Public bounty catalogue](https://gitpay.me/tasks/list?hasBounty=true&sortBy=value&sortDirection=desc&limit=100&page=0)
- [Public open bounty query](https://gitpay.me/tasks/list?hasBounty=true&status=open&sortBy=value&sortDirection=desc&limit=100&page=0)
- [Official claims workflow](https://docs.gitpay.me/docs/en/claims/)

Amounts and successful sponsor funding orders are not evidence of payment to a
contributor. Current policy research is in `gitpay-policy-check.md`; Romania is
listed by the payout provider, but no account verification or confirmed assignment
exists. **Decision: do not implement an old closed task or request an account for
an unavailable reward.**

## Artifex: linked program is suspended

The current [official developer bounty page](https://artifex.com/developers-bug-bounty-program)
is dated April 7, 2026 and says its website-properties program is suspended pending
review. Ghostscript's older bounty page links there. This does not verify an active
cash programme for Ghostscript code fixes. **Decision: do not rely on old reward
announcements; no implementation or testing selected from this lead.**

## OpenProject: sponsored programme ended

The [official announcement](https://www.openproject.org/blog/bug-bounty-program-yes-we-hack/)
has an explicit June 2026 update saying the European Commission-sponsored programme
ended. Its older €100–€5,000 schedule remains visible farther down the same page;
that historical schedule does not establish a current reward. **Decision: reject
this programme as a currently funded opportunity.**

## Accounting and next action

No work was claimed, submitted or implemented for these leads. No sponsor was
contacted. Submissions: 0; confirmed awards: $0; confirmed receipts: $0. Continue
with different programmes whose current official rules establish both availability
and a monetary reward before substantial implementation.
