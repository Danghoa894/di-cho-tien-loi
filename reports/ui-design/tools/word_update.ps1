param([string]$Docx, [string]$Pdf)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.Open($Docx, $false, $false)
  $doc.Fields.Update() | Out-Null
  foreach ($t in $doc.TablesOfContents) { $t.Update() | Out-Null }
  foreach ($t in $doc.TablesOfFigures) { $t.Update() | Out-Null }
  $doc.Fields.Update() | Out-Null
  foreach ($t in $doc.TablesOfContents) { $t.Update() | Out-Null }
  foreach ($t in $doc.TablesOfFigures) { $t.Update() | Out-Null }
  $doc.Save()
  $pages = $doc.ComputeStatistics(2)
  $doc.ExportAsFixedFormat($Pdf, 17)
  $doc.Close($false)
  Write-Output "pages=$pages"
} finally {
  $word.Quit()
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
