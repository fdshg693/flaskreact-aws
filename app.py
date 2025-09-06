import streamlit as st

st.set_page_config(page_title="Hello Streamlit on AWS", page_icon="🟢")
st.title("Hello, AWS + Streamlit!")
name = st.text_input("お名前は？", "")
st.write("こんにちは！" if name == "" else f"こんにちは、{name}さん！")
