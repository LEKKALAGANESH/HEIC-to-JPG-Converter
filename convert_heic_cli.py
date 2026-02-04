#!/usr/bin/env python3
"""
HEIC to JPG Converter - Command Line Interface

Converts HEIC/HEIF files to JPG format.
Supports single files, multiple files, or entire folders.

Usage:
    python convert_heic_cli.py                     # Interactive mode
    python convert_heic_cli.py file.heic           # Convert single file
    python convert_heic_cli.py /path/to/folder     # Convert entire folder
    python convert_heic_cli.py -r /path/to/folder  # Recursive folder conversion
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from PIL import Image
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install pillow pillow-heif")
    sys.exit(1)


def convert_heic_to_jpg(heic_path, output_dir=None, quality=95):
    """
    Convert a single HEIC file to JPG.

    Args:
        heic_path: Path to HEIC file
        output_dir: Output directory (default: same as input)
        quality: JPEG quality (1-100)

    Returns:
        Path to converted JPG file, or None if failed
    """
    heic_path = Path(heic_path)

    if not heic_path.exists():
        print(f"  Error: File not found - {heic_path}")
        return None

    # Determine output path
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = heic_path.parent

    jpg_filename = heic_path.stem + ".jpg"
    jpg_path = output_dir / jpg_filename

    # Skip if already exists
    if jpg_path.exists():
        print(f"  Skipped (exists): {jpg_filename}")
        return jpg_path

    try:
        with Image.open(heic_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            img.save(jpg_path, "JPEG", quality=quality)

        print(f"  Converted: {heic_path.name} -> {jpg_filename}")
        return jpg_path

    except Exception as e:
        print(f"  Failed: {heic_path.name} - {str(e)}")
        return None


def convert_folder(folder_path, recursive=False, create_subfolder=True, quality=95):
    """
    Convert all HEIC files in a folder.

    Args:
        folder_path: Path to folder
        recursive: Also convert files in subfolders
        create_subfolder: Create 'jpg files' subfolder for output
        quality: JPEG quality (1-100)

    Returns:
        Tuple of (converted_count, failed_count)
    """
    folder_path = Path(folder_path)

    if not folder_path.exists():
        print(f"Error: Folder not found - {folder_path}")
        return 0, 0

    # Find HEIC files
    if recursive:
        heic_files = list(folder_path.rglob("*.heic")) + list(folder_path.rglob("*.HEIC"))
        heic_files += list(folder_path.rglob("*.heif")) + list(folder_path.rglob("*.HEIF"))
    else:
        heic_files = list(folder_path.glob("*.heic")) + list(folder_path.glob("*.HEIC"))
        heic_files += list(folder_path.glob("*.heif")) + list(folder_path.glob("*.HEIF"))

    # Remove duplicates
    seen = set()
    unique_files = []
    for f in heic_files:
        if str(f).lower() not in seen:
            seen.add(str(f).lower())
            unique_files.append(f)
    heic_files = unique_files

    if not heic_files:
        print(f"No HEIC files found in: {folder_path}")
        return 0, 0

    print(f"\nProcessing: {folder_path}")
    print(f"Found {len(heic_files)} HEIC file(s)")

    converted = 0
    failed = 0

    for heic_file in sorted(heic_files):
        # Determine output directory
        if create_subfolder:
            output_dir = heic_file.parent / "jpg files"
        else:
            output_dir = heic_file.parent

        result = convert_heic_to_jpg(heic_file, output_dir, quality)
        if result:
            converted += 1
        else:
            failed += 1

    print(f"Completed: {converted} converted, {failed} failed")
    return converted, failed


def interactive_mode():
    """Interactive mode - prompts user for input."""
    print("\n" + "=" * 50)
    print("HEIC to JPG Converter - Interactive Mode")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1. Convert a single file")
        print("  2. Convert a folder")
        print("  3. Convert a folder (recursive - includes subfolders)")
        print("  4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            file_path = input("Enter HEIC file path: ").strip().strip('"')
            if file_path:
                output_dir = input("Output directory (press Enter for same folder): ").strip().strip('"')
                convert_heic_to_jpg(file_path, output_dir if output_dir else None)

        elif choice == "2":
            folder_path = input("Enter folder path: ").strip().strip('"')
            if folder_path:
                subfolder = input("Create 'jpg files' subfolder? (y/n, default: y): ").strip().lower()
                create_subfolder = subfolder != 'n'
                convert_folder(folder_path, recursive=False, create_subfolder=create_subfolder)

        elif choice == "3":
            folder_path = input("Enter folder path: ").strip().strip('"')
            if folder_path:
                subfolder = input("Create 'jpg files' subfolder? (y/n, default: y): ").strip().lower()
                create_subfolder = subfolder != 'n'
                convert_folder(folder_path, recursive=True, create_subfolder=create_subfolder)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-4.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert HEIC/HEIF files to JPG format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_heic_cli.py                      # Interactive mode
  python convert_heic_cli.py photo.heic           # Convert single file
  python convert_heic_cli.py /path/to/folder      # Convert folder
  python convert_heic_cli.py -r /path/to/folder   # Recursive conversion
  python convert_heic_cli.py -o ./output *.heic   # Custom output folder
        """
    )

    parser.add_argument(
        "paths",
        nargs="*",
        help="HEIC files or folders to convert"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively convert files in subfolders"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output directory for converted files"
    )

    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=95,
        help="JPEG quality (1-100, default: 95)"
    )

    parser.add_argument(
        "--no-subfolder",
        action="store_true",
        help="Don't create 'jpg files' subfolder, save in same directory"
    )

    args = parser.parse_args()

    # No arguments - interactive mode
    if not args.paths:
        interactive_mode()
        return

    total_converted = 0
    total_failed = 0

    for path in args.paths:
        path = Path(path)

        if path.is_file():
            # Single file
            result = convert_heic_to_jpg(path, args.output, args.quality)
            if result:
                total_converted += 1
            else:
                total_failed += 1

        elif path.is_dir():
            # Folder
            converted, failed = convert_folder(
                path,
                recursive=args.recursive,
                create_subfolder=not args.no_subfolder,
                quality=args.quality
            )
            total_converted += converted
            total_failed += failed

        else:
            print(f"Warning: Path not found - {path}")

    print("\n" + "=" * 50)
    print(f"TOTAL: {total_converted} converted, {total_failed} failed")
    print("=" * 50)


if __name__ == "__main__":
    main()
