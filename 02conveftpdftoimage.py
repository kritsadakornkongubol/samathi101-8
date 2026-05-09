import fitz  # PyMuPDF
import os
from pathlib import Path
import glob

def pdf_to_png(pdf_path, output_dir=None, dpi=150):
    """
    Convert PDF pages to PNG images
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save PNG files (optional)
        dpi (int): Resolution for the output images
    """
    
    # Convert to Path object for easier handling
    pdf_path = Path(pdf_path)
    
    # Check if PDF file exists
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return False
    
    # Set output directory (create a folder for each PDF)
    if output_dir is None:
        # output_dir = pdf_path.parent / "converted_images" / f"{pdf_path.stem}_images"
        output_dir = pdf_path.parent / "images" 
    else:
        # output_dir = Path(output_dir) / f"{pdf_path.stem}_images"
        output_dir = pdf_path.parent / "images" 
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Open the PDF file
        pdf_document = fitz.open(str(pdf_path))
        
        print(f"Converting '{pdf_path.name}' with {len(pdf_document)} pages...")
        
        # Convert each page to PNG
        for page_num in range(len(pdf_document)):
            # Get the page
            page = pdf_document[page_num]
            
            # Create a matrix for the desired DPI
            mat = fitz.Matrix(dpi/72, dpi/72)
            
            # Render page to an image
            pix = page.get_pixmap(matrix=mat)
            
            # Generate output filename
            # output_filename = output_dir / f"page_{page_num + 1:03d}.png"
            output_filename = output_dir / f"{pdf_path.stem}_{page_num + 1:03d}.png"
            

            
            # Save the image
            pix.save(str(output_filename))
        
        # Close the PDF
        pdf_document.close()
        
        print(f"✓ Completed: {pdf_path.name} -> {output_dir}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {pdf_path.name}: {str(e)}")
        return False

def convert_all_pdfs_in_folder(folder_path, output_base_dir=None, dpi=200):
    """
    Convert all PDF files in a folder to PNG images
    
    Args:
        folder_path (str): Path to folder containing PDF files
        output_base_dir (str): Base directory for output (optional)
        dpi (int): Resolution for the output images
    """
    
    folder_path = Path(folder_path)
    
    # Check if folder exists
    if not folder_path.exists():
        print(f"Error: Folder not found at {folder_path}")
        return
    
    # Find all PDF files in the folder
    pdf_files = list(folder_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to convert:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    print(f"\nStarting conversion...")
    print("=" * 50)
    
    # Set output directory
    if output_base_dir is None:
        output_base_dir = folder_path / "images"
        # output_base_dir = folder_path / "converted_images"
    else:
        output_base_dir = Path(output_base_dir)
    
    # Convert each PDF
    successful = 0
    failed = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
   
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
        
        if pdf_to_png(pdf_file, output_base_dir, dpi):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("CONVERSION SUMMARY:")
    print(f"✓ Successfully converted: {successful} files")
    if failed > 0:
        print(f"✗ Failed to convert: {failed} files")
    print(f"📁 Images saved to: {output_base_dir}")

# Usage
if __name__ == "__main__":
    # Your folder path containing PDF files
    # pdf_folder_path = r"C:\Users\bomb\Documents\วิทันตสาสมาธิ 5 พย 2567\รวมpdf4"
    input_folder = input("Enter the folder path containing PDF files to convert (or press Enter to use default): ").strip()
    pdf_folder_path = r"E:\ครูสมาธิ\งานสาขา\008\008_สมาธิขั้นสูง"
    
    if input_folder:
        pdf_folder_path = input_folder

    # Convert all PDF files in the folder
    convert_all_pdfs_in_folder(pdf_folder_path, dpi=200)  # Higher DPI for better quality
    
    print("\nAll done!")