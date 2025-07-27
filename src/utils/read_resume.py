import PyPDF2
import fitz  # PyMuPDF
from typing import Optional
import os

class ResumeReader:
    """Utility class to read and extract text from resume PDFs"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    def read_with_pypdf2(self) -> str:
        """Read PDF using PyPDF2 library"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF with PyPDF2: {str(e)}")
    
    def read_with_pymupdf(self) -> str:
        """Read PDF using PyMuPDF (fitz) library - better for complex PDFs"""
        try:
            doc = fitz.open(self.pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text() + "\n"
            
            doc.close()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF with PyMuPDF: {str(e)}")
    
    def read_resume(self, method: str = "pymupdf") -> str:
        """
        Read resume PDF and return extracted text
        
        Args:
            method: "pymupdf" or "pypdf2" - extraction method to use
            
        Returns:
            str: Extracted text from the PDF
        """
        if method == "pymupdf":
            return self.read_with_pymupdf()
        elif method == "pypdf2":
            return self.read_with_pypdf2()
        else:
            raise ValueError("Method must be either 'pymupdf' or 'pypdf2'")
    
    def get_resume_summary(self) -> dict:
        """
        Extract resume text and provide basic analysis
        
        Returns:
            dict: Contains full text, word count, and page count
        """
        text = self.read_resume()
        
        return {
            "full_text": text,
            "word_count": len(text.split()),
            "character_count": len(text),
            "page_count": self._get_page_count()
        }
    
    def _get_page_count(self) -> int:
        """Get number of pages in the PDF"""
        try:
            doc = fitz.open(self.pdf_path)
            page_count = len(doc)
            doc.close()
            return page_count
        except:
            try:
                with open(self.pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    return len(pdf_reader.pages)
            except:
                return 0


def read_resume_pdf(pdf_path: str, method: str = "pymupdf") -> str:
    """
    Convenience function to read a resume PDF
    
    Args:
        pdf_path: Path to the PDF file
        method: "pymupdf" or "pypdf2" - extraction method to use
        
    Returns:
        str: Extracted text from the PDF
    """
    reader = ResumeReader(pdf_path)
    return reader.read_resume(method)


def get_resume_info(pdf_path: str) -> dict:
    """
    Convenience function to get resume information
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        dict: Resume information including text and metadata
    """
    reader = ResumeReader(pdf_path)
    return reader.get_resume_summary()


# Example usage
if __name__ == "__main__":
    # Example usage
    pdf_path = "data_files/resumes/Lin Mei_Experiened Level Software.pdf"  # Replace with actual path
    
    try:
        resume_text = read_resume_pdf(pdf_path)
        print("Resume Text:")
        print(resume_text)
        print("\n" + "="*50 + "\n")
        
        resume_info = get_resume_info(pdf_path)
        print(f"Word Count: {resume_info['word_count']}")
        print(f"Page Count: {resume_info['page_count']}")
        
    except FileNotFoundError:
        print("Please provide a valid PDF file path")
    except Exception as e:
        print(f"Error: {e}")