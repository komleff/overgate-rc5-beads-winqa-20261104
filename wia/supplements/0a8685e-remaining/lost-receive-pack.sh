#!/bin/sh
git receive-pack "$@"
qa_rc=$?
if [ "$qa_rc" -eq 0 ]; then
  printf "receive-pack succeeded; forced transport exit73\n" >> D:/CodexArtifacts/overgate-rc5-wia-0a8685e-winqa-20261105/run-0a8685e/lost-receive-pack.trace
  git --git-dir="$1" rev-parse refs/heads/beads-backup >> D:/CodexArtifacts/overgate-rc5-wia-0a8685e-winqa-20261105/run-0a8685e/lost-receive-pack.trace
  exit 73
fi
exit "$qa_rc"
