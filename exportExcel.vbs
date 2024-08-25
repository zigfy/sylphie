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
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[1]/usr/ctxtDY_PATH").text = "C:\Users\zigfy\Documents\SAP\SAP GUI\"
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "FILENAME.XLS"
session.findById("wnd[1]/usr/ctxtDY_PATH").setFocus
session.findById("wnd[1]/usr/ctxtDY_PATH").caretPosition = 47
session.findById("wnd[1]/tbar[0]/btn[0]").press
