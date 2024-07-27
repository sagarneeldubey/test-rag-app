import os

from haystack import Pipeline
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from TestApp.config import settings
from haystack.utils import Secret


os.environ["OPENAI_API_KEY"] = "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"


def get_query_response(query: str):

    fetcher = LinkContentFetcher()
    converter = HTMLToDocument()
    prompt_template = """
    According to the contents of this website:
    {% for document in documents %}
    {{document.content}}
    {% endfor %}
    Answer the given question: {{query}}
    Answer:
    """
    prompt_builder = PromptBuilder(template=prompt_template)
    llm = OpenAIGenerator(
        api_key=Secret.from_token(settings["OPENAI_API_KEY"]), model="gpt-3.5-turbo"
    )

    pipeline = Pipeline()
    pipeline.add_component("fetcher", fetcher)
    pipeline.add_component("converter", converter)
    pipeline.add_component("prompt", prompt_builder)
    pipeline.add_component("llm", llm)

    pipeline.connect("fetcher.streams", "converter.sources")
    pipeline.connect("converter.documents", "prompt.documents")
    pipeline.connect("prompt.prompt", "llm.prompt")

    result = pipeline.run(
        {
            "fetcher": {"urls": ["https://haystack.deepset.ai/overview/quick-start"]},
            "prompt": {"query": query},
        }
    )

    return result["llm"]["replies"][0]
