import sys
import os
from dotenv import load_dotenv
from agency_swarm import set_openai_key
from agency_swarm.agents.browsing import BrowsingAgent
from agency_swarm import Agency, Agent

sys.path.append("../agency_swarm")


load_dotenv()
set_openai_key(os.getenv("OPENAI_API_KEY"))


report_manager = Agent(
    name="Report Manager",
    description="The Report Manager Agent is responsible for supervising data collection from various weather websites and compiling reports as necessary.",
    instructions="As a Report Manager Agent, your role involves direct interaction and oversight of the BrowsingAgent's operations. Your primary duty is to guarantee that the user's task is comprehensively and accurately completed. Achieve this by methodically breaking down each task from the user into smaller steps required to complete it. Then, issue each step of the task as a distinct message to the BrowsingAgent. Make sure to always tell the browsing agent to go back to google search results before proceeding to the the next source. After the necessary data is collection, compile a report and send it to the user. Make sure to ask the browsing agent for direct links to the sources and include them into report. Try to trouble shoot any issues that may arise along the way with the other agents first, before reporting back to the user. Do not respond to the user until the report is complete or you have encountered an issue that you cannot resolve yourself.",
    file_ids=[],
    tools=[],
)


browsing_agent = BrowsingAgent()
# browsing_agent.instructions += "your goal is to analyze my linkedin for relevant experience/skills." # insert credentials here


agency = Agency(
    [report_manager, [report_manager, browsing_agent]],
    shared_instructions="You are a part of a data collection agency with the goal to find the most relevant information about people on the web. Your core value is autonomy and you are free to use any means necessary to achieve your goal. You do not stop until you have found the information you need or you have exhausted all possible means. You always to to compile a comprehensive report with as much information from the web pages as possible.",
)


agency.demo_gradio(height=700)


# demo.close()
