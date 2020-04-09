#this is an example of how to download all files from outlook's main folder (This only downloads .xlsx and .csv but that can be changed) The current implementation deletes the files afterward.

$Outlook = New-Object -comobject outlook.application
$n = $Outlook.GetNamespace("MAPI")

$f = $n.GetDefaultFolder(6);

$filepath = "Y:\SNAndOtherEmailedData\"

$f.Items| foreach
{
  $SendName = $_.SenderName
   $_.attachments|foreach
  {
      Write-Host $_.filename
      $a = $_.filename
    If ($a.Contains(".xlsx"))
      {
        $_.saveasfile((Join-Path $filepath "$a.xlsx"))
      }
    If ($a.Contains(".csv"))
      {
        $_.saveasfile((Join-Path $filepath "$a.csv"))
      }
  }
  $_.Delete()
}
