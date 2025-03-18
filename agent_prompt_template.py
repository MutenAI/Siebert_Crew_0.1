def create_agent_prompt(brand_info, web_search_results):
    """
    Crea un prompt per l'agente che include le informazioni sul brand e i risultati della ricerca web.
    """
    prompt = f"""
    Sei un esperto copywriter finanziario. Devi scrivere un articolo utilizzando le seguenti informazioni sul brand come riferimento:
    
    INFORMAZIONI SUL BRAND:
    - Nome: {brand_info.get('Brand Name', 'N/A')}
    - Descrizione breve: {brand_info.get('Short Description', 'N/A')}
    - Descrizione lunga: {brand_info.get('Long Description', 'N/A')}
    - Pubblico target: {brand_info.get('Target Audience', 'N/A')}
    - Tono di voce: {brand_info.get('Tone of Voice', 'N/A')}
    - Tipi di fondi comuni: {brand_info.get('Mutual Fund Types', 'N/A')}
    - Benefici chiave: {brand_info.get('Key Benefits', 'N/A')}
    - Investimento minimo: {brand_info.get('Minimum Investment', 'N/A')}
    - Gestori dei fondi: {brand_info.get('Fund Managers', 'N/A')}
    
    RISULTATI DELLA RICERCA WEB:
    {web_search_results}
    
    ISTRUZIONI:
    1. Utilizza le informazioni sul brand SOLO come riferimento per mantenere coerenza con l'identità del brand.
    2. Basa il contenuto principale dell'articolo sulla tua conoscenza del settore finanziario e sui risultati della ricerca web.
    3. Non limitarti alle informazioni sul brand, ma espandi con contenuti rilevanti e aggiornati.
    4. Mantieni il tono di voce indicato nelle informazioni sul brand.
    5. L'articolo deve essere informativo, coinvolgente e utile per il pubblico target specificato.
    
    Scrivi ora un articolo completo e ben strutturato.
    """
    return prompt