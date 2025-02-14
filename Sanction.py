import streamlit as st
import datetime

# Temporary data storage (resets when app restarts)
sanctions_db = {}

# App title
st.title("FACKtory Sanctions & Ban Register 🚫")

# Tabs for different actions
tab1, tab2, tab3 = st.tabs(["🔍 Check Status", "➕ Add Sanction", "📜 View All Records"])

# 🔍 Check if someone is banned
with tab1:
    st.subheader("Check if Someone is Banned")
    name = st.text_input("Enter name:", "")
    if st.button("Check"):
        if name in sanctions_db:
            latest_status = sanctions_db[name][-1]["ban_status"]
            st.write(f"🚨 **{name} is {'BANNED' if latest_status == 'Yes' else 'NOT BANNED'}**")
        else:
            st.write(f"✅ **{name} is not in the system**")

# ➕ Add new sanction
with tab2:
    st.subheader("Add a New Sanction")
    new_name = st.text_input("Name:")
    new_sanction = st.text_area("Sanction Details:")
    new_ban_status = st.selectbox("Ban Status:", ["No", "Yes"])
    new_date = datetime.date.today()

    if st.button("Save Sanction"):
        if new_name:
            if new_name not in sanctions_db:
                sanctions_db[new_name] = []
            sanctions_db[new_name].append({
                "sanction": new_sanction,
                "date": new_date,
                "ban_status": new_ban_status
            })
            st.success(f"Sanction for {new_name} added!")

# 📜 View all records
with tab3:
    st.subheader("All Sanctions & Ban Records")
    if sanctions_db:
        for person, records in sanctions_db.items():
            st.write(f"**{person}**")
            for record in records:
                st.write(f"- 📅 {record['date']}: {record['sanction']} (Ban: {record['ban_status']})")
    else:
        st.write("No records yet.")
