import osmnx as ox
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict
from dotenv import dotenv_values
import google.generativeai as genai
from langchain_core.messages import AnyMessage, AIMessage
from langgraph.graph.message import add_messages
from geopy.distance import geodesic


class SearchLocation():

    def __init__(self):
        self.INTENT_TAG_MAP = {
                            "cafe": {"amenity":"cafe"},
                            "mosque": {"amenity": "place_of_worship",
                                       "religion": "muslim"},
                            "church": {"amenity": "place_of_worship",
                                       "religion": "christian"},
                            "museum": {"tourism": "museum"},
                            "park": {"leisure": "park"},
                            "fuel": {"amenity": "fuel"},
                            "pom bensin": {"amenity": "fuel"},
                            "supermarket": {"shop": "supermarket"},
                            "pharmacy": {"amenity": "pharmacy"},
                            "apotek": {"amenity": "pharmacy"},
                            "restaurant": {"amenity": "restaurant"},
                            "clinic":{"amenity":"clinic"},
                            "school":{"amenity":"school"},
                            "bank":{"amenity":"bank"},
                            "atm":{"amenity":"atm"},
                            "hospital":{"amenity":"hospital"},
                            "police":{"amenity":"police"},
                            "cafe":{"amenity":"cafe"},
                            "fast food":{"amenity":"fast_food"},
                            "bus station":{"amenity":"bus_station"},
                            "post office":{"amenity":"post_office"},
                            "car wash":{"amenity":"car_wash"},
                            "market" :{"amenity":"marketplace"}

            }
        config = dotenv_values(".env")
        self.gemini_api_key = config.get("GEMINI_API_KEY","AIzaSyCLcqeBq3Q0gIa-frAZI-qrx0_twYOXeq0")
        self.gemini_model = config.get("MODEL_NAME","gemini-2.5-flash")


    def augment_prompt(self, query_text, options):
        """Augment the query with retrieved documents."""
        prompt_template = f'''
            Anda adalah penunjuk lokasi, cari tahu informasi dari pertanyaan user mengenai lokasi awal user dan objek apa yang dicari
            hasil jawaban cukup lokasi awal dan objek yang dicari, hilangkan kata sekitar, daerah, wilayah dalam jawaban yang anda berikan dan jangan menjelaskan jawaban.
            Berikut adalah pertanyaan user: "{query_text}"

            Pilih salah satu dari kategori berikut:
            {options}

            Jawaban lokasi awal dan kategori yang dipisahkan dengan tanda hubung -, tanpa penjelasan.
        '''

        return prompt_template.strip()

    def search_location(self, nama_tempat, object_,  tags_, radius= 1500, limit=10):
        try:
 
            point = ox.geocode(nama_tempat)
            pois = ox.features_from_point(point, tags=tags_, dist=radius)
            if object_ == 'mosque':
                pois = pois[pois["religion"] == "muslim"]
            elif object_ == 'church':
                pois = pois[pois["religion"] == "christian"]
            pois = pois[pois["name"].notna()]
            pois = pois.head(limit) 


            result = []
            for _, row in pois.iterrows():

                if "geometry" in row:
                    geom = row["geometry"]
                    if geom.geom_type == "Point":
                        poi_loc = (geom.y, geom.x)
                    else:
                        centroid = geom.centroid
                        poi_loc = (centroid.y, centroid.x)

                    # Hitung jarak
                    jarak = geodesic(point, poi_loc).meters

                    # Ambil nama jalan (opsional)
                    street = row.get("addr:street") or row.get("highway") or row.get("street") or row.get("description") or "Jalan tidak diketahui"

                    # Gabungkan
                    result.append(f"- {row['name']} ({int(jarak)} m) – {street}")
                else:
                    street = row.get("addr:street") or row.get("highway") or row.get("street") or "Jalan tidak diketahui"
                    result.append(f"- {row['name']} < 1000 m - {street} ")

            if pois.empty:
                return f"Tidak ditemukan {object_} dalam radius {radius} m dari {nama_tempat}."
            
            return f"Berikut hasil pencarian {object_} dekat {nama_tempat}:\n" + "\n".join(result)
        except Exception as e:
                return f"Tidak ditemukan lokasi awal atau objek yang akan dicari"
           # return f"Error mencari {value}: {e}" 
    
    def llm_router(self, state):
        try:
            #print("state", state)
            query = state["query"]
            #print("query", query)
            kategori = list(self.INTENT_TAG_MAP.keys())
            prompt = self.augment_prompt(query_text=query, options="\n".join(f"- {k}" for k in kategori))
            #print(prompt)
            #print("Memulai proses generasi...")
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel(self.gemini_model)
            response = model.generate_content(prompt)
            results = response.text.strip()
            location, poi = results.split(" - ")
            #print(poi, self.INTENT_TAG_MAP.keys(), poi in self.INTENT_TAG_MAP.keys())
            dict_result = {"query": location, "next": poi if poi in self.INTENT_TAG_MAP.keys() else "fallback"}
            #print(dict_result)
            return dict_result
        except Exception:
            print("error pada modul ini")
    
    def execute(self, query):
        builder = StateGraph(State)
        builder.set_entry_point("router")
        builder.add_node("router", RunnableLambda(self.llm_router))
        for intent, tags in self.INTENT_TAG_MAP.items():
            def make_node(tags):
                return RunnableLambda(lambda s, tags_=tags: {"content": self.search_location(s["query"], s["next"], tags_), "role":"ai", "map":self.create_map(s["query"], s["next"], tags_)})
            builder.add_node(intent, make_node(tags))
            builder.add_edge(intent, END)
        builder.add_node("fallback", RunnableLambda(lambda s: {"content": "Mohon Maaf, saya tidak memiliki informasi atas lokasi tersebut", "role":"ai", "map":object}))
        builder.add_edge("fallback", END)
        builder.add_conditional_edges("router", lambda x: x["next"], {
            **{intent: intent for intent in self.INTENT_TAG_MAP.keys()},
            "fallback": "fallback"
            })
        graph = builder.compile()
        result = graph.invoke({"query": query, "role":"human", "content":"", "map":object, "next":"Alun alun Bandung"})
        return result
    
    def create_map(self, nama_tempat, object_,  tags_, radius= 1500, limit=10):
        try: 
            point = ox.geocode(nama_tempat)
            pois = ox.features_from_point(point, tags=tags_, dist=radius)
            if object_ == 'mosque':
                pois = pois[pois["religion"] == "muslim"]
            elif object_ == 'church':
                pois = pois[pois["religion"] == "christian"]
           # pois = pois[pois["name"].notna()]
            pois = pois.head(limit) 
            pois_named = pois
            pois_data = []
            for _, row in pois_named.iterrows():
                geom = row.geometry

                if geom.geom_type == "Point":
                    poi_coords = (geom.y, geom.x)
                elif geom.geom_type in ["Polygon", "MultiPolygon"]:
                    centroid = geom.centroid
                    poi_coords = (centroid.y, centroid.x)
                else:
                    continue
                dist = int(geodesic(point, poi_coords).meters)
                data = {"coordinates": poi_coords, "name":row['name'], "distance":dist}
                pois_data.append(data)
            point_data = {'point':point, "pois":pois_data}
            return point_data
        except:
            return ""
    
class State(TypedDict):
    query: str
    next: str
    role: str
    content: str
    map:object

if __name__ == "__main__":
    tga = SearchLocation()
    query = "Apa saja masjid di sekitar taman lalu lintas Bandung?"
    results = tga.execute(query)
    print(results)