#!/usr/bin/env python3
"""
Jeweler 3D Studio - Blender Extension Packaging Script
Packs ONLY the Blender addon source files into a flat .zip archive for Blender 4.2+.
Excludes development files (.agents, .skill, overview, .git, __pycache__, etc.).
"""

import os
import sys
import zipfile
from pathlib import Path

# Force UTF-8 stdout encoding for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Files and directories to include in the Blender extension package
ADDON_INCLUDES = [
    "blender_manifest.toml",
    "__init__.py",
    "core",
    "ui",
    "assets",
    "LICENSE",
]

# Patterns/names to strictly exclude
EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".agents",
    ".skill",
    "overview",
    "dist",
    ".pytest_cache",
    ".vscode",
    ".idea",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store",
}

# Dev/source asset paths — not shipped in the extension zip
EXCLUDE_ASSET_PREFIXES = (
    "assets/gems/dark/",
    "assets/gems/light/",
    "assets/gems/references/",
    "assets/gems/svg/",
    "assets/gems/styles/",
)

EXCLUDE_FILENAMES = {
    "gems.blend",
    "round_v2.png",
    "round_v2.svg",
}

# Runtime ships only the Round icon PNG; other cuts are text-only in UI.
EXCLUDE_ASSET_GLOB_PREFIXES = (
    "assets/gems/png/",
)

EXCLUDE_ASSET_GLOB_KEEP = {
    "assets/gems/png/round.png",
}


def should_exclude(relative_posix: str) -> bool:
    """Return True if a file must not be included in the extension zip."""
    if Path(relative_posix).name in EXCLUDE_FILENAMES:
        return True
    if any(relative_posix.startswith(prefix) for prefix in EXCLUDE_ASSET_PREFIXES):
        return True
    if relative_posix.startswith(EXCLUDE_ASSET_GLOB_PREFIXES[0]):
        return relative_posix not in EXCLUDE_ASSET_GLOB_KEEP
    return False


def parse_manifest_info(manifest_path: Path) -> tuple[str, str]:
    """Extracts id and version from blender_manifest.toml."""
    addon_id = "jeweler3dstudio"
    addon_version = "0.1.0"

    if not manifest_path.exists():
        return addon_id, addon_version

    try:
        content = manifest_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("id ="):
                addon_id = line.split("=")[1].strip().strip('"').strip("'")
            elif line.startswith("version ="):
                addon_version = line.split("=")[1].strip().strip('"').strip("'")
    except Exception as e:
        print(f"⚠️ Warning: Could not parse blender_manifest.toml completely: {e}")

    return addon_id, addon_version


def create_extension_zip() -> Path:
    """Builds the extension zip file inside dist/ directory."""
    root_dir = Path(__file__).parent.resolve()
    dist_dir = root_dir / "dist"
    dist_dir.mkdir(exist_ok=True)

    manifest_path = root_dir / "blender_manifest.toml"
    addon_id, addon_version = parse_manifest_info(manifest_path)

    zip_name = f"{addon_id}-{addon_version}.zip"
    zip_path = dist_dir / zip_name

    print(f"📦 Packaging Blender Extension: {addon_id} v{addon_version}")
    print(f"📍 Output path: {zip_path}\n")

    files_added = 0
    total_bytes = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item_name in ADDON_INCLUDES:
            item_path = root_dir / item_name

            if not item_path.exists():
                print(f"⚠️ Skipping missing item: {item_name}")
                continue

            if item_path.is_file():
                arcname = item_name
                zipf.write(item_path, arcname)
                files_added += 1
                total_bytes += item_path.stat().st_size
                print(f"  + {arcname}")

            elif item_path.is_dir():
                for file_path in item_path.rglob("*"):
                    # Check exclusions
                    if any(part in EXCLUDE_DIRS for part in file_path.parts):
                        continue
                    if file_path.suffix.lower() in EXCLUDE_EXTENSIONS:
                        continue
                    if file_path.name.startswith("."):
                        continue

                    if file_path.is_file():
                        arcname = str(file_path.relative_to(root_dir)).replace("\\", "/")
                        if should_exclude(arcname):
                            continue
                        zipf.write(file_path, arcname)
                        files_added += 1
                        total_bytes += file_path.stat().st_size
                        print(f"  + {arcname}")

    print(f"\n✅ Packaged successfully! Added {files_added} files ({total_bytes / 1024:.1f} KB).")
    print(f"📦 Final ZIP: {zip_path}")
    return zip_path


if __name__ == "__main__":
    create_extension_zip()
