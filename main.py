from src.retriever import build_retriever, retrieve_documents
from src.generator import generate_answer


pdf_path = input("Enter the PDF path: ")

# Build the retriever from the PDF
index, chunks = build_retriever(pdf_path)

# Ask the user a question
question = input("Ask a question about the PDF: ")

# Retrieve relevant information
results = retrieve_documents(
    index,
    chunks,
    question
)

# Combine retrieved chunks into context
context = "\n\n".join(results)

# Generate answer using Gemini
answer = generate_answer(
    question,
    context
)

print("\nAnswer:")
print(answer)