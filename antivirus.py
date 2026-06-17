import subprocess
import sys
import os
import time

def verificar_admin():
    """Garante que o script está rodando com privilégios de Administrador."""
    try:
        # Retorna True se for administrador no Windows
        return os.getuid() == 0 if os.name != 'nt' else subprocess.os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def executar_comando(comando, descricao):
    """Executa um comando no prompt e exibe o progresso."""
    print(f"\n[+] Iniciando: {descricao}...")
    print(f" Executando: {' '.join(comando)}")
    
    # Inicia o processo exibindo a saída direto no terminal
    processo = subprocess.Popen(comando, shell=True)
    processo.wait() # Aguarda a conclusão antes de seguir para o próximo
    
    if processo.returncode == 0:
        print(f"[OK] {descricao} concluído com sucesso!")
    else:
        print(f"[AVISO] {descricao} finalizou com código {processo.returncode}.")

def fechar_processos_suspeitos():
    """Exemplo de uso do taskkill para encerrar processos indesejados (Ex: Bloco de Notas)."""
    # /F força o encerramento | /IM especifica o nome da imagem do processo
    # Adicione ou mude o 'notepad.exe' para o processo que deseja fechar
    comando_kill = ["taskkill", "/F", "/IM", "notepad.exe"]
    executar_comando(comando_kill, "Encerramento de processos indesejados (taskkill)")

def iniciar_antivirus():
    print("=" * 60)
    print("         CONSOLE ANTIVÍRUS - MANUTENÇÃO DO SISTEMA         ")
    print("=" * 60)
    
    # 1. Executa a rotina do taskkill primeiro para liberar memória/recursos
    fechar_processos_suspeitos()
    
    # 2. Loop para rodar o sfc /scannow exatamente 3 vezes
    for i in range(1, 4):
        print(f"\n" + "-"*40)
        print(f" REPARO DO SISTEMA - PASSO {i} DE 3")
        print("-"*40)
        
        comando_sfc = ["sfc", "/scannow"]
        executar_comando(comando_sfc, f"Verificação SFC /SCANNOW (Execução {i})")
        
        # Pequena pausa de 3 segundos entre os escaneamentos
        time.sleep(3)

    print("\n" + "=" * 60)
    print("    PROCESSO CONCLUÍDO: O sistema foi verificado 3 vezes!    ")
    print("=" * 60)

if __name__ == "__main__":
    # Verifica se o script está rodando no Windows
    if os.name != 'nt':
        print("Erro: Este script utiliza ferramentas exclusivas do Windows (sfc e taskkill).")
        sys.exit(1)

    # Verifica permissão de Administrador antes de começar
    if not verificar_admin():
        print("ERRO DE PERMISSÃO: Este script precisa ser executado como ADMINISTRADOR.")
        print("Por favor, abra o Prompt de Comando (cmd) como Administrador e digite: python nome_do_arquivo.py")
        input("\nPressione Enter para sair...")
        sys.exit(1)
        
    iniciar_antivirus()

