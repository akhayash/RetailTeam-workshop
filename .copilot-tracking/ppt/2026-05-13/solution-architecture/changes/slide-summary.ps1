$root = 'c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content'
$slides = Get-ChildItem -Path $root -Directory -Filter 'slide-*' | Sort-Object Name
$rows = foreach ($s in $slides) {
    $yaml = Get-Content -Path (Join-Path $s.FullName 'content.yaml') -Raw
    $hasNotes = $yaml -match 'speaker_notes:'
    if ($yaml -match 'layout:\s*(.+)') { $layout = $Matches[1].Trim() } else { $layout = '(none)' }
    $imgCount = 0
    $imagesPath = Join-Path $s.FullName 'images'
    if (Test-Path $imagesPath) {
        $imgCount = (Get-ChildItem $imagesPath -File -ErrorAction SilentlyContinue).Count
    }
    [pscustomobject]@{
        Slide        = $s.Name
        Layout       = $layout
        SpeakerNotes = $hasNotes
        Images       = $imgCount
    }
}
$rows | Format-Table -AutoSize
