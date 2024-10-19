import streamlit as st

from chatbot import ChatBot


def main():
    st.set_page_config(
        page_title="Margarida - Chatbot",
        page_icon="🌼",
    )

    st.title("Me chamo Margarida🌼 e estou aqui ser seu ombro amigo")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chatbot = ChatBot(st.session_state)

    for message in st.session_state.messages:
        if isinstance(message["content"], str):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if user_msg := st.chat_input("Digite sua mensagem aqui..."):
        st.chat_message("user").markdown(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("Estou processando a resposta..."):
                response_placeholder = st.empty()
                full_response = chatbot.process_user_input(user_msg)
                response_placeholder.markdown(full_response)


if __name__ == "__main__":
    main()
