
from operator import add
from typing import TypedDict
from typing_extensions import Annotated
from kumpulan_agent import KumpulanAgent
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableLambda
import re
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    query: str
    w_a : Annotated[list[AnyMessage], add_messages]
    w_k : Annotated[list[AnyMessage], add_messages]
    w_p : Annotated[list[AnyMessage], add_messages]
    w_sb: Annotated[list[AnyMessage], add_messages]
    location:Annotated[list[AnyMessage], add_messages]
    final_answer: Annotated[list[AnyMessage], add_messages]
    role:str
    content:Annotated[list[AnyMessage], add_messages]
    map:object


# Schema config
class Config(TypedDict):
    region: str

class TourGuideAgent():


    def __init__(self):
        pass

    def augment_prompt(query_text, context_string):
        """Augment the query with retrieved documents."""
        prompt_template = f'''
            Anda adalah asisten AI yang bertugas sebagai tour guide atau pengarah wisatawan.
            Tugas Anda adalah merangkum pengetahuan yang didapat dari asisten agent anda berdasarkan pertanyaan atau konteks yang diberikan oleh wisatawan.
            Jika seluruh asisten anda tidak mengetahui jawabannya, maka jangan mencoba mengarang jawaban.

            pengetahuan yang agent lain berikan:
            ---
            {context_string}
            ---

            fakta Pengguna:
            {query_text}

            Pertanyaan (hanya berdasarkan konteks di atas):
        '''

        return prompt_template.strip() 
    
    def select_relevant_node(self, state_):
        final_answers = []
        pattern = re.compile(r"(mohon maaf|tidak ditemukan)", re.IGNORECASE)

        for key, value in state_.items():
            if not isinstance(value, list):
                continue

            for item in value:
                print(item)
                if (isinstance(item, HumanMessage) and not pattern.search(item.content.lower().strip())): 
                    final_answers.append(item.content.strip())
                if (isinstance(item, AIMessage) and not pattern.search(item.content.lower().strip())): 
                    final_answers.append(item.content.strip())
        
        if len(final_answers) == 0:
             final_answers.append("maaf, Kami tidak memiliki informasi dari yang ditanyakan")

        return {"final_answer": final_answers, "map":state_["map"]}
    
    def execute(self, query):
        ka = KumpulanAgent()
        #print("query : ", query)
        builder = StateGraph(State, config_schema=Config)
        builder.add_node("wisata_alam", RunnableLambda(ka.wisata_alam_agent))
        builder.add_node("wisata_kuliner", RunnableLambda(ka.wisata_kuliner_agent))
        builder.add_node("wisata_pendidikan", RunnableLambda(ka.wisata_pendidikan_agent))
        builder.add_node("wisata_sejarah", RunnableLambda(ka.wisata_sejarah_budaya_agent))
        builder.add_node("pencarian_lokasi", RunnableLambda(ka.lokasi_agent))
        builder.add_node("relevant_node", RunnableLambda(self.select_relevant_node))
        builder.add_edge(START, "wisata_alam")
        builder.add_edge(START, "wisata_kuliner")
        builder.add_edge(START, "wisata_pendidikan")
        builder.add_edge(START, "wisata_sejarah")
        builder.add_edge(START, "pencarian_lokasi")
        builder.add_edge("wisata_alam", "relevant_node")
        builder.add_edge("wisata_kuliner", "relevant_node")
        builder.add_edge("wisata_pendidikan", "relevant_node")
        builder.add_edge("wisata_sejarah", "relevant_node")
        builder.add_edge("relevant_node", END)
        graph = builder.compile()
        # Invoke with initial state and config
        result = graph.invoke(
            input={"query":query, "messages": [], "w_a": [], "w_k": [], "w_p":[], "w_sb":[], "location":[], 'final_answer':[], "role":"user","content":[], "map":""}
        )
        #print("hasil", result)
        #print("message: ", result["messages"])
        #print("w_a: ", result["w_a"])
       # print("w_k: ", result["w_k"])
        #print("w_p: ", result["w_p"])
        #print("w_sb: ", result["w_sb"])
        return result

if __name__ == "__main__":
    tga = TourGuideAgent()
    query = "Sebutkan destinasi wisata alam dengan kawah di sekitar Bandung?"
    results = tga.execute(query)
   # print(results)