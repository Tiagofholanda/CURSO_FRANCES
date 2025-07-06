"""
Script para instalar as dependências do projeto.

Este script verifica e instala as dependências necessárias para executar o aplicativo.
"""
import sys
import subprocess
import platform
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Executa um comando no terminal."""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=cwd,
            universal_newlines=True
        )
        
        # Captura a saída em tempo real
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Verifica se houve erro
        return_code = process.poll()
        if return_code != 0:
            error = process.stderr.read()
            print(f"Erro ao executar o comando: {error}")
            return False
        
        return True
    except Exception as e:
        print(f"Erro ao executar o comando: {e}")
        return False

def check_python_version():
    """Verifica a versão do Python."""
    print("Verificando versão do Python...")
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]}+ é necessário. Versão atual: {current_version.major}.{current_version.minor}")
        return False
    
    print(f"✅ Python {current_version.major}.{current_version.minor} é compatível.")
    return True

def create_virtualenv():
    """Cria um ambiente virtual."""
    print("\nCriando ambiente virtual...")
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')
    
    if os.path.exists(venv_dir):
        print(f"✅ Ambiente virtual já existe em {venv_dir}")
        return True
    
    # Comando para criar o ambiente virtual
    if platform.system() == 'Windows':
        command = f"python -m venv {venv_dir}"
    else:
        command = f"python3 -m venv {venv_dir}"
    
    if run_command(command):
        print(f"✅ Ambiente virtual criado em {venv_dir}")
        return True
    else:
        print("❌ Falha ao criar o ambiente virtual.")
        return False

def activate_virtualenv():
    """Ativa o ambiente virtual."""
    print("\nAtivando ambiente virtual...")
    
    if platform.system() == 'Windows':
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        command = f"{activate_script} && echo Ambiente virtual ativado"
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
        command = f"source {activate_script} && echo Ambiente virtual ativado"
    
    if run_command(command):
        print("✅ Ambiente virtual ativado.")
        return True
    else:
        print("❌ Falha ao ativar o ambiente virtual.")
        return False

def install_requirements():
    """Instala as dependências do projeto."""
    print("\nInstalando dependências...")
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        print(f"❌ Arquivo {requirements_file} não encontrado.")
        return False
    
    if platform.system() == 'Windows':
        pip_cmd = os.path.join('venv', 'Scripts', 'pip')
    else:
        pip_cmd = os.path.join('venv', 'bin', 'pip')
    
    command = f"{pip_cmd} install -r {requirements_file}"
    
    if run_command(command):
        print("✅ Dependências instaladas com sucesso!")
        return True
    else:
        print("❌ Falha ao instalar as dependências.")
        return False

def setup_environment():
    """Configura o ambiente de desenvolvimento."""
    print("\nConfigurando o ambiente de desenvolvimento...")
    
    # Verifica a versão do Python
    if not check_python_version():
        return False
    
    # Cria o ambiente virtual
    if not create_virtualenv():
        return False
    
    # Ativa o ambiente virtual
    if not activate_virtualenv():
        return False
    
    # Instala as dependências
    if not install_requirements():
        return False
    
    print("\n✅ Configuração concluída com sucesso!")
    print("\nPara ativar o ambiente virtual, execute:")
    if platform.system() == 'Windows':
        print("  .\\venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    
    print("\nPara executar o aplicativo, use:")
    print("  streamlit run app.py")
    
    return True

if __name__ == "__main__":
    setup_environment()
