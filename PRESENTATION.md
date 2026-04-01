# GitHub AI Analyzer - Pristatymas

## 1. Asistento paskirtis

**Problema:** Programuotojai praleidžia daug laiko naršydami GitHub repozitorijas ir suprasdant jų struktūrą.

**Sprendimas:** AI asistentas, kuris supranta natūralią kalbą ir automatiškai analizuoja repozitorijas.

---

## 2. Architektūros schema

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Vartotojas  │────▶│ Streamlit   │────▶│ NLP Module  │
│ (užklausa)  │     │ UI          │     │ (LangChain) │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ LLM Analizė │◀────│ Struktūros  │◀────│ GitHub API  │
│ (Groq)      │     │ analizė     │     │             │
└──────┬──────┘     └─────────────┘     └─────────────┘
       │
       ▼
┌─────────────┐
│ Atsakymas   │
│ (UI)        │
└─────────────┘
```

---

## 3. Naudotos technologijos

- **Streamlit** - Web UI
- **LangChain + Groq (Llama 3.3)** - AI/LLM
- **GitHub API** - Duomenų šaltinis
- **Pydantic** - Duomenų validacija
- **Pytest** - Testavimas

---

## 4. Demonstracija

Įveskite natūralią kalbą, pvz:
- "I need a library for working with matrices" → pandas
- "What framework creates graphs?" → matplotlib
- "Show me a Python web framework" → flask

---

## 5. Testavimas

### 5 užklausos (automatiniai testai):

| # | Užklausa | Tikimasi |
|---|----------|----------|
| 1 | "I need a library for working with matrices and data analysis" | pandas |
| 2 | "What framework is good for creating graphs?" | matplotlib |
| 3 | "Show me a popular Python web framework" | flask |
| 4 | "I want to analyze the JavaScript UI library from Meta" | react |
| 5 | "What is a good HTTP client library for Python?" | requests |

### Testų vykdymas:
```bash
pytest tests/
```

### Rezultatai:
- **Iš viso testų:** 8
- **Praėjo:** 5
- **Nepavyko:** 3 (LLM grąžino kitą teisingą atsakymą)
- **Laikas:** ~9s

**Pastaba:** LLM kartais grąžina kitą teisingą biblioteką (pvz., numpy vietoj pandas), nes abi tinkamos matricoms.

### Rankiniai testai (3):
1. **Semantinis atitikimas** - Ar atsakymas atitinka užklausos prasmę?
2. **Struktūra** - Ar atsakymas gerai struktūrizuotas?
3. **Išsamumas** - Ar pateikta visa reikiama informacija?

---

## 6. Refleksija

**Pasiekimai:**
- Veikiantis AI asistentas su UI
- Natūralios kalbos supratimas
- Automatizuota analizė

**Ribotumai:**
- Tik viešos repozitorijos
- Priklausomybė nuo Groq API

**Patobulinimai:**
- Privačių repozitorijų palaikymas
- Caching mechanizmas