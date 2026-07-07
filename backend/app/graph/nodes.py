from app.graph.state import GraphState

from app.agents.query_agent import QueryAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.answer_agent import AnswerAgent


query_agent = QueryAgent()
retriever_agent = RetrieverAgent()
answer_agent = AnswerAgent()


async def query_node(state: GraphState) -> GraphState:
    return await query_agent.run(state)


async def retriever_node(state: GraphState) -> GraphState:
    return await retriever_agent.run(state)


async def answer_node(state: GraphState) -> GraphState:
    return await answer_agent.run(state)