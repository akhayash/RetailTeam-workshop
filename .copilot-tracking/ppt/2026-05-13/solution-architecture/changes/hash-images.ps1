$paths = @(
    'c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content\slide-006\images\image-01.png',
    'c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content\slide-006\images\image-02.png',
    'c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content\slide-006\images\image-03.png',
    'c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content\slide-008\images\image-01.png',
    'c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content\slide-008\images\image-02.png',
    'c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content\slide-008\images\image-03.png'
)
$rows = foreach ($p in $paths) {
    [pscustomobject]@{
        Slide = (Split-Path (Split-Path $p -Parent) -Parent | Split-Path -Leaf)
        File  = (Split-Path $p -Leaf)
        Size  = (Get-Item $p).Length
        Hash  = (Get-FileHash $p -Algorithm SHA1).Hash
    }
}
$rows | Format-Table -AutoSize
