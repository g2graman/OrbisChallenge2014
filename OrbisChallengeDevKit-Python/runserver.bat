@ECHO OFF

set JDK_HOME05="C:\Program Files\Java\jdk1.8.0_20\bin"
set JRE8="C:\Program Files\Java\jre8\bin"

set JDK_HOME86_05="C:\Program Files (x86)\Java\jdk1.8.0_20\bin"
set JRE868="C:\Program Files (x86)\Java\jre8\bin"

set JARPATH="lib\tron.jar"

echo [Checking Path Variable]
java.exe -version >nul 2>&1
if ERRORLEVEL 1 goto :UserHome05
ECHO [Java Found]
java.exe -jar %JARPATH% %*
goto :eof


:UserHome05
echo [Checking Default Jdk 1.8.0_20 Folder]
IF DEFINED JDK_HOME05 %JDK_HOME05%\java.exe -version >nul 2>&1
if ERRORLEVEL 1 goto :UserHome05_86
ECHO [Java Found]
%JDK_HOME05%\java.exe -jar %JARPATH% %*
goto :eof


:UserHome05_86
IF DEFINED JDK_HOME86_05 %JDK_HOME86_05%\java.exe -version >nul 2>&1
if ERRORLEVEL 1 goto :JREHome
ECHO [Java Found]
%JDK_HOME86_05%\java.exe -jar %JARPATH% %*
goto :eof


:JREHome
echo [Checking Default Jre8 Folder]
IF DEFINED JRE8 %JRE8%\java.exe -version >nul 2>&1
if ERRORLEVEL 1 goto :JREHome86
ECHO [Java Found]
%JRE8%\java.exe -jar %JARPATH% %*
goto :eof


:JREHome86
IF DEFINED JRE868 %JRE868%\java.exe -version >nul 2>&1
if ERRORLEVEL 1 goto :usage
ECHO [Java Found]
%JRE868%\java.exe -jar %JARPATH% %*
goto :eof

:usage
echo java.exe was not found on your path!
echo This script requires:
echo 1) an installation of the Java Development Kit or an installation of the Java Runtime Environment, and
echo 2) either java.exe is on the path, or that the one of JAVA_HOME, JDK_HOME or JRE_HOME environment variables 
echo is set and points to the installation directory. If not, it will look under
echo C:\Program Files\Java\jdk1.1.8.0_20\bin and 
echo C:\Program Files\Java\jre8\bin
