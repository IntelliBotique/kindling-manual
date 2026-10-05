# Kindling rewrites, gated October 4, 2026

The ten rewrites (K-3.5 to K-8.5) passed the Field Manual lane's gate and are ready to wire on manual.kindling.foundation as written.

## What the gate did
- **Independent check.** Two readers who had not seen the writing went through all ten chapters. The writing session had confirmed only that each cited spec section exists; the readers checked that each section says what the draft claims. They also re-matched 313 quotations against the spec, the master and the live sites, recomputed every worked example, and checked the law against official pages. They found 35 problems and fixed 33. The full log is in CHECK_LOG.md.
- **The fixes that mattered:**
  - **K-4.7 (state privacy law).** Connecticut's amended law, from July 1, 2026, covers anyone processing sensitive data at any volume, and a peer-support Pool is that case. It is now stated. The chapter's three verify marks were replaced with quoted official text: Virginia's deletion-record rule, California's right-to-delete exceptions, Washington's My Health My Data Act, the FTC health-breach rule, and the sensitive-data definitions. Whether a given Pool is covered stays a question for counsel, and the chapter says so.
  - **K-4.3 (handovers).** Consent proofs do not "move with the manifest." The spec makes the proof a reference to the handshake response. The handover table now says so.
  - **K-3.7.** It had read §1.3 as a ban. It now treats §1.3 as a non-goal, as K.1 does.
  - **K-3.6.** It contradicted itself on whether Mycelial is real. Fixed.
  - **K-8.5.** The "call an attorney first" step for breach-notice law was restored from the master.
  - **K-6.3.** An unsourced sentence about state grant programs was removed.
  - **K-4.8.** Threshold is no longer called a hosting desk; its site says it "hosts no Pools itself."
  - **K-7.1.** Leaving a Pool out of the well-known file is the library's habit, not a spec rule.
- **Verify marks left: 2, both in K-4.8.** They cover product liability for dinners sold beside a Pool, and how a litigation hold sits beside the 60-second withdrawal. No official source answers either, so both stay marked.
- **Not updated.** RESEARCH_README.md and the research session's ledger describe the drafts before the gate; CHECK_LOG.md lists every change since. The ledger itself is not in this folder.

## For the build
- **xrefs.md** lists the wiring changes. Its one trap: each draft carries its own "Figures checked" line, so the build must not stamp a second one.
- **Numbering.** The ten keep their source numbers with a K- prefix, so every "Ch 3.6" in K.1 to K.4 points at its rewrite.

## For the master (handled by the lane)
- **8.5.** The broken "see Vols 4 and 13–15" is corrected to "Vols 4 and 13."
- **4.8, workers' comp.** Not applied. The proposed line repeats a ruling that Volume 13's own state entries contradict; about a dozen states start at three to five employees. This is Josh's decision.
