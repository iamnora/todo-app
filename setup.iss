[Setup]
AppName=Sevimli ToDo List
AppVersion=1.0
DefaultDirName={pf}\Sevimli ToDo List
DefaultGroupName=Sevimli ToDo List
OutputDir=output
OutputBaseFilename=SevimliToDoList_Setup

[Files]
Source: "dist\Sevimli ToDo List.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "todo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sevimli ToDo List"; Filename: "{app}\Sevimli ToDo List.exe"; IconFilename: "{app}\todo.ico"
Name: "{commondesktop}\Sevimli ToDo List"; Filename: "{app}\Sevimli ToDo List.exe"; IconFilename: "{app}\todo.ico" 