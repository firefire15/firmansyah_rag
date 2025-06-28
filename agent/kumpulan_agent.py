from search_location_rag import SearchLocation
from wisata_kuliner_data import WisataKulinerData
from wisata_pendidikan_data import WisataPendidikanData
from wisata_sejarah_budaya_data import WisataSejarahBudayaData
from wisata_alam_data import WisataAlamData
from wisata_sejarah_budaya_rag import WisataSejarahBudayaAgent
from wisata_kuliner_rag import WisataKulinerAgent
from wisata_pendidikan_rag import WisataPendidikanAgent
from wisata_alam_rag import WisataAlamAgent
from typing import TypedDict, Annotated
from operator import add
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class KumpulanAgent():

    def __init__(self):
        self.wisata_alam_data = WisataAlamData()
        self.wisata_alam = WisataAlamAgent()
        self.wisata_kuliner_data = WisataKulinerData()
        self.wisata_kuliner = WisataKulinerAgent()
        self.wisata_pendidikan_data = WisataPendidikanData()
        self.wisata_pendidikan = WisataPendidikanAgent()
        self.wisata_sejarah_budaya_data = WisataSejarahBudayaData()
        self.wisata_sejarah_budaya = WisataSejarahBudayaAgent()
        self.search_location = SearchLocation()

    def wisata_alam_agent(self, input_):
        chunks, vectorstore_chroma = self.wisata_alam_data.execute()
        print("input : ", input_)
        result = self.wisata_alam.execute(query=input_['query'], chunks=chunks, vectorstore_chroma=vectorstore_chroma)
        return {'w_a': result}
    def wisata_kuliner_agent(self, input_):
        chunks, vectorstore_chroma = self.wisata_kuliner_data.execute()
        result = self.wisata_kuliner.execute(query=input_['query'], chunks=chunks, vectorstore_chroma=vectorstore_chroma)
        return {'w_k': result}
    def wisata_pendidikan_agent(self, input_):
        chunks, vectorstore_chroma = self.wisata_pendidikan_data.execute()
        result = self.wisata_pendidikan.execute(query=input_['query'], chunks=chunks, vectorstore_chroma=vectorstore_chroma)
        return {'w_p': result}
    def wisata_sejarah_budaya_agent(self, input_):
        chunks, vectorstore_chroma = self.wisata_sejarah_budaya_data.execute()
        result = self.wisata_sejarah_budaya.execute(query=input_['query'], chunks=chunks, vectorstore_chroma=vectorstore_chroma)
        return {'w_sb': result}
    def lokasi_agent(self, input_):
        result = self.search_location.execute(query=input_['query'])
        return {'location': result}
    
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    fnb: Annotated[list[str], add]
    weather: str

# Schema config
class Config(TypedDict):
    region: str

