import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_demo_excel():
    """Erstellt eine Demo-Excel-Datei mit mehreren Zählpunkten"""
    
    # Zeitreihe für einen Tag (15-Minuten-Intervalle)
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    time_series = []
    for i in range(96):  # 24 Stunden * 4 (15-Minuten-Intervalle)
        time_series.append(start_time + timedelta(minutes=15*i))
    
    # Zählpunkt 1: Hauptlast (Gebäude)
    main_load = []
    for i, time in enumerate(time_series):
        # Tageslast-Profil: Morgens und abends höher
        hour = time.hour
        if 6 <= hour <= 8:  # Morgen
            base_load = 25 + np.random.normal(0, 2)
        elif 18 <= hour <= 22:  # Abend
            base_load = 30 + np.random.normal(0, 3)
        elif 23 <= hour or hour <= 5:  # Nacht
            base_load = 5 + np.random.normal(0, 1)
        else:  # Tag
            base_load = 15 + np.random.normal(0, 2)
        
        main_load.append(max(0, base_load))
    
    # Zählpunkt 2: Produktion (Maschinen)
    production_load = []
    for i, time in enumerate(time_series):
        hour = time.hour
        if 7 <= hour <= 17:  # Arbeitszeit
            base_load = 20 + np.random.normal(0, 5)
        else:  # Nachtschicht minimal
            base_load = 2 + np.random.normal(0, 1)
        
        production_load.append(max(0, base_load))
    
    # Zählpunkt 3: Klimaanlage
    hvac_load = []
    for i, time in enumerate(time_series):
        hour = time.hour
        if 8 <= hour <= 18:  # Bürozeiten
            base_load = 15 + np.random.normal(0, 2)
        else:  # Nachts aus
            base_load = 1 + np.random.normal(0, 0.5)
        
        hvac_load.append(max(0, base_load))
    
    # Zählpunkt 4: Beleuchtung
    lighting_load = []
    for i, time in enumerate(time_series):
        hour = time.hour
        if 6 <= hour <= 22:  # Beleuchtung an
            base_load = 8 + np.random.normal(0, 1)
        else:  # Nachts aus
            base_load = 1 + np.random.normal(0, 0.3)
        
        lighting_load.append(max(0, base_load))
    
    # DataFrames erstellen
    df_main = pd.DataFrame({
        'Zeitstempel': time_series,
        'Hauptlast_kW': main_load
    })
    
    df_production = pd.DataFrame({
        'Zeitstempel': time_series,
        'Produktion_kW': production_load
    })
    
    df_hvac = pd.DataFrame({
        'Zeitstempel': time_series,
        'Klimaanlage_kW': hvac_load
    })
    
    df_lighting = pd.DataFrame({
        'Zeitstempel': time_series,
        'Beleuchtung_kW': lighting_load
    })
    
    # Excel-Datei erstellen
    with pd.ExcelWriter('demo_load_profile.xlsx', engine='openpyxl') as writer:
        df_main.to_excel(writer, sheet_name='Hauptlast', index=False)
        df_production.to_excel(writer, sheet_name='Produktion', index=False)
        df_hvac.to_excel(writer, sheet_name='Klimaanlage', index=False)
        df_lighting.to_excel(writer, sheet_name='Beleuchtung', index=False)
    
    print("✅ Demo-Excel-Datei erstellt: demo_load_profile.xlsx")
    print("📊 Zählpunkte:")
    print("  - Hauptlast: Gebäudelast (25-30 kW Peak)")
    print("  - Produktion: Maschinen (20 kW Arbeitszeit)")
    print("  - Klimaanlage: HVAC-System (15 kW Bürozeiten)")
    print("  - Beleuchtung: Licht (8 kW Tag)")
    print("")
    print("💡 Verwende diese Datei zum Testen des Excel-Imports!")

if __name__ == "__main__":
    create_demo_excel() 