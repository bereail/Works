' Lanzador de un solo clic para el proyecto Freelancer
' - No muestra ventana de consola
' - Si el servidor ya está corriendo en :8002, no lo duplica
' - Si no está corriendo, lo levanta en segundo plano y espera a que responda
' - Abre el navegador en http://127.0.0.1:8002/

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strPath

Function ServidorActivo()
    On Error Resume Next
    Set objHTTP = CreateObject("WinHttp.WinHttpRequest.5.1")
    objHTTP.SetTimeouts 500, 500, 500, 500
    objHTTP.Open "GET", "http://127.0.0.1:8002/", False
    objHTTP.Send
    ServidorActivo = (Err.Number = 0) And (objHTTP.Status = 200)
    On Error Goto 0
End Function

If Not ServidorActivo() Then
    objShell.Run """" & strPath & "\iniciar_oculto.bat""", 0, False

    ' Esperar hasta que el servidor responda (máx ~10 segundos)
    intentos = 0
    Do While (Not ServidorActivo()) And intentos < 20
        WScript.Sleep 500
        intentos = intentos + 1
    Loop
End If

objShell.Run "http://127.0.0.1:8002/", 1, False
