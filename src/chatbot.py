from anthropic import Anthropic

from config import IDENTITY, MODEL, TASK_SPECIFIC_INSTRUCTIONS

anthropic_api_key = ""


class ChatBot:
    def __init__(self, session_state):
        self.anthropic = Anthropic(api_key=anthropic_api_key)
        self.session_state = session_state

        # Inicializa o sistema com as instruções apenas uma vez
        if "system_initialized" not in self.session_state:
            self.initialize_system()

    def initialize_system(self):
        self.session_state.system_initialized = True
        self.session_state.context_message = {
            "role": "user",
            "content": TASK_SPECIFIC_INSTRUCTIONS,
        }

        # Gera a primeira resposta do sistema com o contexto completo
        init_response = self.generate_message(
            messages=[self.session_state.context_message], max_tokens=100
        )

        if init_response.content[0].type == "text":
            self.session_state.system_response = {
                "role": "assistant",
                "content": init_response.content[0].text,
            }

    def generate_message(self, messages, max_tokens):
        try:
            response = self.anthropic.messages.create(
                model=MODEL,
                system=IDENTITY,
                max_tokens=max_tokens,
                messages=messages,
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_recent_messages(self, num_messages=5):
        # Retorna as mensagens mais recentes para contexto
        return (
            self.session_state.messages[-num_messages:]
            if len(self.session_state.messages) > num_messages
            else self.session_state.messages
        )

    def process_user_input(self, user_input):
        # Adiciona a nova mensagem do usuário
        self.session_state.messages.append({"role": "user", "content": user_input})

        # Usa apenas as mensagens recentes para contexto
        # context = self.get_recent_messages()

        # Prepara o contexto para a API
        context = [
            self.session_state.context_message,  # Inclui o contexto inicial
            self.session_state.system_response,  # Inclui a resposta inicial do sistema
        ] + self.get_recent_messages()  # Adiciona as mensagens recentes

        response_message = self.generate_message(
            messages=context,
            max_tokens=2048,
        )

        if "error" in response_message:
            return f"An error occurred: {response_message['error']}"

        if response_message.content[0].type == "text":
            response_text = response_message.content[0].text
            self.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
            return response_text
        else:
            raise Exception("An error occurred: Unexpected response type")
