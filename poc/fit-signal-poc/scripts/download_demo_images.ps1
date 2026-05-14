<#
.SYNOPSIS
  Download demo images for the Fit Signal PoC pipeline smoke test.

.DESCRIPTION
  These images verify that the MediaPipe Pose Landmarker pipeline runs end
  to end. They are NOT suitable for fit-signal accuracy validation because
  the subjects are not in an A-pose.

  For real validation, place photos you have explicit consent to use under
  data/raw/front/ and data/raw/side/ (both gitignored).

  Licenses:
    - MediaPipe public assets bucket: Apache-2.0
    - Pixabay: Pixabay Content License (commercial use OK, no attribution
      required)
#>

[CmdletBinding()]
param(
  [string]$Root = (Resolve-Path "$PSScriptRoot/..").Path
)

$ErrorActionPreference = "Stop"

$demoDir = Join-Path $Root "data/raw/_demo"
New-Item -ItemType Directory -Force -Path $demoDir | Out-Null

$samples = @(
  @{
    Name    = "mediapipe_pose_sample.jpg"
    Url     = "https://storage.googleapis.com/mediapipe-assets/pose.jpg"
    License = "Apache-2.0 (MediaPipe sample assets)"
  },
  @{
    Name    = "pixabay_girl_4051811.jpg"
    Url     = "https://cdn.pixabay.com/photo/2019/03/12/20/39/girl-4051811_960_720.jpg"
    License = "Pixabay Content License (commercial use OK, no attribution required)"
  }
)

foreach ($s in $samples) {
  $out = Join-Path $demoDir $s.Name
  if (Test-Path $out) {
    Write-Host "skip (already exists): $($s.Name)"
    continue
  }
  Write-Host "downloading $($s.Name) ..."
  Invoke-WebRequest -Uri $s.Url -OutFile $out -UseBasicParsing
  Write-Host "  saved: $out  [$($s.License)]"
}

Write-Host ""
Write-Host "Done. See data/raw/SOURCES.md for provenance and licenses."
Write-Host "NOTE: Side-view photos are not downloaded automatically."
Write-Host "      Find suitable images yourself (e.g., search 'standing side"
Write-Host "      profile full body' on Pixabay) and place them in data/raw/side/."
