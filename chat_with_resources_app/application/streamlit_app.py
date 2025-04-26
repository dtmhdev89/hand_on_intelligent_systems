from application import add_project_root_to_system_path
add_project_root_to_system_path()

import os
from typing import Literal, TypeAlias
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
# from langchain.chains.question_answering import load_qa_chain  # will be deprecated
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from chat_with_resources_app.components.resources_parsers.pdf_parser import PdfParser
from chat_with_resources_app.components.embeddings.embeddings import Embeddings
from chat_with_resources_app.components.vector_searchs.vector_search import VectorSearch
from chat_with_resources_app.components.llm_providers.llm_provider import LlmProvider
from chat_with_resources_app.components.llm_providers.api_key_validator import ApiKeyValidator


class ResourcesChatApp:

    SupportedAIProvider: TypeAlias = Literal[
        "openai",
        "google-genai"
    ]

    def __init__(self, ai_provider: SupportedAIProvider):
        self.ai_provider = ai_provider
        self._qa_prompt = None
    
    def gui(self):
        st.set_page_config(page_title="Chat to your resources app")
        st.header("Chat to your resources app")

        ApiKeyValidator(ai_provider=self.ai_provider).validate_and_input()
        api_key_set = os.environ.get(
            ApiKeyValidator.AI_PROVIDER_ENV_KEY[self.ai_provider]
        )

        if  api_key_set:
            pdf_file = st.file_uploader("Upload a PDF", type="pdf")
            
            if pdf_file is not None:
                pdf_parser = PdfParser(pdf_file)
                text = pdf_parser.extract_text()
                
                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,  # characters
                    chunk_overlap=200,  # characters
                    length_function=len
                )

                chunks = text_splitter.split_text(text)

                embeddings = Embeddings(
                    emb_type="google-genai"
                ).factory_embedding()
                vector_search = VectorSearch(
                    search_algorithm="faiss",
                    embeddings=embeddings
                ).factory_search()
                vector_search.build_text_indexes(chunks)

                user_question = st.text_input("Ask a Question about the resources:")

                if user_question:
                    docs = vector_search.similarity_search(user_question)
                    llm_provider = LlmProvider(
                        provider=self.ai_provider
                    ).factory_provider()
                    llm = llm_provider.llm
                    cb = llm_provider.fn_callback

                    chain = self._setup_chain(llm=llm)

                    if cb:
                        with cb:
                            response = chain.invoke(
                                {
                                    "context": docs,
                                    "question": user_question
                                }
                            )
                    else:
                        response = chain.invoke(
                            {
                                "context": docs,
                                "question": user_question
                            }
                        )

                    st.write(response)
    
    def _setup_chain(self, llm):
        chain = create_stuff_documents_chain(
            llm=llm,
            prompt=self._qa_prompt_template(),
            document_variable_name="context"
        )

        return chain

    def _qa_prompt_template(self):
        """Prompt Template for qa"""

        if self._qa_prompt is None:
            self._qa_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""You are a helpful assistant. 
                Use the following context to answer the question.

                Context:
                {context}

                Question: {question}
                Answer:"""
            )

        return self._qa_prompt


ResourcesChatApp(ai_provider="google-genai").gui()
