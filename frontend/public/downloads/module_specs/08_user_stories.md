# Akki — User Stories

This document captures what each user can do or achieve within Akki, organized by module. Each story follows the format: *As a \[role\], I can \[action\], so that \[benefit\].*

## Connect

-   As a **DPO**, I can complete or review the organization’s Setup form, so that our governance rules and data sources are accurately declared before anything goes live.
-   As a **DPO**, I can edit any Setup field before signing off, so that mistakes are corrected without triggering unnecessary governance overhead.
-   As a **DPO**, I can sign off and lock the configuration, so that the organization’s initial state becomes permanent and provable.
-   As a **DPO**, I can add a new source after sign-off, so that the estate can grow without re-triggering the full setup ceremony.
-   As a **Data Engineer**, I can connect each declared source and test the connection, so that only verified, working sources count toward the estate.
-   As a **Data Engineer**, I can review and correct a database’s mapping sample, so that the system reads our data correctly before anything is measured against it.
-   As a **Data Engineer**, I can retry a failed connection, so that a temporary issue doesn’t block a source indefinitely.

## Registry

-   As **any user**, I can view “What You Hold,” so that I understand what our estate actually contains, not just what was declared.
-   As **any user**, I can check “how this was measured” for any figure, so that I trust the number instead of taking it on faith.
-   As **any user**, I can drill into a Source Profile, so that I can inspect one source’s composition and quality in detail.
-   As **any user**, I can browse “What This Estate Can Do,” so that I discover opportunities the estate supports before committing to any work.
-   As a **Data Engineer or DPO**, I can trigger a census manually, so that I get updated numbers immediately rather than waiting for the automatic refresh.
-   As **any user**, I can see when a census was auto-triggered and why, so that I understand why the numbers just changed.

## Extract

-   As an **Analyst**, I can shape an objective from an opportunity or from scratch, so that I turn a business need into a scoped, priced piece of work.
-   As an **Analyst**, I can see a plan preview and sample results before committing, so that I know the cost and coverage before anything is spent.
-   As an **Analyst**, I can save an objective as a draft at any stage, so that I don’t lose progress if I need to step away.
-   As an **Analyst**, I can view a formal quote with price, validity, and cancellation terms, so that I know exactly what I’m agreeing to before I commission the run.
-   As a **Run/Commission Approver**, I can approve or return a commissioned objective, so that nothing runs without a human check.
-   As an **Analyst**, I can track a running objective’s progress and see quarantined batches, so that I know honestly how the work is going, including its problems.
-   As an **Analyst**, I can extend an objective’s scope, so that I can grow the work without losing the original run’s history.
-   As an **Analyst**, I can cancel a running objective, so that I can stop work that’s no longer needed without justifying myself.
-   As a **Model Acceptor**, I can review a model’s six-check scorecard and accept or reject it, so that only models that measurably work get used.
-   As a **Model Acceptor**, I can resubmit a rejected model as a new version, so that improvement work isn’t wasted and stays linked to its history.
-   As **any user**, I can browse Extracted Intel, so that I know what artifacts the organization has produced and can find them again.
-   As an **Analyst**, I can attempt to export or integrate an artifact, so that I can get the rights decision at the point I actually need the data, not before.

## Govern

-   As a **DPO**, I can view The DPO’s Estate, so that I have provable evidence governance is actually working, not just configured.
-   As a **DPO**, I can run test packs after a rule change, so that I can prove each rail still fires correctly before signing the go-live record.
-   As a **DPO**, I can propose a rule change and see it move through counter-signature and a waiting period, so that no rule changes silently or unilaterally.
-   As a **DPO**, I can cancel a rule change before it applies, so that I can catch a mistake before it takes effect.
-   As a **DPO**, I can request a data deletion under dual approval, so that nothing sensitive is destroyed without a second check.
-   As a **DPO**, I can review a quarantined batch and its evidence, so that I can decide whether it should proceed or stay blocked.
-   As a **DPO**, I can review items in the Release Review queue, so that nothing leaves the organization without my explicit approval.
-   As a **DPO**, I can view and edit governance waiting periods, so that I can tune how much deliberation time each type of change requires.
-   As a **DPO**, I can initiate a Governance Co-Signer or Sponsor succession with the required attestations, so that changing who holds this authority is never a single person’s unilateral decision.

## Prove

-   As **any user**, I can ask the estate a question in plain language, so that I get answers grounded in verified fact instead of guesswork.
-   As **any user**, I can see exactly why an answer can’t be given, so that I know whether more extraction would help or the evidence simply doesn’t support it.
-   As **any user**, I can queue an extraction gap directly from a question, so that a “we don’t know yet” becomes a tracked next step instead of a dead end.
-   As **any user**, I can walk a proof through its reasoning and raw evidence, so that I can defend the answer to someone else without taking my word for it.
-   As **any user**, I can draft a memo from an answer, so that I can hand a finding to someone outside the conversation with its proof intact.
-   As a **DPO**, I can review external-bound memos before release, so that nothing leaves the organization without a final check.
-   As a **DPO**, I can generate a public, no-login receipt link, so that an auditor or regulator can independently verify a claim themselves.
-   As a **DPO**, I can revoke a public receipt link, so that I retain control over what stays externally accessible.

## Team

-   As a **Master Admin**, I can invite a new user with a specific role, so that the right people get access without me manually configuring permissions.
-   As a **Master Admin**, I can view every user’s role and status in one table, so that I always know who currently has access.
-   As a **Master Admin**, I can deactivate or reassign a user’s role, so that access stays current as people’s responsibilities change.
-   As a **DPO**, I can approve or return a Master Admin promotion request, so that the most powerful role in the product is never granted without my review.

## Shared / Cross-Cutting

-   As **any user**, I can open Ask Akki from any screen, so that I can get a quick, in-context answer without losing my place in what I was doing.
-   As **any user**, I can receive notifications for approvals and time-sensitive events, so that I never miss something that’s blocking my own or someone else’s work.
