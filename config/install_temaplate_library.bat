@echo off
setlocal EnableExtensions

rem REPO_DIR es la raiz del repositorio (un nivel arriba de config\)
set "REPO_DIR=%~dp0.."
if "%REPO_DIR:~-1%"=="\" set "REPO_DIR=%REPO_DIR:~0,-1%"

set "BIN_DIR=%USERPROFILE%\bin"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

if exist "%BIN_DIR%\crear-proyecto.cmd" del "%BIN_DIR%\crear-proyecto.cmd"

(
echo @echo off
echo py "%REPO_DIR%\src\crear_proyecto.py" %%*
) > "%BIN_DIR%\create_project.cmd"

(
echo @echo off
echo py "%REPO_DIR%\src\md_a_latex.py" %%*
) > "%BIN_DIR%\md-a-latex.cmd"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$bin = [Environment]::GetFolderPath('UserProfile') + '\bin'; " ^
  "$path = [Environment]::GetEnvironmentVariable('Path', 'User'); " ^
  "$repoSrc = '%REPO_DIR%\src'; " ^
  "$pythonPath = [Environment]::GetEnvironmentVariable('PYTHONPATH', 'User'); " ^
  "if ([string]::IsNullOrWhiteSpace($path)) { [Environment]::SetEnvironmentVariable('Path', $bin, 'User') } " ^
  "elseif (($path -split ';' | ForEach-Object { $_.Trim() }) -notcontains $bin) { [Environment]::SetEnvironmentVariable('Path', $path + ';' + $bin, 'User') } " ^
  "if ([string]::IsNullOrWhiteSpace($pythonPath)) { [Environment]::SetEnvironmentVariable('PYTHONPATH', $repoSrc, 'User') } " ^
  "elseif (($pythonPath -split ';' | ForEach-Object { $_.Trim() }) -notcontains $repoSrc) { [Environment]::SetEnvironmentVariable('PYTHONPATH', $pythonPath + ';' + $repoSrc, 'User') }"

echo.
echo Instalacion completada.
echo.
echo Comandos disponibles en una nueva terminal:
echo   create_project project_name
echo   create_project project_name --type latex
echo   create_project project_name --type julia
echo   create_project project_name --2route D:\Projects
echo   md-a-latex informe.md --compilar
echo.
echo Tambien se agrego src\ a PYTHONPATH de usuario:
echo   %REPO_DIR%\src
echo Asi podras usar import funciones_template as ft desde cualquier proyecto.

endlocal