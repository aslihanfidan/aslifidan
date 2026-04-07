import math
import streamlit as st

st.set_page_config(
    page_title="Konaklama Hak Edis Sorgulama",
    page_icon="📍",
    layout="centered",
)

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(170deg, #0f172a 0%, #1a1a2e 50%, #0f172a 100%);
}
[data-testid="stHeader"] { background: transparent; }
label { font-size: 11px !important; text-transform: uppercase; letter-spacing: 1.8px; color: #64748b !important; font-weight: 600; }
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}
textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 11px !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-weight: 800 !important; }
html, body, [class*="css"] { color: #e2e8f0; font-family: 'Segoe UI', system-ui, sans-serif; }
hr { border-color: rgba(255,255,255,0.08) !important; }
</style>
""",
    unsafe_allow_html=True,
)

OFFICE_LAT = 40.8253
OFFICE_LON = 29.3711
OFFICE_NAME = "Cayirova, Kocaeli"
ROAD_FACTOR = 1.35

RING_STOPS = [
    {"name": "Bakirkoy Metrobus", "lat": 40.9795, "lon": 28.8724},
    {"name": "Merter E5", "lat": 41.0087, "lon": 28.8956},
    {"name": "Halicioglu E5", "lat": 41.0472, "lon": 28.9397},
    {"name": "Zincirlikuyu Metro", "lat": 41.0703, "lon": 29.0119},
    {"name": "Kadikoy Haldun Taner", "lat": 40.9905, "lon": 29.0282},
    {"name": "Acibadem Koprusu", "lat": 41.0019, "lon": 29.0499},
    {"name": "Unalan", "lat": 41.0055, "lon": 29.0437},
    {"name": "Bostanci", "lat": 40.9632, "lon": 29.0936},
    {"name": "Maltepe", "lat": 40.9342, "lon": 29.1323},
    {"name": "Kartal", "lat": 40.8925, "lon": 29.1886},
    {"name": "Pendik", "lat": 40.8747, "lon": 29.2322},
    {"name": "Tepeustu Shell", "lat": 40.9985, "lon": 29.1768},
    {"name": "Cekmekoy Metro", "lat": 41.0328, "lon": 29.1755},
]

DISTRICTS = {
    "Avrupa Yakasi": {
        "Arnavutkoy": {"lat": 41.185, "lon": 28.739, "m": ["Adnan Menderes", "Anadolu", "Arnavutkoy Merkez", "Ataturk", "Baklali", "Balaban", "Bogazkoy Istiklal", "Bolluca", "Boyalik", "Cilingir", "Deliklikaya", "Dursunkoy", "Durusu", "Fatih", "Hacimasli", "Hadimkoy", "Haracci", "Hastane", "Hicret", "Imrahor", "Islambey", "Karlibayir", "Karaburun", "Merkez", "Nene Hatun", "Sazan", "Tasoluk", "Tayakadin", "Terkos", "Yassoren", "Yenikent", "Yenikoy", "Yildirim"]},
        "Avcilar": {"lat": 40.98, "lon": 28.722, "m": ["Ambarli", "Cihangir", "Denizkoskler", "Firuzkoy", "Gumuspala", "Merkez", "Mustafa Kemal", "Parseller", "Tahtakale", "Universite", "Yesilkent"]},
        "Bagcilar": {"lat": 41.037, "lon": 28.857, "m": ["Baglar", "Barbaros", "Cinar", "Demirkapi", "Fevzicakmak", "Goztepe", "Gunesli", "Hurriyet", "Inonu", "Kazimkarabekir", "Kemalpasa", "Kirazli", "Mahmutbey", "Merkez", "Sancaktepe", "Yavuzselim", "Yenigun", "Yildizteppe", "Yuzyil"]},
        "Bahcelievler": {"lat": 41.0, "lon": 28.862, "m": ["Bahcelievler", "Cobancesme", "Cumhuriyet", "Fevzicakmak", "Hurriyet", "Kocasinan", "Siyavuspasa", "Soganli", "Sirinevler", "Yenibosna", "Zafer"]},
        "Bakirkoy": {"lat": 40.98, "lon": 28.872, "m": ["Atakoy 1. kisim", "Atakoy 2-5-6. kisim", "Atakoy 3-4-11. kisim", "Atakoy 7-8-9-10. kisim", "Basinkoy", "Cevizlik", "Florya", "Kartaltepe", "Merkez", "Osmaniye", "Sakizagaci", "Senlikoy", "Yesilkoy", "Yesilyurt", "Zuhuratbaba"]},
        "Basaksehir": {"lat": 41.093, "lon": 28.809, "m": ["Altinsehir", "Bahcesehir 1. Kisim", "Bahcesehir 2. Kisim", "Basak", "Guvercintepe", "Ikitelli", "Kayabasi", "Merkez", "Sahintepe", "Ziya Gokalp"]},
        "Bayrampasa": {"lat": 41.044, "lon": 28.912, "m": ["Altintepsi", "Cevatpasa", "Ismetpasa", "Kocatepe", "Merkez", "Muratpasa", "Orta", "Terazidere", "Vatan", "Yenidogan", "Yildirim"]},
        "Besiktas": {"lat": 41.043, "lon": 29.005, "m": ["Abbasaga", "Arnavutkoy", "Bebek", "Cihannuma", "Dikilitas", "Etiler", "Gayrettepe", "Kurucesme", "Levent", "Levazim", "Mecidiye", "Muradiye", "Nisbetiye", "Ortakoy", "Sinanpasa", "Turkali", "Ulus", "Visnezade", "Yildiz"]},
        "Beylikduzu": {"lat": 41.002, "lon": 28.642, "m": ["Adnan Kahveci", "Baris", "Beylikduzu", "Buyuksehir", "Cumhuriyet", "Dereagzi", "Gurpinar", "Kavakli", "Marmara", "Sahil", "Yakuplu"]},
        "Beyoglu": {"lat": 41.037, "lon": 28.977, "m": ["Asmalimescit", "Bedrettin", "Bereketzade", "Bulbul", "Camiikebir", "Cihangir", "Cukur", "Evliya Celebi", "Fetihtepe", "Firuzaga", "Galata", "Gumussuyu", "Haciahmet", "Halicioglu", "Huseyinaga", "Kaptanpasa", "Kalyoncukulugu", "Kemankese", "Kilicali Pasa", "Kulaksiz", "Mueyyetzade", "Okcumusa", "Omeravni", "Piri Pasa", "Purtelas", "Sahkulu", "Sutluce", "Tomtom", "Yenisehir"]},
        "Buyukcekmece": {"lat": 41.02, "lon": 28.585, "m": ["Alkent", "Batikoy", "Beykent", "Buyukcekmece", "Cumhuriyet", "Fatih", "Gurpinar", "Kamiloba", "Karaagac", "Kumburgaz", "Merkez", "Mimarsinan", "Muratbey", "Pinartepe", "Sinanoba", "Tepecik", "Turkoba", "Ulus", "Yenimahalle"]},
        "Catalca": {"lat": 41.143, "lon": 28.461, "m": ["Akarlar", "Ataturk", "Baklali", "Cakil", "Ciftlikkoy", "Cilingir", "Dagyenice", "Elbasan", "Ferhatpasa", "Gokcali", "Hallacli", "Incegiz", "Izzettin", "Kabakca", "Kaleici", "Kalfa", "Kalfakoy", "Karacakoy", "Kestanelik", "Kinikli", "Merkez", "Muratbey", "Nakkas", "Oren", "Ovayenice", "Subasi", "Yalikoy", "Yaylacik", "Yenikoy"]},
        "Esenler": {"lat": 41.044, "lon": 28.877, "m": ["Birlik", "Ciftehavuzlar", "Davutpasa", "Fatih", "Fevzicakmak", "Havaalani", "Kazimkarabekir", "Menderes", "Merkez", "Mimarsinan", "Namik Kemal", "Nenehatun", "Orcureis", "Tuna", "Turgutreis", "Yavuzselim"]},
        "Esenyurt": {"lat": 41.028, "lon": 28.676, "m": ["Akcaburgaz", "Ardicli", "Ataturk", "Balikoylu", "Barbaros Hayrettin Pasa", "Cumhuriyet", "Fatih", "Guzelyurt", "Inonu", "Karaagac", "Kirac", "Mehtercesme", "Merkez", "Namik Kemal", "Nisantepe", "Piri Reis", "Saadetdere", "Sultanmurat", "Talatpasa", "Tekstilkent", "Turgut Ozal", "Yenikent", "Zafer"]},
        "Eyupsultan": {"lat": 41.049, "lon": 28.934, "m": ["Aksemsettin", "Alibeykoy", "Circir", "Defterdar", "Dugmeciler", "Emniyettepe", "Esentepe", "Eyup Merkez", "Fetihtepe", "Gokturk", "Islambey", "Karadolap", "Merkez", "Mihrisah Sultan", "Muhsine Hatun", "Nisanca", "Nisanci", "Pirinci", "Rami Cuma", "Rami Yeni", "Sakarya", "Silahtaraga", "Topcular", "Yesilpinar", "Yesilvadi"]},
        "Fatih": {"lat": 41.019, "lon": 28.94, "m": ["Akdeniz", "Aksaray", "Atikali Pasa", "Bali Pasa", "Balat", "Beyazit", "Binbirdirek", "Cankurtaran", "Cerrahpasa", "Capa", "Carsamba", "Cibali", "Edirnekapi", "Fener", "Haseki", "Hobyar", "Hocagiyasettin", "Hirkaisherif", "Iskenderpasa", "Kadirga", "Karagumruk", "Katip Kasim", "Keresteciler", "Kumkapi", "Laleli", "Mesih Pasa", "Molla Fenari", "Molla Gurani", "Molla Husrev", "Nisanca", "Samatya", "Seyyid Omer", "Sirkeci", "Sultanahmet", "Suleymaniye", "Topkapi", "Unkapani", "Vefa", "Yavuzselim", "Yedikule", "Yenikapi", "Zeyrek"]},
        "Gaziosmanpasa": {"lat": 41.068, "lon": 28.914, "m": ["Barbaros Hayrettin Pasa", "Baglarbasi", "Fevzicakmak", "Hurriyet", "Karlitepe", "Karayollari", "Kazimkarabekir", "Merkez", "Mevlana", "Naci Askin", "Pazarici", "Sarigol", "Yenidogan", "Yenimahalle", "Yildirim", "Yildiztabya"]},
        "Gungoren": {"lat": 41.019, "lon": 28.881, "m": ["Abdurrahman Nafiz Gurman", "Akincilar", "Gencosman", "Gunestepe", "Guven", "Haznedar", "Mareshal Cakmak", "Mehmet Nesih Ozmen", "Merkez", "Sanayi", "Tozkoparan"]},
        "Kagithane": {"lat": 41.08, "lon": 28.973, "m": ["Caglayan", "Celiktepe", "Emniyet", "Gultepe", "Gursel", "Hamidiye", "Harmantepe", "Hurriyet", "Merkez Efendi", "Nurtepe", "Ortabayir", "Piyalepasa", "Sanayi", "Seyrantepe", "Sirintepe", "Talatpasa", "Yahya Kemal"]},
        "Kucukcekmece": {"lat": 41.002, "lon": 28.783, "m": ["Atakent", "Besyol", "Cennet", "Cumhuriyet", "Fatih", "Fevzicakmak", "Gultepe", "Halkali", "Inonu", "Istasyon", "Kanarya", "Kemalpasa", "Mehmet Akif", "Sogutlucesme", "Sultanmurat", "Tevfikbey", "Yarimburgaz", "Yesilova"]},
        "Sariyer": {"lat": 41.167, "lon": 29.05, "m": ["Aydinevler", "Baltalimani", "Bahcekoy", "Buyukdere", "Camitepe", "Cayirbasi", "Cumhuriyet", "Darussafaka", "Emirgan", "Fatih Sultan Mehmet", "Ferahevler", "Istinye", "Kazimkarabekir", "Kemer", "Kirecburnu", "Kocatas", "Maden", "Merkez", "Omurtepe", "Pinar", "Poligon", "PTT Evleri", "Resitpasa", "Rumelihisari", "Rumelikavagi", "Senevler", "Tarabya", "Uskumrukoy", "Yenikoy", "Zekeriyakoy"]},
        "Silivri": {"lat": 41.073, "lon": 28.246, "m": ["Alibey", "Bekirli", "Beyciler", "Buyukcavuslu", "Buyukkilicli", "Buyuksinekli", "Canta", "Cayirdere", "Celtik", "Cumhuriyet", "Danamandira", "Fener", "Gazitepe", "Gumusyaka", "Kadikoy", "Kavakli", "Kurfalli", "Merkez", "Mimarsinan", "Ortakoy", "Piri Mehmet Pasa", "Selimpasa", "Semizkumlar", "Seymen", "Yolcati"]},
        "Sultangazi": {"lat": 41.105, "lon": 28.864, "m": ["50. Yil", "75. Yil", "Cebeci", "Cumhuriyet", "Esentepe", "Gazi", "Habipler", "Ismetpasa", "Kazimkarabekir", "Malkocoglu", "Merkez", "Sultanciftligi", "Ugur Mumcu", "Yayla", "Yunusemre", "Zubeyde Hanim"]},
        "Sisli": {"lat": 41.061, "lon": 28.985, "m": ["19 Mayis", "Ayazaga", "Bozkurt", "Cumhuriyet", "Duatepe", "Ergenekon", "Esentepe", "Eskisehir", "Ferikoy", "Fulya", "Gulbahar", "Halaskargazi", "Halide Edip Adivar", "Halilrifatpasa", "Harbiye", "Huzur", "Inonu", "Kaptanpasa", "Kurtulus", "Kustepe", "Mahmutsevket Pasa", "Maslak", "Mecidiyekoy", "Mesrutiyet", "Nisantasi", "Okmeydani", "Osmanbey", "Pangalti", "Pasa", "Tesvikiye", "Topagaci"]},
        "Zeytinburnu": {"lat": 41.005, "lon": 28.901, "m": ["Bestelsiz", "Cirpici", "Gokalp", "Kazlicesme", "Maltepe", "Merkezefendi", "Nuripasa", "Seyitnizam", "Sumer", "Telsiz", "Veliefendi", "Yenidogan", "Yesiltepe"]},
    },
    "Anadolu Yakasi": {
        "Adalar": {"lat": 40.876, "lon": 29.091, "m": ["Burgazada", "Heybeliada", "Kinaliada", "Maden", "Nizam"]},
        "Atasehir": {"lat": 40.983, "lon": 29.127, "m": ["Asik Veysel", "Ataturk", "Barbaros", "Esatpasa", "Ferhatpasa", "Fetih", "Icerenkoy", "Inonu", "Kayisdagi", "Kucukbakkalkoy", "Mimar Sinan", "Mustafa Kemal", "Namik Kemal", "Ornek", "Yenicamlica", "Yenisahra"]},
        "Beykoz": {"lat": 41.107, "lon": 29.093, "m": ["Acarkent", "Acarlar", "Alibahdir", "Anadolufeneri", "Anadoluhisari", "Anadolukavagi", "Baklaci", "Beykoz Merkez", "Camlibahce", "Cavusbasi", "Cengeldere", "Ciftlik", "Cigdem", "Cubuklu", "Dereseki", "Elmali", "Fatih", "Gokturk", "Goztepe", "Gumussuyu", "Incirlikoy", "Kanlica", "Kavacik", "Merkez", "Ortacesme", "Pasabahce", "Polonezkoy", "Riva", "Ruzgarlibahce", "Soguksu", "Tokatkoy", "Yalikoy", "Yavuzselim", "Yenimahalle"]},
        "Cekmekoy": {"lat": 41.04, "lon": 29.17, "m": ["Alemdag", "Aydinlar", "Cumhuriyet", "Camlik", "Catalmese", "Eksioglu", "Gungoren", "Hamidiye", "Huseyinli", "Kirazlidere", "Kocullu", "Mehmet Akif", "Merkez", "Mimar Sinan", "Nisantepe", "Omerli", "Resadiye", "Sirapinar", "Sogukpinar", "Sultanciftligi", "Tasdelen"]},
        "Kadikoy": {"lat": 40.99, "lon": 29.026, "m": ["Acibadem", "Bostanci", "Caddebostan", "Caferaga", "Dumlupinar", "Egitim", "Erenkoy", "Fenerbahce", "Feneryolu", "Fikirtepe", "Goztepe", "Hasanpasa", "Kadikoy Merkez", "Kosuyolu", "Kozyatagi", "Merdivenkoy", "Moda", "Odokuzmayis", "Osmanaga", "Rasimpasa", "Sahrayicedit", "Suadiye", "Zuhtupasa"]},
        "Kartal": {"lat": 40.8895, "lon": 29.188, "m": ["Atalar", "Carsi", "Cevizli", "Cumhuriyet", "Esentepe", "Gumuspinar", "Hurriyet", "Karlitepe", "Kartal Merkez", "Kordonboyu", "Orhantepe", "Orta", "Petrolis", "Rahmanlar", "Soganlik", "Topselvi", "Ugur Mumcu", "Yakacik", "Yali", "Yukari"]},
        "Maltepe": {"lat": 40.935, "lon": 29.1305, "m": ["Altaycesme", "Altintepe", "Aydinevler", "Baglarbasi", "Basibuyuk", "Cevizli", "Cinar", "Esenkent", "Feyzullah", "Findikli", "Girne", "Gulsuyu", "Gulensu", "Idealtepe", "Kucukyali", "Maltepe Merkez", "Yali", "Zumrutevler"]},
        "Pendik": {"lat": 40.8765, "lon": 29.2335, "m": ["Ahmetyesevi", "Bahcelievler", "Ballica", "Bati", "Camcesme", "Camlik", "Cinardere", "Dogu", "Dumlupinar", "Emirli", "Ertugrul Gazi", "Esenler", "Esenyali", "Fatih", "Fevzi Cakmak", "Gocbeyli", "Gullubaglar", "Guzelyali", "Harmandere", "Kavakpinar", "Kaynarca", "Kurna", "Kurtdogmus", "Kurtkoy", "Orhangazi", "Orta", "Ramazanoglu", "Sanayi", "Sapanbaglar", "Suluntepe", "Seyhli", "Velibaba", "Yayalar", "Yenimahalle", "Yenisehir", "Yesilbaglar"]},
        "Sancaktepe": {"lat": 41.002, "lon": 29.231, "m": ["Abdurrahman Gazi", "Akpinar", "Ataturk", "Emek", "Eyup Sultan", "Fatih", "Hilal", "Inonu", "Kemal Turkler", "Meclis", "Merve", "Mevlana", "Osmangazi", "Pasakoy", "Safa", "Sarigazi", "Veysel Karani", "Yenidogan", "Yunus Emre"]},
        "Sultanbeyli": {"lat": 40.96, "lon": 29.262, "m": ["Abdurrahman Gazi", "Adil", "Ahmet Yesevi", "Aksemsettin", "Battalgazi", "Fatih", "Hamidiye", "Hasanpasa", "Mecidiye", "Mehmet Akif", "Mimar Sinan", "Necip Fazil", "Orhangazi", "Turgut Reis", "Yavuz Selim"]},
        "Sile": {"lat": 41.176, "lon": 29.612, "m": ["Agva", "Ahmetli", "Balibey", "Bickidere", "Bucakli", "Cavus", "Celebi", "Darlik", "Degirmencayiri", "Dogancilar", "Gokmasli", "Goce", "Imrendere", "Kabakoz", "Kalem", "Karacakoy", "Kervansaray", "Kizilca", "Kumbaba", "Merkez", "Sahilkoy", "Sofular", "Sortullu", "Suayipli", "Teke", "Ulupelit", "Uvezli", "Yaka", "Yenikoy", "Yesilvadi"]},
        "Tuzla": {"lat": 40.8165, "lon": 29.3005, "m": ["Aydinli", "Aydintepe", "Cami", "Evliya Celebi", "Fatih", "Icmeler", "Istasyon", "Mescit", "Mimar Sinan", "Orhanli", "Postane", "Sifa", "Teporen", "Yayla"]},
        "Umraniye": {"lat": 41.0166, "lon": 29.12, "m": ["Adem Yavuz", "Altinsehir", "Armaganevler", "Asagi Dudullu", "Atakent", "Cemil Meric", "Cakmak", "Camlik", "Dumlupinar", "Elmali Kent", "Esenevler", "Esenkent", "Esensehir", "Fatih Sultan Mehmet", "Hekimbasi", "Huzur", "Ihlamurkuyu", "Inkilap", "Istiklal", "Kazim Karabekir", "Madenler", "Mehmet Akif", "Namik Kemal", "Parseller", "Saray", "Site", "Tantavi", "Tatliisu", "Topagaci", "Umraniye Merkez", "Yaman Evler", "Yukari Dudullu"]},
        "Uskudar": {"lat": 41.0234, "lon": 29.015, "m": ["Acibadem", "Ahmediye", "Altunizade", "Ayazma", "Aziz Mahmut Hudayi", "Bahcelievler", "Barbaros", "Beylerbeyi", "Bulgurlu", "Burhaniye", "Camlica", "Cengelkoy", "Cicekci", "Dogancilar", "Emek", "Emniyet", "Ferah", "Fistikagaci", "Gulfem Hatun", "Guzeltepe", "Icadiye", "Ihsaniye", "Kandilli", "Kisikli", "Kucuksu", "Kuleli", "Kupluce", "Kuzguncuk", "Libadiye", "Murat Reis", "Nakkashtepe", "Pazarbasi", "Selimiye", "Sultantepe", "Vanikoy", "Yavuzturk", "Zeynep Kamil"]},
    },
}


def haversine(lat1, lon1, lat2, lon2):
    r = 6371
    to_rad = lambda d: d * math.pi / 180
    dlat = to_rad(lat2 - lat1)
    dlon = to_rad(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(to_rad(lat1)) * math.cos(to_rad(lat2)) * math.sin(dlon / 2) ** 2
    return r * 2 * math.asin(math.sqrt(a))


def classify(bird_km, road_km):
    if road_km >= 100:
        return "yes", "KONAKLAMA VERILMELI", "Yol mesafesi 100 km uzerindedir. Konaklama kriterini karsilar."
    if bird_km >= 85 or road_km >= 80:
        return "maybe", "DEGERLENDIRMEYE ALINMALI", "Tahmini yol mesafesi 100 km sinirina yakindir. Bireysel degerlendirme onerilir."
    return "no", "KONAKLAMA VERILMEMELI", "Mesafe 100 km kriterinin altindadir."


def nearest_ring(lat, lon):
    best, best_d = None, float("inf")
    for s in RING_STOPS:
        d = haversine(lat, lon, s["lat"], s["lon"])
        if d < best_d:
            best_d = d
            best = s
    return best, best_d


st.markdown(
    "<h1 style='text-align:center;font-size:24px;font-weight:700;margin-bottom:4px'>Konaklama Hak Edis Sorgulama</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#64748b;font-size:13px;margin-bottom:24px'>Referans: <b>Cayirova, Kocaeli</b> &nbsp;|&nbsp; Kriter: 100 km</p>",
    unsafe_allow_html=True,
)

yaka = st.selectbox("Yaka", ["--- Seciniz ---"] + list(DISTRICTS.keys()))
ilce_list = sorted(DISTRICTS[yaka].keys()) if yaka != "--- Seciniz ---" else []
ilce = st.selectbox("Ilce", ["--- Seciniz ---"] + ilce_list, disabled=(yaka == "--- Seciniz ---"))

mah_list = sorted(DISTRICTS[yaka][ilce]["m"]) if (yaka != "--- Seciniz ---" and ilce != "--- Seciniz ---") else []
mahalle = st.selectbox("Mahalle (opsiyonel)", ["--- Seciniz ---"] + mah_list, disabled=(ilce == "--- Seciniz ---"))

yorum = st.text_area(
    "Yorum / Aciklama (opsiyonel)",
    placeholder="Varsa ek bilgi veya itiraz gerekcenizi yazabilirsiniz…",
    height=90,
)

hesapla = st.button("Mesafe Hesapla ve Degerlendir", disabled=(ilce == "--- Seciniz ---"))

st.divider()

if hesapla and ilce != "--- Seciniz ---":
    info = DISTRICTS[yaka][ilce]
    bird_km = haversine(OFFICE_LAT, OFFICE_LON, info["lat"], info["lon"])
    road_km = bird_km * ROAD_FACTOR
    level, verdict, desc = classify(bird_km, road_km)
    ring_stop, ring_dist = nearest_ring(info["lat"], info["lon"])

    color_map = {"yes": "#0d9488", "maybe": "#d97706", "no": "#475569"}
    bg = color_map[level]
    mah_label = (" / " + mahalle) if mahalle != "--- Seciniz ---" else ""

    st.markdown(
        "<div style='background:" + bg + ";border-radius:16px;padding:22px 26px;margin-bottom:16px;color:white'>"
        "<div style='font-size:11px;text-transform:uppercase;letter-spacing:2px;opacity:0.75;margin-bottom:6px'>"
        "Sonuc &mdash; " + ilce + mah_label + "</div>"
        "<div style='font-size:20px;font-weight:800;margin-bottom:10px'>" + verdict + "</div>"
        "<div style='font-size:13px;line-height:1.6;opacity:0.9'>" + desc + "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    col1.metric("Kus Ucusu Mesafe", str(round(bird_km, 1)) + " km")
    col2.metric("Tahmini Yol Mesafesi", str(round(road_km, 0))[:-2] + " km")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='background:rgba(99,179,237,0.08);border:1px solid rgba(99,179,237,0.25);"
        "border-radius:16px;padding:18px 22px;margin-bottom:16px'>"
        "<div style='font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#64748b;margin-bottom:8px;font-weight:600'>"
        "En Yakin Ring Servisi Duragi</div>"
        "<div style='font-size:20px;font-weight:700;color:#63b3ed;margin-bottom:10px'>" + ring_stop["name"] + "</div>"
        "<div style='font-size:13px;color:#94a3b8'>Ilce merkezine kus ucusu uzaklik: "
        "<b style='color:#e2e8f0'>" + str(round(ring_dist, 1)) + " km</b></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("Tum ring duraklari (uzaklik sirasi)"):
        all_stops = sorted(
            [{"name": s["name"], "dist": haversine(info["lat"], info["lon"], s["lat"], s["lon"])} for s in RING_STOPS],
            key=lambda x: x["dist"],
        )
        for i, s in enumerate(all_stops):
            marker = "En yakin" if i == 0 else str(i + 1) + "."
            st.write(marker + "  " + s["name"] + " — " + str(round(s["dist"], 1)) + " km")

    st.markdown(
        "<div style='background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);"
        "border-radius:12px;padding:14px 18px;font-size:12px;color:#64748b;line-height:1.7'>"
        "<b style='color:#94a3b8'>Metodoloji:</b> Ilce merkez koordinati uzerinden Haversine hesabi. "
        "Yol mesafesi x" + str(ROAD_FACTOR) + " katsayisi ile turetilmistir. "
        "Kesin mesafe icin Google Maps dogrulamasi onerilir.</div>",
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        "<div style='background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);"
        "border-radius:16px;padding:16px 20px'>"
        "<div style='font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#475569;"
        "margin-bottom:10px;font-weight:600'>Tanimli Ring Servis Duraklari (" + str(len(RING_STOPS)) + ")</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for i, s in enumerate(RING_STOPS):
        cols[i % 3].markdown(
            "<span style='font-size:12px;color:#94a3b8'>• " + s["name"] + "</span>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;font-size:11px;color:#334155;margin-top:28px'>Akademi Egitim Teknolojileri &nbsp;·&nbsp; Konaklama Karar Destek Araci</p>",
    unsafe_allow_html=True,
)
