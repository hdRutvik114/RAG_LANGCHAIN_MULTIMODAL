from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class GenerationService:
    def __init__(self, chat_model: BaseChatModel):
        self.chat_model = chat_model

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a precise document question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not invent facts.
- If the context does not contain the answer, clearly say so.
- Cite supporting pages using [Page X].
- Be clear and concise.

Context:
{context}"""
            ),
            ("human", "{question}"),
        ])

        self.chain = self.prompt | self.chat_model | StrOutputParser()

    def generate(self, question: str, context: str) -> str:
        if not question.strip():
            raise ValueError("Question cannot be empty")

        if not context.strip():
            return "I couldn't find relevant information in the provided documents."

        return self.chain.invoke({
            "question": question,
            "context": context,
        })