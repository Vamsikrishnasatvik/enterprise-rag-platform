from langgraph.graph import START, END, StateGraph

from app.graph.state import GraphState
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.answer_agent import AnswerAgent

supervisor = SupervisorAgent()
retriever = RetrieverAgent()
answer = AnswerAgent()


def supervisor_node(state: GraphState):
    return supervisor(state)


def retriever_node(state: GraphState):
    return retriever(state)


def answer_node(state: GraphState):
    return answer(state)


def build_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("answer", answer_node)

    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", "retriever")
    workflow.add_edge("retriever", "answer")
    workflow.add_edge("answer", END)

    return workflow.compile()


graph = build_workflow()