import azure.functions as func

import fastapi
from typing import List
import logging
from TestApp.pipeline import get_query_response

LOGGER = logging.getLogger(__name__)
app = fastapi.FastAPI()

from pydantic import BaseModel


class Request(BaseModel):
    query: str


@app.post("/query")
async def whitelist_categories(req: Request) -> str:
    """ """
    LOGGER.info(f"Query sent: {req} ")

    response = get_query_response(req.query)
    return response
