import os, time
import streamlit as st
from streamlit_chat import message
from rag import RagOpr

ragOprRef = RagOpr()

st.set_page_config(page_title="iris-RAG-Gen",layout="wide")

#Function used to refresh the page
def refresh_page():
    st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)

def display_messages():    
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))

def process_input(id):
    if 'OPENAI_API_KEY' not in st.session_state:
        st.warning('Please enter OpenAI API key!', icon='⚠')       
    else:    
        if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
            user_text = st.session_state["user_input"].strip()
            with st.spinner(f"Thinking about {user_text}"):                
                time.sleep(1) # help the spinner to show up
            agent_text = ragOprRef.ragSearch(user_text,id)

            st.session_state["messages"].append((user_text, True))
            st.session_state["messages"].append((agent_text, False))

def process_openAI():
    if 'OPENAI_API_KEY' not in st.session_state:
        st.warning('Please enter OpenAI API key!', icon='⚠')        
    else:        
        if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
            user_text = st.session_state["user_input"].strip()
            with st.spinner(f"Thinking about {user_text}"):                
                time.sleep(1) # help the spinner to show up
            agent_text = ragOprRef.openAI(user_text)

            st.session_state["messages"].append((user_text, True))
            st.session_state["messages"].append((agent_text, False))



def deleteDoc(id):
    #Delete document from database
    with st.spinner(f"Please wait, Deleting Document"):               
           ragOprRef.delete_document(id)
        
    #Refresh the page
    refresh_page()

def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []   
    
    st.header("iris-RAG-Gen Application")
    
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    # Check if the key was successfully retrieved
    if openai_api_key:
        st.session_state["OPENAI_API_KEY"] = openai_api_key
    
    #SideBar 
    st.sidebar.markdown(
        "## How to use\n"
        "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        "2. Select file to Injest📄\n"
        "3. Enter Description and Clink Injest📄\n"
        "4. Select Document and Chat💬\n"
     )
    
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
    
    # file uploader widget, Allow only PDF and TXT Documents
    st.sidebar.markdown("---")    
    uploaded_file = st.sidebar.file_uploader('Ingest document (PDF or TXT):', type=["txt", "pdf"], accept_multiple_files=False)
   
    # Ingest Document, if the user uploaded files and clicked the add data button
    if uploaded_file:         
        description = st.sidebar.text_input("Enter a description for the file")

        # check emply value    
        if description:
            add_data = st.sidebar.button('Ingest Document', key='add_data')
            if add_data:                
            # check if the API key is not valid
                if not api_key_input:
                    st.warning('Please enter OpenAI API key!', icon='⚠')
                    st.stop()
                #Get file type
                file_type = uploaded_file.type
                uploaded_dir = "/irisdev/app/docs"
                for file in uploaded_file:   
                    file_path = os.path.join(uploaded_dir, uploaded_file.name)            
                    with open(file_path, mode='wb') as w:
                        w.write(uploaded_file.getvalue())           
                    
                with st.spinner(f"Please wait, Ingesting Document"):      
                    #Ingest document
                    ragOprRef.ingestDoc(file_path,description,file_type)                  
                #Refresh the page after ingesting document    
                refresh_page()    
      
    
    #Check if documents are injested
    docCount = ragOprRef.get_rag_count()
    selectOption = 0
    #init confirm delete session state
    if 'confirm_delete' not in st.session_state:
        st.session_state.confirm_delete = False
    #Select OpenAI option if no document is ingested,
    #Otherwise select document    
    if docCount > 0:
        selectOption = 1
    
    st.sidebar.markdown("---")
    rb = st.sidebar.radio(
    "Select Chat Option",
    ('OpenAI','Select Document'),index=selectOption)    
    #init selection variable
    st.session_state['rb'] = rb
    if rb == 'Select Document':
        selected_doc = st.sidebar.selectbox("Documents", ragOprRef.get_rag_documents_desc()) 
        #Reset user_input
        if 'user_input' in st.session_state:
            st.session_state.user_input = ""           
        if selected_doc:        
            parts = selected_doc.split(":", 1)
            selected_id = parts[0] 
            selected_doc = parts[1]                     
            st.subheader("🦜🔗 Chat with '"+ selected_doc +"' Document:")
            st.text_input("Ask a question :", key="user_input", on_change=lambda: process_input((selected_id)))
            #Delete Document 
            # Delete button with icon
            if st.sidebar.button("🗑️ Delete Selected Document"):
                st.session_state.confirm_delete = True
            # Show confirmation dialog
            if st.session_state.confirm_delete:
                st.sidebar.write(f"Are you sure to delete the document with ID {selected_id}?")
                if st.sidebar.button("Yes, Delete"):
                    deleteDoc(selected_id)
                    
    else:
        if 'user_input' in st.session_state:
            st.session_state.user_input = ""           
        
        st.subheader("🦜🔗 OpenAI Chat:")       
        st.text_input("Chat with OpenAI:", key="user_input", on_change=process_openAI)
    
    display_messages()
if __name__ == "__main__":
    page()