from app.graph.state import GraphState

from app.agents.query_agent import QueryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.answer_agent import AnswerAgent
from app.agents.verifier_agent import VerifierAgent

query_agent = QueryAgent()
planner_agent = PlannerAgent()
retriever_agent = RetrieverAgent()
answer_agent = AnswerAgent()
verifier_agent = VerifierAgent()

def query_node(state: GraphState) -> GraphState:
    return query_agent.run(state)


def planner_node(state: GraphState) -> GraphState:
    return planner_agent.run(state)


def retriever_node(state: GraphState) -> GraphState:
    return retriever_agent.run(state)


def answer_node(state: GraphState) -> GraphState:
    return answer_agent.run(state)


def verifier_node(state: GraphState) -> GraphState:
    return verifier_agent.run(state)