from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedln import scrape_linkedln_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from dotenv import load_dotenv
from output_parser import summary_parser, Summary
from typing import Tuple
import os


def ice_break_with(name: str,)->Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedln_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template = """"
    Given the Linkedin information {information} about a person give me the following
    1. A short Summary
    2. An Interesting Fact
    3. If the person has any enemy

    \n{format_instructions}

    """

    summary_prompt_template = PromptTemplate(
       input_variables= "information" , template=summary_template,
       partial_variables= {"format_instructions":summary_parser.get_format_instructions()},
   ) 

    llm = ChatOllama(model="llama3")
    #llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")

    #chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser    
    res:Summary = chain.invoke(input={"information":linkedin_data})
    return res, linkedin_data.get("profile_pic_url")


if __name__ == '__main__' :
    print("Enter Ice-Breaker")
    load_dotenv()
    ice_break_with(name="Shreya Chakraborty USF Accenture")
  