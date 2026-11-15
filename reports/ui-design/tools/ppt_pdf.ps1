param([string]$Pptx, [string]$Pdf)
$app = New-Object -ComObject PowerPoint.Application
try {
  $p = $app.Presentations.Open($Pptx, $true, $false, $false)
  $p.SaveAs($Pdf, 32)
  Write-Output ("slides=" + $p.Slides.Count)
  $p.Close()
} finally { $app.Quit() }
