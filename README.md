## GraphRAG_ChatBot
harry potter chatbot which answers questions using a knowledge graph

This project is an interactive chatbot that answers questions about *Harry Potter and the Prisoner of Azkaban* by combining:
- **Semantic retrieval using FAISS and HuggingFace embeddings** to find relevant context from the book.
- **A knowledge graph in Neo4j** containing structured entities and relationships (characters, spells, locations, events, etc.).
- **GPT-4o via OpenAI** to generate clear, engaging responses that combine structured facts and unstructured book content.
- **Streamlit interface** for a clean, conversational user experience.

The chatbot allows users to explore the book deeply while understanding connections between characters, locations, and magical elements through a structured retrieval pipeline.

Demo run-

![Uploading Untitled video - Made with Clipchamp.gif…]()


# What is a Knowledge Graph?
A **knowledge graph** represents entities (nodes) and relationships (edges) visually and structurally to capture real-world relationships. In this project, the Neo4j knowledge graph contains:
- Characters like Harry, Hermione, Ron, Sirius Black.
- Spells like Expecto Patronum.
- Locations like Hogwarts, Hogsmeade.
- Events like Shrieking Shack Confrontation or escape from the Azkaban prison.
- Relationships like "is a friend of", "is a teacher at", "cast spell on".

The knowledge graph created using Neo4j-

![Untitledvideo-MadewithClipchamp2-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/23e11cf4-4d2b-4e5d-8a3e-169e654d3078)


When a user asks a question, the system can:
- Retrieve facts directly from the graph.
- Combine these structured facts with detailed book context.
