import streamlit as st
import hashlib
from datetime import datetime

# Dados dos usuários diretamente no código
USERS = {
    "filipe": {
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "admin"
    },
    "tiagofholanda": {
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "admin"
    },
    "aluno1": {
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "aluno"
    },
    "aluno2": {
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "aluno"
    },
    "aluno3": {
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "aluno"
    },
    "aluno4": {
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "aluno"
    },
    "aluno5": {
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "aluno"
    }
}

def get_users():
    return USERS

def login(redirect_to=None):
    """
    Exibe o formulário de login e gerencia a autenticação do usuário.
    
    Args:
        redirect_to: Página para redirecionar após o login bem-sucedido
    """
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        if redirect_to:
            st.switch_page(redirect_to)
        return True
    
    # Estilo profissional para o formulário de login
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
            box-sizing: border-box;
        }
        
        .login-wrapper {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .login-container {
            width: 100%;
            max-width: 480px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(8.5px);
            padding: 40px;
            position: relative;
            overflow: hidden;
        }
        
        .login-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            pointer-events: none;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 32px;
        }
        
        .login-logo {
            width: 80px;
            height: 80px;
            margin: 0 auto 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 32px;
            font-weight: 700;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .login-title {
            color: #2c3e50;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 8px;
        }
        
        .login-subtitle {
            color: #7f8c8d;
            font-size: 14px;
            margin: 0;
        }
        
        .stTextInput>div>div>input {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 14px 16px;
            font-size: 15px;
            transition: all 0.3s ease;
            background-color: #f8f9fa;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            background-color: white;
        }
        
        .stButton>button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 8px 0 24px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 24px 0;
            color: #95a5a6;
            font-size: 14px;
        }
        
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #e0e0e0;
            margin: 0 12px;
        }
        
        .contact-info {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 24px;
            border-left: 4px solid #667eea;
            position: relative;
            overflow: hidden;
        }
        
        .contact-info::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .contact-info h4 {
            color: #2c3e50;
            margin: 0 0 12px;
            font-size: 16px;
            display: flex;
            align-items: center;
        }
        
        .contact-info h4 svg {
            margin-right: 8px;
            color: #667eea;
        }
        
        .contact-info p {
            color: #7f8c8d;
            font-size: 14px;
            margin: 0 0 16px;
            line-height: 1.5;
        }
        
        .whatsapp-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #25D366;
            color: white !important;
            text-decoration: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        }
        
        .whatsapp-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
            text-decoration: none;
        }
        
        .whatsapp-link svg {
            margin-right: 8px;
            width: 20px;
            height: 20px;
        }
        
        .stAlert {
            border-radius: 8px;
            padding: 12px 16px;
        }
        
        @media (max-width: 576px) {
            .login-container {
                padding: 30px 20px;
                margin: 20px;
            }
            
            .login-title {
                font-size: 24px;
            }
        }
    </style>
    
    <div class="login-wrapper">
        <div class="login-container">
            <div class="login-header">
                <div class="login-logo">F</div>
                <h1 class="login-title">Acesso ao Curso</h1>
                <p class="login-subtitle">Faça login para continuar</p>
            </div>
    """, unsafe_allow_html=True)
    
    # Campos do formulário
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    # Botão de login
    if st.button("Entrar"):
        users = get_users()
        if username in users and users[username]["password"] == hashlib.sha256(password.encode()).hexdigest():
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username]["role"]
            st.session_state["login_time"] = datetime.now().isoformat()
            st.rerun()
        else:
            st.error("❌ Credenciais inválidas. Verifique seu usuário e senha.")
    
    # Divisor
    st.markdown("<div class='divider'>ou</div>", unsafe_allow_html=True)
    
    # Seção de contato
    st.markdown("""
    <div class="contact-info">
        <h4><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg> Precisa de Acesso?</h4>
        <p>Entre em contato pelo WhatsApp para obter suas credenciais de acesso ao curso de francês.</p>
        <a href="https://wa.me/5511999999999" class="whatsapp-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
            Falar no WhatsApp
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Impede que o usuário acesse outras partes do app sem fazer login
    st.stop()
    
    # Mensagens de login removidas conforme solicitado

def logout():
    """Realiza o logout do usuário e redireciona para a página de login"""
    # Limpa todos os dados da sessão
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Redireciona para a página de introdução
    st.switch_page("pages/00_Introdução.py")

def auth_required(admin_only=False):
    """
    Decorador para proteger rotas que requerem autenticação.
    
    Args:
        admin_only: Se True, apenas usuários com papel de admin podem acessar
        
    Returns:
        bool: True se autenticado, caso contrário redireciona para login
    """
    # Verifica se o usuário está autenticado
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        # Obtém o caminho do script atual de forma compatível
        import inspect
        import os
        frame = inspect.currentframe()
        try:
            # Tenta obter o caminho do arquivo que chamou esta função
            frame_info = inspect.getouterframes(frame)[1]
            script_path = os.path.basename(frame_info.filename)
            # Armazena a página atual para redirecionar após o login
            login(redirect_to=script_path)
        finally:
            del frame  # Importante para evitar vazamento de memória
        return False
    
    # Verifica se é necessário privilégio de admin
    if admin_only and st.session_state.get("role") != "admin":
        st.error("🔒 Acesso negado. Apenas administradores podem acessar esta página.")
        st.stop()
        return False
    
    # Adiciona botão de logout no canto superior direito
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Sair", key="logout_btn"):
            logout()
    
    return True
