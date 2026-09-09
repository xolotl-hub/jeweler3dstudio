Add-Type -AssemblyName System.Drawing

$darkDir = "assets/gems/dark"
$lightDir = "assets/gems/light"
$svgDir = "assets/gems/svg"

if (-not (Test-Path $darkDir)) { New-Item -ItemType Directory -Path $darkDir -Force | Out-Null }
if (-not (Test-Path $lightDir)) { New-Item -ItemType Directory -Path $lightDir -Force | Out-Null }
if (-not (Test-Path $svgDir)) { New-Item -ItemType Directory -Path $svgDir -Force | Out-Null }

function Draw-Sparkle {
    param($g, [float]$cx, [float]$cy, [float]$size, [bool]$isDark)
    $sparkleColor = if ($isDark) { [System.Drawing.Color]::FromArgb(240, 255, 255, 255) } else { [System.Drawing.Color]::FromArgb(200, 255, 255, 255) }
    $brush = New-Object System.Drawing.SolidBrush($sparkleColor)
    
    [System.Drawing.PointF[]]$pts = @(
        (New-Object System.Drawing.PointF($cx, ($cy - $size))),
        (New-Object System.Drawing.PointF(($cx + $size*0.2), ($cy - $size*0.2))),
        (New-Object System.Drawing.PointF(($cx + $size), $cy)),
        (New-Object System.Drawing.PointF(($cx + $size*0.2), ($cy + $size*0.2))),
        (New-Object System.Drawing.PointF($cx, ($cy + $size))),
        (New-Object System.Drawing.PointF(($cx - $size*0.2), ($cy + $size*0.2))),
        (New-Object System.Drawing.PointF(($cx - $size), $cy)),
        (New-Object System.Drawing.PointF(($cx - $size*0.2), ($cy - $size*0.2)))
    )
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddPolygon($pts)
    $g.FillPath($brush, $path)
    $path.Dispose()
    $brush.Dispose()
}

function Render-GemIcon {
    param(
        [string]$name,
        [scriptblock]$drawGeometry,
        [string]$svgContent
    )
    
    # Save SVG
    $svgFile = Join-Path $svgDir "$name.svg"
    [System.IO.File]::WriteAllText($svgFile, $svgContent)

    # Render Dark & Light PNGs
    foreach ($isDark in @($true, $false)) {
        $bmp = New-Object System.Drawing.Bitmap 256, 256
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.Clear([System.Drawing.Color]::FromArgb(0, 0, 0, 0))

        & $drawGeometry $g $isDark

        $outDir = if ($isDark) { $darkDir } else { $lightDir }
        $outFile = Join-Path $outDir "$name.png"
        $bmp.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)

        $g.Dispose()
        $bmp.Dispose()
    }
    Write-Output "Generated icon: $name"
}

# Color palettes
function Get-Colors {
    param([bool]$isDark)
    if ($isDark) {
        return @{
            LinePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(230, 210, 235, 255), 2.5)
            ThinPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(180, 160, 200, 245), 1.5)
            TableBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(80, 80)),
                (New-Object System.Drawing.PointF(180, 180)),
                [System.Drawing.Color]::FromArgb(230, 225, 245, 255),
                [System.Drawing.Color]::FromArgb(160, 100, 150, 210)
            )
            FacetBrush1 = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(40, 40)),
                (New-Object System.Drawing.PointF(220, 220)),
                [System.Drawing.Color]::FromArgb(190, 180, 220, 255),
                [System.Drawing.Color]::FromArgb(130, 70, 115, 175)
            )
            FacetBrush2 = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(220, 40)),
                (New-Object System.Drawing.PointF(40, 220)),
                [System.Drawing.Color]::FromArgb(210, 205, 235, 255),
                [System.Drawing.Color]::FromArgb(110, 50, 95, 150)
            )
            BackBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(128, 20)),
                (New-Object System.Drawing.PointF(128, 236)),
                [System.Drawing.Color]::FromArgb(120, 120, 170, 225),
                [System.Drawing.Color]::FromArgb(60, 40, 75, 120)
            )
        }
    } else {
        return @{
            LinePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(240, 30, 45, 70), 2.5)
            ThinPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(180, 60, 80, 110), 1.5)
            TableBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(80, 80)),
                (New-Object System.Drawing.PointF(180, 180)),
                [System.Drawing.Color]::FromArgb(240, 255, 255, 255),
                [System.Drawing.Color]::FromArgb(190, 210, 230, 245)
            )
            FacetBrush1 = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(40, 40)),
                (New-Object System.Drawing.PointF(220, 220)),
                [System.Drawing.Color]::FromArgb(210, 235, 245, 255),
                [System.Drawing.Color]::FromArgb(160, 180, 205, 225)
            )
            FacetBrush2 = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(220, 40)),
                (New-Object System.Drawing.PointF(40, 220)),
                [System.Drawing.Color]::FromArgb(230, 245, 250, 255),
                [System.Drawing.Color]::FromArgb(140, 160, 185, 210)
            )
            BackBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.PointF(128, 20)),
                (New-Object System.Drawing.PointF(128, 236)),
                [System.Drawing.Color]::FromArgb(170, 200, 220, 240),
                [System.Drawing.Color]::FromArgb(120, 145, 175, 200)
            )
        }
    }
}

# 1. ROUND
Render-GemIcon "round" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $cx = 128; $cy = 128; $r = 96
    
    # Outer circle
    $g.FillEllipse($c.BackBrush, ($cx - $r), ($cy - $r), ($r * 2), ($r * 2))
    $g.DrawEllipse($c.LinePen, ($cx - $r), ($cy - $r), ($r * 2), ($r * 2))
    
    # 16 Girdle points
    $gpts = @()
    for ($i=0; $i -lt 16; $i++) {
        $a = $i * [Math]::PI / 8.0
        $gpts += New-Object System.Drawing.PointF(($cx + $r * [Math]::Cos($a)), ($cy + $r * [Math]::Sin($a)))
    }
    
    # 8 Star points
    $spts = @()
    $sr = $r * 0.72
    for ($i=0; $i -lt 8; $i++) {
        $a = $i * [Math]::PI / 4.0
        $spts += New-Object System.Drawing.PointF(($cx + $sr * [Math]::Cos($a)), ($cy + $sr * [Math]::Sin($a)))
    }

    # 8 Table points
    $tpts = @()
    $tr = $r * 0.52
    for ($i=0; $i -lt 8; $i++) {
        $a = ($i * [Math]::PI / 4.0) + ([Math]::PI / 8.0)
        $tpts += New-Object System.Drawing.PointF(($cx + $tr * [Math]::Cos($a)), ($cy + $tr * [Math]::Sin($a)))
    }

    # Draw star facets & kites
    for ($i=0; $i -lt 8; $i++) {
        $p = New-Object System.Drawing.Drawing2D.GraphicsPath
        $p.AddPolygon(@($tpts[$i], $spts[$i], $tpts[($i+7)%8]))
        $b = if ($i % 2 -eq 0) { $c.FacetBrush1 } else { $c.FacetBrush2 }
        $g.FillPath($b, $p)
        $g.DrawPath($c.ThinPen, $p)
        $p.Dispose()
    }

    # Upper girdle triangles
    for ($i=0; $i -lt 8; $i++) {
        $g.DrawLine($c.ThinPen, $spts[$i], $gpts[$i*2])
        $g.DrawLine($c.ThinPen, $spts[$i], $gpts[($i*2+15)%16])
        $g.DrawLine($c.ThinPen, $spts[$i], $gpts[($i*2+1)%16])
    }

    # Table face
    $tp = New-Object System.Drawing.Drawing2D.GraphicsPath
    $tp.AddPolygon($tpts)
    $g.FillPath($c.TableBrush, $tp)
    $g.DrawPath($c.LinePen, $tp)
    $tp.Dispose()

    Draw-Sparkle $g 80 75 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"><circle cx="128" cy="128" r="96" fill="url(#gemGrad)" stroke="#D0E8FF" stroke-width="3"/></svg>'

# 2. OVAL
Render-GemIcon "oval" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $cx = 128; $cy = 128; $rx = 76; $ry = 104
    
    $g.FillEllipse($c.BackBrush, ($cx - $rx), ($cy - $ry), ($rx * 2), ($ry * 2))
    $g.DrawEllipse($c.LinePen, ($cx - $rx), ($cy - $ry), ($rx * 2), ($ry * 2))
    
    # Table ellipse
    $trx = $rx * 0.52; $try = $ry * 0.52
    $g.FillEllipse($c.TableBrush, ($cx - $trx), ($cy - $try), ($trx * 2), ($try * 2))
    $g.DrawEllipse($c.LinePen, ($cx - $trx), ($cy - $try), ($trx * 2), ($try * 2))

    for ($i=0; $i -lt 8; $i++) {
        $a = $i * [Math]::PI / 4.0
        $x1 = $cx + $trx * [Math]::Cos($a); $y1 = $cy + $try * [Math]::Sin($a)
        $x2 = $cx + $rx * [Math]::Cos($a); $y2 = $cy + $ry * [Math]::Sin($a)
        $g.DrawLine($c.ThinPen, $x1, $y1, $x2, $y2)
    }
    Draw-Sparkle $g 86 68 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"><ellipse cx="128" cy="128" rx="76" ry="104" fill="#B0D0F0" stroke="#FFF" stroke-width="3"/></svg>'

# 3. CUSHION
Render-GemIcon "cushion" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddBezier(55, 45, 128, 30, 128, 30, 201, 45)
    $path.AddBezier(201, 45, 226, 128, 226, 128, 201, 211)
    $path.AddBezier(201, 211, 128, 226, 128, 226, 55, 211)
    $path.AddBezier(55, 211, 30, 128, 30, 128, 55, 45)
    
    $g.FillPath($c.BackBrush, $path)
    $g.DrawPath($c.LinePen, $path)

    # Cushion Table
    $tpath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $tpath.AddPolygon(@(
        (New-Object System.Drawing.PointF(95, 75)),
        (New-Object System.Drawing.PointF(161, 75)),
        (New-Object System.Drawing.PointF(181, 95)),
        (New-Object System.Drawing.PointF(181, 161)),
        (New-Object System.Drawing.PointF(161, 181)),
        (New-Object System.Drawing.PointF(95, 181)),
        (New-Object System.Drawing.PointF(75, 161)),
        (New-Object System.Drawing.PointF(75, 95))
    ))
    $g.FillPath($c.TableBrush, $tpath)
    $g.DrawPath($c.LinePen, $tpath)
    
    $g.DrawLine($c.ThinPen, 75, 95, 55, 45)
    $g.DrawLine($c.ThinPen, 181, 95, 201, 45)
    $g.DrawLine($c.ThinPen, 181, 161, 201, 211)
    $g.DrawLine($c.ThinPen, 75, 161, 55, 211)
    $path.Dispose(); $tpath.Dispose()
    Draw-Sparkle $g 80 70 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 4. EMERALD
Render-GemIcon "emerald" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(75, 40)),
        (New-Object System.Drawing.PointF(181, 40)),
        (New-Object System.Drawing.PointF(216, 75)),
        (New-Object System.Drawing.PointF(216, 181)),
        (New-Object System.Drawing.PointF(181, 216)),
        (New-Object System.Drawing.PointF(75, 216)),
        (New-Object System.Drawing.PointF(40, 181)),
        (New-Object System.Drawing.PointF(40, 75))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    # Step 1
    $step1 = @(
        (New-Object System.Drawing.PointF(85, 58)),
        (New-Object System.Drawing.PointF(171, 58)),
        (New-Object System.Drawing.PointF(198, 85)),
        (New-Object System.Drawing.PointF(198, 171)),
        (New-Object System.Drawing.PointF(171, 198)),
        (New-Object System.Drawing.PointF(85, 198)),
        (New-Object System.Drawing.PointF(58, 171)),
        (New-Object System.Drawing.PointF(58, 85))
    )
    $g.DrawPolygon($c.ThinPen, $step1)

    # Table
    $table = @(
        (New-Object System.Drawing.PointF(96, 78)),
        (New-Object System.Drawing.PointF(160, 78)),
        (New-Object System.Drawing.PointF(178, 96)),
        (New-Object System.Drawing.PointF(178, 160)),
        (New-Object System.Drawing.PointF(160, 178)),
        (New-Object System.Drawing.PointF(96, 178)),
        (New-Object System.Drawing.PointF(78, 160)),
        (New-Object System.Drawing.PointF(78, 96))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    for ($i=0; $i -lt 8; $i++) {
        $g.DrawLine($c.ThinPen, $outer[$i], $table[$i])
    }
    Draw-Sparkle $g 82 65 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 5. PEAR
Render-GemIcon "pear" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddBezier(128, 32, 185, 95, 205, 165, 170, 205)
    $path.AddBezier(170, 205, 128, 228, 128, 228, 86, 205)
    $path.AddBezier(86, 205, 51, 165, 71, 95, 128, 32)
    
    $g.FillPath($c.BackBrush, $path)
    $g.DrawPath($c.LinePen, $path)

    # Table
    $tpath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $tpath.AddBezier(128, 70, 160, 105, 170, 155, 150, 178)
    $tpath.AddBezier(150, 178, 128, 192, 128, 192, 106, 178)
    $tpath.AddBezier(106, 178, 86, 155, 96, 105, 128, 70)
    $g.FillPath($c.TableBrush, $tpath)
    $g.DrawPath($c.LinePen, $tpath)

    $g.DrawLine($c.ThinPen, 128, 32, 128, 70)
    $g.DrawLine($c.ThinPen, 170, 205, 150, 178)
    $g.DrawLine($c.ThinPen, 86, 205, 106, 178)
    $path.Dispose(); $tpath.Dispose()
    Draw-Sparkle $g 128 50 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 6. MARQUISE
Render-GemIcon "marquise" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddBezier(128, 26, 215, 80, 215, 176, 128, 230)
    $path.AddBezier(128, 230, 41, 176, 41, 80, 128, 26)
    $g.FillPath($c.BackBrush, $path)
    $g.DrawPath($c.LinePen, $path)

    $tpath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $tpath.AddBezier(128, 65, 180, 95, 180, 161, 128, 191)
    $tpath.AddBezier(128, 191, 76, 161, 76, 95, 128, 65)
    $g.FillPath($c.TableBrush, $tpath)
    $g.DrawPath($c.LinePen, $tpath)

    $g.DrawLine($c.ThinPen, 128, 26, 128, 65)
    $g.DrawLine($c.ThinPen, 128, 191, 128, 230)
    $g.DrawLine($c.ThinPen, 205, 128, 172, 128)
    $g.DrawLine($c.ThinPen, 51, 128, 84, 128)
    $path.Dispose(); $tpath.Dispose()
    Draw-Sparkle $g 128 45 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 7. PRINCESS
Render-GemIcon "princess" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(40, 40)),
        (New-Object System.Drawing.PointF(216, 40)),
        (New-Object System.Drawing.PointF(216, 216)),
        (New-Object System.Drawing.PointF(40, 216))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(85, 85)),
        (New-Object System.Drawing.PointF(171, 85)),
        (New-Object System.Drawing.PointF(171, 171)),
        (New-Object System.Drawing.PointF(85, 171))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    $g.DrawLine($c.ThinPen, 40, 40, 85, 85)
    $g.DrawLine($c.ThinPen, 216, 40, 171, 85)
    $g.DrawLine($c.ThinPen, 216, 216, 171, 171)
    $g.DrawLine($c.ThinPen, 40, 216, 85, 171)

    # Princess cross
    $g.DrawLine($c.ThinPen, 128, 40, 128, 85)
    $g.DrawLine($c.ThinPen, 128, 171, 128, 216)
    $g.DrawLine($c.ThinPen, 40, 128, 85, 128)
    $g.DrawLine($c.ThinPen, 171, 128, 216, 128)
    Draw-Sparkle $g 70 65 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 8. RADIANT
Render-GemIcon "radiant" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(65, 40)),
        (New-Object System.Drawing.PointF(191, 40)),
        (New-Object System.Drawing.PointF(216, 65)),
        (New-Object System.Drawing.PointF(216, 191)),
        (New-Object System.Drawing.PointF(191, 216)),
        (New-Object System.Drawing.PointF(65, 216)),
        (New-Object System.Drawing.PointF(40, 191)),
        (New-Object System.Drawing.PointF(40, 65))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(85, 75)),
        (New-Object System.Drawing.PointF(171, 75)),
        (New-Object System.Drawing.PointF(185, 90)),
        (New-Object System.Drawing.PointF(185, 166)),
        (New-Object System.Drawing.PointF(171, 181)),
        (New-Object System.Drawing.PointF(85, 181)),
        (New-Object System.Drawing.PointF(71, 166)),
        (New-Object System.Drawing.PointF(71, 90))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    for ($i=0; $i -lt 8; $i++) {
        $g.DrawLine($c.ThinPen, $outer[$i], $table[$i])
    }
    Draw-Sparkle $g 75 65 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 9. ASSCHER
Render-GemIcon "asscher" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(80, 40)),
        (New-Object System.Drawing.PointF(176, 40)),
        (New-Object System.Drawing.PointF(216, 80)),
        (New-Object System.Drawing.PointF(216, 176)),
        (New-Object System.Drawing.PointF(176, 216)),
        (New-Object System.Drawing.PointF(80, 216)),
        (New-Object System.Drawing.PointF(40, 176)),
        (New-Object System.Drawing.PointF(40, 80))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(96, 70)),
        (New-Object System.Drawing.PointF(160, 70)),
        (New-Object System.Drawing.PointF(186, 96)),
        (New-Object System.Drawing.PointF(186, 160)),
        (New-Object System.Drawing.PointF(160, 186)),
        (New-Object System.Drawing.PointF(96, 186)),
        (New-Object System.Drawing.PointF(70, 96)),
        (New-Object System.Drawing.PointF(70, 96))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    # Concentric windmill
    $g.DrawLine($c.ThinPen, 80, 40, 128, 128)
    $g.DrawLine($c.ThinPen, 176, 40, 128, 128)
    $g.DrawLine($c.ThinPen, 216, 80, 128, 128)
    $g.DrawLine($c.ThinPen, 216, 176, 128, 128)
    $g.DrawLine($c.ThinPen, 176, 216, 128, 128)
    $g.DrawLine($c.ThinPen, 80, 216, 128, 128)
    $g.DrawLine($c.ThinPen, 40, 176, 128, 128)
    $g.DrawLine($c.ThinPen, 40, 80, 128, 128)
    Draw-Sparkle $g 85 65 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 10. HEART
Render-GemIcon "heart" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddBezier(128, 70, 128, 30, 45, 30, 45, 105)
    $path.AddBezier(45, 105, 45, 165, 128, 225, 128, 225)
    $path.AddBezier(128, 225, 211, 165, 211, 105, 211, 105)
    $path.AddBezier(211, 105, 211, 30, 128, 30, 128, 70)
    $g.FillPath($c.BackBrush, $path)
    $g.DrawPath($c.LinePen, $path)

    $tpath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $tpath.AddBezier(128, 95, 128, 65, 75, 65, 75, 115)
    $tpath.AddBezier(75, 115, 75, 155, 128, 195, 128, 195)
    $tpath.AddBezier(128, 195, 181, 155, 181, 115, 181, 115)
    $tpath.AddBezier(181, 115, 181, 65, 128, 65, 128, 95)
    $g.FillPath($c.TableBrush, $tpath)
    $g.DrawPath($c.LinePen, $tpath)

    $g.DrawLine($c.ThinPen, 128, 70, 128, 95)
    $g.DrawLine($c.ThinPen, 128, 195, 128, 225)
    $g.DrawLine($c.ThinPen, 45, 105, 75, 115)
    $g.DrawLine($c.ThinPen, 211, 105, 181, 115)
    $path.Dispose(); $tpath.Dispose()
    Draw-Sparkle $g 90 60 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 11. TRILLION (Curved Triangle)
Render-GemIcon "trillion" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddBezier(128, 35, 185, 100, 225, 175, 220, 205)
    $path.AddBezier(220, 205, 128, 225, 128, 225, 36, 205)
    $path.AddBezier(36, 205, 31, 175, 71, 100, 128, 35)
    $g.FillPath($c.BackBrush, $path)
    $g.DrawPath($c.LinePen, $path)

    $table = @(
        (New-Object System.Drawing.PointF(128, 85)),
        (New-Object System.Drawing.PointF(175, 168)),
        (New-Object System.Drawing.PointF(81, 168))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    $g.DrawLine($c.ThinPen, 128, 35, 128, 85)
    $g.DrawLine($c.ThinPen, 220, 205, 175, 168)
    $g.DrawLine($c.ThinPen, 36, 205, 81, 168)
    $path.Dispose()
    Draw-Sparkle $g 128 60 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 12. TRILLIANT (Sharp Triangle)
Render-GemIcon "trilliant" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(128, 32)),
        (New-Object System.Drawing.PointF(224, 210)),
        (New-Object System.Drawing.PointF(32, 210))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(128, 95)),
        (New-Object System.Drawing.PointF(176, 178)),
        (New-Object System.Drawing.PointF(80, 178))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    $g.DrawLine($c.ThinPen, 128, 32, 128, 95)
    $g.DrawLine($c.ThinPen, 224, 210, 176, 178)
    $g.DrawLine($c.ThinPen, 32, 210, 80, 178)
    Draw-Sparkle $g 128 55 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 13. BAGUETTE
Render-GemIcon "baguette" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(65, 35)),
        (New-Object System.Drawing.PointF(191, 35)),
        (New-Object System.Drawing.PointF(191, 221)),
        (New-Object System.Drawing.PointF(65, 221))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(90, 65)),
        (New-Object System.Drawing.PointF(166, 65)),
        (New-Object System.Drawing.PointF(166, 191)),
        (New-Object System.Drawing.PointF(90, 191))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    $g.DrawLine($c.ThinPen, 65, 35, 90, 65)
    $g.DrawLine($c.ThinPen, 191, 35, 166, 65)
    $g.DrawLine($c.ThinPen, 191, 221, 166, 191)
    $g.DrawLine($c.ThinPen, 65, 221, 90, 191)
    Draw-Sparkle $g 85 50 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 14. OCTAGON
Render-GemIcon "octagon" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @()
    for ($i=0; $i -lt 8; $i++) {
        $a = $i * [Math]::PI / 4.0
        $outer += New-Object System.Drawing.PointF((128 + 92 * [Math]::Cos($a)), (128 + 92 * [Math]::Sin($a)))
    }
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @()
    for ($i=0; $i -lt 8; $i++) {
        $a = $i * [Math]::PI / 4.0
        $table += New-Object System.Drawing.PointF((128 + 52 * [Math]::Cos($a)), (128 + 52 * [Math]::Sin($a)))
    }
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    for ($i=0; $i -lt 8; $i++) {
        $g.DrawLine($c.ThinPen, $outer[$i], $table[$i])
    }
    Draw-Sparkle $g 80 70 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 15. SQUARE
Render-GemIcon "square" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(45, 45)),
        (New-Object System.Drawing.PointF(211, 45)),
        (New-Object System.Drawing.PointF(211, 211)),
        (New-Object System.Drawing.PointF(45, 211))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(85, 85)),
        (New-Object System.Drawing.PointF(171, 85)),
        (New-Object System.Drawing.PointF(171, 171)),
        (New-Object System.Drawing.PointF(85, 171))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    $g.DrawLine($c.ThinPen, 45, 45, 85, 85)
    $g.DrawLine($c.ThinPen, 211, 45, 171, 85)
    $g.DrawLine($c.ThinPen, 211, 211, 171, 171)
    $g.DrawLine($c.ThinPen, 45, 211, 85, 171)
    Draw-Sparkle $g 75 70 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 16. TRIANGLE
Render-GemIcon "triangle" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(128, 38)),
        (New-Object System.Drawing.PointF(218, 206)),
        (New-Object System.Drawing.PointF(38, 206))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(128, 98)),
        (New-Object System.Drawing.PointF(173, 176)),
        (New-Object System.Drawing.PointF(83, 176))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    $g.DrawLine($c.ThinPen, 128, 38, 128, 98)
    $g.DrawLine($c.ThinPen, 218, 206, 173, 176)
    $g.DrawLine($c.ThinPen, 38, 206, 83, 176)
    Draw-Sparkle $g 128 65 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

# 17. FLANDERS
Render-GemIcon "flanders" {
    param($g, $isDark)
    $c = Get-Colors $isDark
    $outer = @(
        (New-Object System.Drawing.PointF(70, 42)),
        (New-Object System.Drawing.PointF(186, 42)),
        (New-Object System.Drawing.PointF(214, 70)),
        (New-Object System.Drawing.PointF(214, 186)),
        (New-Object System.Drawing.PointF(186, 214)),
        (New-Object System.Drawing.PointF(70, 214)),
        (New-Object System.Drawing.PointF(42, 186)),
        (New-Object System.Drawing.PointF(42, 70))
    )
    $g.FillPolygon($c.BackBrush, $outer)
    $g.DrawPolygon($c.LinePen, $outer)

    $table = @(
        (New-Object System.Drawing.PointF(88, 68)),
        (New-Object System.Drawing.PointF(168, 68)),
        (New-Object System.Drawing.PointF(188, 88)),
        (New-Object System.Drawing.PointF(188, 168)),
        (New-Object System.Drawing.PointF(168, 188)),
        (New-Object System.Drawing.PointF(88, 188)),
        (New-Object System.Drawing.PointF(68, 168)),
        (New-Object System.Drawing.PointF(68, 88))
    )
    $g.FillPolygon($c.TableBrush, $table)
    $g.DrawPolygon($c.LinePen, $table)

    for ($i=0; $i -lt 8; $i++) {
        $g.DrawLine($c.ThinPen, $outer[$i], $table[$i])
    }
    Draw-Sparkle $g 80 62 12 $isDark
} '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"></svg>'

Write-Output "All 17 luxury gem icons rendered in dark/ and light/ formats!"
