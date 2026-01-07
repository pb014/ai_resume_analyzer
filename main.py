import argparse, os, sys, time, threading
from pathlib import Path
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

class ResumeReader:
    #constructor
    def __init__(self, api_key = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key required!!")
        
        #initializing the gemini client
        self.client = genai.Client(api_key=self.api_key)

    #function to summarize this text
    def extract_text(self, pdf_path: Path) -> str:
        """Extracts text from a PDF file"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            return f"Error reading PDF: {e}"
        
    def summarize_resume(self, text, max_words = 250):
        prompt = (  
                    f"Act as a Senior HR Manager. Analyze the following resume text and "
                    f"summarize it in roughly {max_words} words. "
                    f"Use bullet points for skills."
                    f"Focus heavily on measurable impact and years of experience. \n\n"
                    f"RESUME:\n{text}"
                )
        response = self.client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt 
        )

        return response.text or ""

def loading_spinner(stop_event):
    chars = ["|", "/", "-", "\\"]
    while not stop_event.is_set():
        for char in chars:
            sys.stdout.write(f'\r[Thinking] {char}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 25 + '\r')

def main():
    parser = argparse.ArgumentParser(description="CV Reader")
    
    #positional argument
    parser.add_argument("pdf_path", type=str, help="Path to the resume PDF file")
    
    #Optional arguments
    parser.add_argument("-l", "--max_length", type=int, default=200, help="Max summary length in words")
    parser.add_argument("-o", "--output", type=str, help="Output text file path to save the summary")
    parser.add_argument("-k", "--key", type=str, help="Manually provide Gemini API Key")

    args = parser.parse_args()

    #converting the string to a path object
    pdf_file = Path(args.pdf_path)

    if not pdf_file.exists():
        print(f"Error: The file '{args.pdf_path}' does not exist.")
        return

    try:
        #defining the reader
        reader = ResumeReader(api_key=args.key)

        raw_text = reader.extract_text(pdf_file)
        
        if not raw_text.strip():
            print("Error: Could not extract any text from the PDF.")
            return
        
        stop_loading = threading.Event()

        spinner_thread = threading.Thread(target = loading_spinner, args=(stop_loading, ))
        spinner_thread.start()

        summary = reader.summarize_resume(raw_text, max_words=args.max_length)
        
        stop_loading.set()
        spinner_thread.join()

        print("\n" + "Analysis Complete".center(30, "-"))
        print(summary)

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(summary, encoding="utf-8")
            print(f"\n[Success] Summary saved to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()