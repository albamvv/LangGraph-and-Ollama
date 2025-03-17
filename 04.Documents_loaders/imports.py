from langchain_community.document_loaders import PyMuPDFLoader
import os
import tiktoken
from langchain_ollama import ChatOllama
from langchain_core.prompts import (SystemMessagePromptTemplate, HumanMessagePromptTemplate,
                                    ChatPromptTemplate)
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
import asyncio
import re
from scripts import llm