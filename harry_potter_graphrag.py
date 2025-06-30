import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

# ========= STEP 1: Read and Chunk PDF =========
def make_chunks(text, chunk_size=150):
    words = text.split()
    chunks = []
    for i in range(0, len(words), 120):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

reader = PdfReader("Harry Potter and the Prisoner of Azkaban.pdf")
full_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
chunks = make_chunks(full_text)

# ========= STEP 2: Vector Embedding (FAISS) =========
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if not os.path.exists("faiss_index_hp/index.faiss"):
    vectorstore = FAISS.from_texts(chunks, embedding=embedding_model)
    vectorstore.save_local("faiss_index_hp")
else:
    vectorstore = FAISS.load_local("faiss_index_hp", embedding=embedding_model)

# ========= STEP 3: Graph Setup (Neo4j) =========
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

llm_openai = ChatOpenAI(
    temperature=0,
    model="gpt-4o",  # faster and cheaper than gpt-4
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

graph_chain = GraphCypherQAChain.from_llm(llm=llm_openai, graph=graph, verbose=False)

# ========= STEP 4: Hybrid QA Prompt =========
final_prompt = PromptTemplate(
    input_variables=["context", "graph_knowledge", "question"],
    template="""
You are a wizarding expert helping users with detailed answers about *Harry Potter and the Prisoner of Azkaban*.

You are given:
- Context from the book
- Factual relationships from a knowledge graph

### Context from Book:
{context}

### Facts from Graph:
{graph_knowledge}

### Question:
{question}

Use both the book context and graph knowledge to answer in under 150 words. If one of them is missing, use the other.
Respond creatively like a wizard from Hogwarts!
"""
)

hybrid_chain = LLMChain(llm=llm_openai, prompt=final_prompt)

# ========= STEP 5: Hybrid QA Function =========
def get_query_and_response(query):
    # Get vector-based context
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # Get graph-based relationships
    try:
        graph_knowledge = graph_chain.run(query)
    except Exception as e:
        graph_knowledge = "Graph response unavailable."

    # Generate hybrid response
    answer = hybrid_chain.run({
        "context": context,
        "graph_knowledge": graph_knowledge,
        "question": query
    })

    return answer

# ======== TEST QUERY ========
if __name__ == "__main__":
    test_question = "Who gave Harry the Marauder's Map and what does it do?"
    response = get_query_and_response(test_question)
    print(response)
