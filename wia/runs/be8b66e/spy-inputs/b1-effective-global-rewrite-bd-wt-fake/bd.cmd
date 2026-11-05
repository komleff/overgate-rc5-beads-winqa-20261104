@echo off
if "%~1"=="--version" (
echo version >> "D:\CodexArtifacts\overgate-rc5-wia-be8b66e-winqa-20261105\cases\b1\b1-effective-global-rewrite-bd-wt-fake\version.log"
echo bd version 1.2.2 ^(synthetic^)
exit /b 0
)
echo %* >> "D:\CodexArtifacts\overgate-rc5-wia-be8b66e-winqa-20261105\cases\b1\b1-effective-global-rewrite-bd-wt-fake\forbidden.log"
exit /b 93
