import os
from typing import List, Dict
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFProcessor:
    """
    Process PDF files and extract text content
    """

    def __init__(self, pdf_directory: str = "data"):
        """
        Initialize PDF processor

        Args:
            pdf_directory: Directory containing PDF files
        """
        self.pdf_directory = pdf_directory
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Each chunk will be ~1000 characters
            chunk_overlap=200,  # 200 characters overlap between chunks
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def get_pdf_files(self) -> List[str]:
        """
        Get all PDF files from the directory

        Returns:
            List of PDF file paths
        """
        pdf_files = []
        for file in os.listdir(self.pdf_directory):
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(self.pdf_directory, file))
        return pdf_files

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a single PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text as string
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() + "\n"

            return text
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return ""

    def process_all_pdfs(self) -> List[Dict[str, str]]:
        """
        Process all PDFs and split into chunks

        Returns:
            List of dictionaries containing text chunks and metadata
        """
        all_chunks = []
        pdf_files = self.get_pdf_files()

        print(f"Found {len(pdf_files)} PDF files")

        for pdf_path in pdf_files:
            print(f"\nProcessing: {os.path.basename(pdf_path)}")

            # Extract text
            text = self.extract_text_from_pdf(pdf_path)

            if not text.strip():
                print(f"  Warning: No text extracted from {pdf_path}")
                continue

            # Split into chunks
            chunks = self.text_splitter.split_text(text)
            print(f"  Created {len(chunks)} chunks")

            # Add metadata to each chunk
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    'text': chunk,
                    'source': os.path.basename(pdf_path),
                    'chunk_id': i
                })

        print(f"\nTotal chunks created: {len(all_chunks)}")
        return all_chunks

    def get_sample_chunk(self, chunks: List[Dict[str, str]], index: int = 0) -> None:
        """
        Print a sample chunk for verification

        Args:
            chunks: List of text chunks
            index: Index of chunk to display
        """
        if chunks and index < len(chunks):
            chunk = chunks[index]
            print("\n" + "=" * 50)
            print("SAMPLE CHUNK")
            print("=" * 50)
            print(f"Source: {chunk['source']}")
            print(f"Chunk ID: {chunk['chunk_id']}")
            print(f"Text length: {len(chunk['text'])} characters")
            print("\nContent preview:")
            print("-" * 50)
            print(chunk['text'][:300] + "...")
            print("=" * 50)


# Test the processor
if __name__ == "__main__":
    print("Starting PDF Processing...")
    print("=" * 50)

    # Initialize processor
    processor = PDFProcessor()

    # Process all PDFs
    chunks = processor.process_all_pdfs()

    # Show sample chunk
    if chunks:
        processor.get_sample_chunk(chunks, 0)
        processor.get_sample_chunk(chunks, 1)
    else:
        print("No chunks created. Check your PDF files.")

    print("PDF Processing completed.")
    print("=" * 50)