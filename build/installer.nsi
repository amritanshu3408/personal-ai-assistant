; Basic NSIS installer skeleton for Personal AI Assistant
; Customize product paths after electron-builder / PyInstaller output exists.

!define PRODUCT_NAME "Personal AI Assistant"
!define PRODUCT_VERSION "0.1.0"
!define PRODUCT_PUBLISHER "Personal"

Name "${PRODUCT_NAME}"
OutFile "PersonalAIAssistant-Setup.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  ; File /r "..\electron\dist\*"
  ; File /r "..\backend\dist\*"
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\Personal AI Assistant.exe"
SectionEnd
