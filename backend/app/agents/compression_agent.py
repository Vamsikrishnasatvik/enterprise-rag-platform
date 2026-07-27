import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.compression_service import compress_context

logger = logging.getLogger(__name__)

# Compress anything larger than roughly one page of text
COMPRESSION_THRESHOLD = 1000


class CompressionAgent(BaseAgent):

    def __init__(self):
        super().__init__("CompressionAgent")

    def run(self, state: GraphState) -> GraphState:

        chunks = state.get("retrieved_chunks", [])

        # ---------------------------------------------------------
        # Nothing Retrieved
        # ---------------------------------------------------------

        if not chunks:

            logger.info(
                "Compression skipped | no retrieved chunks"
            )

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

        logger.info(
            "Compression Check | chunks=%d | context_length=%d",
            len(chunks),
            len(context),
        )

        # ---------------------------------------------------------
        # Skip Compression for Small Context
        # ---------------------------------------------------------

        if len(context) < COMPRESSION_THRESHOLD:

            logger.info(
                "Skipping compression | context already small"
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
        # Compress Context
        # ---------------------------------------------------------

        logger.info(
            "Compressing context..."
        )

        compressed = compress_context(
            question=state["question"],
            context=context,
        )

        # ---------------------------------------------------------
        # Compression Fallback
        # ---------------------------------------------------------

        if not compressed or not compressed.strip():

            logger.warning(
                "Compression returned empty context. "
                "Using original context."
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
                "compression_ratio": round(
                    len(compressed) / max(len(context), 1),
                    2,
                ),
            }
        )

        return state