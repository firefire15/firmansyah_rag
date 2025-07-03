import re
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

class WisataAlamData():

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(self.base_dir, "data", "wisata_alam.txt")
        self.nama_file = self.file_path
        print(self.file_path)
        self.collection_name = "wisata_alam_collection"

    def cleaning_text(self):
        with open(self.nama_file, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace('\n', ' ')
        pattern = re.compile(r'''
            (?<!\d)\.(?=\s+[A-Z])   
        ''', re.VERBOSE)
        content = pattern.sub('<SP>', content)

        sentences = [sentence.strip() for sentence in content.split('<SP>') if sentence.strip()]

        return sentences

    def get_chunks(self, knowledge_base, chunk_size=400, chunk_overlap=70):
        text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=chunk_size, 
                        chunk_overlap=chunk_overlap, 
                        length_function=len
        )
        chunks = text_splitter.split_text("\n".join(knowledge_base))
        return chunks

    def get_ollama_embedding(self):
        embedding_Ollama = OllamaEmbeddings(model="nomic-embed-text:latest")
        return embedding_Ollama
    
    def get_vectorstore_chroma(self, chunks):
        try:
            vectorstore_chroma = Chroma.from_texts(
                texts=chunks,
                embedding=self.get_ollama_embedding(),
                persist_directory=".chroma_db",
                collection_name=self.collection_name
                )

            vectorstore_chroma.persist()
            return vectorstore_chroma
        except:
            raise

    def execute(self):
        knowledge_base = self.cleaning_text()
        chunks = self.get_chunks(knowledge_base=knowledge_base)
        vectorstore_chroma = self.get_vectorstore_chroma(chunks=chunks)
        return chunks, vectorstore_chroma
