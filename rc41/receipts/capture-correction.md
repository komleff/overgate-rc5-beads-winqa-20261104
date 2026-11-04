# QA capture correction after first STOP

The original H2 invocation used UTF8 decoding with replacement. Its immutable receipt and executed harness are preserved at QA commit c5969ccfd9c287862a07cb3cd2f29555844ec8eb; no original child bytes can be reconstructed from replacement characters.

The local harness now saves stdout/stderr binary files before decoding, hashes those exact streams, and reports the chosen display encoding. This fixes the capture class for future separately authorized commands; it does not alter old receipts, OverGate source or the H2 FAIL. No bootstrap/restore or candidate retry was performed for this correction. Runtime remains HOLD until PM explicitly assigns a diagnostic or a new exact pin.
