# Course explanation refresh: content and release review

Prepared 2026-11-07 (Asia/Taipei). Review branch; not a production publication.

## Scope

Five localized homepages, five new guides, five existing press kits, shared
navigation, localized social cards, canonical/language metadata and indexing.
Native code, App Store metadata, privacy-policy substance, domain and hosting
are outside this change. No analytics or external font requests were added.

The local website checkout was behind the deployed website. Implementation starts
from remote `main` at `c919af3`, not the older local `1712376` checkout.

## Content evidence

RunCraft's registered specifications govern the proposed behavior. The following
are source document names in the native application repository, not website
implementation specifications:

- `docs/spec/RUNNER_CAPABILITY_AND_PLAN_SELECTION_SPEC.md`: goal metadata is
  independent of course creation; background reuse is attributed, preparation
  requirements remain independent, and book/source-family names stay internal.
- `docs/spec/TRAINING_SOURCE_FIDELITY_SPEC.md`: RF-HRV-01 and RF-SAME-DAY-01
  separate descriptive observations from replacement-workout prescriptions.
- `docs/spec/TODAY_OVERVIEW_SPEC.md`: dated observations and actual planned work;
  missing data does not become a positive readiness assessment.
- `docs/spec/FUTURE_COURSE_REPLANNING_SPEC.md`: explicit next-course choices,
  preserved history and independent return/recovery review.
- `docs/spec/PRICING.md`: trial starts at first App Store acquisition, Free Mode
  does not allow new RunCraft recordings, and Lifetime is a non-subscription
  purchase. Historical training comparisons are superseded by source fidelity.
- `docs/research/TESTFLIGHT_64_RELEASE_CHECKPOINT_20261106.md` and release notes:
  1.1.1 (64) was distributed through TestFlight. Saving race metadata separately
  from course arrangement is in this candidate; saved VDOT reuse does not invent
  performance provenance.

The last direct Taiwan storefront observation in the planning audit, 2026-11-06,
showed 1.0.6. It was not reverified during this implementation. Build 64 evidence
is not proof of App Store availability or physical-device acceptance.

## Claim decisions

| Public subject | Action | Replacement meaning |
| --- | --- | --- |
| Adaptive-coach identity | Replace | Plans, pace guidance, guided execution and explicit review |
| Automatic recovery-day adjustment | Remove | Dated observations provide context and caution |
| Health signal calculates an Easy replacement | Remove | No automatic replacement dose or readiness clearance |
| ACWR predicts injury; universal 80/20 | Remove | No injury prediction or universal intensity quota |
| Automatic fitness/pace progression | Replace | Performance-informed pace guidance; predictions are estimates |
| Race date immediately creates a suitable course | Replace | Save the goal; separately review supported course requirements |
| Source table/color/advanced-family names | Omit | Ordinary runner language; no copied source tables or endorsement |
| Free running vs free tier | Clarify | RunCraft recording needs trial/Lifetime; imports/history remain free |
| Purchase-only press price | Replace | Free download, trial and optional Lifetime; no invented discount |
| Blanket cloud-health statement | Narrow | On-device processing, selected private iCloud records, optional exports |

The retained founder biography is personal history, not evidence of a released
adaptive training feature. Existing privacy-policy pages were not rewritten.

## Assets

Retained live-workout and Watch screenshots are existing deterministic product
assets from the website baseline. They illustrate recording/guidance, not the
new goal-creation flow or completion of native device acceptance. They have not
been recaptured as build-64 screenshots in this task.

Remove `plan.png`, `coaching.png`, `recovery.png` and `insights.png` from press
promotion to avoid carrying legacy planning/automatic-adjustment depictions into
the new story. Existing asset URLs remain on disk for compatibility. No updated
page references the retired adjustment images. Social cards use localized type
and the real app icon, with no legacy plan screenshot or scientific guarantee.

## Validation

Executed against the implementation on 2026-11-07:

- Static validation: all five locale schemas, 15 pages, 465 local references,
  canonical/language links, retired-claim checks and reproducible generation pass.
- Browser layouts: 15 pages × four widths (375, 430, 768, 1440), 60 checks pass
  without horizontal overflow, failed images or page JavaScript errors.
- axe: 30 WCAG A/AA audits on narrow and wide layouts, zero reported violations.
  Automated checks do not establish complete accessibility conformance.
- All five languages: dialog focus entry/wrap/return, Escape, anchor navigation,
  resize dismissal, scroll unlocking, language disclosure and FAQ pass.
- Guide language switching, saved-language redirects, unknown-language handling,
  reduced motion and no-JavaScript reading/FAQ pass.
- Traditional Chinese desktop and mobile screenshots visually inspected.
- JavaScript syntax and `git diff --check` pass. Native app tests are not relevant
  to this website-only change and were not run.

The first browser run exposed a resize-assertion timing issue in the test;
waiting for the actual resize handler resolved it. The first complete axe run
found inline links distinguishable only by color; underlined inline links fixed
the finding. Final checks were rerun successfully.

## Publication conditions

1. Recheck the actual production version before merging/deploying. Candidate-only
   goal/setup/continuity claims must not be advertised as available in an older
   App Store binary. Keep this branch in review until the matching release.
2. Confirm native course coverage and current app wording on the release candidate.
   Do not infer full distance/family coverage from a successful website build.
3. Review Japanese and Korean editorial terminology with a fluent reader before
   broad publication. Structure and intended feature boundaries are synchronized;
   automated checks are not a substitute for language review.
4. If new native course screenshots are added, capture the released workflow with
   nonpersonal fixtures and record build, locale and scope. Do not reuse retired
   adjustment screenshots to imply the new course logic.
5. Run the checks again after any subsequent content change. Merge/publication,
   App Store submission and storefront release remain separate from this review.

No traffic baseline, conversion result, field Watch latency result or new native
screenshot coverage is claimed by this website review.
