Add-Type -AssemblyName System.Drawing

$bmp = New-Object System.Drawing.Bitmap 256, 256
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::FromArgb(0, 0, 0, 0))

$pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 200, 220, 255), 2)
$g.DrawEllipse($pen, 20, 20, 216, 216)

$bmp.Save("scratch/test_draw.png", [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bmp.Dispose()
Write-Output "Generated scratch/test_draw.png successfully"
