Param(
  [string]$BaseUrl = 'http://127.0.0.1:8000',
  [Parameter(Mandatory=$true)][string]$Username,
  [Parameter(Mandatory=$true)][string]$Password,
  [string]$Q = ''
)

$api = "$BaseUrl/api"
$body = @{ username=$Username; password=$Password } | ConvertTo-Json
$tokenResp = Invoke-RestMethod -Method Post -Uri "$api/token/" -ContentType 'application/json' -Body $body
$access = $tokenResp.access
$headers = @{ Authorization = "Bearer $access" }

if ($Q -and $Q.Trim().Length -gt 0) {
  $url = "$api/libros/?q=$([uri]::EscapeDataString($Q))"
} else {
  $url = "$api/libros/"
}

$list = Invoke-RestMethod -Method Get -Uri $url -Headers $headers
Write-Output ($list | ConvertTo-Json -Depth 5)
