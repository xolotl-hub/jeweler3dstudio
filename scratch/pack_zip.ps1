$root = Split-Path $PSScriptRoot -Parent

$dist = Join-Path $root "dist"
New-Item -ItemType Directory -Force -Path $dist | Out-Null
$zipPath = Join-Path $dist "jeweler3dstudio-0.1.0.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$excludeDirs = @('__pycache__', '.git', '.agents', '.skill', 'overview', 'dist', '.pytest_cache', '.vscode', '.idea')
$excludeExt = @('.pyc', '.pyo', '.pyd', '.DS_Store')
$excludePrefixes = @('assets/gems/dark/', 'assets/gems/light/', 'assets/gems/svg/', 'assets/gems/styles/')
$excludeNames = @('round_v2.png', 'round_v2.svg')
$includes = @('blender_manifest.toml', '__init__.py', 'core', 'ui', 'assets', 'LICENSE')

$count = 0
$bytes = 0L

$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($item in $includes) {
        $path = Join-Path $root $item
        if (-not (Test-Path $path)) {
            Write-Host "skip missing: $item"
            continue
        }

        if (Test-Path $path -PathType Leaf) {
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $path, $item) | Out-Null
            $count++
            $bytes += (Get-Item $path).Length
            Write-Host "  + $item"
            continue
        }

        Get-ChildItem -Path $path -Recurse -File | ForEach-Object {
            $rel = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
            if ($rel.Split('/') | Where-Object { $excludeDirs -contains $_ }) { return }
            if ($excludeExt -contains $_.Extension.ToLower()) { return }
            if ($_.Name.StartsWith('.')) { return }
            if ($excludeNames -contains $_.Name) { return }
            foreach ($prefix in $excludePrefixes) {
                if ($rel.StartsWith($prefix)) { return }
            }

            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $rel) | Out-Null
            $count++
            $bytes += $_.Length
            Write-Host "  + $rel"
        }
    }
}
finally {
    $zip.Dispose()
}

Write-Host ""
Write-Host "OK $count files $([math]::Round($bytes / 1KB, 1)) KB -> $zipPath"
