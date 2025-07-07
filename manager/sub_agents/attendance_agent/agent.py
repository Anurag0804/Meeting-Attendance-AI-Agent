from google.adk.agents import LlmAgent
from google.adk.models import Gemini
import pandas as pd
import io  # for in-memory buffer

def update_attendance(names, date):
    output = io.BytesIO()

    # Create or update DataFrame in memory
    df = pd.DataFrame(columns=['Name'])  # start empty each time

    df['Name'] = names
    df[date] = ['✔️'] * len(names)

    # Write to BytesIO buffer
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')

    output.seek(0)
    return output  # return the in-memory Excel file

attendance_agent = LlmAgent(
    name="excel_updater_agent",
    instruction="Generates an attendance Excel sheet dynamically with extracted names and marks attendance for the selected date, returning it in-memory for download.",
    model=Gemini(model_name="gemini-1.5-flash")
)
