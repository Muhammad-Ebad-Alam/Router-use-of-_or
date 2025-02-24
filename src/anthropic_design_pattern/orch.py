from typing import cast
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

class InstructionGenrater(BaseModel):
    work_instructions: list[str] = Field(description="list of instructions")

@task
def call_orchestrator(idea: str):
    instructions = llm.with_structured_output(InstructionGenrater).invoke(
        f"generate instructions for the workers to generate a Idea validation report for the following idea: {idea} Keep workers count under 3"
    )
    return instructions
@task 
def call_worker(instruction: str):
    return llm.invoke(instruction).content

@task 
def combine_result(result: list[str])->str:
    return "\n\n".join(result)

@entrypoint()
def orchestrator_worker(idea: str):
    instructions = call_orchestrator(idea).result()
    workers = [call_worker(instruction) for instruction in instructions.work_instructions]
    result = [worker.result() for worker in workers]
    final_result = combine_result(result).result()
    return final_result

def main():
    final_result = orchestrator_worker.invoke("creating a lead generation agent")
    print("\n\n",final_result)
    






