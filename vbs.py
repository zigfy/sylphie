import subprocess

def create_vbs_script(file_path, username, password, transaction, skus, store, start_date, end_date, export_path, export_file):
    vbs_script = f'''
If Not IsObject(application) Then
   Set SapGuiAuto  = GetObject("SAPGUI")
   Set application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(connection) Then
   Set connection = application.Children(0)
End If
If Not IsObject(session) Then
   Set session    = connection.Children(0)
End If
If IsObject(WScript) Then
   WScript.ConnectObject session,     "on"
   WScript.ConnectObject application, "on"
End If
session.findById("wnd[0]").maximize
session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "{username}"
session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "{password}"
session.findById("wnd[0]/usr/pwdRSYST-BCODE").setFocus
session.findById("wnd[0]/usr/pwdRSYST-BCODE").caretPosition = Len("{password}")
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/tbar[0]/okcd").text = "{transaction}"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/btn%_S_MATNR_%_APP_%-VALU_PUSH").press
'''
    for i, sku in enumerate(skus):
        vbs_script += f'session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,{i}]").text = "{sku}"\n'
    
    vbs_script += f'''
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[1]/tbar[0]/btn[8]").press
session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "{store}"
session.findById("wnd[0]/usr/ctxtS_DATUM-LOW").text = "{start_date}"
session.findById("wnd[0]/usr/ctxtS_DATUM-HIGH").text = "{end_date}"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/tbar[1]/btn[8]").press
session.findById("wnd[0]/tbar[1]/btn[26]").press
session.findById("wnd[0]/tbar[1]/btn[38]").press
session.findById("wnd[0]/tbar[1]/btn[45]").press
session.findById("wnd[1]/usr/ctxtDY_PATH").text = "{export_path}"
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "{export_file}"
session.findById("wnd[1]").sendVKey 0
session.findById("wnd[0]/tbar[0]/okcd").text = "/n/n/n/n/n"
session.findById("wnd[0]").sendVKey 0
    '''
    
    with open(file_path, 'w') as file:
        file.write(vbs_script)

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

# Parâmetros do Script
file_path = "sap_script.vbs"
username = "seu_usuario_sap"
password = "sua_senha_sap"
transaction = "VKP2"
skus = ["5100695", "5062938", "5071190"]
store = "1048"
start_date = "01.08.2023"
end_date = "31.08.2023"
export_path = "C:\\Users\\zigfy\\Documents\\SAP\\SAP GUI\\"
export_file = "FILE_LOCAL.XLS"

# Gerar e executar o script VBS
create_vbs_script(file_path, username, password, transaction, skus, store, start_date, end_date, export_path, export_file)
run_sap_script(file_path)
