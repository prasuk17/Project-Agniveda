#install gpt_index,langchain
#import warning
#warnings.filterwarnings("ignore")
import os
from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper
from langchain import OpenAI
import openai
#import Configuration
import sys
os.environ["OPENAI_API_KEY"] = "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"
#OpenAI.api_key = "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"
openai.api_key  =  os.environ["OPENAI_API_KEY"]
#key = "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"


from llama_index import ServiceContext,StorageContext,load_index_from_storage

def createIndex(path):
    max_input = 4096
    tokens = 256
    chunk_size = 600              #how much data should grab in one go.
    #max_chunk_overlap = 20
    
    prompthelper = PromptHelper(max_input,tokens,chunk_overlap_ratio= 0.1,chunk_size_limit = chunk_size)
    
    
    
    # define LLM 
    llmPredictor = LLMPredictor(llm=OpenAI(temprature=0,model_name="text-ada-001",max_tokens=tokens))
    
    # Load data
    docs = SimpleDirectoryReader(path).load_data()
    
    
    #create vector index
    service_context = ServiceContext.from_defaults(llm_predictor = llmPredictor,prompt_helper = prompthelper)
    vectorIndex = GPTVectorStoreIndex.from_documents(documents = docs,service_context = service_context)
    vectorIndex.storage_context.persist(persist_dir = 'stored')
    
    return vectorIndex

#createIndex('Knowledge')

def answerMe(question):
    storage_context = StorageContext.from_defaults(persist_dir = 'stored')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response




   
 
