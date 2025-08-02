import streamlit as st
from datetime import date
from PIL import Image
import numpy as np
import pandas as pd
import easyocr
import io

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# OCR extraction with filtering
def extract_names_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image_np = np.array(image)
    results = reader.readtext(image_np, detail=0)

    EXCLUDE_KEYWORDS = ["Mute", "Unmute", "Zoom", "Recording", "Live", "AM", "PM"]
    names = [
        line.strip()
        for line in results
        if line.strip()
        and 2 <= len(line.strip()) <= 30
        and 1 <= len(line.strip().split()) <= 5
        and any(c.isalpha() for c in line.strip())
        and not any(excl.lower() in line.lower() for excl in EXCLUDE_KEYWORDS)
    ]

    seen = set()
    unique_names = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)
    return unique_names

# Initialize session state
if 'excel_ready' not in st.session_state:
    st.session_state.excel_ready = False
if 'excel_data' not in st.session_state:
    st.session_state.excel_data = None
if 'selected_names' not in st.session_state:
    st.session_state.selected_names = []
if 'all_names_for_dates' not in st.session_state:
    st.session_state.all_names_for_dates = {}
if 'combined_names' not in st.session_state:
    st.session_state.combined_names = []

st.title("📸 PresenceAI")

uploaded_files = st.file_uploader(
    "Upload meeting participant screenshot(s):",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write("## 📅 Select Date for Each Uploaded Screenshot")

    files_and_dates = []
    for idx, uploaded_file in enumerate(uploaded_files):
        st.write(f"### 📄 {uploaded_file.name}")
        selected_date = st.date_input(
            f"Select attendance date for {uploaded_file.name}",
            value=date.today(),
            key=f"date_{idx}_{uploaded_file.name}"
        )
        files_and_dates.append((uploaded_file, selected_date))

    if st.button("Extract Names"):
        st.session_state.all_names_for_dates = {}
        combined_names = set()

        for uploaded_file, selected_date in files_and_dates:
            st.write(f"🔍 Extracting from **{uploaded_file.name}** ...")
            names = extract_names_from_image(uploaded_file)
            st.write(f"✅ Names detected in {uploaded_file.name}:")
            st.json(names if names else "_No names detected. Check image clarity._")

            date_str = selected_date.strftime("%Y-%m-%d")
            if date_str not in st.session_state.all_names_for_dates:
                st.session_state.all_names_for_dates[date_str] = set()
            st.session_state.all_names_for_dates[date_str].update(names)
            combined_names.update(names)

        st.session_state.combined_names = sorted(list(combined_names))
        st.session_state.excel_ready = False

if st.session_state.combined_names:
    st.write("## ✅ Preview Detected Names")
    selected_names = st.multiselect(
        "Select participant names to include in attendance:",
        options=st.session_state.combined_names,
        default=st.session_state.combined_names
    )

    if st.button("Confirm and Generate Attendance Sheet"):
        if not selected_names:
            st.warning("⚠️ Please select at least one name to generate attendance.")
        else:
            combined_df = pd.DataFrame({'Name': selected_names})
            for date_str in st.session_state.all_names_for_dates.keys():
                combined_df[date_str] = combined_df['Name'].apply(
                    lambda x: '✔️' if x in st.session_state.all_names_for_dates[date_str] else '✖️'
                )

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                combined_df.to_excel(writer, index=False, sheet_name='Attendance')
            output.seek(0)

            st.session_state.excel_data = output.getvalue()
            st.session_state.excel_ready = True
            st.success("✅ Attendance sheet generated! Download below.")

# Always show the download button if the Excel is ready
if st.session_state.excel_ready:
    st.download_button(
        label="📥 Download Attendance Sheet",
        data=st.session_state.excel_data,
        file_name="attendance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
