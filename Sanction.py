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
st.title("FACKtory Sanctions & Ban Register 🚫")

tab1, tab2, tab3 = st.tabs(["🔍 Check Status", "➕ Add Sanction", "📜 View All Records"])

# 🔍 Check if someone is banned
with tab1:
    st.subheader("Check if Someone is Banned")
    name = st.text_input("Enter name:")
    if st.button("Check"):
        if name in sanctions_db:
            latest_status = sanctions_db[name][-1]["ban_status"]
            latest_date = sanctions_db[name][-1]["date_of_suspension"]
            return_date = sanctions_db[name][-1].get("date_of_return", "N/A")
            reason = sanctions_db[name][-1]["ban_reason"]
            st.write(f"🚨 **{name} is {'BANNED' if latest_status == 'Yes' else 'NOT BANNED'}**")
            st.write(f"📅 Date of Suspension: {latest_date}")
            st.write(f"📅 Date of Return: {return_date}")
            st.write(f"🔴 Ban Reason: {reason}")
        else:
            st.write(f"✅ **{name} is not in the system**")

# ➕ Add new sanction
with tab2:
    st.subheader("Add a New Sanction")
    new_name = st.text_input("Name:")
    new_sanction = st.text_area("Sanction Details:")
    new_ban_status = st.selectbox("Ban Status:", ["No", "Yes"])
    new_date_of_suspension = str(datetime.date.today())
    new_date_of_return = st.date_input("Date of Return:")
    new_ban_reason = st.text_area("Ban Reason (Action for ban):")

    if st.button("Save Sanction"):
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
            st.success(f"Sanction for {new_name} added!")

# 📜 View all records
with tab3:
    st.subheader("All Sanctions & Ban Records")
    if sanctions_db:
        for person, records in sanctions_db.items():
            st.write(f"**{person}**")
            for record in records:
                st.write(f"- 📅 Date of Suspension: {record['date_of_suspension']}")
                st.write(f"📅 Date of Return: {record['date_of_return']}")
                st.write(f"🔴 Sanction: {record['sanction']}")
                st.write(f"🔴 Ban Reason: {record['ban_reason']}")
                st.write(f"⚠️ Ban Status: {'BANNED' if record['ban_status'] == 'Yes' else 'NOT BANNED'}")
    else:
        st.write("No records yet.")

