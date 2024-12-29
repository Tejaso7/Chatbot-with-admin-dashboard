from file_loaders import FileLoader
from text_chunkers import Chunker
from create_vectors import Chromadb

chroma=Chromadb()

def create_db(file):
    try:
        content=FileLoader.load_file(file)
        chunks=Chunker.split_chunking(content)
        for item in Chunker.batch(chunks):
            chroma.add_docs(item)
        return "Database created successfully"
    except Exception as e:
        return f"Error creating database: {e}"
    
    
def generate_response(query):
    
    
    pass

if __name__ == "__main__":
    file="../uploads/ram.pdf"
    vectordb=create_db(file)
    print(vectordb)
    