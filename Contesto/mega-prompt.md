# Mega-Prompt per lo Sviluppo del Content Editor System

## Obiettivo del Progetto
Sviluppare un sistema backend funzionante di generazione di contenuti utilizzando Crew AI, con un focus sul corretto funzionamento del flusso di lavoro e su un logging dettagliato che permetta di monitorare tutte le attività degli agenti.

## Requisiti Tecnici

### Framework e Tecnologie
- **Crew AI**: Utilizzare questo framework per la gestione degli agenti
- **Serper API**: Integrare per le ricerche web
- **LLM**: Supportare sia Claude (Anthropic) che GPT (OpenAI) per ogni agente individualmente
- **Output**: Solo su terminale, nessuna interfaccia grafica richiesta
- **Logging**: Implementare un sistema di logging dettagliato

### Struttura delle Directory e File
Il sistema deve utilizzare la seguente struttura per i dati:
```
[directory base]/RAG/
  ├── Rag1/
  │   └── brandinfo.csv   (informazioni sul brand)
  ├── Rag2/
  │   └── bestpractices.csv   (best practice per contenuti)
  └── Rag3/
      └── compliance_info.csv   (regole di compliance)
```

## Flusso di Lavoro Dettagliato

### Automazione: Creazione di Contenuti Brand con CrewAI

**Obiettivo**: Automatizzare la creazione di contenuti per il brand, seguendo un processo strutturato che va dall'inizializzazione, alla ricerca, creazione della bozza, revisione e finalizzazione.

**Risorse RAG**:
- RAG1: brandinfo.csv
- RAG2: bestpractices.csv
- RAG3: compliance_info.csv

**Output Atteso**:
- Report della ricerca web
- Bozza iniziale del contenuto
- Contenuto rivisto e ottimizzato, conforme alle best practice e alle normative

**Inputs**:
- {brandcontext}: proveniente da RAG1 (brandinfo.csv – ad es. {brandname}, {toneofvoice}, {primarytarget}, ecc.)
- {content_request}: il brief fornito dall'utente
- {bestpractices}: proveniente da RAG2 (bestpractices.csv – ad es. {structure}, {ideallength}, {requiredelements}, {recommended_tone})
- {compliancestandards}: proveniente da RAG3 (complianceinfo.csv – ad es. {sector}, {regulation}, {mandatory_elements}, ecc.)

### Agenti e Task

#### 1. Leader Agent
**Ruolo**: Coordina l'intero flusso, definisce gli obiettivi e verifica il risultato finale.

**Tasks**:
1. **Inizializzazione**
   - Accesso a RAG1 (brandinfo.csv) per recuperare il {brandcontext}
   - Input: {brandinfo.csv} → utilizzo delle variabili {brandname}, {toneofvoice}, {primarytarget}, {secondarytarget}, {uniquesellingpoints}, etc.

2. **Brief e Dispatch**
   - Riceve il {contentrequest} e lo invia al Web Searcher
   - Integra informazioni rilevanti del {brandcontext}
   - Input: {contentrequest} + {brandcontext}

3. **Finalizzazione**
   - Valuta il contenuto finale (prodotto da Editor Agent) e approva o richiede modifiche
   - Input: {optimizedcontentdraft}

#### 2. Web Searcher Agent
**Ruolo**: Raccoglie informazioni e dati dal web per contestualizzare l'argomento.

**Tasks**:
1. **Ricerca Online**
   - Utilizza la SERPER API per effettuare una ricerca basata sulle indicazioni del {contentrequest}
   - Approfondisce ulteriormente il contesto del brand
   - Output: {researchreport} (report strutturato con dati e link)

#### 3. Copywriter Agent
**Ruolo**: Produce la bozza iniziale del contenuto.

**Tasks**:
1. **Creazione Contenuti**
   - Accede a RAG1 per i dettagli del brand ({brandcontext})
   - Accede a RAG2 per le best practice (ad es. {structure}, {ideallength}, {requiredelements}, {recommendedtone})
   - Combina il {researchreport} con il contesto e le linee guida
   - Output: {firstdraftcontent}

#### 4. Editor Agent
**Ruolo**: Revisiona, ottimizza e verifica la conformità del contenuto.

**Tasks**:
1. **Revisione e Ottimizzazione**
   - Accede a tutti i RAG:
     - RAG1 e RAG2: verifica coerenza del tono e della struttura
     - RAG3: direttive per garantire che il contenuto rispetti le normative di settore
   - Controlla che il contenuto non violi {mandatoryelements} o includa {forbiddenelements}
   - Integra eventuali {disclaimers} se richiesto
   - Output: {optimizedcontentdraft}

## Schema dei RAG utilizzati da ciascun Agente

**Leader Agent**:
- Utilizza RAG1 per ottenere {brandcontext}
- Invia e gestisce il {contentrequest} al Web Searcher
- Valuta il contenuto finale

**Web Searcher Agent**:
- Basandosi su {contentrequest} e dati rilevanti di RAG1, avvia la ricerca online
- Produce {researchreport}

**Copywriter Agent**:
- Utilizza RAG1 per il contesto di brand 
- Utilizza RAG2 per incorporare le best practice nella stesura della bozza
- Integra i dati raccolti nel {researchreport}

**Editor Agent**:
- Utilizza i dati aggregati insieme a RAG3 per verificare la conformità
- Suggerisce modifiche necessarie
- Genera {optimizedcontentdraft}

## Requisiti di Implementazione

### Struttura del Codice
- Utilizzare un'architettura modulare e ben organizzata
- Implementare classi separate per la gestione degli agenti, dei CSV, e del logging
- Utilizzare best practice di programmazione Python

### Gestione CSV
- Implementare un robusto sistema di caricamento e parsing dei CSV
- Gestire correttamente i casi in cui i file CSV non esistono (crearli automaticamente)
- Validare il contenuto dei CSV

### Logging Avanzato
- **Requisito Critico**: Implementare un sistema di logging estremamente dettagliato
- Registrare ogni azione di ogni agente con timestamp
- Registrare ogni input e output
- Registrare ogni accesso ai dati CSV
- Visualizzare il log in tempo reale nel terminale
- Salvare il log completo in un file per riferimento futuro

### Configurazione LLM
- Permettere la scelta di Claude (Anthropic) o GPT (OpenAI) per ogni singolo agente
- Gestire correttamente le API key necessarie
- Implementare fallback in caso di errori di connessione

### Gestione Errori
- Implementare una robusta gestione degli errori
- Fornire messaggi di errore chiari e informativi
- Recuperare gracefully da problemi di connessione o API

## Note per lo Sviluppatore
1. **Focus sul Backend**: Non è richiesta alcuna interfaccia grafica, l'output deve essere solo su terminale
2. **Logging Critico**: Il sistema di logging è una componente fondamentale e deve essere il più dettagliato possibile
3. **Compatibilità Crew AI**: Il codice deve essere facilmente caricabile sulla piattaforma Crew AI
4. **Modularità**: Implementare il codice in modo modulare per facilitare future estensioni
5. **Configurabilità**: Permettere all'utente di specificare la directory base, le chiavi API e i modelli LLM

## Esempi di Implementazione

### Esempio di Log Atteso
```
[2025-03-15 14:32:45] [Leader] Inizializzazione - Accesso a RAG1
[2025-03-15 14:32:46] [Leader] Caricato brandinfo.csv: {'brandname': 'ExampleCorp', 'toneofvoice': 'professional'}
[2025-03-15 14:32:48] [Leader] Brief creato: "Creare un articolo sui nuovi trend di investimento"
[2025-03-15 14:32:50] [WebSearcher] Ricerca iniziata con SERPER API
[2025-03-15 14:32:55] [WebSearcher] Risultati ricerca: 15 articoli pertinenti trovati
...
```

### Formato dei File CSV

**RAG1/brandinfo.csv**:
```
campo,valore
brandname,ExampleCorp
toneofvoice,professionale e autorevole
primarytarget,investitori istituzionali
...
```

**RAG2/bestpractices.csv**:
```
tipo_contenuto,structure,ideallength,requiredelements,recommended_tone
articolo_blog,intro-3punti-conclusione,800-1200,call-to-action|sottotitoli,informativo
...
```

**RAG3/compliance_info.csv**:
```
sector,regulation,mandatory_elements,forbidden_elements,disclaimers
finanziario,CONSOB,trasparenza costi|chiarezza rischi,promesse rendimento garantito,rischi investimento
...
```

## Deliverables Richiesti
1. Codice Python completo e ben documentato
2. File README con istruzioni dettagliate per l'uso
3. Script di esempio per la configurazione iniziale
4. Requirements.txt con tutte le dipendenze necessarie

## Consegna
Il sistema deve essere consegnato come repository Git completo e funzionante, pronto per essere scaricato ed eseguito con requisiti minimi di configurazione.
