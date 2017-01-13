@echo off
set PATH=%CD%;%PATH%;
"%~dp0\java" signapktool.jar "%~dp0\sign\testkey.x509.pem" "%~dp0\sign\testkey.pk8" %*