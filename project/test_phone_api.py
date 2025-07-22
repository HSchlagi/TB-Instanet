#!/usr/bin/env python3
"""
Test-Skript für die neue Telefonnummer-Funktionalität
"""

import requests
import json

def test_phone_functionality():
    """Testet die Telefonnummer-Funktionalität"""
    
    url = "http://127.0.0.1:5000/api/customers"
    
    # Test-Daten mit Telefonnummer
    test_customer = {
        "name": "Test Kunde mit Telefon",
        "company": "Test GmbH",
        "contact": "test@test.at",
        "phone": "+43 123 456 789"
    }
    
    print("🧪 Teste Telefonnummer-Funktionalität...")
    print("=" * 50)
    
    try:
        # POST Request - Kunde erstellen
        print("📝 Erstelle Kunde mit Telefonnummer...")
        response = requests.post(url, json=test_customer)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            data = response.json()
            customer_id = data.get('id')
            print(f"✅ Kunde erfolgreich erstellt mit ID: {customer_id}")
            
            # GET Request - Kunde abrufen
            print(f"\n📖 Rufe Kunde {customer_id} ab...")
            get_response = requests.get(f"{url}/{customer_id}")
            
            if get_response.status_code == 200:
                customer_data = get_response.json()
                print(f"✅ Kunde abgerufen:")
                print(f"   Name: {customer_data.get('name')}")
                print(f"   Firma: {customer_data.get('company')}")
                print(f"   E-Mail: {customer_data.get('contact')}")
                print(f"   Telefon: {customer_data.get('phone')}")
                
                # Prüfe ob Telefonnummer korrekt gespeichert wurde
                if customer_data.get('phone') == test_customer['phone']:
                    print("✅ Telefonnummer korrekt gespeichert!")
                else:
                    print("❌ Telefonnummer nicht korrekt gespeichert!")
                    
            else:
                print(f"❌ Fehler beim Abrufen des Kunden: {get_response.status_code}")
                
        else:
            print(f"❌ Fehler beim Erstellen des Kunden: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server nicht erreichbar. Starte den Server mit 'python run.py'")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    test_phone_functionality() 