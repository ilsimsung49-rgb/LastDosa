@echo off
set USER_NAME=%USERNAME%
cd /d "C:\Users\%USER_NAME%\Desktop\LastDosa"
"C:\Users\%USER_NAME%\AppData\Local\Programs\Python\Python314\python.exe" -m streamlit run app.py
pause