@echo off
if "%~1"=="--version" (
echo version >> "D:\CodexArtifacts\overgate-rc5-wia-be8b66e-winqa-20261105\cases\b1\b1-bootstrap-relative-count-url-fake\version-only.log"
echo bd version 1.2.2 ^(synthetic-version-probe^)
exit /b 0
)
echo %* >> "D:\CodexArtifacts\overgate-rc5-wia-be8b66e-winqa-20261105\cases\b1\b1-bootstrap-relative-count-url-fake\forbidden-call.log"
exit /b 93
