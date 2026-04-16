from dotenv import load_dotenv
import streamlit as st

from agent import creer_agent, creer_tools

load_dotenv()

st.set_page_config(page_title="Agent LangChain", page_icon="🤖", layout="wide")
st.title("Agent LangChain")
st.caption("Interface conversationnelle Streamlit")


@st.cache_resource
def get_agent():
    return creer_agent()


@st.cache_resource
def get_tools():
    return creer_tools()


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.subheader("Outils disponibles")
    for tool in get_tools():
        st.markdown(f"**{tool.name}**")
        st.caption(tool.description)

    st.divider()
    if st.button("Réinitialiser la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            try:
                result = get_agent().invoke({"input": prompt})
                answer = result.get("output", "Aucune réponse générée.")
            except Exception as exc:
                answer = f"Erreur lors de l'exécution de l'agent : {exc}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
