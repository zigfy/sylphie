import subprocess

def run_sap_script(vbs_files: list):
    for vbs_files in vbs_files:
        try:
            print(f'{vbs_files}')
            result = subprocess.run(['cscript', f'{vbs_files}'], capture_output=True, text=True)
            if result.returncode == 0:
                print("Script executado com sucesso!")
                print(result.stdout)
            else:
                print("Erro ao executar o VBS script.")
                print(result.stderr)
        except Exception as e:
            print(f"Ocorreu um erro não mapeado: {e}")