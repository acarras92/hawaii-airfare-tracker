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

$Project   = 'C:\Users\acarr\OneDrive\Documents\Claude\Projects\hawaii-airfare-tracker'
$Claude    = 'C:\Users\acarr\AppData\Roaming\npm\claude.cmd'
$NpmDir    = 'C:\Users\acarr\AppData\Roaming\npm'
# Load ONLY the flight-search MCP, explicitly. Project-scoped servers are otherwise
# "pending approval" and unreliable in headless -p runs; --strict-mcp-config makes
# the morning run deterministic regardless of approval-state drift.
$McpConfig = Join-Path $Project 'scripts\flight-search.mcp.json'

# Ensure the npm-global shims (claude, node) resolve under Task Scheduler's PATH.
if ($env:Path -notlike "*$NpmDir*") { $env:Path = "$NpmDir;$env:Path" }

$LogDir = Join-Path $Project 'logs'
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Today  = Get-Date -Format 'yyyy-MM-dd'
$LogFile = Join-Path $LogDir "daily-$Today.log"

$Prompt = @'
Invoke the hawaii-daily-collection skill (via the Skill tool) to load its full SKILL.md, then execute today's Hawaii airfare + WTI oil collection EXACTLY as it specifies. Key points: read the skill's RUN_LOG.md first; do the Step 1 outage canary (one JFK->LAX trunk search) before the full batch; if the flight-search MCP is down (success:true / count:0 on every route), take the oil-only degraded path and stop; otherwise collect every live corridor x target_date combo, aggregate, run collect_data.py, build_dashboard.py, then run scripts/verify_collection.py as the gate and act on its exit code (0 -> commit "Daily collection YYYY-MM-DD"; 2 -> commit "Daily update YYYY-MM-DD (oil only; ...)"; 1 -> do NOT push, fix or log). Append a one-line RUN_LOG.md entry at the end. Work fully autonomously; do not ask for confirmation.
'@

Set-Location $Project
"=== run_daily.ps1 start $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Out-File -FilePath $LogFile -Append -Encoding utf8

& cmd /c "`"$Claude`" -p `"$Prompt`" --strict-mcp-config --mcp-config `"$McpConfig`" --dangerously-skip-permissions < NUL" *>> $LogFile
$agentCode = $LASTEXITCODE

# Claude's own exit code is NOT a reliable signal: on 2026-07-24 it exited 0 having
# collected 2 of 50 combos, because it left the batch running in the background and
# the session ended when this process returned. Re-verify the data independently and
# report THAT as the task's result, so Task Scheduler's LastTaskResult tells the truth.
#   0 = full collection   2 = oil-only (flight-search outage)   1 = failed
$verifyOut  = & cmd /c "py `"$Project\scripts\verify_collection.py`" 2>&1"
$verifyCode = $LASTEXITCODE
$verifyOut | Out-File -FilePath $LogFile -Append -Encoding utf8

$verdict = switch ($verifyCode) {
    0       { 'PASS (flights + oil)' }
    2       { 'OIL-ONLY (no flights stored today)' }
    default { 'FAIL (verify gate rejected today''s data)' }
}
"=== verify: exit=$verifyCode $verdict (agent exit=$agentCode) ===" | Out-File -FilePath $LogFile -Append -Encoding utf8

"=== run_daily.ps1 end   $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') exit=$verifyCode ===" | Out-File -FilePath $LogFile -Append -Encoding utf8
exit $verifyCode
