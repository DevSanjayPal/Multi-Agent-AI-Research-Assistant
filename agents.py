from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
from rich import print

load_dotenv()

llm = ChatMistralAI(model = "SxiiGf9hSwSzfbKN1WHhQXdIFgcDinjE", temperature=0)

# 1st agent
def search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

# 2nd agent
def reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )

# Chains / runables
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.
     
     Topic : {topic}
     Research Gathered: {research}
     Structure the report as:
     - Instroduction
     - Key Finding( minimum 3 well-explained poimts)
     - Conclusion
     - Sources (List all URLs found in the research)

     Be detailed, factual and   professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()  # 1st chain

# Critic chain / Feedback or score chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive reseaarch critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.
     
     Report: {report}

     Respond in this exact format:

     Score: X/10

     Strengths:
     - ...
     - ...
     
     Areas to improve:
     - ...
     - ...
     
      One line verdict:
     ..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()  # 2nd chain
