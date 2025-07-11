import fitz  # PyMuPDF
import re
from pathlib import Path

def extract_pdf_text(pdf_path):
    """
    Extract text from PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted and cleaned text
    """
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        # Extract text from all pages
        full_text = ""
        for page_num in range(len(doc)):
            page: fitz.Page = doc.load_page(page_num)
            text = page.get_text()
            full_text += text
            
        doc.close()
        
        # Clean the text for LLM/RAG use
        cleaned_text = clean_text_for_llm(full_text)
        
        return cleaned_text
        
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return None

def clean_text_for_llm(text):
    """
    Clean extracted text to make it more suitable for LLM processing.
    
    Args:
        text (str): Raw extracted text
        
    Returns:
        str: Cleaned text
    """
    # Remove excessive whitespace while preserving paragraph breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Remove trailing/leading whitespace from lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove excessive spaces within lines
    text = re.sub(r' +', ' ', text)
    
    # Remove empty lines at the beginning and end
    text = text.strip()
    
    return text

def save_text_to_file(text, output_path):
    """
    Save extracted text to a file.
    
    Args:
        text (str): Text to save
        output_path (str): Output file path
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text saved to: {output_path}")
    except Exception as e:
        print(f"Error saving text to {output_path}: {str(e)}")

def main():
    """
    Main function to demonstrate PDF text extraction.
    """
    
    pdf_path = "konspekt.pdf"
    print(f"Extracting text from: {pdf_path}")
    
    # Extract text
    extracted_text = extract_pdf_text(pdf_path)
    
    if extracted_text:     
        # Save to file
        output_filename = f"{Path(pdf_path).stem}_extracted.txt"
        save_text_to_file(extracted_text, output_filename)
        
        print(f"\nFull extracted text saved to: {output_filename}")
        
    else:
        print("Failed to extract text from the PDF.")

if __name__ == "__main__":
    main()
