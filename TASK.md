Praktinio darbo aprašymas
Tema: Virtualaus asistento kūrimas ir testavimas (su kodu)
Tikslas: sukurti veikiantį virtualaus asistento prototipą, kuris interpretuoja vartotojo užklausą natūralia
kalba, vykdo užduotį pagal pasirinktą paskirtį ir pateikia struktūruotą atsakymą. Įvertinti asistento veikimą
naudojant testavimo metodus ir metrikas.
Nemažinama – rodė, bet leidau pasitaisyti.
-1 – pranešė iš anksto, kad nespėja ir vėliau atsiskaitys.*
-2 – nepranešė iš anksto, neatėjo.
*Nemažinama, jeigu tomis dienomis studentas buvo komandiruotėje arba negalavo ir gali įrodyti.
1. Pasirinkite asistento tipą ir paskirtį
Galimi scenarijai (studentai gali rinktis arba sugalvoti savo):
 Personalized Daily Briefing Bot – naujienų, orų ir kalendoriaus santrauka (API + LLM + TTS).
 Healthcare Assistant – realaus laiko sveikatos duomenų analizė (RapidAPI + LLM + CrewAI).
 AI Coding Assistant – kodo paaiškinimai, klaidų radimas, siūlymai (Code LLaMA, StarCoder).
 Customer Support Chatbot (RAG) – dokumentų paieška ir atsakymai (FastEmbed + SQLite +
Groq AI).
 Data Analysis Assistant – kriptovaliutų tendencijų analizė (LangChain + Llama3 + Exa API).
 Agentic Task Manager – autonominis užduočių vykdymas (LangGraph + Mixtral).
 Voice-Activated AI Assistant (Jarvis Clone) – balso sąveika (Whisper + TTS + LangChain).
Pagrįskite pasirinkimą:
 Kodėl ši sritis aktuali?
 Kokią problemą sprendžia asistentas?
2. Architektūros projektavimas
 Sukurkite architektūros schemą, kuri apimtų:
o Įvesties analizę (intent detection, entity extraction).
o Užduoties vykdymą (API integracijos, duomenų analizė, RAG pipeline).
o Atsakymo generavimą (LLM, santrauka, struktūrizuotas formatas).
o Papildomas funkcijas (konteksto išlaikymas, maršrutizavimas, atmintis, logų saugojimas).
 Nurodykite technologijas ir bibliotekas (pvz., LangChain, Hugging Face, spaCy, OpenAI API,
Haystack, LlamaIndex, CrewAI).
3. Prototipo kūrimas
 Įgyvendinkite agentą, kuris:
o Priima vartotojo užklausą natūralia kalba.
o Naudoja bent vieną NLP metodą (intent detection, entity extraction).
o Vykdo bent vieną užduotį autonomiškai (pvz., paieška, analizė, rekomendacija).
o Pateikia atsakymą struktūruotai (JSON, lentelė, santrauka).
 Naudokite bent 3 technologijas iš sąrašo arba bent 3 savo norimas.
 Aiškiai atskirkite komponentus kode (užklausos analizė, vykdymas, atsakymo generavimas).
Virtualus asistentas privalo turėti vartotojo sąsają (UI):
 Galimi variantai:
o Web UI (pvz., naudojant Streamlit, Gradio, Flask).
o Generatyvinis UI (Gen UI) – dinamiškai generuojama sąsaja pagal užduotį (pvz.,
LangChain + Streamlit).
 UI turi leisti:
o Įvesti vartotojo užklausą natūralia kalba.
o Rodyti asistento atsakymą struktūruotai (tekstas, lentelė, JSON).
o Jei reikalinga – pridėti papildomas funkcijas (pvz., failų įkėlimas, balso įvestis, TTS
atsakymui).
4. Testavimas
 Paruoškite testavimo planą, kuris apimtų:
o Funkcionalumo testus (pvz., ar agentas vykdo užduotis pagal paskirtį).
o NLP kokybės testus (pvz., intent detection, entity extraction tikslumas).
o Atsakymų kokybės vertinimą (pvz., BLEU, ROUGE, semantinis atitikimas).
 Sukurkite testų rinkinį:
o 5 skirtingų vartotojų užklausos.
o Apibrėžkite tikėtinus atsakymus arba vertinimo kriterijus.
 Įgyvendinkite testavimą:
o Automatiniai testai (3) (pvz., G-Eval, DeepEval, LLM-as-a-judge).
o Rankinis vertinimas (3) (pvz., semantinis atitikimas, atsakymo struktūra).
 Pateikite testavimo rezultatus (lentelės, grafikai, klaidų analizė).
5. Pristatymas + klausimai-atsakymai (10-20 min.), visos dalys BŪTINOS
o Asistento paskirtis.
o Architektūros schema.
o Naudotos technologijos.
o Demonstracija gyvai arba per video (su identifikacija, pvz., watermark).
o Testavimo metodai ir rezultatai (grafikai, lentelės).
o Refleksija: iššūkiai, ribotumai, patobulinimai.
Papildomos sąlygos dėl šaltinių
 Galima naudoti viešus pavyzdžius, bet privaloma atlikti esminius pakeitimus:
o Patobulinti funkcionalumą.
o Integruoti papildomas funkcijas.
o Pakeisti realizacijos būdą.
o Pridėti naujas sąsajas ar integracijas.
 Aiškiai nurodyti, kuri kodo dalis yra originali, o kuri – patobulinta.
Vertinimo kriterijai (maks. 10 balų)
Vertinimo aspektas Balai
Asistento sudėtingumas 3
Architektūros aiškumas 2
Funkcionalumo veikimas 2
Pristatymas (kalbėjimas + Q&A) 3