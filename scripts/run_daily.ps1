<#
  run_daily.ps1 — unattended morning runner for the Hawaii airfare + oil tracker.

  Invoked by Windows Task Scheduler. Launches Claude Code headless to execute the
  hawaii-daily-collection skill end to end (outage canary -> collect -> verify gate
  -> commit/push), logging to logs\daily-YYYY-MM-DD.log.

  Unattended runs cannot answer permission prompts, so this passes
  --dangerously-skip-permissions. That lets the run use the flight-search MCP, run
  py scripts, and git push without prompting. Only register the scheduled task if
  you accept that trade-off for this project.

  Manual test:  powershell -ExecutionPolicy Bypass -File scripts\run_daily.ps1
#>

$ErrorActionPreference = 'Stop'

$Project = 'C:\Users\acarr\OneDrive\Documents\Claude\Projects\hawaii-airfare-tracker'
$Claude  = 'C:\Users\acarr\AppData\Roaming\npm\claude.cmd'
$NpmDir  = 'C:\Users\acarr\AppData\Roaming\npm'

# Ensure the npm-global shims (claude, node) resolve under Task Scheduler's PATH.
if ($env:Path -notlike "*$NpmDir*") { $env:Path = "$NpmDir;$env:Path" }

$LogDir = Join-Path $Project 'logs'
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Today  = Get-Date -Format 'yyyy-MM-dd'
$LogFile = Join-Path $LogDir "daily-$Today.log"

$Prompt = @'
Run today's Hawaii airfare + WTI oil collection by following the hawaii-daily-collection skill EXACTLY. Steps: read the skill's RUN_LOG.md first; do the Step 1 outage canary (one JFK->LAX trunk search) before the full batch; if the flight-search MCP is down (success:true / count:0 on every route), take the oil-only degraded path and stop; otherwise collect every live corridor x target_date combo, aggregate, run collect_data.py, build_dashboard.py, then run scripts/verify_collection.py as the gate and act on its exit code (0 commit "Daily collection", 2 commit "Daily update ... (oil only; ...)", 1 do NOT push — fix or log). Append a one-line RUN_LOG.md entry at the end. Work fully autonomously; do not ask for confirmation.
'@

Set-Location $Project
"=== run_daily.ps1 start $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Out-File -FilePath $LogFile -Append -Encoding utf8

& cmd /c "`"$Claude`" -p `"$Prompt`" --dangerously-skip-permissions" *>> $LogFile
$code = $LASTEXITCODE

"=== run_daily.ps1 end   $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') exit=$code ===" | Out-File -FilePath $LogFile -Append -Encoding utf8
exit $code
