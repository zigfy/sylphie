import subprocess

def run_sap_script(script_path):
    try:
        result = subprocess.run(['cscript', script_path], capture_output=True, text=True)
        if result.returncode == 0:
            print("Script executado com sucesso!")
            print(result.stdout)
        else:
            print("Erro na execução do script.")
            print(result.stderr)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")