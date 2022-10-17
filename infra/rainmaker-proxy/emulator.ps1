# Clear cache of powershell in order to solve Azurite stuck problems. Unitil now, it works.
Remove-Variable * -ErrorAction SilentlyContinue; Remove-Module *; $error.Clear(); Clear-Host
# Start Azurite blob queue and table in three new ports.
azurite --blobPort 20000 --queuePort 20001 --tablePort 20002
