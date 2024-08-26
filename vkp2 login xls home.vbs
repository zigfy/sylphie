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
'Rem get logged
session.findById("wnd[0]").maximize
session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "zigfy"
session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "password"
session.findById("wnd[0]/usr/pwdRSYST-BCODE").setFocus
session.findById("wnd[0]/usr/pwdRSYST-BCODE").caretPosition = 12
session.findById("wnd[0]").sendVKey 0
'end of login
'search for VKP2
session.findById("wnd[0]/tbar[0]/okcd").text = "VKP2"
session.findById("wnd[0]").sendVKey 0
'get SKUs
session.findById("wnd[0]/usr/btn%_S_MATNR_%_APP_%-VALU_PUSH").press
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,0]").text = "5100695"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,1]").text = "5062938"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,2]").text = "5100695"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,3]").text = "5062938"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,4]").text = "5071190"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,5]").text = "751790"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,6]").text = "5067891"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL-SLOW_I[1,7]").text = "5126817"
session.findById("wnd[1]/tbar[0]/btn[0]").press 'verify if the entries are correct
session.findById("wnd[1]/tbar[0]/btn[8]").press 'confirm skus
session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "1048" 'enter store(s)
session.findById("wnd[0]/usr/ctxtS_DATUM-LOW").text = "01.08.2023" 'start date
session.findById("wnd[0]/usr/ctxtS_DATUM-HIGH").text = "31082023" 'end date
session.findById("wnd[0]/usr/ctxtS_DATUM-HIGH").setFocus
session.findById("wnd[0]/usr/ctxtS_DATUM-HIGH").caretPosition = 8
session.findById("wnd[0]").sendVKey 0 'confirm with enter
'export xls file
session.findById("wnd[0]/tbar[1]/btn[8]").press
session.findById("wnd[0]/tbar[1]/btn[26]").press
session.findById("wnd[0]/tbar[1]/btn[38]").press
session.findById("wnd[0]/tbar[1]/btn[45]").press
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[1]/usr/ctxtDY_PATH").text = "C:\Users\zigfy\Documents\SAP\SAP GUI\" 'filepath
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "FILE LOCAL.XLS" 'filename
session.findById("wnd[1]/usr/ctxtDY_FILENAME").caretPosition = 14
session.findById("wnd[1]").sendVKey 0
'file saved

session.findById("wnd[0]/tbar[0]/okcd").text = "home" 'trying to get homepage
session.findById("wnd[0]").sendVKey 0 'pressed enter
session.findById("wnd[0]/tbar[0]/btn[3]").press
session.findById("wnd[0]/tbar[0]/btn[3]").press 'tryied to click on green "v" button
session.findById("wnd[0]/tbar[0]/okcd").text = "/n/n/n/n/n" 'entered into homepage successfully
session.findById("wnd[0]").sendVKey 0
