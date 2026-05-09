import os
from pathlib import Path

def rename_files_in_folder(folder_path, dry_run=True):
    """
    Rename all files in a folder by removing everything after the first underscore from the end
    
    Args:
        folder_path (str): Path to folder containing files to rename
        dry_run (bool): If True, only show what would be renamed without actually renaming
    """
    
    folder_path = Path(folder_path)
    
    # Check if folder exists
    if not folder_path.exists():
        print(f"Error: Folder not found at {folder_path}")
        return
    
    # Get all files in the folder
    files = [f for f in folder_path.iterdir() if f.is_file()]
    
    if not files:
        print(f"No files found in {folder_path}")
        return
    
    print(f"Found {len(files)} files in the folder")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No files will be renamed")
        print("Set dry_run=False to actually rename files")
    else:
        print("\n🔄 RENAMING FILES...")
    
    print("=" * 80)
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in files:
        try:
            # Get filename without extension
            filename_without_ext = file_path.stem
            file_extension = file_path.suffix
            
            # Find the first underscore from the end
            # We'll split by underscore and find where the UUID-like pattern starts
            parts = filename_without_ext.split('_')
            
            # Look for the part that looks like a UUID (contains hyphens and is long)
            new_parts = []
            for part in parts:
                # If we find a part that looks like a UUID (contains hyphens and is reasonably long)
                if '-' in part and len(part) > 20:
                    # Stop here - don't include this part and anything after it
                    break
                new_parts.append(part)
            
            # Reconstruct the new filename
            if len(new_parts) < len(parts):  # Only rename if we found something to remove
                new_filename_without_ext = '_'.join(new_parts)
                new_filename = new_filename_without_ext + file_extension

                new_filename =new_filename.replace("__","_")



                new_file_path = folder_path / new_filename
                
                print(f"📝 Original: {file_path.name}")
                print(f"   New:      {new_filename}")
                
                if not dry_run:
                    # Check if new filename already exists
                    if new_file_path.exists():
                        print(f"   ⚠️  WARNING: Target file already exists, skipping...")
                        skipped_count += 1
                    else:
                        # Rename the file
                        file_path.rename(new_file_path)
                        print(f"   ✅ Renamed successfully")
                        renamed_count += 1
                else:
                    print(f"   ℹ️  Would be renamed")
                    renamed_count += 1
                
                print()
            else:
                print(f"⏭️  Skipped: {file_path.name} (no UUID pattern found)")
                skipped_count += 1
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
            error_count += 1
    
    # Summary
    print("=" * 80)
    print("SUMMARY:")
    if dry_run:
        print(f"📊 Files that would be renamed: {renamed_count}")
    else:
        print(f"✅ Successfully renamed: {renamed_count}")
    print(f"⏭️  Skipped: {skipped_count}")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")

def preview_renames(folder_path):
    """Preview what files would be renamed without actually renaming them"""
    rename_files_in_folder(folder_path, dry_run=True)

def execute_renames(folder_path):
    """Actually rename the files"""
    rename_files_in_folder(folder_path, dry_run=False)

# Usage
if __name__ == "__main__":
    # Your folder path
    # folder_path = r"C:\Users\bomb\Documents\วิทันตสาสมาธิ 5 พย 2567\รวมpdf4"
    folder_path = input("Enter the folder path containing files to rename (or press Enter to use default): ").strip()
    
    if not folder_path:
        folder_path = r"E:\ครูสมาธิ\งานสาขา\008\008_สมาธิขั้นสูง"
    
    print("🔍 PREVIEW MODE")
    print("This will show you what files would be renamed without actually renaming them.")
    print()
    
    # First, preview the changes
    preview_renames(folder_path)
    
    # Uncomment the lines below to actually perform the renaming
    print("\n" + "="*80)
    print("🔄 ACTUAL RENAMING")
    execute_renames(folder_path)
    
    print("\n💡 To actually rename the files:")
    print("   1. Review the preview above")
    print("   2. Uncomment the last two lines in the script")
    print("   3. Run the script again")