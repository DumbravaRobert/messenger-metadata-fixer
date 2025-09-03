$MessagesRoot = "<facebook_export_path>"
$Destination = "<move_destination_path>"                  

if (!(Test-Path -Path $Destination)) {
    New-Item -ItemType Directory -Path $Destination | Out-Null
}


$MessageFolders = @("inbox", "e2ee_cutover", "archived_threads", "filtered_threads", "message_requests")

$MediaFolders = @("photos", "videos", "audio")

foreach ($MsgFolder in $MessageFolders) {
    $RootPath = Join-Path $MessagesRoot $MsgFolder

    if (Test-Path $RootPath) {
        Get-ChildItem -Path $RootPath -Directory -Recurse | Where-Object { $_.Name -in $MediaFolders } | ForEach-Object {
            $FolderType = $_.Name
            $TargetFolder = Join-Path $Destination $FolderType


            if (!(Test-Path -Path $TargetFolder)) {
                New-Item -ItemType Directory -Path $TargetFolder | Out-Null
            }

            Get-ChildItem -Path $_.FullName -File | ForEach-Object {
                $DestFile = Join-Path $TargetFolder $_.Name


                if (Test-Path $DestFile) {
                    $NewName = "{0}_{1}{2}" -f ($_.BaseName), (Get-Random -Maximum 99999), $_.Extension
                    $DestFile = Join-Path $TargetFolder $NewName
                }

                Move-Item -Path $_.FullName -Destination $DestFile
            }
        }
    }
}