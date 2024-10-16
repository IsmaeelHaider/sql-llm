from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseSequentialChain
from pydantic import BaseModel

from api.integrations.db import db, db_schema
from api.integrations.openai import llm, PROMPT

llm_router = APIRouter(tags=["llm"])


class QuestionSchema(BaseModel):
    question: str


@llm_router.get(
    "/ask/",
)
async def ask_llm(request: QuestionSchema) -> StreamingResponse:
    """Endpoint to ask question to llm with streaming response."""

    schema = db_schema
    question = request.question
    decider_template = f"""Given an input question, identify the most relevant tables in the database to answer the question.
    Database schema:
    {schema}
    Question: {question}
    Relevant tables:"""
    decider_prompt = PromptTemplate(
        input_variables=["schema", "question"], template=decider_template
    )
    # decider_chain = LLMChain(llm=llm, prompt=decider_prompt)
    db_chain = SQLDatabaseSequentialChain.from_llm(
        llm=llm, db=db, decider_prompt=decider_prompt, verbose=True
    )

    async def generate():
        # Get the result of the chain (this will still run sequentially)
        result = db_chain.run(PROMPT.format(question=request.question))

        # Split the result into smaller chunks for streaming
        # (You might need to adjust the chunk size)
        chunk_size = 50
        for i in range(0, len(result), chunk_size):
            yield result[i : i + chunk_size]

    return StreamingResponse(generate(), media_type="text/event-stream")