$Outlook = New-Object -comobject outlook.application

$n = $Outlook.GetNamespace("MAPI")

$f = $n.GetDefaultFolder(6)

$filepath = "C:\Users\cdurrans\Downloads\Brainware_backups\"

$count = 1

$f.Items | foreach {
    $SendName = $_.SenderName
    if ($SendName = "GSCReports@churchofjesuschrist.org")
    {
        $_.attachments|foreach  {
            Write-Host $_.filename
            $a = $_.filename
            If ($a.Contains(".xlsx"))
            {
                $_.saveasfile((Join-Path $filepath "$a$count.xlsx"))
                $count = $count + 1
            }
            If ($a.Contains(".csv"))
            {
                $_.saveasfile((Join-Path $filepath "$a$count.csv"))
                $count = $count + 1
            }
        }
    }
    
}
exit;