import os
import time
import streamlit as st
from streamlit_chat import message
from util import RagOpr

ragOprRef = RagOpr()
st.set_page_config(page_title="iris-RAG-Gen")


def display_messages():    
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))


def process_input():
    if not st.session_state["OPENAI_API_KEY"].startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    else:
        
        if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
            user_text = st.session_state["user_input"].strip()
            with st.spinner(f"Thinking about {user_text}"):                
                time.sleep(1) # help the spinner to show up
            agent_text = ragOprRef.ragSearch(user_text)

            st.session_state["messages"].append((user_text, True))
            st.session_state["messages"].append((agent_text, False))

def process_openAI():
    if not st.session_state["OPENAI_API_KEY"].startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    else:
        
        if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
            user_text = st.session_state["user_input"].strip()
            with st.spinner(f"Thinking about {user_text}"):                
                time.sleep(1) # help the spinner to show up
           
            agent_text = ragOprRef.openAI(user_text)

            st.session_state["messages"].append((user_text, True))
            st.session_state["messages"].append((agent_text, False))


def ingestDoc():
    if not st.session_state["OPENAI_API_KEY"].startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    else:
        with st.spinner(f"Please wait, Ingesting Document"):
            ragOprRef.ingestDoc()
                
        
        docCount = ragOprRef.get_rag_count()
        if docCount > 0:
            st.session_state["messages"].append(
                ("Document successfully ingested", False)
            )
        else:
            st.session_state["messages"].append(
                ("Error while Ingesting Document", False)
            )

def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        #_service.clear()
    
    st.header("iris-RAG-Gen Application")

    st.sidebar.markdown(
        "## How to use\n"
        "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        "2. Ingest the document from below📄"       
    )

    openai_api_key = os.environ.get('OPENAI_API_KEY')
    # Check if the key was successfully retrieved
    if openai_api_key:
        st.session_state["OPENAI_API_KEY"] = openai_api_key
    
    api_key_input = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )
    if api_key_input:
        st.session_state["OPENAI_API_KEY"] = api_key_input
        os.environ['OPENAI_API_KEY']  = api_key_input

    st.sidebar.markdown("---")
           
    st.sidebar.title("Embedded Python Doc")   
    docCount = ragOprRef.get_rag_count()
   
    if docCount > 0:
        st.sidebar.subheader("Document Ingested")          
    else:
        if st.sidebar.button("Ingest Document"):
            ingestDoc()
       
    st.sidebar.markdown("---")
        
    if docCount > 0:
        rb = st.sidebar.radio(
        "## Select Chat option",
        ('Embedded Python Document','OpenAI'))    
        #init selection variable
        st.session_state['rb'] = rb
        if rb == 'Embedded Python Document':
            st.subheader("🦜🔗 Chat with Embedded Python Document:")
            st.text_input("Ask a question about [Embedded Python](https://docs.intersystems.com/iris20231/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON) :", key="user_input", on_change=process_input)
        else:
            st.subheader("🦜🔗 OpenAI Chat:")
            #CreateNewFunctionLater
            st.text_input("Ask any question:", key="user_input", on_change=process_openAI)
    else:
        st.subheader("🦜🔗 OpenAI Chat:")
        #CreateNewFunctionLater
        st.text_input("Ask any question:", key="user_input", on_change=process_openAI)
    display_messages()
if __name__ == "__main__":
    page()