from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.schema import Document
# import asyncio,logging
# from log import LoggerConfig
# logger_config = LoggerConfig()
# logger = logger_config.get_logger(__name__)

class Chunker():
    def __init__(self):
        self.chunk_size = 500
        self.chunk_overlap =300
        pass
    def split_chunking(content):
        try:        
            # Split the documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=550, chunk_overlap=300)
            documents = [Document(page_content=content)]
            #chunks = text_splitter.split_documents(documents)
            chunks = text_splitter.split_text(content)

            chunks = str(chunks).replace("\n", " ")
            
            documents = [
                Document(page_content=chunks, metadata={"title": "ram"}),
            ]
        
            return documents
        except Exception as e:
            print(f"Error splitting text: {e}")
            return None

    def semantic_chunking(content):
        try:
            # Split the documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=550, chunk_overlap=300)
            chunks = text_splitter.split_documents(docs)
            return chunks
        except Exception as e:
            print(f"Error splitting text: {e}")
            return None
        
    def sentence_chunking(content):
        try:
            # Split the documents into chunks
            text_splitter = SentenceTransformersTokenTextSplitter(language='english', chunk_size=550, chunk_overlap=300)
            chunks = text_splitter.split_documents(docs)
            return chunks
        except Exception as e:
            print(f"Error splitting text: {e}")
            return None
        
    async def create_batches(text, batch_size=5000):
        for i in range(0, len(text), batch_size):
            yield text[i:i + batch_size]
        
    def batch(text,batch_size=3000):
        try:
            batch_number = (len(text) + batch_size - 1) // batch_size 
            
            for i in range(batch_number):
                start_index = i * batch_size
                end_index = min((i + 1) * batch_size, len(text))
                batch = text[start_index:end_index]
                yield batch
        except Exception as e:
            return (f"Error managing Batches: {e}, {len(text)}")
        
##Testing

# from embeddings import embedder
#chunker=Chunker()
if __name__ == "__main__":
    from file_loaders import FileLoader
    file="../uploads/ram.pdf"
    
    content=FileLoader.load_file(file)
    
    doc=Chunker.split_chunking(content)

    print("...", doc)
