import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.compression_service import compress_context

logger = logging.getLogger(__name__)

# Compress anything larger than roughly one page of text.
COMPRESSION_THRESHOLD = 1000


class CompressionAgent(BaseAgent):
    """
    Compresses large retrieval contexts before answer generation.

    Small contexts are passed through unchanged to avoid unnecessary
    LLM calls and preserve maximum context.
    """

    def __init__(self):
        super().__init__("CompressionAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        chunks = state.get(
            "retrieved_chunks",
            [],
        )

        # ---------------------------------------------------------
        # Nothing Retrieved
        # ---------------------------------------------------------

        if not chunks:

            logger.info(
                "Compression skipped | no retrieved chunks"
            )

            state.update(
                {
                    "retrieval_context": "",
                }
            )

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": self.name,
                    "compressed": False,
                    "reason": "no_chunks",
                }
            )

            return state

        # ---------------------------------------------------------
        # Build Context
        # ---------------------------------------------------------

        context = "\n\n".join(
            chunk.payload.get(
                "content",
                "",
            ).strip()
            for chunk in chunks
        )

        context_length = len(context)

        logger.info(
            "Compression Check | chunks=%d | context_length=%d",
            len(chunks),
            context_length,
        )

        # ---------------------------------------------------------
        # Skip Compression
        # ---------------------------------------------------------

        if context_length < COMPRESSION_THRESHOLD:

            logger.info(
                "Skipping compression | context already small"
            )

            state.update(
                {
                    "retrieval_context": context,
                }
            )

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": self.name,
                    "compressed": False,
                    "reason": "small_context",
                    "context_length": context_length,
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
            question=state.get(
                "question",
                "",
            ),
            context=context,
        )

        # ---------------------------------------------------------
        # Fallback
        # ---------------------------------------------------------

        if not compressed or not compressed.strip():

            logger.warning(
                "Compression returned empty context. "
                "Using original context."
            )

            compressed = context

        compressed_length = len(compressed)

        compression_ratio = round(
            compressed_length / max(context_length, 1),
            2,
        )

        logger.info(
            "Compression completed | original=%d | compressed=%d",
            context_length,
            compressed_length,
        )

        state.update(
            {
                "retrieval_context": compressed,
            }
        )

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "compressed": True,
                "original_length": context_length,
                "compressed_length": compressed_length,
                "compression_ratio": compression_ratio,
            }
        )

        return state