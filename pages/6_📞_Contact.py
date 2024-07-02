import streamlit as st
from chatbox import chatbox

st.set_page_config(page_title='Contact', page_icon='📞', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('📞 Contact Information')
chatbox()

# Contact Information
st.write("**Mr.** Dinh Long Huynh - Master's Student at Uppsala University")
st.write('**Phone:** (+46) 735 671 651 - (+84) 938 548 597')
st.write('**Email:** dinhlong240600@gmail.com')
st.write('**Linkedin:** https://www.linkedin.com/in/dinh-long-huynh-996193241/')
st.write('**GitHub:** https://github.com/DinhLongHuynh')
st.write('*Copyright © 2024 Dinh Long Huynh*')
