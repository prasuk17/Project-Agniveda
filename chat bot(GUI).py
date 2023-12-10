from tkinter import *
import warnings
import os
from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper
from langchain import OpenAI
import openai
import sys
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key  =  os.environ["OPENAI_API_KEY"]
from llama_index import ServiceContext,StorageContext,load_index_from_storage
warnings.filterwarnings("ignore")

def createIndex(path):
    max_input = 4096
    tokens = 256
    chunk_size = 600              
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

createIndex('Knowledge')

def answerMe(question):
    storage_context = StorageContext.from_defaults(persist_dir = 'stored')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
bot_name = "Veda"

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        msg2 = f"{bot_name}: {answerMe(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()

