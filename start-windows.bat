@echo off
REM Hermes for Web 실행 배치 파일 (Windows용)
chcp 65001 > nul
echo =======================================
echo Hermes Web UI 서버를 시작합니다.
echo =======================================
set HERMES_WEBUI_PORT=8788

REM 가상환경이 있으면 활성화
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

python server.py
pause
