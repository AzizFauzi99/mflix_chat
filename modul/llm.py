from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.engine = os.environ['ENGINE']
        self.api_key = os.environ['OPENAI_API_AZURE_KEY']
        self.azure_endpoint = os.environ['OPENAI_API_BASE']
        self.api_version = os.environ['OPENAI_API_VERSION']
        self.embedding_model = os.environ['OPENAI_API_EMBEDDINGS_MODEL']
        self.chat_model = os.environ['OPENAI_AZURE_MODEL']
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=self.api_version
        )

    def get_embedding(self, text):
        """
        Generate embeddings for the given text using the specified model.
        """
        try:
            response = self.client.embeddings.create(input=text, model=self.embedding_model).data[0].embedding
            return response
        except Exception as e:
            return str(e)

    def chat(self, question, context, stream=False, temperature=0):
        """
        Chat with the model using the provided question and context.
        """
        try:

            f = open("D:/Gen-AI/mflix-testing/prompt/template.txt","r")
            persona = f.read()
            f.close()

            # context retrieval
            context_str = ""
            for item in context:
                context_str += str(item) + "\n"
            context_str = context_str.strip()

            response = self.client.chat.completions.create(
                stream=stream,
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": persona},
                    {"role": "system", "content": context_str},
                    {"role": "user", "content": question}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)

   