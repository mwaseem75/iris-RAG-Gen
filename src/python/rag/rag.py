from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
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
        self.engine = create_engine(self.CONNECTION_STRING)
        #self.conn = engine.connect()
        
    def get_rag_count(self):   
            
        with self.engine.connect() as conn:
            with conn.begin():     
                sql = text("""
                    SELECT TOP 1 * from rag_documents
                    """)
                results = []
                try:
                    results = conn.execute(sql).fetchall()
                except Exception as e:
                    print(e)
                    
        return len(results)
    
    def get_rag_documents_desc(self):
        with self.engine.connect() as conn:
            with conn.begin():     
                sql = text("""
                    SELECT id||': '||description as docs FROM SQLUser.rag_documents order by id
                    """)
                results = []
                try:
                    results = conn.execute(sql).fetchall()
                except Exception as e:
                   print(e)

        descriptions = [row[0] for row in results]       
        return descriptions


    def get_collection_name(self,fileDesc,fileType):
        # check if rag_documents table exists, if not then create it 
        with self.engine.connect() as conn:
            with conn.begin():     
                sql = text("""
                    SELECT *
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = 'SQLUser'
                    AND TABLE_NAME = 'rag_documents';
                    """)
                result = []
                try:
                    result = conn.execute(sql).fetchall()
                except Exception as err:
                    print("An exception occurred:", err)               
                    return ''       
                #if table is not created, then create rag_documents table first
                if len(result) == 0:
                    sql = text("""
                        CREATE TABLE rag_documents (
                        description VARCHAR(255),
                        docType VARCHAR(50) )
                        """)
                    try:    
                        result = conn.execute(sql) 
                    except Exception as err:
                        print("An exception occurred:", err)                
                    return ''
       
        #Insert description value 
        with self.engine.connect() as conn:
            with conn.begin():     
                sql = text("""
                    INSERT INTO rag_documents 
                    (description,docType) 
                    VALUES (:desc,:ftype)
                    """)
                try:    
                    result = conn.execute(sql, {'desc':fileDesc,'ftype':fileType})
                except Exception as err:
                    print("An exception occurred:", err)                
                    return ''

                #select ID of last inserted record
                sql = text("""
                    SELECT LAST_IDENTITY()
                """)
                try:
                    result = conn.execute(sql).fetchall()
                except Exception as err:
                    print("An exception occurred:", err)
                    return ''
              
        return "rag_document"+str(result[0][0])

    def ingestDoc(self,filePath,fileDesc,fileType):                

        embeddings = OpenAIEmbeddings()	
        #Load the document based on the fle type
        if fileType == "text/plain":
            loader = TextLoader(filePath)       
        elif fileType == "application/pdf":
            loader = PyPDFLoader(filePath)       
        
        print(loader)
        documents = loader.load()        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)
        
        #texts = text_splitter.split_text(documents)
        texts = text_splitter.split_documents(documents)
        
        COLLECTION_NAME = self.get_collection_name(fileDesc,fileType)

        #COLLECTION_NAME = "rag_document"
        db = IRISVector.from_documents(
            embedding=embeddings,
            documents=texts,
            collection_name = COLLECTION_NAME,
            connection_string=self.CONNECTION_STRING,
        )
    
    def ragSearch(self,prompt,id):
        COLLECTION_NAME = "rag_document"+str(id)
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
    
    def delete_document(self,docID):
        # check if rag_documents table exists, if not then create it 
        with self.engine.connect() as conn:
            with conn.begin():     
                sql = text("""
                    DELETE FROM rag_documents
                    WHERE ID = :id;
                """)
                try:    
                    result = conn.execute(sql, {'id': docID})
                except Exception as err:
                    print("An exception occurred:", err)                
                    return ''

                #select ID of last inserted record
                table_name = "rag_document"+str(docID)
                sql = "DROP TABLE "+ table_name                
                try:
                    result = conn.execute(text(sql))
                except Exception as err:
                    print("An exception occurred:", err)
                    return ''
              
        return 'Table delete successfully'