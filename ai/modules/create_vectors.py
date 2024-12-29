from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import pathlib
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
    
class Chromadb():
    
    def __init__(self, collection_name="Information", persist_directory=os.getenv("DATABASE_PATH")):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Ensure the directory exists
        pathlib.Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize Embedding Model
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key)
        
        # Initialize or load persistent Chroma vectorstore
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
    
    def add_text(self, documents):
        """
        Adds a list of text chunks to the vectorstore and persists it.
        """
  
        self.vectorstore.add_texts(texts=documents, metadatas="DownSyndrome")
        #self.vectorstore.persist()
        return f"Successfully added chunks to the vectorstore."
    
    def add_docs(self, documents_content, metadatas="ADHD"):
        """
        Adds a list of document chunks to the vectorstore and persists it.
        Each chunk is converted to a Document object.
        """
        # if metadata_list is None:
        #     metadata_list = [{} for _ in chunks]  # Create empty metadata if none provided
        
        # # Convert chunks into Documents
        # documents = [Document(page_content=documents_content, metadata=metadatas) 
        #             for documents_content, metadata in zip(documents_content, metadatas)]
        
        self.vectorstore.add_documents(documents=documents_content)
        return f"Successfully added documents to the vectorstore."


    def search(self):
        """
        Searches the vectorstore for the most relevant results to the query.
        """
        #results= self.vectorstore.similarity_search(query, k=5)   #similarity_search(query, k=k) as_retriever(search_type="mmr", search_kwargs={"k": 5}) 
        results= self.vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5}) 

        print(f"result of similarity search is: {results}")
        return results
    
    
    # def __init__(self):
    #     openai_api_key = os.getenv('OPENAI_API_KEY')
    #     #self.file_path = os.makedirs(os.getenv("DATABASE_PATH"), exist_ok=True) # "../vectorstore/chroma_db"

    #     # Initialize Embedding Model
    #     self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    #     #self.vectorstore = Chroma(embedding_function=self.embeddings,persist_directory=self.file_path)
        
    # def add_text(self,chunks,file_path):
    #     vectorstore = Chroma(collection_name="conditions",embedding_function=self.embeddings,persist_directory=file_path)
    #     vectorstore.add_texts(texts=chunks)
    #     return vectorstore

    # def connect_to_existing_chroma_db(self):
    #     persist_directory =os.getenv("DATABASE_PATH")
    #     if not os.path.isdir(persist_directory):
    #         raise FileNotFoundError(f"Database directory not found: {persist_directory}")
        
    #     settings = Settings(persist_directory=persist_directory)
    #     return Client(settings)
        
        
        
        
        
        
    # def add_document(self,collection_name,documents,uuids):
    #     vectorstore = Chroma(collection_name=collection_name,embedding_function=self.embeddings,persist_directory=self.file_path)
    #     #uuids = [str(uuid4()) for _ in range(len(documents))]
    #     vectorstore.add_texts(documents=documents, ids=uuids)
    #     return "Created a Vectorstore Successfully."
    # def update(self,chunks):
    #     vectorstore = Chroma(embedding_function=self.embeddings,persist_directory=self.file_path)
    #     vectorstore.update_texts(texts=chunks)
    #     vectorstore.persist()
    #     return "Updated a Vectorstore Successfully."
    

if __name__ == "__main__":
    chroma = Chromadb()
    file= "../uploads/ram.pdf"
    doc,meta=Chunker.split_chunking(file)
    #text = str(chunks).replace("\n", " ")    
    chroma.add_text(doc,meta)
    query = "about ram"
    results = chroma.search(query)