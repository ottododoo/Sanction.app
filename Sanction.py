import streamlit as st
import json
import os
import datetime

# File to store data
FILE_PATH = "sanctions_data.json"

# Load existing data
def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    return {}

# Save data to JSON file
def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

# Initialize data
sanctions_db = load_data()

# Streamlit App
st.title("FACKtory Register: Hausverbot & Sanktionen 🚫")

tab1, tab2, tab3 = st.tabs(["🔍 Prüfe Hausverbot", "➕ Neue Sanktion", "📜 Alle Sanktionen und Hausverbote"])

# 🔍 Check if someone has a ban
with tab1:
    st.subheader("Prüfe, ob jemand Hausverbot hat")
    name = st.text_input("Name der Person:")
    if st.button("Prüfen"):
        if name in sanctions_db:
            latest_status = sanctions_db[name][-1].get("ban_status", "N/A")
            latest_date = sanctions_db[name][-1].get("date_of_suspension", "N/A")
            return_date = sanctions_db[name][-1].get("date_of_return", "N/A")
            reason = sanctions_db[name][-1].get("ban_reason", "N/A")
            st.write(f"🚨 **{name} hat {'Hausverbot' if latest_status == 'Yes' else 'kein Hausverbot'}**")
            st.write(f"📅 Datum des Hausverbots: {latest_date}")
            st.write(f"📅 Rückkehrdatum: {return_date}")
            st.write(f"🔴 Grund für das Hausverbot: {reason}")
        else:
            st.write(f"✅ **{name} ist nicht im System**")

# ➕ Add new sanction
with tab2:
    st.subheader("Neue Sanktion oder Hausverbot hinzufügen")
    new_name = st.text_input("Name der Person:")
    new_sanction = st.text_area("Details der Sanktion:")
    new_ban_status = st.selectbox("Hausverbot:", ["Nein", "Ja"])
    new_date_of_suspension = str(datetime.date.today())
    new_date_of_return = st.date_input("Datum der Rückkehr:")
    new_ban_reason = st.text_area("Grund für das Hausverbot:")

    if st.button("Sanktion speichern"):
        if new_name:
            if new_name not in sanctions_db:
                sanctions_db[new_name] = []
            sanctions_db[new_name].append({
                "sanction": new_sanction,
                "date_of_suspension": new_date_of_suspension,
                "date_of_return": str(new_date_of_return),
                "ban_status": new_ban_status,
                "ban_reason": new_ban_reason
            })
            save_data(sanctions_db)  # Save to JSON
            st.success(f"Sanktion für {new_name} hinzugefügt!")

# 📜 View all records
with tab3:
    st.subheader("Alle Sanktionen & Hausverbote")
    if sanctions_db:
        for person, records in sanctions_db.items():
            st.write(f"**{person}**")
            for record in records:
                st.write(f"- 📅 Datum des Hausverbots: {record.get('date_of_suspension', 'N/A')}")
                st.write(f"📅 Rückkehrdatum: {record.get('date_of_return', 'N/A')}")
                st.write(f"🔴 Sanktion: {record.get('sanction', 'N/A')}")
                st.write(f"🔴 Grund für das Hausverbot: {record.get('ban_reason', 'N/A')}")
                st.write(f"⚠️ Hausverbot: {'Ja' if record.get('ban_status') == 'Yes' else 'Nein'}")
    else:
        st.write("Noch keine Datensätze vorhanden.")


