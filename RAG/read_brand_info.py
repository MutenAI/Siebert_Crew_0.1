import pandas as pd
import os

def read_brand_info():
    """
    Legge direttamente il file brand_info.csv e restituisce un dizionario con le informazioni sul brand.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'Rag 1', 'brand_info.csv')
    
    try:
        # Leggi il file CSV
        df = pd.read_csv(file_path)
        
        # Converti il DataFrame in un dizionario per un facile accesso
        brand_info = {}
        for _, row in df.iterrows():
            brand_info[row['Area']] = row['Key Info']
            
        return brand_info
    except Exception as e:
        print(f"Errore nella lettura del file brand_info.csv: {e}")
        return {}

if __name__ == "__main__":
    # Test della funzione
    brand_info = read_brand_info()
    print("Informazioni sul brand:")
    for area, info in brand_info.items():
        print(f"{area}: {info}")