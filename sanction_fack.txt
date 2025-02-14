import streamlit as st
import pandas as pd
from datetime import datetime

# File to store sanction data
DATA_FILE = "sanctions_register.csv"

# Load or initialize CSV
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Name", "Ban", "Sanctions"])
    df.to_csv(DATA_FILE, index=False)

# App title
st.title("🏠 FACKtory Sanctions Register")

# **Check if a person is banned or has sanctions**
st.subheader("🔍 Check a person's status")
name = st.text_input("Enter the person's name:")

if name:
    person_data = df[df["Name"].str.lower() == name.lower()]
    
    if not person_data.empty:
        ban_status = person_data.iloc[0]["Ban"]
        sanctions = person_data.iloc[0]["Sanctions"]

        st.write(f"**Ban:** {'❌ Yes' if ban_status == 'Yes' else '✅ No'}")
        st.write(f"**Sanctions:** {sanctions if sanctions else 'No sanctions recorded'}")
    else:
        st.warning("Person not found in the system.")

# **Add a new sanction or ban**
st.subheader("➕ Report a new violation")

new_name = st.text_input("Name of the person being sanctioned:")
sanction = st.text_area("Reason for the sanction:")
ban_option = st.checkbox("Issue a ban")

if st.button("Save"):
    if new_name:
        # Check if the person is already in the database
        if new_name in df["Name"].values:
            df.loc[df["Name"] == new_name, "Sanctions"] += f"\n{datetime.now().date()}: {sanction}"
            if ban_option:
                df.loc[df["Name"] == new_name, "Ban"] = "Yes"
        else:
            # Add new person to the register
            new_entry = pd.DataFrame([{
                "Name": new_name, 
                "Ban": "Yes" if ban_option else "No", 
                "Sanctions": f"{datetime.now().date()}: {sanction}"
            }])
            df = pd.concat([df, new_entry], ignore_index=True)

        df.to_csv(DATA_FILE, index=False)
        st.success(f"Sanction for {new_name} recorded successfully!")
    else:
        st.error("Please enter a name.")
