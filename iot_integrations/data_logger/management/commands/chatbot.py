import gradio as gr
import time
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Chatbot'
    
    def handle(self, *args, **options):
        DB_URI = 'sqlite:///db.sqlite3'
        OPENAI_KEY = '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'
        
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.ClearButton([msg, chatbot])

            def respond(message, chat_history):
                llm = OpenAI(temperature=0, openai_api_key=OPENAI_KEY)
                db_uri = DB_URI
                db = SQLDatabase.from_uri(db_uri)
                db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
                bot_message = db_chain.run(message)
                chat_history.append((message, bot_message))
                time.sleep(2)
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])

        demo.launch(server_name="0.0.0.0")