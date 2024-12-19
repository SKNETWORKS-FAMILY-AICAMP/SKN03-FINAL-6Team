from langgraph.graph import StateGraph, END
from .agentstate_option import AgentState
from langchain_core.agents import AgentFinish
from .agent import agent_excute

def build_workflow(agent_runnable):
    def run_agent(data):
        return {"agent_outcome": agent_runnable.invoke(data)}

    def execute_tools(data):
        agent_action = data['agent_outcome']
        output = agent_excute(agent_action, None)
        return {"intermediate_steps": [(agent_action, str(output))]}

    def should_continue(data):
        if isinstance(data['agent_outcome'], AgentFinish):
            return "end"
        else:
            return "continue"

    workflow = StateGraph(state_schema=AgentState)
    workflow.add_node("agent", run_agent)
    workflow.add_node("action", execute_tools)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END
        }
    )
    workflow.add_edge('action', 'agent')
    
    return workflow