from app.graph.state import GraphState

from app.agents.query_agent import QueryAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.answer_agent import AnswerAgent


query_agent = QueryAgent()
retriever_agent = RetrieverAgent()
answer_agent = AnswerAgent()


def query_node(state: GraphState) -> GraphState:
    return query_agent.run(state)


def retriever_node(state: GraphState) -> GraphState:
    return retriever_agent.run(state)


def answer_node(state: GraphState) -> GraphState:
    return answer_agent.run(state)