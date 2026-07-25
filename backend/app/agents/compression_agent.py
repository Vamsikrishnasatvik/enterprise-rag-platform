import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.compression_service import compress_context

logger = logging.getLogger(__name__)


class CompressionAgent(BaseAgent):

    def __init__(self):
        super().__init__("CompressionAgent")

    def run(self, state: GraphState) -> GraphState:

        chunks = state.get("retrieved_chunks", [])

        # ---------------------------------------------------------
        # Nothing Retrieved
        # ---------------------------------------------------------

        if not chunks:

            logger.info("Compression skipped | no retrieved chunks")

            state["retrieval_context"] = ""

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": "CompressionAgent",
                    "compressed": False,
                    "reason": "no_chunks",
                }
            )

            return state

        # ---------------------------------------------------------
        # Build Context
        # ---------------------------------------------------------

        context = "\n\n".join(
            chunk.payload.get("content", "")
            for chunk in chunks
        )

        # ---------------------------------------------------------
        # Skip Compression for Small Contexts
        # ---------------------------------------------------------

        if len(chunks) <= 3 or len(context) < 4000:

            logger.info(
                "Skipping compression | chunks=%d | context_length=%d",
                len(chunks),
                len(context),
            )

            state["retrieval_context"] = context

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": "CompressionAgent",
                    "compressed": False,
                    "reason": "small_context",
                    "context_length": len(context),
                }
            )

            return state

        # ---------------------------------------------------------
        # Compress Large Context
        # ---------------------------------------------------------

        compressed = compress_context(
            question=state["question"],
            context=context,
        )

        # Fallback if compression fails or returns empty
        if not compressed.strip():

            logger.warning(
                "Compression returned empty context. Falling back to original."
            )

            compressed = context

        logger.info(
            "Compression completed | original=%d | compressed=%d",
            len(context),
            len(compressed),
        )

        state["retrieval_context"] = compressed

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "CompressionAgent",
                "compressed": True,
                "original_length": len(context),
                "compressed_length": len(compressed),
            }
        )

        return state