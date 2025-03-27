import streamlit as st

st.title("🎈 My new app - RIGEL PARCO")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

st.button("I hate you", type="primary")
if st.button("I love you"):
    st.write("I love you too")
else:
    st.write("I love you though")

if st.button("Dont click it", type="primary"):
    st.write("[click this link](https://www.youtube.com/watch?v=dQw4w9WgXcQ).")
