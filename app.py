import streamlit as st
from source.streamlit_auth import get_auth
import psutil
import plotly.express as px

if __name__ == '__main__':

    # pages config
    st.set_page_config(
        page_title="Welcome page",
        page_icon="Welcome",
    )

    # memory
    available_vmem = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 2)

    # streamlit auth
    name, authentication_status, username, authenticator = get_auth(st.secrets["auth_path"])

    if authentication_status:
        authenticator.logout('Logout', 'main')
        if 'st_started' not in st.session_state:
            with st.spinner("Стартуем"):
                st.session_state['st_started'] = True

        # start page
        st.write("# Welcome to the main page")
        st.plotly_chart(
            px.pie(values=[psutil.cpu_percent(), 100 - psutil.cpu_percent()],
                   names=["Used CPU", "Free CPU"],
                   color=["Used CPU", "Free CPU"],
                   color_discrete_map={"Used CPU": "tomato", "Free CPU": "oceanblue"},
                   hole=0.5)
        )
        st.plotly_chart(px.pie(values=[psutil.virtual_memory().percent, 100 - psutil.virtual_memory().percent],
                               names=["Used VMEM", "Free VMEM"],
                               color=["Used VMEM", "Free VMEM"],
                               color_discrete_map={"Used VMEM": "tomato", "Free VMEM": "oceanblue"},
                               hole=0.5)
                        )

    elif not authentication_status:
        st.error('Username/password is incorrect')
        try:
            del st.session_state['st_started']
        except KeyError as e:
            print(e)
            pass
    elif authentication_status is None:
        st.warning('Please enter your username and password')
        try:
            del st.session_state['st_started']
        except KeyError as e:
            print(e)
            pass