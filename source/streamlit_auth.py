import streamlit_authenticator as stauth
from source.file_opener import yaml_open

def get_auth(path: str) -> tuple:
    yaml_data = yaml_open(path)

    authenticator = stauth.Authenticate(
        yaml_data['credentials']
        , yaml_data['cookie']['name']
        , yaml_data['cookie']['key']
        , yaml_data['cookie']['expiry_days']
    )

    name, authentication_status, username = authenticator.login()
    return name, authentication_status, username, authenticator