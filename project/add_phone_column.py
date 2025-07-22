#!/usr/bin/env python3
"""
Skript zum Hinzufügen der Telefonnummer-Spalte zur Customer-Tabelle
"""

import sqlite3
import os

def add_phone_column():
    """Fügt die phone-Spalte zur customer-Tabelle hinzu"""
    
    # Pfad zur Datenbank
    db_path = os.path.join('instance', 'bess.db')
    
    if not os.path.exists(db_path):
        print("❌ Datenbank nicht gefunden!")
        return False
    
    try:
        # Verbindung zur Datenbank
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Prüfe ob die Spalte bereits existiert
        cursor.execute("PRAGMA table_info(customer)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'phone' in columns:
            print("✅ Telefonnummer-Spalte existiert bereits!")
            return True
        
        # Füge die phone-Spalte hinzu
        cursor.execute("ALTER TABLE customer ADD COLUMN phone VARCHAR(50)")
        
        # Commit der Änderungen
        conn.commit()
        
        print("✅ Telefonnummer-Spalte erfolgreich hinzugefügt!")
        
        # Zeige die aktualisierte Tabellenstruktur
        cursor.execute("PRAGMA table_info(customer)")
        columns = cursor.fetchall()
        
        print("\n📋 Aktualisierte Customer-Tabelle:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Hinzufügen der Spalte: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔧 Füge Telefonnummer-Spalte zur Customer-Tabelle hinzu...")
    print("=" * 60)
    
    success = add_phone_column()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
        print("💡 Starte den Server neu um die Änderungen zu übernehmen.")
    else:
        print("\n❌ Migration fehlgeschlagen!") 