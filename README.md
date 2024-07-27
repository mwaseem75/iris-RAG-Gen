# Summary
Iris-RAG-Gen is a generative AI Retrieval-Augmented Generation (RAG) application that leverages the functionality of IRIS Vector Search to personalize ChatGPT with the help of the Streamlit web framework, LangChain, and OpenAI. The application uses IRIS as a vector store. 

RAG is a powerful AI model that combines the strengths of retrieval-based and generative models. It leverages a pre-trained language model to generate responses based on retrieved documents, enabling more accurate and context-aware answers.

[![one](https://img.shields.io/badge/Platform-InterSystems%20IRIS-blue)](https://www.intersystems.com/data-platform/) [![one](https://img.shields.io/badge/LLM-GPT%203-Purple)](https://openai.com/index/gpt-3-apps/) [![one](https://img.shields.io/badge/Framework-Langchain-teal)](https://www.langchain.com/) [![one](https://img.shields.io/badge/WebFrameWork-Streamlit-Orange)](https://streamlit.io/) [![one](https://img.shields.io/badge/VectorStore-IRIS-blue)](https://www.intersystems.com/data-platform/) [![one](https://img.shields.io/badge/ORM-SQLAlchemy-teal)](https://www.sqlalchemy.org/)  [![one](https://img.shields.io/badge/OpenAI-ChatGPT-yellow)](https://openai.com/) [![OEX](https://img.shields.io/badge/Available%20on-Intersystems%20Open%20Exchange-00b2a9.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE) [![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mwaseem75/iris-RAG-Gen/blob/main/LICENSE)
<img width="825" alt="image" src="https://github.com/user-attachments/assets/1b108ff9-351e-441f-ac9b-b1533904cfc4">



# Features
* Ingest Vector Data in IRIS
* Personalize ChatGPT
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
Application requires OpenAI API Key, sign up for OpenAI API on [this page](https://platform.openai.com/account/api-keys). Once you signed up and logged in, click on Personal, and select View API keys in drop-down menu. Create and copy the API Key

![image](https://github.com/mwaseem75/irisChatGPT/assets/18219467/7e7c7880-b9ac-4a60-9ec9-289dd2375a73)

## Run Streamlit Web Application
To run the application Navigate to [**http://localhost:8051**](http://localhost:8051) 

Click on the Ingest Document button to Store [Embedded Python](https://docs.intersystems.com/iris20231/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON) PDF Document 
<img width="955" alt="image" src="https://github.com/user-attachments/assets/d4c704b3-f5f9-427b-b87b-5770eb97d9a8">

Navigate to the Management Portal SQL [(http://localhost:53795/csp/sys/exp/%25CSP.UI.Portal.SQL.Home.zen?$NAMESPACE=USER)](http://localhost:53795/csp/sys/exp/%25CSP.UI.Portal.SQL.Home.zen?$NAMESPACE=USER) to view Vector Data [SuperUser | SYS]
<img width="947" alt="image" src="https://github.com/user-attachments/assets/ab35e8a9-9582-42a7-8e8c-4c8f2dd55b5a">

Once ingested, the application is ready to chat with the document. 
<img width="956" alt="image" src="https://github.com/user-attachments/assets/db8c144c-3c35-4521-bca6-e9910b7cbc81">

Click OpenAI radio button form OpenAI Chat
<img width="953" alt="image" src="https://github.com/user-attachments/assets/8a4edf79-de3b-455c-b186-7cf1687ae977">

