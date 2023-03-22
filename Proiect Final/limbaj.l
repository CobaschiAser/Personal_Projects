%{
#include <stdio.h>
#include "y.tab.h"
#include "Types.h"

%}
%option noyywrap
%%

"int" { yylval.varType = strdup(yytext); return TIP; }
"float" { yylval.varType = strdup(yytext); return TIP; }
"bool" { yylval.varType = strdup(yytext); return TIP; }
"char" { yylval.varType = strdup(yytext); return TIP; }
"string" { yylval.varType = strdup(yytext); return TIP; }
"const" {return CONST;}

@[a-zA-Z][a-zA-Z0-9]* { yylval.varName = strdup(yytext); return ID; }

"=" {return ASSIGN;}

[0-9]+ { yylval.intVal = atoi(yytext); return NR_INT;}

[0-9]+[.][0-9]+ {  float number = 0;
                        int i = 0;
                        while(yytext[i] != '.'){
                            number *= 10;
                            number += (yytext[i] - '0');
                            i++;
                        }
                        i++;
                        int decimal=1;
                        float FloatNumber;
                        while(yytext[i]!='\0'){
                            FloatNumber *= 10;
                            FloatNumber += (yytext[i] - '0');
                            i++;
                            decimal *= 10;
                        }
                        number=number+FloatNumber/decimal;
                        yylval.floatVal = number; 
                        return NR_FLOAT;
                     }
 
"true" { yylval.boolVal=1; return BOOL_VAL;}
"false" { yylval.boolVal=0; return BOOL_VAL;}

\"[a-zA-Z0-9]*\" { yylval.stringVal = strdup(yytext); return EXPLICIT_STRING;}
\'[a-zA-Z0-9]\' { char* ch = strdup(yytext); yylval.charVal = ch[0]; return EXPLICIT_CHAR;}

"return" {return RETURN;}
"if" {return IF;}
"else" {return ELSE;}
"then" {return THEN;}
"for" {return FOR;}
"while" {return WHILE;}
"do" {return DO;}
"class" {return CLASS;}

"&&" {return AND;}
"||" {return OR;}

"<" {return LESS;}
">" {return GREATER;}
"==" {return EQ;}
"!=" {return NEQ;}
">=" {return GEQ;}
"<=" {return LEQ;}

"Eval" {return EVAL;}
"TypeOf" {return TYPEOF;}
"Main" {return MAIN;}

[ \t] ;
\n {yylineno++;}
. {return yytext[0];}
