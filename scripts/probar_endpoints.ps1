Param(
  [string]$BaseUrl = 'http://127.0.0.1:8000',
  [Parameter(Mandatory=$true)][string]$Username,
  [Parameter(Mandatory=$true)][string]$Password
)

$api = "$BaseUrl/api"

$tokenResp = Invoke-RestMethod -Method Post -Uri "$api/token/" -ContentType 'application/json' -Body (@{ username=$Username; password=$Password } | ConvertTo-Json)
$access = $tokenResp.access
$headers = @{ Authorization = "Bearer $access" }

Write-Output "Listando libros"
$list1 = Invoke-RestMethod -Method Get -Uri "$api/libros/" -Headers $headers
Write-Output ($list1 | ConvertTo-Json -Depth 5)

$nuevo = @{ titulo='El Quijote'; autor='Miguel de Cervantes'; anio_publicacion=1605; categoria='Novela'; disponible=$true } | ConvertTo-Json
Write-Output "Creando libro"
$created = Invoke-RestMethod -Method Post -Uri "$api/libros/" -Headers $headers -ContentType 'application/json' -Body $nuevo
Write-Output ($created | ConvertTo-Json -Depth 5)
$id = $created.id

Write-Output "Detalle libro"
$detail = Invoke-RestMethod -Method Get -Uri "$api/libros/$id/" -Headers $headers
Write-Output ($detail | ConvertTo-Json -Depth 5)

$actualizado = @{ titulo='El Quijote (Edición Revisada)'; autor='Miguel de Cervantes'; anio_publicacion=1605; categoria='Novela'; disponible=$true } | ConvertTo-Json
Write-Output "Actualizando libro"
$updated = Invoke-RestMethod -Method Put -Uri "$api/libros/$id/" -Headers $headers -ContentType 'application/json' -Body $actualizado
Write-Output ($updated | ConvertTo-Json -Depth 5)

Write-Output "Eliminando libro"
Invoke-RestMethod -Method Delete -Uri "$api/libros/$id/" -Headers $headers
Write-Output "Eliminado"

Write-Output "Confirmando 404"
try {
  $again = Invoke-RestMethod -Method Get -Uri "$api/libros/$id/" -Headers $headers -ErrorAction Stop
  Write-Output ($again | ConvertTo-Json -Depth 5)
} catch {
  Write-Output "404 OK"
}
