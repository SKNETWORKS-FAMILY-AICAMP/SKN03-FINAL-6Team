from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor

def create_agent(client, tools, prompt):
    return create_openai_functions_agent(client, tools, prompt)

def agent_excute(agent_outcome, tools):
    tool_executor = ToolExecutor(tools)
    return tool_executor.invoke(agent_outcome)

def is_agent_finish(agent_outcome):
    return isinstance(agent_outcome, AgentFinish)