@echo off
set PATH=%CD%;%PATH%;
call "%~dp0\javasdk"
"%JDK%\jdb" -connect "com.sun.jdi.SocketAttach:hostname=localhost,port=6002"