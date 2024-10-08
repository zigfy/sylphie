import subprocess
# vbs login part ->
# session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "{username}"
# session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "{password}"
# session.findById("wnd[0]/usr/pwdRSYST-BCODE").setFocus
# session.findById("wnd[0]/usr/pwdRSYST-BCODE").caretPosition = Len("{password}")
# session.findById("wnd[0]").sendVKey 0

def create_vkp2_script(file_path, username, password, transaction, skus, store, start_date, end_date, export_path, filename):
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
session.findById("wnd[0]/tbar[0]/okcd").text = "{transaction}"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/btn%_S_MATNR_%_APP_%-VALU_PUSH").press
'''
   for i, sku in enumerate(skus):
      vbs_script += f'''session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,0]").text = "{sku}"\n
                        session.findById("wnd[1]").sendVKey 13'''
                        
   vbs_script += f'''
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[1]/tbar[0]/btn[8]").press
session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "{store}"
session.findById("wnd[0]/usr/ctxtS_DATUM-LOW").text = "{start_date}"
session.findById("wnd[0]/usr/ctxtS_DATUM-HIGH").text = "{end_date}"
session.findById("wnd[0]/tbar[1]/btn[8]").press 'execution f9
session.findById("wnd[0]/tbar[1]/btn[26]").press 'normal view
session.findById("wnd[0]/tbar[1]/btn[38]").press 'grid control
session.findById("wnd[0]/tbar[1]/btn[45]").press 'export file
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").select 'option 1
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus 'option 2
session.findById("wnd[1]/tbar[0]/btn[0]").press 'confirm export
session.findById("wnd[1]/usr/ctxtDY_PATH").text = "{export_path}" 'dir path
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "{filename}.htm" 'filename
session.findById("wnd[1]/usr/ctxtDY_PATH").caretPosition = Len("{export_path}")
session.findById("wnd[1]").sendVKey 0
session.findById("wnd[0]/tbar[0]/okcd").text = "/n/n/n/n/n"
session.findById("wnd[0]").sendVKey 0
'''
   
   with open(file_path, 'w') as file:
      file.write(vbs_script)
      
   return file_path

########################################################

def cret_vkp2_script(file_path: str, username: str, password: str, transaction: str, skus: list, store: str, start_date, end_date, export_path: str, filename: str) -> list:
   vbs_files = []
   htm_files = []
   chunk_size = 100
   skus_chunks = [skus[i:i + chunk_size] for i in range(0, len(skus), chunk_size)]
   files = []

   for idx, skus_chunk in enumerate(skus_chunks):
      lote_filename = f"{filename}_lote_{idx+1}.htm"

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
      session.findById("wnd[0]/tbar[0]/okcd").text = "{transaction}"
      session.findById("wnd[0]").sendVKey 0
      session.findById("wnd[0]/usr/btn%_S_MATNR_%_APP_%-VALU_PUSH").press
      '''

      for sku in skus_chunk:
            vbs_script += f'''
            session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,0]").text = "{sku}"
            session.findById("wnd[1]").sendVKey 13
            '''

      vbs_script += f'''
      session.findById("wnd[1]/tbar[0]/btn[0]").press
      session.findById("wnd[1]/tbar[0]/btn[8]").press
      session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "{store}"
      session.findById("wnd[0]/usr/ctxtS_DATUM-LOW").text = "{start_date}"
      session.findById("wnd[0]/usr/ctxtS_DATUM-HIGH").text = "{end_date}"
      session.findById("wnd[0]/tbar[1]/btn[8]").press 'execution f9
      session.findById("wnd[0]/tbar[1]/btn[26]").press 'normal view
      session.findById("wnd[0]/tbar[1]/btn[38]").press 'grid control
      session.findById("wnd[0]/tbar[1]/btn[45]").press 'export file
      session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").select 'option 1
      session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus 'option 2
      session.findById("wnd[1]/tbar[0]/btn[0]").press 'confirm export
      session.findById("wnd[1]/usr/ctxtDY_PATH").text = "{export_path}" 'dir path
      session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "{lote_filename}" 'filename
      session.findById("wnd[1]/usr/ctxtDY_PATH").caretPosition = Len("{export_path}")
      session.findById("wnd[1]").sendVKey 0
      session.findById("wnd[0]/tbar[0]/okcd").text = "/n/n/n/n/n"
      session.findById("wnd[0]").sendVKey 0
      '''

      with open(f"{file_path}_lote_{idx+1}.vbs", 'w') as file:
         file.write(vbs_script)
      
      vbs_files.append(f"{export_path + filename}_lote_{idx+1}.vbs")
      htm_files.append(f"{export_path + filename}_lote_{idx+1}.htm")

   return vbs_files, htm_files