import requests
import json

def test_customer_update():
    url = "http://127.0.0.1:5000/api/customers"
    
    # Erst einen Kunden erstellen
    new_customer = {
        "name": "Test Kunde Update",
        "company": "Test GmbH",
        "contact": "test@update.at",
        "phone": "+43 123 456 789"
    }
    
    print("🧪 Teste Kundenaktualisierung...")
    print("=" * 50)
    
    try:
        # 1. Kunde erstellen
        print("📝 Erstelle Test-Kunde...")
        response = requests.post(url, json=new_customer)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            data = response.json()
            customer_id = data.get('id')
            print(f"✅ Kunde erfolgreich erstellt mit ID: {customer_id}")
            
            # 2. Kunde abrufen
            print(f"\n📖 Rufe Kunde {customer_id} ab...")
            get_response = requests.get(f"{url}/{customer_id}")
            if get_response.status_code == 200:
                customer_data = get_response.json()
                print(f"✅ Kunde abgerufen: {customer_data.get('name')}")
                
                # 3. Kunde aktualisieren
                print(f"\n✏️ Aktualisiere Kunde {customer_id}...")
                updated_data = {
                    "name": "Test Kunde Aktualisiert",
                    "company": "Test GmbH Aktualisiert",
                    "contact": "updated@test.at",
                    "phone": "+43 987 654 321"
                }
                
                update_response = requests.put(f"{url}/{customer_id}", json=updated_data)
                print(f"Status Code: {update_response.status_code}")
                print(f"Response: {update_response.text}")
                
                if update_response.status_code == 200:
                    print("✅ Kunde erfolgreich aktualisiert!")
                    
                    # 4. Aktualisierten Kunden abrufen
                    print(f"\n📖 Rufe aktualisierten Kunden ab...")
                    final_response = requests.get(f"{url}/{customer_id}")
                    if final_response.status_code == 200:
                        final_data = final_response.json()
                        print(f"✅ Aktualisierter Kunde:")
                        print(f"   Name: {final_data.get('name')}")
                        print(f"   Firma: {final_data.get('company')}")
                        print(f"   E-Mail: {final_data.get('contact')}")
                        print(f"   Telefon: {final_data.get('phone')}")
                        
                        if final_data.get('name') == updated_data['name']:
                            print("✅ Aktualisierung erfolgreich bestätigt!")
                        else:
                            print("❌ Aktualisierung nicht korrekt!")
                    else:
                        print(f"❌ Fehler beim Abrufen des aktualisierten Kunden: {final_response.status_code}")
                else:
                    print(f"❌ Fehler beim Aktualisieren des Kunden: {update_response.status_code}")
            else:
                print(f"❌ Fehler beim Abrufen des Kunden: {get_response.status_code}")
        else:
            print(f"❌ Fehler beim Erstellen des Kunden: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server nicht erreichbar. Starte den Server mit 'python run.py'")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    test_customer_update() 