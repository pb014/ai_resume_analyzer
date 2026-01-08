# AI Resume Reader

AI Resume Reader powered by Google gemini which creates a dedicated summary for your resume identifying key achievements and technical skills in seconds. Equipped with a command line interface for easy use.

## Key Features
- **One-Shot Analysis** 
- **HR Persona Prompting** 
- **Smooth CLI Experience** 

## Installation & Setup

  ## 1. Prerequisites
  - [Mamba](https://mamba.readthedocs.io/en/latest/installation.html) or Conda installed on your system.
  - A **Google Gemini API Key**. You can get one for free at [Google AI Studio](https://aistudio.google.com/).
  
  ## 2. Clone and Prepare
  ```bash
  # Clone the repository
  git clone https://github.com/pb014/ai_resume_analyzer
  cd ai-resume-reader
  
  # Create the environment using Mamba
  mamba env create -f environment.yml
  
  # Activate the environment
  mamba activate ai
  ```

  ## 3. Configure API key
  - Create a .env file in the root directory:
    ```bash
    touch .env
  - Open .env and add your key
    ```bash
    GEMINI_API_KEY=your_actual_key_here

## Usage

  Run the script from your terminal by providing the path to a PDF resume.
  - Standard Usage (make sure to keep your resume in the same directory)
    ```bash
    python main.py path/to/resume.pdf

  - Advanced usage
    ```bash
    python main.py -h
  
  

