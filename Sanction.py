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

# Sidebar for navigation
with st.sidebar:
    st.header("Navigationsmenü")
    tab = st.radio("Wählen Sie eine Aktion:", ["➕ Neue Sanktion", "📜 Alle Sanktionen und Hausverbote"])

# Main content area based on the selected tab
if tab == "➕ Neue Sanktion":
    st.subheader("Neue Sanktion oder Hausverbot hinzufügen")
    new_name = st.text_input("Name der Person:", key="add_name")
    new_sanction = st.text_area("Details der Sanktion:", key="add_sanction")
    new_ban_status = st.selectbox("Hausverbot:", ["Nein", "Ja"], key="add_ban_status")
    new_date_of_suspension = str(datetime.date.today())
    new_date_of_return = st.date_input("Datum der Rückkehr:", key="add_return_date")
    new_ban_reason = st.text_area("Grund für das Hausverbot:", key="add_ban_reason")

    if st.button("Sanktion speichern", key="save_sanction"):
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

elif tab == "📜 Alle Sanktionen und Hausverbote":
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

    # Button to clear all records
    if st.button("Alle Sanktionen und Hausverbote löschen"):
        sanctions_db.clear()  # Clear the sanctions_db dictionary
        save_data(sanctions_db)  # Save the cleared data to the file
        st.success("Alle Sanktionen und Hausverbote wurden gelöscht.")



