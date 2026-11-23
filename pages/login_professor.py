import streamlit as st

from database.queries import buscar_professor_por_email
from database.security import verificar_senha


st.set_page_config(
    page_title="Login - Professor",
    page_icon="👨‍🏫"
)


st.title(" Área do Professor")

st.write("Entre com seus dados para acessar o sistema.")


email = st.text_input("E-mail")

senha = st.text_input(
    "Senha",
    type="password"
)


st.divider()


if st.button(
    "ENTRAR",
    use_container_width=True
):

    if not email or not senha:

        st.warning(
            "Preencha o e-mail e a senha."
        )

    else:

        professor = buscar_professor_por_email(email)

        if professor is None:

            st.error(
                "E-mail ou senha incorretos."
            )

        else:

            senha_correta = verificar_senha(
                senha,
                professor[4]
            )

            if senha_correta:

                st.session_state["professor_logado"] = True

                st.session_state["professor_id"] = professor[0]

                st.session_state["professor_escola_id"] = professor[1]

                st.session_state["nome_professor"] = professor[2]

                st.switch_page(
                    "pages/painel_professor.py"
                )

            else:

                st.error(
                    "E-mail ou senha incorretos."
                )