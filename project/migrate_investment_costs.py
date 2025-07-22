import sqlite3
import os

def migrate_investment_costs():
    db_path = os.path.join('instance', 'bess.db')
    if not os.path.exists(db_path):
        print("❌ Datenbank nicht gefunden!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Aktuelle Spalten prüfen
        cursor.execute("PRAGMA table_info(investment_cost)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print("🔧 Migriere InvestmentCost-Tabelle...")
        print("=" * 60)
        
        # Neue Spalten hinzufügen
        new_columns = [
            ('component_subtype', 'VARCHAR(50)'),
            ('cost_per_unit', 'FLOAT'),
            ('power_kw', 'FLOAT'),
            ('capacity_kwh', 'FLOAT'),
            ('manufacturer', 'VARCHAR(100)'),
            ('model', 'VARCHAR(100)'),
            ('quantity', 'INTEGER DEFAULT 1')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                print(f"➕ Füge Spalte '{column_name}' hinzu...")
                cursor.execute(f"ALTER TABLE investment_cost ADD COLUMN {column_name} {column_type}")
            else:
                print(f"✅ Spalte '{column_name}' existiert bereits")
        
        # Tabelle anzeigen
        cursor.execute("PRAGMA table_info(investment_cost)")
        columns = cursor.fetchall()
        
        print("\n📋 Aktualisierte InvestmentCost-Tabelle:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
        
        conn.commit()
        print("\n✅ Migration erfolgreich abgeschlossen!")
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei der Migration: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔧 Migriere InvestmentCost-Tabelle für intelligente Kostenverwaltung...")
    print("=" * 80)
    success = migrate_investment_costs()
    if success:
        print("\n✅ Migration erfolgreich!")
        print("💡 Starte den Server neu um die Änderungen zu übernehmen.")
    else:
        print("\n❌ Migration fehlgeschlagen!") 