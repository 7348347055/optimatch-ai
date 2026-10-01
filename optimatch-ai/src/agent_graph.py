import os
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# Define the State Dictionary passed between agents
class AgentState(TypedDict):
    resume_text: str
    job_description: str
    extracted_profile: str
    gap_analysis: str
    recommendations: str

def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2,max_retries=5)

# Agent 1: Profiler
def profiler_node(state: AgentState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        "Extract core competencies, technical skills, and experiences from the following resume. Format as a clean summary:\n{resume_text}"
    )
    chain = prompt | llm
    result = chain.invoke({"resume_text": state["resume_text"]})
    return {"extracted_profile": result.content}

# Agent 2: Benchmarker
def benchmark_node(state: AgentState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        "Compare this candidate profile against the job description. Identify missing critical skills, ATS keyword gaps, and industry benchmarks.\n\nProfile:\n{profile}\n\nJob Description:\n{jd}"
    )
    chain = prompt | llm
    result = chain.invoke({
        "profile": state["extracted_profile"],
        "jd": state["job_description"]
    })
    return {"gap_analysis": result.content}

# Agent 3: Optimizer
def optimization_node(state: AgentState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        "Based on this gap analysis, provide 3 to 5 highly actionable recommendations to optimize this resume for ATS screening. Suggest specific bullet-point rewrites.\n\nGap Analysis:\n{gap_analysis}"
    )
    chain = prompt | llm
    result = chain.invoke({"gap_analysis": state["gap_analysis"]})
    return {"recommendations": result.content}

def build_optimatch_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("Profiler", profiler_node)
    workflow.add_node("Benchmarker", benchmark_node)
    workflow.add_node("Optimizer", optimization_node)
    
    workflow.set_entry_point("Profiler")
    workflow.add_edge("Profiler", "Benchmarker")
    workflow.add_edge("Benchmarker", "Optimizer")
    workflow.add_edge("Optimizer", END)
    
    return workflow.compile()