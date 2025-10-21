import os
from dotenv import load_dotenv
import google.generativeai as genai
from vector_store import VectorStore

# Load environment variables
load_dotenv()


class RAGChatbot:
    """
    RAG-based chatbot for Turkish Health Tourism
    """

    def __init__(self):
        """
        Initialize RAG chatbot
        """
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)

        # Configure generation settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 300,  # Limit output length
        }

        self.model = genai.GenerativeModel(
            'models/gemini-2.0-flash',
            generation_config=generation_config
        )

        print("✓ Gemini model initialized")

        # Initialize vector store
        self.vector_store = VectorStore()
        print("✓ Vector store loaded")

    def create_prompt(self, query: str, context_docs: list) -> str:
        """
        Create a prompt for the LLM with context

        Args:
            query: User's question
            context_docs: Retrieved documents from vector store

        Returns:
            Formatted prompt string
        """
        # Combine context documents
        context = "\n\n".join([f"Document {i + 1}:\n{doc}"
                               for i, doc in enumerate(context_docs)])

        prompt = f"""You are an expert assistant on Turkish Health Tourism. 
    Use the following context documents to answer the user's question accurately and concisely.

    Context Documents:
    {context}

    User Question: {query}

    Instructions:
    - Provide a concise answer (maximum 150 words)
    - Use bullet points for lists when appropriate
    - Focus on the most important information
    - If the context doesn't contain enough information, say so briefly
    - Be professional and helpful
    - Cite the document sources at the end

    Answer:"""

        return prompt

    def get_answer(self, query: str, n_results: int = 3) -> dict:
        """
        Get answer for a user query using RAG

        Args:
            query: User's question
            n_results: Number of context documents to retrieve

        Returns:
            Dictionary containing answer and sources
        """
        print(f"\nProcessing query: '{query}'")
        print("-" * 50)

        # Step 1: Retrieve relevant documents
        print("Searching vector database...")
        search_results = self.vector_store.search(query, n_results=n_results)

        context_docs = search_results['documents'][0]
        metadatas = search_results['metadatas'][0]

        print(f"✓ Found {len(context_docs)} relevant documents")

        # Step 2: Create prompt with context
        prompt = self.create_prompt(query, context_docs)

        # Step 3: Generate answer using Gemini
        print("Generating answer with Gemini...")
        response = self.model.generate_content(prompt)

        answer = response.text

        # Extract unique sources
        sources = list(set([meta['source'] for meta in metadatas]))

        print("✓ Answer generated")

        return {
            'query': query,
            'answer': answer,
            'sources': sources,
            'context_docs': context_docs
        }

    def chat(self):
        """
        Interactive chat loop
        """
        print("\n" + "=" * 50)
        print("RAG CHATBOT - Turkish Health Tourism")
        print("=" * 50)
        print("Ask questions about health tourism in Turkey")
        print("Type 'exit' to quit")
        print("=" * 50 + "\n")

        while True:
            # Get user input
            user_query = input("You: ").strip()

            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! 👋")
                break

            if not user_query:
                continue

            # Get answer
            result = self.get_answer(user_query)

            # Display answer
            print("\n" + "=" * 50)
            print("ASSISTANT:")
            print("=" * 50)
            print(result['answer'])
            print("\n" + "-" * 50)
            print(f"Sources: {', '.join(result['sources'])}")
            print("=" * 50 + "\n")


def test_chatbot():
    """
    Test the chatbot with sample questions
    """
    print("=" * 50)
    print("TESTING RAG CHATBOT")
    print("=" * 50)

    chatbot = RAGChatbot()

    test_questions = [
        "What is health tourism in Turkey?",
        "What are the main types of health tourism services?",
        "Why do people choose Turkey for medical tourism?"
    ]

    for question in test_questions:
        result = chatbot.get_answer(question)

        print("\n" + "=" * 50)
        print(f"QUESTION: {question}")
        print("=" * 50)
        print(f"ANSWER:\n{result['answer']}")
        print(f"\nSOURCES: {', '.join(result['sources'])}")
        print("=" * 50)


if __name__ == "__main__":
    # Test with sample questions
    test_chatbot()

    # Uncomment below to start interactive chat
    # chatbot = RAGChatbot()
    # chatbot.chat()