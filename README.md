# Summary
Iris-RAG-Gen is a generative AI Retrieval-Augmented Generation (RAG) application that leverages the functionality of IRIS Vector Search to personalize ChatGPT with the help of the Streamlit web framework, LangChain, and OpenAI. The application uses IRIS as a vector store. 

RAG is a powerful AI model that combines the strengths of retrieval-based and generative models. It leverages a pre-trained language model to generate responses based on retrieved documents, enabling more accurate and context-aware answers.

[![one](https://img.shields.io/badge/Platform-InterSystems%20IRIS-blue)](https://www.intersystems.com/data-platform/) [![one](https://img.shields.io/badge/LLM-GPT%203-Purple)](https://openai.com/index/gpt-3-apps/) [![one](https://img.shields.io/badge/Framework-Langchain-teal)](https://www.langchain.com/) [![one](https://img.shields.io/badge/WebFrameWork-Streamlit-Orange)](https://streamlit.io/) [![one](https://img.shields.io/badge/VectorStore-IRIS-blue)](https://www.intersystems.com/data-platform/) [![one](https://img.shields.io/badge/ORM-SQLAlchemy-teal)](https://www.sqlalchemy.org/)  [![one](https://img.shields.io/badge/OpenAI-ChatGPT-yellow)](https://openai.com/) [![OEX](https://img.shields.io/badge/Available%20on-Intersystems%20Open%20Exchange-00b2a9.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE) [![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE)
<img width="910" alt="image" src="https://github.com/user-attachments/assets/9882a6c3-f66a-4330-8f4f-1d3ebc77f349">

# Application Interface
![image](https://github.com/user-attachments/assets/486b1a90-5b5c-4d6a-8da4-b184dcf87e1e)

# Features
* Ingest Documents (PDF or TXT) into IRIS
* Chat with the selected Ingested document 
* Delete Ingested Documents
* OpenAI ChatGPT

# Installation
1. Clone/git pull the repo into any local directory

```
git clone https://github.com/mwaseem75/iris-RAG-Gen.git
```

2. Open a Docker terminal in this directory and run:

```
docker-compose build
```

3. Run the IRIS container:

```
docker-compose up -d 
```
# Getting Started 
## Get OpenAI Key
Application requires OpenAI API Key, sign up for OpenAI API on [this page](https://platform.openai.com/account/api-keys). Once you have signed up and logged in, click on Personal, and select View API keys in drop-down menu. Create and copy the API Key

![image](https://github.com/mwaseem75/irisChatGPT/assets/18219467/7e7c7880-b9ac-4a60-9ec9-289dd2375a73)

## Run Streamlit Web Application
To run the application Navigate to [**http://localhost:8051**](http://localhost:8051) 

Follow the Below Steps to Ingest the document:
* Enter OpenAI Key
* Select Document (PDF or TXT)
* Enter Document Description
* Click on the Ingest Document Button

![image](https://github.com/user-attachments/assets/4a1ca5b2-8eb3-432d-ace9-4e7374ee768d)

Once the Document is Ingested, Select the document from 'Select Chat Option'
![image](https://github.com/user-attachments/assets/d616c313-97cd-4313-aade-5f9ac80572b3)

Select the Document and press enter. The application will read the vector data and return the relevant answer
![image](https://github.com/user-attachments/assets/522b9381-bbed-4ffb-b729-61e967384c04)
  
To delete the Ingested document, Press the 'Delete selected Document' Button, Once confirmed, the Document will be deleted.
![image](https://github.com/user-attachments/assets/d56585f9-3d5f-4b85-a473-10a28046bc8f)


## View Data
Navigate to the Management Portal SQL [(http://localhost:53795/csp/sys/exp/%25CSP.UI.Portal.SQL.Home.zen?$NAMESPACE=USER)](http://localhost:53795/csp/sys/exp/%25CSP.UI.Portal.SQL.Home.zen?$NAMESPACE=USER) to view Vector Data [SuperUser | SYS]

Documents Description is saved in the 'rag_documents' table.
Type the below SQL command to retrieve the data
```
SELECT 
id, description, docType
FROM SQLUser.rag_documents
```
![image](https://github.com/user-attachments/assets/6c5c9b02-72aa-4348-9abe-694a3141e344)

The vector data is saved in 'rag_document + id' table. (id of the rag_documents)
![image](https://github.com/user-attachments/assets/0ff66ce7-b48e-4b68-a24a-7233710a12e0)


Type the below SQL command to retrieve vector data
```
SELECT top 5
id, embedding, document, metadata
FROM SQLUser.rag_document2
```
![image](https://github.com/user-attachments/assets/950f9e04-6acf-4673-bff1-0d7d0965c8a8)


For OpenAI Chat, Select OpenAI option from 'Select Chat Option'
![image](https://github.com/user-attachments/assets/d598e6bc-8ebb-469a-82a5-e26c4d3bd35a)


