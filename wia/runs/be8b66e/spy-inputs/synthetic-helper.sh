#!/bin/sh
printf "%s\n" "$1" >> "D:/CodexArtifacts/overgate-rc5-wia-be8b66e-winqa-20261105/cases/b2-auth/synthetic-helper.log"
if [ "$1" = get ]; then printf "username=windows-qa\npassword=synthetic-test-only\n"; fi
