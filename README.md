Conversational Q&A Chatbot with PDF
This project implements a conversational Question & Answer (Q&A) chatbot that allows users to upload PDF documents and interactively query their content. By leveraging natural language processing techniques, the chatbot provides accurate and context-aware responses based on the uploaded PDF files.

Features
PDF Upload: Users can upload PDF documents for analysis.
Text Extraction: Extracts and processes text content from uploaded PDFs.
Conversational Interface: Engage in a dialogue with the chatbot to ask questions related to the PDF content.
Contextual Responses: Provides answers based on the context of the uploaded documents.

Installation
Clone the Repository:

git clone https://github.com/Shyamal1508/conversational_qa_chatbot_with_pdf.git
cd conversational_qa_chatbot_with_pdf

Create a Virtual Environment:

python3 -m venv venv
source venv/bin/activate

Usage
Run the Streamlit Application:

streamlit run app.py
Interact with the Chatbot:

Upload a PDF document using the provided interface.

Enter your questions in the chat input box.

Receive answers based on the content of the uploaded PDF.

conversational_qa_chatbot_with_pdf/
├── app.py             # Main application script
├── .env               # Environment variables (e.g., API keys)
├── temp.pdf           # Sample PDF file for testing
└── README.md          # Project documentation
