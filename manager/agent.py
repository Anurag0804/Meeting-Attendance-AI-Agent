from google.adk.agents import SequentialAgent
from manager.sub_agents.ocr_agent.agent import ocr_agent
from manager.sub_agents.attendance_agent.agent import attendance_agent

root_agent = SequentialAgent(
    name="zoom_attendance_root_agent",
    # description="Extract names from screenshots and mark attendance in Excel.",
    sub_agents=[ocr_agent, attendance_agent]
)
