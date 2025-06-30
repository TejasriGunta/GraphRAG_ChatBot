import streamlit as st
from rag import get_query_and_response as get_response

st.title("🧙 Harry Potter ChatBot")
st.caption("Ask a question about *Harry Potter and the Prisoner of Azkaban*.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.last_graph_knowledge = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Welcome to the world of WIZARDRY, enter your question here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = get_response(prompt)
    response_str = str(response)

    with st.chat_message("assistant"):
        st.markdown(response_str)
    st.session_state.messages.append({"role": "assistant", "content": response_str})

    # Save last retrieved graph knowledge for optional display
    if isinstance(response, dict) and "graph_knowledge" in response:
        st.session_state.last_graph_knowledge = response["graph_knowledge"]
    else:
        st.session_state.last_graph_knowledge = "Graph knowledge not available or extracted separately."

if st.checkbox("Show Retrieved Graph Entities"):
    st.subheader("Retrieved Knowledge Graph Entities")
    st.markdown(st.session_state.last_graph_knowledge if st.session_state.last_graph_knowledge else "No graph knowledge retrieved yet.")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.last_graph_knowledge = ""
