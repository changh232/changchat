import os
import streamlit as st
from streamlit_option_menu import option_menu
from openai import AzureOpenAI
import AIConfig

## bot config ##
st.session_state["openai_model"] = os.environ['OPENAI_MODEL']
client = AzureOpenAI(
    azure_endpoint=os.environ['OPENAI_API_URI'],
    api_key=os.environ['OPENAI_API_KEY'],
    api_version=os.environ['OPENAI_API_VERSION']
)

## page layout ##
st.set_page_config(
    page_title="Ins Bot",
    page_icon="🛤",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Assistant")

with st.sidebar:
    choice = option_menu("Bot", list(AIConfig.types.keys()),
                            icons=["house", "kanban", "bi bi-robot"],
                            menu_icon="app-indicator", default_index=0,
                            styles={
                                "container": {"padding": "4!important", "background-color": "#fafafa"},
                                "icon": {"color": "black", "font-size": "25px"},
                                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#fafafa"},
                                "nav-link-selected": {"background-color": "#08c7b4"}
                            }, key='menu')
    ai_mess = st.chat_message("human")
    ai_mess.write(f"보험 {choice} 도우미")
    if "AItype" not in st.session_state:
        st.session_state["AItype"] = choice
    if st.session_state["AItype"] != choice:
        st.session_state.messages.append({"role":"system","content": AIConfig.types[choice]})

    st.markdown("[![SKcc](https://www.skcc.co.kr/img/Image_Resource.SK_SVG.svg?0CBb3gEwrwAJW+94rlh_8Q)](https://www.skcc.co.kr/)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.chat.completions.create(
        model=st.session_state["openai_model"], messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
