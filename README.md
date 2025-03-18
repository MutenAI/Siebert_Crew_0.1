# Siebert Content Crew

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CrewAI Framework](https://img.shields.io/badge/Framework-CrewAI-blue)](https://www.crewai.com)

## Introduzione
Il Siebert Content Crew è un sistema avanzato di automazione per la creazione di contenuti basato sul framework CrewAI, integrato con un sistema RAG (Retrieval-Augmented Generation) per garantire coerenza con le linee guida aziendali e conformità legale.

## 🛠 Installazione

1. **Prerequisiti di sistema**
   - Python 3.10 o superiore
   - Git per il controllo versione
   - Accesso all'API di OpenAI

```bash
git clone https://github.com/MutenAI/Siebert_Crew.git
cd Siebert_Crew
```

2. **Configurazione ambiente virtuale**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Configurazione chiavi API**
Creare un file `.env` nella root del progetto con:
```ini
OPENAI_API_KEY="your-api-key-here"
```

## 🏗 Architettura del Sistema

### Componenti principali
1. **CrewAI**
   - Orchestrazione degli agenti intelligenti
   - Gestione del ciclo di vita dei task
   - Comunicazione inter-agente

2. **Sistema RAG**
   - **Rag 1/**: Metadati aziendali e informazioni di brand
     - File: brand_info.csv
     - Struttura: [Nome Brand, Sito Web, Descrizione, Target Audience, Tono di Voce]
   - **Rag 2/**: Best practice per contenuti finanziari
     - File: best_practices.csv
     - Esempio: [Tipo Contenuto, Struttura Consigliata, Esempi]
   - **Rag 3/**: Conformità legale e requisiti
     - File: compliance_info.csv
     - Campi obbligatori: [Settore Regolamentato, Disclaimer, Norme GDPR]

## 🔄 Flusso di Lavoro

1. **Inizializzazione Sistema**
   ```mermaid
   graph TD
     A[Caricamento Configurazioni] --> B[Verifica File RAG]
     B --> C[Connessione API Esterne]
   ```

2. **Orchestrazione Agenti**
   - **Analista Contenuti**: Verifica requisiti tecnici
   - **Copywriter AI**: Genera contenuti applicando:
     - Template predefiniti
     - Ottimizzazione SEO
     - Adattamento tono di voce
   - **Revisore Legale**: Controlla:
     - Presenza disclaimer
     - Conformità GDPR
     - Restrizioni di settore

3. **Generazione Output**
   - Formati supportati:
     - Markdown (per blog/post)
     - PDF (documenti ufficiali)
     - JSON (integrazioni API)

## 🚀 Esecuzione

```bash
# Modalità sviluppo con hot-reload
python3 src/crew_automation_content_editor_launcher/main.py --watch --rag-dir ./RAG

# Modalità produzione
python3 src/crew_automation_content_editor_launcher/main.py --production --log-level WARNING
```



---
*Proprietà di Fylle SRL - Sviluppato per il cliente Siebert*

