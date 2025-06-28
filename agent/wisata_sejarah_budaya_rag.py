from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain # Untuk HyDE
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers.bm25 import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from wisata_sejarah_budaya_data import WisataSejarahBudayaData

from dotenv import dotenv_values

class WisataSejarahBudayaAgent():
    def __init__(self):
        self.collection_name = "wisata_sejarah_budaya_collection"
        config = dotenv_values(".env")
        self.gemini_api_key = config.get("GEMINI_API_KEY","AIzaSyCLcqeBq3Q0gIa-frAZI-qrx0_twYOXeq0")
        self.gemini_model = config.get("MODEL_NAME","gemini-2.5-flash")

    def augment_prompt(self, query_text, context_string):
        """Augment the query with retrieved documents."""
        prompt_template = f'''
            Anda adalah asisten AI yang bertugas sebagai orang yang mempromosikan tempat bersejarah dan kebudayaan di Kota Bandung.
            Tugas Anda adalah mencari pengetahuan berdasarkan pertanyaan atau konteks yang diberikan oleh tour guide atau pengarah wisatawan.
            Jika anda tidak mengetahui jawabannya yang sesuai konteks, maka jangan mencoba mengarang jawaban.

            pengetahuan yang didapatkan:
            ---
            {context_string}
            ---

            fakta Pengguna:
            {query_text}

            Jawaban hanya berdasarkan konteks di atas, jawablah dengan jelas dan sopan agar mereka mengerti:
        '''

        return prompt_template.strip() 
    
    def get_ollama_embedding(self):
        embedding_Ollama = OllamaEmbeddings(model="nomic-embed-text:latest")
        return embedding_Ollama

    def get_dense_retriever(self, vectorstore_chroma):
        dense_retriever = vectorstore_chroma.as_retriever(search_kwargs={"k": 5})
        return dense_retriever

    def get_bm25_retriever(self, chunks):
        bm25_retriever = BM25Retriever.from_texts(
        texts=chunks, 
        embedding=self.get_ollama_embedding()
        )
        return bm25_retriever
    
    def get_ensemble_retirever(self, chunks, vectorstore_chroma):
        ensemble_retriever = EnsembleRetriever(
                retrievers=[self.get_dense_retriever(vectorstore_chroma=vectorstore_chroma), self.get_bm25_retriever(chunks)],
                weights=[0.5, 0.5]
        )
        return ensemble_retriever

    def ensemble_retriever(self, query, chunks, vectorstore_chroma):
        ensemble_retriever = self.get_ensemble_retirever(chunks, vectorstore_chroma)
        results = ensemble_retriever.invoke(query)
        return results
    
    def execute(self, query, chunks, vectorstore_chroma):
        results = self.ensemble_retriever(query, chunks, vectorstore_chroma)
        context = "\n\n".join([doc.page_content for doc in results])
        
        final_prompt = self.augment_prompt(query, context)
        #print("Memulai proses generasi...")
        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel(self.gemini_model)
        response = model.generate_content(final_prompt)

        return response.text

if __name__ == "__main__":
    waa = WisataSejarahBudayaAgent()
    query = "Jelaskan Mengenai Konferensi Asia Afrika"
    results = waa.execution(query=query)
    print(results)