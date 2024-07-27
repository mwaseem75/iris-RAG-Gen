from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_iris import IRISVector
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from sqlalchemy import create_engine,text
import os


class RagOpr:
    def __init__(self, host='localhost', port=1972, namespace='USER', username='SuperUser', password='SYS') -> None:          
        self.CONNECTION_STRING = f"iris://{username}:{password}@{host}:{port}/{namespace}"
        engine = create_engine(self.CONNECTION_STRING)
        self.conn = engine.connect()
        
    def get_rag_count(self):
        
        sql = text("""
            SELECT TOP 1 * from rag_document
            """)
        results = []
        try:
            results = self.conn.execute(sql).fetchall()
        except Exception as e:
            pass
                    
        return len(results)
    
    def ingestDoc(self):      

        embeddings = OpenAIEmbeddings()	
        loader = PyPDFLoader('/irisdev/app/docs/GEPYTHON.pdf')       
        documents = loader.load()
        print(documents)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        
        COLLECTION_NAME = "rag_document"
        db = IRISVector.from_documents(
            embedding=embeddings,
            documents=texts,
            collection_name=COLLECTION_NAME,
            connection_string=self.CONNECTION_STRING,
        )
    
    def ragSearch(self,prompt):
        COLLECTION_NAME = "rag_document"
        embeddings = OpenAIEmbeddings()	
        db2 = IRISVector (
            embedding_function=embeddings,    
            collection_name=COLLECTION_NAME,
            connection_string=self.CONNECTION_STRING,
        )
        docs_with_score = db2.similarity_search_with_score(prompt)
        relevant_docs = ["".join(str(doc.page_content)) + " " for doc, _ in docs_with_score]
        llm = ChatOpenAI(
            temperature=0,    
            model_name="gpt-3.5-turbo"
        )
        conversation_sum = ConversationChain(
            llm=llm,
            memory= ConversationSummaryMemory(llm=llm),
            verbose=False
        )
        
        template = f"""
        Prompt: {prompt}

        Relevant Docuemnts: {relevant_docs}
        """

        resp = conversation_sum(template)
        return resp['response']

    def openAI(self,prompt):
        MODEL = "gpt-3.5-turbo"
        apiKey = os.environ.get('OPENAI_API_KEY')
	    #llm
        try:
            llm = ChatOpenAI(temperature=0,openai_api_key=apiKey, model_name=MODEL, verbose=False) 
		    #Conversational memory is how a chatbot can respond to multiple queries
            entity_memory = ConversationEntityMemory(llm=llm, k=10 )
            qa = ConversationChain(llm=llm,   prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE, memory=entity_memory)
            ret = '\n'+qa.run(prompt)+'\n'
        except Exception as e:  
            print(e)
            
        return ret