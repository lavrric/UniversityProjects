@echo off
lex spec.lxi
gcc lex.yy.c -o lexus
if not ERRORLEVEL 1 (
    .\lexus.exe ../test_programs/p1_err.txt
) else (
    echo !!!! !!!! Lex compiling failed !!!! !!!!
)


