import streamlit as st
from streamlit_folium import st_folium
import folium
import time
from tour_guide_rag import TourGuideAgent

def create_map_folium(query, data):
    try:
        if 'point' in data and 'pois' in data:
            point = data['point']
            m = folium.Map(location=point, zoom_start=15)
            folium.Marker(point, tooltip="Titik Pencari {}".format(query), icon=folium.Icon(color="green")).add_to(m)
            pois = data['pois']
            for poi in pois:
                folium.Marker(
                poi['coordinates'],
                tooltip=f"{poi['name']} ({poi['distance']} m)",
                icon=folium.Icon(color="blue")
                ).add_to(m)
            return m
        else:
            return {}
    except Exception as e:
        print(e)
        return {}

def response_generator(response_messages):
    bot_answers = ""
    for ans in response_messages['final_answer']:
        bot_answers += ""+ans.content+" \n" 

    for word in bot_answers.split():
        yield word + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.id_message = 1

if "agent" not in st.session_state:
    st.session_state.agent = TourGuideAgent()

if "maps" not in st.session_state:
    st.session_state.maps = {}
    st.session_state.id_maps = 1
    st.session_state.arr_id_maps = []
 

st.title("Semua Tentang Bandung")
id_maps_hist = 1
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg['role'] == 'assistant' and msg['map_response']['map_status'] == 1:
            map_data =  msg['map_response']['map_data']
            maps = create_map_folium(map_data["query"], map_data["map"])
            if maps:
               # with st.expander("Lihat Peta Hasil Pencarian"):
                st_maps =  st_folium(maps, width=725, height=500, key="key_map_hist_{}".format(id_maps_hist))
    id_maps_hist += 1 

prompt = st.chat_input("Tulis pertanyaanmu...")

if prompt:
    st.session_state.messages.append({"role":"user", "content":prompt, "map_response":{}})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_message = st.session_state.agent.execute(prompt)
        response = st.write_stream(response_generator(response_messages=response_message))
        map_response = {"map_data":{}, "map_status":0}
        if 'location' in response_message and len(response_message['location']) > 0:
            map_data = (response_message['location'][0].additional_kwargs)
            map_response["map_data"] = map_data
            map_response["map_status"] = 1
            maps = create_map_folium(map_data['query'], map_data['map'])
            if maps:
                #with st.expander("Lihat Peta Hasil Pencarian"):
                st_maps = st_folium(maps, width=725, height=500, key="key_map_{}".format(st.session_state.id_maps))
                st.session_state.id_maps += 1
                st.success("Berhasil membuat peta dari data.")
            else:
                st.warning("Gagal membuat peta dari data.")
    
    messages_hist = {"_id": st.session_state.id_message, "role": "assistant", "content": response, "map_response":map_response}
    print("messages_hist", messages_hist)
    st.session_state.messages.append(messages_hist)
    st.session_state.id_message += 1
    
       

        