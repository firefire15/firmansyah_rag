
Tugas Akhir
Tema Proyek		: BOT Pelayanan
Judul Proyek 		: Chatbot Pelayanan Kunjungan Wisatawan di Kota Bandung

1.	Ringkasan
Proyek ini berisi tentang pertanyaan dan jawaban yang sering dilontarkan oleh wisatawan local ataupun mancanegara ketika mengunjungi Kota Bandung. Biasanya turis akan menanyakan mengenai jaringan transportasi apa yang tersedia baik di dalam kota maupun dari berbagai kota, lokasi penginapan, tempat wisata bersejarah atau ikonik, makanan ataupun minuman dan sebagainya. Agar lebih terasa manfaatnya, pengguna bisa memasukkan pertanyaan dan jawaban yang spesifik tergantung tema. Semisal: turis ingin mengikuti sebuah event game di Bandung, maka model yang ada dapat di-tuning menurut event tersebut. Selain untuk kepentingan tertentu, chatbot ini juga menyediakan pertanyaan-pertanyaan umum yang biasanya ditanyakan oleh wisatawan local ataupun mancanegara ketika berkunjung ke Kota Bandung, seperti menanyakan Lokasi menarik, tempat ibadah, dsb.     
2.	Latar Belakang:
a.	Identifikasi dan jelaskan masalah atau peluang yang ingin dipecahkan.
Proyek ini terinspirasi ketika menjadi POC di sebuah event sebuah game di Bandung. Event Game ini menarik banyak perhatian penggemarnya terutama dari mancanegara. Pada tahun 2019 dan 2023. Event ini diikuti oleh ratusan orang yang berasal dari dalam negeri maupun luar negeri. Kesulitan yang dialami adalah melayani pertanyaan mengenai tempat-tempat yang bisa dijadikan untuk berkumpul sesama penggemar game. Jika menggunakan google ataupun ChatGPT, tentunya jawaban akan terlalu umum, bahkan tergolong ambigu dan tidak dapat melihat konteks komunitas game ini dimainkan yakni di Kota Bandung. 
Di sisi lain, karena game ini termasuk game peperangan dari dua tim bedasarkan GPS di tengah Kota Bandung, aturan pada game ini pun cukup banyak, seperti waktu mulai game, Playbox wilayah peperangan. dsb. Dengan detail aturan seperti itu, tentunya akan banyak mendapatkan pertanyaan dari para peserta, meskipun terdapat infografis dan dokumen yang menjelaskan mengenai aturan tersebut. Di sisi lain, selain untuk bermain game, peserta pun tertarik untuk mengunjungi berbagai destinasi wisata di Kota Bandung. Destinasi wisata sepert wisata alam, kuliner dan Sejarah selalu menjadi sasaran pertanyaan. Selain itu, lokasi tempat ibadah seperti masjid juga sering dicari oleh pemain di sela-sela game berlangsung. Tentu saja akan merepotkan jika pertanyaan ini diulangi-ulang. 
Dari permasalahan tersebut, tercetuslah ide bagaimana membuat sebuah chatbot yang dapat melayani jawaban dari para pemain yang dapat juga disebut wisatawan yang mengunjungi Kota Bandung. Selain bermain game, mereka pun sering mengunjungi objek-objek wisata, tempat ibadah, dan berbagai macam tempat sambil melakukan dokumentasi. Terkadang, sebagai warga local pun kebanyakan belum tau beberapa destinasi wisata seperti kuliner ataupun destinasi Sejarah yang di mata wisatawan hal tersebut cukup terkenal.


b.	Berikan konteks mengenai mengapa proyek ini penting.
Konteks yang membuat proyek ini penting adalah karena belum adanya aplikasi yang dapat mempermudah wisatawan memperoleh informasi di kota Bandung, Terkadang untuk mendapatkan informasi kurang termutakhirkan atau harus mencari dari berbagai website. Selain itu, para wisatawan atau tamu cukup kesulitan mencari informasi tersebut karena belum adanya aplikasi yang relevan. Oleh karena itu, dengan adanya chatbot ini diharapkan dapat memberikan informasi kepada wisatawan yang akan mengunjungi destinasi wisata di kota Bandung dengan baik. 

3.	Tujuan Proyek:
a.	Tentukan secara jelas apa yang ingin dicapai dengan proyek ini.
i.	Chatbot dapat menyediakan jawaban yang relevan dan akurat
ii.	Chatbot dapat meningkatkan kepuasan pengguna aplikasi
iii.	Chatbot mempercepat waktu respon atau memberikan jawaban
iv.	Chatbot dapat menangani pertanyaan di luar konteks yang diberikan
v.	Chatbot dapat menghindari halusinasi atau informasi yang salah.
b.	Gambarkan matrik keberhasilan yang akan digunakan untuk menilai pencapaian tujuan.
No	Tujuan Proyek	Indikator Keberhasilan	Metrik / Parameter	Target	Sumber Data / Evaluasi
1	Menyediakan jawaban yang relevan dan akurat	Tingkat relevansi jawaban terhadap dokumen ataupun data yang diberikan pada database	rating yang dievaluasi secara manual dan dicek kebenarannya	≥ 85% relevan	Evaluasi manual
2	Meningkatkan kepuasan pengguna	Feedback atau rating dari pengguna	Skor kepuasan dengan skala likert (1–5)	Rata-rata ≥ 4.0	Survei pengguna
3	Mempercepat waktu respon	Rata-rata waktu respon chatbot hingga mengeluarkan jawaban	Waktu rata-rata (detik)	≤ 10 detik	Log aplikasi
4	Menangani pertanyaan di luar konteks (OOD)	Kemampuan chatbot menolak/menjawab tepat	Persentase respon "tidak tahu" yang tepat	≥ 90% akurat	Log percakapan / human evaluation
5	Menghindari hallucination / informasi salah	Jumlah jawaban yang keliru atau tidak berdasar	% jawaban dengan referensi salah	< 6%	Audit konten / evaluasi pakar





4.	Metodologi
a.	Jelaskan langkah-langkah yang akan diambil untuk mencapai tujuan proyek.
i.	Melakukan identifikasi dan pengumpulan data mengenai jenis pertanyaan yang biasa diajukan wisatawan. Identifikasi ini bisa berasal dari analisis website www.jabarprov.go.id mengenai informasi tempat wisata di Kota Bandung ataupun dari website lain yang jawabannya relevan dan benar, sehingga dapat dipertangungjawabkan.

ii.	Data lain yang berhubungan dan relevant dengan event, yang berisi pertanyaan umum ataupun yang berhubungan dengan game, sterdapat pada dokumentasi penulis.

iii.	Data Lokasi berasal dari Open Street Maps. Dapat diunduh langsung lalu ditransformasikan ke dalam database, atau pada program python langsung menyertakan library tersebut. Dalam hal ini bisa memakai tools bawaan dari LLM. 

iv.	Melakukan pengkodean dengan python untuk menghasilkan fitur chatbot yang sesuai dengan matriks keberhasilan;

v.	Melakukan pengkodean dengan python via Streamlit.app untuk keperluan hosting dan testing program;

vi.	Melakukan pengujian dari perbaikan dari program jikalau model LLM terdapat halusinasi ataupun menjawab di luar konteks dari jawaban yang diberikan.

b.	Jelaskan Teknologi yang akan digunakan (Versi bahasa, library, atau IDE)
Bahasa Pemrograman yang digunakan : Python
IDE: Visual Studio Code
Library: scikit.learn, pandas dataframe, numpy, LangChain, Langgraph, Osmnx, matplotlib dan seaborn untuk visualisasi jika dibutuhkan.
Database: Chroma DB (DB berbasis Vector), MySQL (jika diperlukan)
c.	Tentukan dataset yang akan digunakan dan bagaimana data tersebut akan dikumpulkan, diproses, dan dianalisis.
Dataset dari web akan dikumpulkan dan disimpan pada database menurut formatnya. Sementara itu dataset dari dokumen pribadi akan dipilah atau dipisahkan menurut kegunaannya. Sementara itu dataset dari Open Street Map akan tetap pada library tersebut, yang nantinya akan dimunculkan oleh Bot. Dataset dari OSM dapat juga disimpan di dalam database relasional. Data untuk sumber QnA disimpan ke dalam vector DB seperti Chroma DB agar dapat dengan mudah diolah.
d.	Gambarkan model atau algoritma yang akan digunakan.
Algoritma yang digunakan adalah RAG (Retrieval-Augmented Generation) yang digambarkan pada bagan di bawah ini
 
Gambar 1: Penggambaran Proses RAG
Proses RAG sendiri dimulai dari penambahan informasi yang relevan. Setelah itu kita memberikan konteks berupa prompt yang dipersiapkan. Gabungan dari Prompt, kueri dan konteks yang diberikan akan menghasilkan sebuah teks sebagai jawaban berdasarkan penambahan informasi yang relevan dari database serta LLM EndPoint.
5.	Pemilihan Algoritma dan Model
a.	Jelaskan mengapa model atau algoritma tertentu dipilih.
Retrieval Augmented Generative (RAG) dipilih karena mempu melakukan tuning terhadap informasi yang relevan dari pencarian user. Hal ini dapat menghindari jawaban halusinasi dari LLM. Untuk tuning algoritma dan tambahan model lainnya akan dijelaskan kemudian sambil melakukan pengembangan aplikasi Chatbot.

6.	Arsitektur Aplikasi yang dipilih
Berdasarkan analisis dari permasalahan yang ada, arsitektur yang dipilih pada pengembangan aplikasi ini adalah Multiagent RAG Chatbot. Disebut dengan multiagent dikarenakan agent-agent untuk memjawab pertanyaan dengan spesifikasi tertentu dipisahkan agar mendapatkan konteks jawaban yang lebih akurat. Setelah dipisahkan, jawaban dari berbagai agent tersebut akan disatukan dan dirangkum oleh aggregator, sehingga user mendapatkan jawaban dari agent tersebut.

Dalam kasus ini, kami membagi agent berdasarkan data spesialisasinya yakni Agent Wisata Alam, Agent Wisata Kuliner, Agent WIsata Pendidikan, Agent Wisata Sejarah, dan Agent Pencarian Lokasi. Kelima Agent tersebut mengambil data dari sumber yang berbeda dan memiliki prompt yang sendiri-sendiri. Khusus untuk pencarian lokasi. Aplikasi akan mencari tempat tertentu (Point of Interest) POI yang ditanyakan oleh wisatawan. Misalnya wisatawan menanyakan data café di seputaran Gedung Sate. Maka aplikasi akan menyajikan data tersebut beserta sajian peta titik lokasi mula-mula dan lokasi titik yang dicari oleh wisatawan.  Berikut adalah arsitekturnya.

 

Pertama-tama, user memasukkan sebuah query untuk kemudian Agent Aggregator akan menyebarkannya ke lima agent. Lima agent tersebut adalah Wisata Alam Agent, Wisata Kuliner Agent, WIsata Sejarah dan Budaya Agent, Wisata Pendidikan Agent, dan Pencarian Lokasi. Keempat Agent WIsata: Alam, Kuliner Sejarah dan Budaya, serta Pendidikan menggunakan siste RAG yang terdiri atas Melakukan Pembersihan Data, membuah sebuah chunk, melakukan embedding dokumen, dan menyimpan data pada chroma DB (Databaase Vector). Data keempat agent tersebut berasal dari data text dalam format txt. Setelah itu, untuk menyimpan chunk digunakan Database Chroma DB.
Setelah database siap atau telah dibentuk, query yang diberikan oleh user dimasukan ke dalam prompting dan konteks. Model GeminiLLM akan membantu membuatkan respon sebagai jawabannya. Jawaban dari model Gemini LLM disimpan pada variable untuk disatukan kepada jawaban lain dari pencarian Lokasi (Jika Ada).
Di sisi lain, jika query yang user berikan cocok dengan pencarian Lokasi, maka program akan mengarahkan ke pencarian Lokasi. Di sata dilakukan prompting untuk memisahkan Lokasi awal yang dianggap sebagai titik awal user dengan Lokasi tempat Point Of Interest (POI) yang dicari. Hasil identifikasi tersebut digunakan untuk melakukan query ke Open Street Map (OSM). Jawabannya langsung dimasukkan ke dalam variable untuk dilemparkan kepada Agent Aggregator. Agent Aggregator kemudian mendistribusikan jawaban kepada front end untuk ditampilkan kepada user.
Library Langgraph memudahkan dalam melakukan untaian setiap proses yang memiliki multi agent. Data yang dilempar akan dengan mudah diolah dan diatur oleh system. Di sini terdapat aplikasi penggunaan langgraph yaitu ketika dari Aggregator melempat ke berbagai agent, serta dari pencarian Lokasi untuk mengidentifikasi banyaknya POI. Dengan demikian setiap POI tidak tertukar satu sama lain.

7.	Hasil Aplikasi
 

 
