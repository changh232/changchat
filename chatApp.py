import streamlit as st
from openai import AzureOpenAI
import AIConfig

st.title("testApp")

client = AzureOpenAI(
    api_key = AIConfig.api_key,
    api_version = AIConfig.api_version,
    azure_endpoint = AIConfig.api_base
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "say yes only"}
    ]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    stream = client.chat.completions.create(
        model = AIConfig.model,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True
    )
    response = st.write_stream(stream)
st.session_state.messages.append({"role": "assistant", "content": response})

# chat_completion = client.chat.completions.create(
#     model = AIConfig.model,
#     messages = [
#         {"role": "system", "content": "say yes only"},
#         {"role": "user", "content": "say no"}
#     ],
#     stream=True
# )