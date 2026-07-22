import logging

from pydantic_ai import Agent, RunContext

from agents.dependencies import AgentDependencies

from prompts.refusal_prompt import REFUSAL_PROMPT

from utils.audit_logger import log_tool_invocation


logger = logging.getLogger(__name__)


def register_tools(
    agent: Agent,
) -> None:
    """
    Registers all tools used by the Policy Agent.
    """


    @agent.tool
    def retrieve_policy(
        ctx: RunContext[AgentDependencies],
        query: str,
    ) -> dict:
        """
        Retrieves relevant HR & IT policy information
        from the vector database.

        Returns:
            context:
                Retrieved policy text for the LLM.

            sources:
                Document names and page numbers.
        """

        logger.info(
            "Retriever Tool invoked for query: %s",
            query,
        )

        log_tool_invocation(
            "Policy Retriever Tool",
        )


        retrieved_chunks = ctx.deps.retriever.search(
            query=query,
        )


        logger.info(
            "Retriever returned %d chunk(s).",
            len(retrieved_chunks),
        )


        if not retrieved_chunks:

            logger.warning(
                "No policy information found for query: %s",
                query,
            )

            return {
                "context": REFUSAL_PROMPT,
                "sources": [],
            }


        formatted_chunks = []

        sources = []


        for chunk in retrieved_chunks:

            formatted_chunks.append(
                (
                    f"Source: {chunk.source}\n"
                    f"Page: {chunk.page}\n"
                    f"Chunk ID: {chunk.chunk_id}\n"
                    f"Similarity Score: "
                    f"{chunk.similarity_score:.4f}\n\n"
                    f"Content:\n"
                    f"{chunk.content}"
                )
            )


            sources.append(
                {
                    "document": chunk.source,
                    "page": chunk.page,
                }
            )


        logger.info(
            "Formatted %d retrieved chunk(s).",
            len(retrieved_chunks),
        )


        context = (
            "Retrieved Policy Context\n"
            "=========================\n\n"
            "The following information was retrieved "
            "from Nimbus Technologies HR & IT policy documents.\n\n"
            "Instructions:\n"
            "- Answer ONLY using retrieved policy information.\n"
            "- Do NOT use outside knowledge.\n"
            "- If information is insufficient, refuse politely.\n"
            "- Mention source document name and page number.\n\n"
            +
            ("\n" + "=" * 80 + "\n").join(
                formatted_chunks
            )
        )


        return {
            "context": context,
            "sources": sources,
        }



    @agent.tool
    def calculate_completed_months(
        ctx: RunContext[AgentDependencies],
        joining_date: str,
        reference_date: str,
    ) -> int:
        """
        Calculates completed months of service.
        """

        logger.info(
            "Completed Months Tool invoked."
        )

        log_tool_invocation(
            "Completed Months Tool",
        )


        completed_months = (
            ctx.deps.calculator.completed_months(
                joining_date=joining_date,
                reference_date=reference_date,
            )
        )


        logger.info(
            "Completed months calculated: %d",
            completed_months,
        )


        return completed_months



    @agent.tool
    def calculate_leave_balance(
        ctx: RunContext[AgentDependencies],
        completed_months: int,
        accrual_rate: float,
    ) -> float:
        """
        Calculates employee accrued leave balance.
        """

        logger.info(
            "Leave Calculator Tool invoked."
        )

        log_tool_invocation(
            "Leave Calculator Tool",
        )


        leave_balance = (
            ctx.deps.calculator.calculate_leave_balance(
                completed_months=completed_months,
                accrual_rate=accrual_rate,
            )
        )


        logger.info(
            "Calculated leave balance: %.2f",
            leave_balance,
        )


        return leave_balance



    @agent.tool
    def calculate_notice_period(
        ctx: RunContext[AgentDependencies],
        completed_months: int,
        minimum_months: int,
        lower_notice_days: int,
        higher_notice_days: int,
    ) -> int:
        """
        Calculates employee notice period.
        """

        logger.info(
            "Notice Period Tool invoked."
        )

        log_tool_invocation(
            "Notice Period Tool",
        )


        notice_period = (
            ctx.deps.calculator.calculate_notice_period(
                completed_months=completed_months,
                minimum_months=minimum_months,
                lower_notice_days=lower_notice_days,
                higher_notice_days=higher_notice_days,
            )
        )


        logger.info(
            "Calculated notice period: %d",
            notice_period,
        )


        return notice_period



    @agent.tool
    def calculate_years_of_service(
        ctx: RunContext[AgentDependencies],
        completed_months: int,
    ) -> float:
        """
        Converts completed months into years of service.
        """

        logger.info(
            "Years of Service Tool invoked."
        )

        log_tool_invocation(
            "Years of Service Tool",
        )


        years = (
            ctx.deps.calculator.years_of_service(
                completed_months=completed_months,
            )
        )


        logger.info(
            "Calculated years of service: %.2f",
            years,
        )


        return years



    @agent.tool
    def get_current_date(
        ctx: RunContext[AgentDependencies],
    ) -> str:
        """
        Returns today's system date.
        """

        logger.info(
            "Date Tool invoked."
        )

        log_tool_invocation(
            "Date Tool",
        )


        today = ctx.deps.date_tool.today()


        logger.info(
            "Current date: %s",
            today,
        )


        return today