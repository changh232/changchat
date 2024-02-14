import AIConfig
import streamlit as st
from streamlit_option_menu import option_menu

## bot config ##
st.session_state["openai_model"] = AIConfig.model
client = AIConfig.client
p_type = 0

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

    st.session_state.messages = [{"role":"system","content": AIConfig.types[choice]}]
    st.markdown("[![SKcc](https://www.skcc.co.kr/img/Image_Resource.SK_SVG.svg?0CBb3gEwrwAJW+94rlh_8Q)](https://www.skcc.co.kr/)")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask your question"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message 
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        # for m in st.session_state.messages:
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
print(st.session_state.messages)
