@echo off
yacc -d parser.y
lex spec_v2.lxi
gcc lex.yy.c parser.tab.c -o result
.\result ..\test_programs\test.txt