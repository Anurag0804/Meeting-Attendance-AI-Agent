
## 📸 Zoom Attendance Marker

A **Streamlit app powered by EasyOCR** to automate **Zoom participant attendance tracking** directly from meeting screenshots. Upload multiple participant screenshots, select attendance dates, extract names, confirm participants, and download a clean Excel sheet for your records.

---

## 🚀 Features

✅ **Upload Multiple Screenshots:** Drag and drop Zoom participant screenshots.
✅ **Per-Date Selection:** Assign attendance dates for each screenshot individually.
✅ **Accurate OCR:** Uses EasyOCR with smart filtering to extract participant names reliably.
✅ **Preview & Confirm:** Review detected names and deselect any incorrect entries before recording attendance.
✅ **Dynamic Excel Generation:** Generates an `.xlsx` attendance sheet in-memory without saving to disk.
✅ **Downloadable Records:** Download your attendance sheet instantly for record-keeping.
✅ **Streamlit-based:** Clean, interactive, and lightweight.

---

## 🛠️ Tech Stack

* **Python 3.11+**
* **Streamlit** for UI
* **EasyOCR** for text extraction
* **Pandas & XlsxWriter** for Excel handling
* **Google ADK 1.4.2** (structure ready for conversational extension)

---

## 📂 Project Structure

```
ZOOM ATTENDENCE AGENT/
│
├── .venv/                   # Virtual environment (excluded by .gitignore)
├── .env                     # Environment variables if needed
├── .gitignore
├── README.md                # This documentation file
├── requirements.txt         # Dependencies
├── app.py                   # Streamlit app entry point
│
├── manager/
│   ├── __init__.py
│   ├── agent.py             # Root agent (for ADK routing if extended)
│   ├── .env                 # ADK environment configuration
│   │
│   └── sub_agents/
│       ├── __init__.py
│       │
│       ├── ocr_agent/
│       │   ├── __init__.py
│       │   └── agent.py     # Handles OCR extraction using EasyOCR
│       │
│       └── attendance_agent/
│           ├── __init__.py
│           └── agent.py     # Handles attendance Excel generation logic


```

---

## ⚡ Setup Instructions


1️⃣ **Create Virtual Environment:**

```bash
python -m venv .venv
```

2️⃣ **Activate Environment:**

* **Windows:**

  ```bash
  .venv\Scripts\activate
  ```
* **macOS/Linux:**

  ```bash
  source .venv/bin/activate
  ```

3️⃣ **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4️⃣ **Run the App:**

```bash
streamlit run app.py
```

---

## 🖼️ Usage

1️⃣ **Upload participant screenshots** (PNG, JPG, JPEG).
2️⃣ **Assign attendance dates** for each screenshot.
3️⃣ Click **“Extract Names”** to detect participant names.
4️⃣ **Review and confirm detected names** (deselect non-participants if needed).
5️⃣ Click **“Confirm and Generate Attendance Sheet”**.
6️⃣ Click **“Download Attendance Sheet”** to save your Excel file.

---

## 📝 Output Excel Sheet

* Column 1: **Name**
* Subsequent columns: **Dates with ✔️ for present, ✖️ for absent.**
* Auto-updates based on your uploaded files and selected dates.

---

## 🩶 Notes

✅ No paid APIs (uses EasyOCR and local processing).
✅ Structure aligned for **Google ADK integration** if you wish to extend with conversational flows later.

---

## 💡 Optional Future Enhancements

* Face-matching integration for improved accuracy.
* Auto-date detection from screenshot file names.
* CSV export option alongside Excel.
* Deployment on Streamlit Community Cloud for easy sharing.

---

## 📧 Contact

If you face issues or wish to extend the project:

**Anurag Ray Chaudhuri**
📧 \anuragrc27@gmail.com

---
