%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "myfunctions.h"
extern FILE* yyin;
extern char* yytext;

struct variable param_list[20];
int param_count=0;
struct variable localVar[20];
int LocalVarCount=0;
struct variable apel_list[20];
int apel_count=0;
struct variable globalVar[20];
int GlobalVarCount=0;
struct variable ClassVar[20];
int ClassVarCount=0;
struct function ClassFunctions[20];
int ClassFunctionsCount = 0;


%}
%token CONST ASSIGN RETURN IF ELSE THEN FOR WHILE DO CLASS MAIN EVAL TYPEOF 
%token AND OR LESS GREATER EQ NEQ GEQ LEQ
%union {
    char* varType;
    char* varName;
    char* stringVal;
    char charVal;
    int intVal;
    int boolVal;
    float floatVal;
    char* var;
    char functionID[100];
    char typeID[100];
    struct node* ASTnode;
}

%token <varType> TIP
%token <varName> ID
%token <intVal> NR_INT
%token <floatVal> NR_FLOAT
%token <boolVal> BOOL_VAL
%token <charVal> EXPLICIT_CHAR
%token <stringVal> EXPLICIT_STRING

%type <var> returnVar
%type <ASTnode> int_expression
%type <ASTnode> int_expressionVAL
%type <intVal> var
%type <boolVal> bool_expression
%type <functionID> apel
%type <functionID> lista_apel
%type <typeID> typeEXP
%type <intVal> EvalFunc

%left '+' '-'
%left '*' '/'
%left '%'

%left AND OR
%left GEQ LEQ LESS GREATER NEQ EQ

%start progr
%%

progr: global_variables progr      
     | function_declaration progr  
     | user_types progr            
     | main                        {printf("Progrma corect sintactic!\n");fflush(stdout);}
     ;

global_variables : TIP ID ';'                               {globalVar[GlobalVarCount] = declareVar($2, $1, NCONSTANT, GLOBAL, 0, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | TIP ID ASSIGN int_expression ';'         {globalVar[GlobalVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, GLOBAL, evalAST($4, localVar, LocalVarCount, globalVar, GlobalVarCount), yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($4); GlobalVarCount++;}
                 | TIP ID ASSIGN NR_INT ';'                 {globalVar[GlobalVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | TIP ID ASSIGN NR_FLOAT ';'               {globalVar[GlobalVarCount] = initVarFLOAT($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | TIP ID ASSIGN BOOL_VAL ';'               {globalVar[GlobalVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | TIP ID ASSIGN EXPLICIT_CHAR ';'          {globalVar[GlobalVarCount] = initVarCHAR($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | TIP ID ASSIGN EXPLICIT_STRING ';'        {globalVar[GlobalVarCount] = initVarSTRING($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | TIP ID '[' NR_INT ']' ';'                {globalVar[GlobalVarCount] = declareVar($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | CONST TIP ID ASSIGN int_expression ';'   {globalVar[GlobalVarCount] = initVarINT_BOOL($3, $2, CONSTANT, GLOBAL, evalAST($5, localVar, LocalVarCount, globalVar, GlobalVarCount), yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($5); GlobalVarCount++;}
                 | CONST TIP ID ASSIGN NR_INT ';'           {globalVar[GlobalVarCount] = initVarINT_BOOL($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}  
                 | CONST TIP ID ASSIGN NR_FLOAT ';'         {globalVar[GlobalVarCount] = initVarFLOAT($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | CONST TIP ID ASSIGN BOOL_VAL ';'         {globalVar[GlobalVarCount] = initVarINT_BOOL($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | CONST TIP ID ASSIGN EXPLICIT_CHAR ';'    {globalVar[GlobalVarCount] = initVarCHAR($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | CONST TIP ID ASSIGN EXPLICIT_STRING ';'  {globalVar[GlobalVarCount] = initVarSTRING($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 | CLASS ID ID ';'                          {globalVar[GlobalVarCount] = initiClassItem($3, $2, GLOBAL, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); GlobalVarCount++;}
                 ;

function_declaration : TIP ID '(' lista_param ')' '{' commands RETURN returnVar ';' '}'   {checkReturn($1, $9); declareFunction($2, $1, yylineno, param_list, param_count, localVar, LocalVarCount); param_count = 0; LocalVarCount = 0;}
                     | TIP ID '('  ')' '{' commands RETURN returnVar ';' '}'              {checkReturn($1, $8); declareFunction($2, $1, yylineno, param_list, 0, localVar, LocalVarCount); param_count = 0; LocalVarCount = 0;}
                     | TIP ID '(' lista_param ')' '{' RETURN returnVar ';' '}'            {checkReturn($1, $8); declareFunction($2, $1, yylineno, param_list, param_count, localVar, 0); param_count = 0; LocalVarCount = 0;}
                     | TIP ID '('  ')' '{' RETURN returnVar ';' '}'                       {checkReturn($1, $7); declareFunction($2, $1, yylineno, param_list, 0, localVar, 0); param_count = 0; LocalVarCount = 0;}
                     ;

lista_param : lista_param ',' param 
            | param
            ;

returnVar : ID                          {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); char id[2]; id[0] = GetTypeIDvar(poz); id[1] = '\0'; $$ = id;}
          | ID '[' NR_INT ']'           {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); char id[2]; id[0] = GetTypeIDarray(poz, $3); id[1] = '\0'; $$ = id;}
          | ID '(' ')'                  {char id[2]; id[0] = GetTypeIDfunction($1, ""); id[1] = '\0'; $$ = id;}
          | ID '(' lista_apel ')'       {char id[2]; id[0] = GetTypeIDfunction($1, $3); id[1] = '\0'; $$ = id;}
          | int_expression              {$$ = "i";}
          | NR_INT                      {$$ = "i";}
          | NR_FLOAT                    {$$ = "f";}
          | BOOL_VAL                    {$$ = "b";}
          | bool_expression             {$$ = "b";}
          | EXPLICIT_CHAR               {$$ = "c";}
          | EXPLICIT_STRING             {$$ = "s";} 
          ;

param : TIP ID                {AddParam($2, $1, NCONSTANT, 0, param_list, param_count); localVar[LocalVarCount] = param_list[param_count]; param_count++; LocalVarCount++;}
      | TIP ID '[' NR_INT ']' {AddParam($2, $1, NCONSTANT, $4, param_list, param_count); localVar[LocalVarCount] = param_list[param_count]; param_count++; LocalVarCount++;}
      | CONST TIP ID          {AddParam($3, $2, CONSTANT, 0, param_list, param_count); localVar[LocalVarCount] = param_list[param_count]; param_count++; LocalVarCount++;}
      ;

user_types : CLASS ID '{' declareClass '}' ';' {declareClass($2, ClassVar, ClassVarCount, ClassFunctions, ClassFunctionsCount, yylineno); ClassVarCount = 0; ClassFunctionsCount = 0; LocalVarCount = 0;}
           ;
           
declareClass : declareClassVariable 
             | declareClass declareClassVariable
             | declareClassFunction
             | declareClass declareClassFunction
             ;

declareClassFunction : TIP ID '(' lista_param ')' '{' commands RETURN returnVar ';' '}'   {checkReturn($1, $9); ClassFunctions[ClassFunctionsCount] = declareClassFunction($2, $1, yylineno, param_list, param_count, localVar, LocalVarCount, ClassFunctions, ClassFunctionsCount); param_count = 0; LocalVarCount = 0; ClassFunctionsCount++;}
                     | TIP ID '('  ')' '{' commands RETURN returnVar ';' '}'              {checkReturn($1, $8); ClassFunctions[ClassFunctionsCount] = declareClassFunction($2, $1, yylineno, param_list, 0, localVar, LocalVarCount, ClassFunctions, ClassFunctionsCount); param_count = 0; LocalVarCount = 0; ClassFunctionsCount++;}
                     | TIP ID '(' lista_param ')' '{' RETURN returnVar ';' '}'            {checkReturn($1, $8); ClassFunctions[ClassFunctionsCount] = declareClassFunction($2, $1, yylineno, param_list, param_count, localVar, 0, ClassFunctions, ClassFunctionsCount); param_count = 0; LocalVarCount = 0; ClassFunctionsCount++;}
                     | TIP ID '('  ')' '{' RETURN returnVar ';' '}'                       {checkReturn($1, $7); ClassFunctions[ClassFunctionsCount] = declareClassFunction($2, $1, yylineno, param_list, 0, localVar, 0,ClassFunctions, ClassFunctionsCount); param_count = 0; LocalVarCount = 0; ClassFunctionsCount++;}
                     ;

declareClassVariable : TIP ID ';'                               {ClassVar[ClassVarCount] = declareVar($2, $1, NCONSTANT, GLOBAL, 0, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | TIP ID ASSIGN int_expression ';'         {ClassVar[ClassVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, GLOBAL, evalAST($4, localVar, LocalVarCount, globalVar, GlobalVarCount), yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($4); ClassVarCount++;}
                     | TIP ID ASSIGN NR_INT ';'                 {ClassVar[ClassVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | TIP ID ASSIGN NR_FLOAT ';'               {ClassVar[ClassVarCount] = initVarFLOAT($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | TIP ID ASSIGN BOOL_VAL ';'               {ClassVar[ClassVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | TIP ID ASSIGN EXPLICIT_CHAR ';'          {ClassVar[ClassVarCount] = initVarCHAR($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | TIP ID ASSIGN EXPLICIT_STRING ';'        {ClassVar[ClassVarCount] = initVarSTRING($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | TIP ID '[' NR_INT ']' ';'                {ClassVar[ClassVarCount] = declareVar($2, $1, NCONSTANT, GLOBAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | CONST TIP ID ASSIGN int_expression ';'   {ClassVar[ClassVarCount] = initVarINT_BOOL($3, $2, CONSTANT, GLOBAL, evalAST($5, localVar, LocalVarCount, globalVar, GlobalVarCount), yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($5); ClassVarCount++;} 
                     | CONST TIP ID ASSIGN NR_INT ';'           {ClassVar[ClassVarCount] = initVarINT_BOOL($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;} 
                     | CONST TIP ID ASSIGN NR_FLOAT ';'         {ClassVar[ClassVarCount] = initVarFLOAT($3 ,$2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | CONST TIP ID ASSIGN BOOL_VAL ';'         {ClassVar[ClassVarCount] = initVarINT_BOOL($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | CONST TIP ID ASSIGN EXPLICIT_CHAR ';'    {ClassVar[ClassVarCount] = initVarCHAR($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     | CONST TIP ID ASSIGN EXPLICIT_STRING ';'  {ClassVar[ClassVarCount] = initVarSTRING($3, $2, CONSTANT, GLOBAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); ClassVarCount++;}
                     ;     

main : MAIN '(' ')' '{' commands '}' {AddLocalVariablesMain(localVar,LocalVarCount);AddLocalVariables(globalVar,GlobalVarCount); afisare_tabel_variabile(); afisare_tabel_functii();}
     ;

commands : assignment ';'
         | commands assignment ';'
         | callFunction ';'
         | commands callFunction ';'
         | local_variables 
         | commands local_variables
         | ifStatement
         | commands ifStatement
         | forStatement
         | commands forStatement
         | whileStatement
         | commands whileStatement
         | dowhileStatement
         | commands dowhileStatement
         | EVAL '(' EvalFunc ')' ';'             {printf("%d : Eval result is : %d \n", yylineno, $3); fflush(stdout);}
         | commands EVAL '(' EvalFunc ')' ';'    {printf("%d : Eval result is : %d \n", yylineno, $4); fflush(stdout);}
         | TYPEOF '(' typeEXP ')' ';'            {printf("%d : TypeId is : %s \n", yylineno, $3); fflush(stdout);}
         | commands TYPEOF '(' typeEXP ')' ';'   {printf("%d : TypeId is : %s \n", yylineno, $4); fflush(stdout);}
         ;

assignment : ID ASSIGN ID                                   {struct variable* poz1 = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); struct variable* poz2 = VarInDomain($3, localVar, LocalVarCount, globalVar, GlobalVarCount);  assign(poz1, -1, VARIABLE, poz2, -1, VARIABLE);}
           | ID ASSIGN ID '['NR_INT']'                      {struct variable* poz1 = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); struct variable* poz2 = VarInDomain($3, localVar, LocalVarCount, globalVar, GlobalVarCount);  assign(poz1, -1, VARIABLE, poz2, $5, ARRAY);}
           | ID '['NR_INT']' ASSIGN ID                      {struct variable* poz1 = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); struct variable* poz2 = VarInDomain($6, localVar, LocalVarCount, globalVar, GlobalVarCount);  assign(poz1, $3, ARRAY, poz2, -1, VARIABLE);}
           | ID '['NR_INT']' ASSIGN ID '['NR_INT']'         {struct variable* poz1 = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); struct variable* poz2 = VarInDomain($6, localVar, LocalVarCount, globalVar, GlobalVarCount);  assign(poz1, $3, ARRAY, poz2, $8, ARRAY);}
           | ID ASSIGN int_expression                       {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignINT(poz, -1, VARIABLE, evalAST($3, localVar, LocalVarCount, globalVar, GlobalVarCount)); freeAST($3);}
           | ID ASSIGN NR_INT                               {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignINT(poz, -1, VARIABLE, $3);}
           | ID ASSIGN NR_FLOAT                             {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignFLOAT(poz, -1, VARIABLE, $3);}
           | ID ASSIGN BOOL_VAL                             {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignBOOL(poz, -1, VARIABLE, $3);}
           | ID ASSIGN EXPLICIT_CHAR                        {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignCHAR(poz, -1, VARIABLE, $3);}
           | ID ASSIGN EXPLICIT_STRING                      {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignSTRING(poz, -1, VARIABLE, $3);}
           | ID '[' NR_INT ']' ASSIGN int_expression        {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignINT(poz, $3, ARRAY, evalAST($6, localVar, LocalVarCount, globalVar, GlobalVarCount)); freeAST($6);}
           | ID '[' NR_INT ']' ASSIGN NR_INT                {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignINT(poz, $3, ARRAY, $6);}
           | ID '[' NR_INT ']' ASSIGN NR_FLOAT              {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignFLOAT(poz, $3, ARRAY, $6);}
           | ID '[' NR_INT ']' ASSIGN BOOL_VAL              {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignBOOL(poz, $3, ARRAY, $6);}
           | ID '[' NR_INT ']' ASSIGN EXPLICIT_CHAR         {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignCHAR(poz, $3, $6, ARRAY);}
           | ID '[' NR_INT ']' ASSIGN EXPLICIT_STRING       {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); assignSTRING(poz, $3, ARRAY, $6);}
           ;

callFunction : ID '(' lista_apel ')'    {checkLista_Apel($1, $3);}
             | ID '(' ')'               {checkLista_Apel($1, "");}
             ;

lista_apel : lista_apel ',' apel   {strcat($1, $3); strcpy($$, $1); }
           | apel                  {strcpy($$, $1);}
           ;

apel : ID                     {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); char id[2]; id[0] = GetTypeIDvar(poz); id[1] = '\0'; strcpy($$, id);}
     | ID '[' NR_INT ']'      {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); char id[2]; id[0] = GetTypeIDarray(poz, $3); id[1] = '\0'; strcpy($$, id);}
     | ID '(' ')'             {char id[2]; id[0] = GetTypeIDfunction($1, ""); id[1] = '\0'; strcpy($$, id);}
     | ID '(' lista_apel ')'  {char id[2]; id[0] = GetTypeIDfunction($1, $3); id[1] = '\0'; strcpy($$, id);}
     | int_expression         {strcpy($$, "i");}
     | NR_INT                 {strcpy($$, "i");}
     | NR_FLOAT               {strcpy($$, "f");}
     | BOOL_VAL               {strcpy($$, "b");}
     | EXPLICIT_CHAR          {strcpy($$, "c");}
     | EXPLICIT_STRING        {strcpy($$, "s");} 
     ;

local_variables : TIP ID ';'                                {localVar[LocalVarCount] = declareVar($2, $1, NCONSTANT, LOCAL, 0, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | TIP ID ASSIGN int_expression ';'          {localVar[LocalVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, LOCAL, evalAST($4,localVar,LocalVarCount,globalVar,GlobalVarCount), yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($4); LocalVarCount++;}
                | TIP ID ASSIGN NR_INT ';'                  {localVar[LocalVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, LOCAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | TIP ID ASSIGN NR_FLOAT ';'                {localVar[LocalVarCount] = initVarFLOAT($2, $1, NCONSTANT, LOCAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | TIP ID ASSIGN BOOL_VAL ';'                {localVar[LocalVarCount] = initVarINT_BOOL($2, $1, NCONSTANT, LOCAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | TIP ID ASSIGN EXPLICIT_CHAR ';'           {localVar[LocalVarCount] = initVarCHAR($2, $1, NCONSTANT, LOCAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | TIP ID ASSIGN EXPLICIT_STRING ';'         {localVar[LocalVarCount] = initVarSTRING($2, $1, NCONSTANT, LOCAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | TIP ID '[' NR_INT ']' ';'                 {localVar[LocalVarCount] = declareVar($2, $1, NCONSTANT, LOCAL, $4, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | CONST TIP ID ASSIGN int_expression ';'    {localVar[LocalVarCount] = initVarINT_BOOL($3, $2, CONSTANT, LOCAL,evalAST($5, localVar, LocalVarCount, globalVar, GlobalVarCount), yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($5); LocalVarCount++;}
                | CONST TIP ID ASSIGN NR_INT ';'            {localVar[LocalVarCount] = initVarINT_BOOL($3, $2, CONSTANT, LOCAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | CONST TIP ID ASSIGN NR_FLOAT ';'          {localVar[LocalVarCount] = initVarFLOAT($3, $2, CONSTANT, LOCAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | CONST TIP ID ASSIGN BOOL_VAL ';'          {localVar[LocalVarCount] = initVarINT_BOOL($3, $2, CONSTANT, LOCAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | CONST TIP ID ASSIGN EXPLICIT_CHAR ';'     {localVar[LocalVarCount] = initVarCHAR($3, $2, CONSTANT, LOCAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | CONST TIP ID ASSIGN EXPLICIT_STRING ';'   {localVar[LocalVarCount] = initVarSTRING($3, $2, CONSTANT, LOCAL, $5, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                | CLASS ID ID ';'                           {localVar[LocalVarCount] = initiClassItem($3, $2, LOCAL, yylineno, localVar, LocalVarCount, globalVar, GlobalVarCount); LocalVarCount++;}
                ;

ifStatement : IF '(' bool_expression ')' THEN '{' commands '}'                  {printf("%d : ", yylineno); if($3 == 1) printf("If condition met.\n"); else printf("If condition not met.\n"); fflush(stdout);}
            | IF '(' bool_expression ')' '{' commands '}' ELSE '{' commands '}' {printf("%d : ", yylineno); if($3 == 1) printf("If condition met.\n"); else printf("Else condition met.\n"); fflush(stdout);}
            ;

forStatement : FOR '(' assignment ';' bool_expression ';' assignment ')' '{' commands '}' {printf("%d : ", yylineno); if($5 == 1) printf("Entering for.\n"); else printf("For condition not met.\n");fflush(stdout);}
             ;

whileStatement : WHILE '(' bool_expression ')' '{' commands '}' {printf("%d : ", yylineno); if($3 == 1) printf("Entering while loop.\n"); else printf("While condition not met.\n"); fflush(stdout);}
               ;

dowhileStatement : DO '{' commands '}' WHILE '('bool_expression')' ';' {printf("%d : ", yylineno); if($7 == 1) printf("Entering while loop.\n"); else printf("Do While condition not met.\n"); fflush(stdout);}
                 ;

typeEXP : typeEXP '+' typeEXP      {if(strcmp($1, $3) == 0) strcpy($$, $1); else yyerror("Semantic Error");}
        | typeEXP '-' typeEXP      {if(strcmp($1, $3) == 0) strcpy($$, $1); else yyerror("Semantic Error");}
        | typeEXP '*' typeEXP      {if(strcmp($1, $3) == 0) strcpy($$, $1); else yyerror("Semantic Error");}
        | typeEXP '/' typeEXP      {if(strcmp($1, $3) == 0) strcpy($$, $1); else yyerror("Semantic Error");}
        | typeEXP '%' typeEXP      {if(strcmp($1, $3) == 0) strcpy($$, $1); else yyerror("Semantic Error");}
        | '(' typeEXP ')'          {strcpy($$, $2);}
        | ID                       {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); char id[2]; id[0] = GetTypeIDvar(poz); id[1] = '\0'; strcpy($$, id);}
        | ID '[' NR_INT ']'        {struct variable* poz = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount);  char id[2]; id[0] = GetTypeIDarray(poz, $3 ); id[1] = '\0'; strcpy($$, id);}
        | ID '(' ')'               {char id[2]; id[0] = GetTypeIDfunction($1, ""); id[1] = '\0'; strcpy($$, id);}
        | ID '(' lista_apel ')'    {char id[2]; id[0] = GetTypeIDfunction($1, $3); id[1] = '\0'; strcpy($$, id);}
        | NR_INT                   {strcpy($$, "i");}
        | NR_FLOAT                 {strcpy($$, "f");}
        | BOOL_VAL                 {strcpy($$, "b");}
        | EXPLICIT_CHAR            {strcpy($$, "c");}
        | EXPLICIT_STRING          {strcpy($$, "s");} 
        ;

EvalFunc : int_expression          {$$ = evalAST($1, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($1);}
         | ID                      {$$ = GetIntValue($1, localVar, LocalVarCount, globalVar, GlobalVarCount);}
         | ID '[' NR_INT ']'       {$$ = GetIntArrayValue($1, $3, localVar, LocalVarCount, globalVar, GlobalVarCount);}
         | ID '(' ')'              {checkLista_Apel($1, ""); $$ = 0;}
         | ID '(' lista_apel')'    {checkLista_Apel($1, $3); $$ = 0;}
         | NR_INT                  {$$ = $1;}
         ;

int_expression : int_expressionVAL '+' int_expression        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "+", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '-' int_expression        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "-", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '*' int_expression        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "*", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '/' int_expression        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "/", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '%' int_expression        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "%", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '+' int_expressionVAL        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "+", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '-' int_expressionVAL        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "-", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '*' int_expressionVAL        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "*", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '/' int_expressionVAL        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "/", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '%' int_expressionVAL        {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "%", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '+' int_expression           {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "+", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '-' int_expression           {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "-", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '*' int_expression           {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "*", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '/' int_expression           {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "/", -1, -1, OP, $1, $3); $$ = root;}
               | int_expression '%' int_expression           {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "%", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '+' int_expressionVAL     {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "+", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '-' int_expressionVAL     {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "-", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '*' int_expressionVAL     {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "*", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '/' int_expressionVAL     {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "/", -1, -1, OP, $1, $3); $$ = root;}
               | int_expressionVAL '%' int_expressionVAL     {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, "%", -1, -1, OP, $1, $3); $$ = root;}
               | '(' int_expression ')'                      {$$ = $2;}          
               ;

int_expressionVAL : ID                    {struct variable* x = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); char t = GetTypeIDvar(x); if(t != 'i') yyerror("Non integer value in integer expression!"); 
                                             struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, $1, -1, -1, IDs, NULL, NULL); $$ = root; 
                                          }   
                  | ID '['NR_INT']'       {struct variable* x = VarInDomain($1, localVar, LocalVarCount, globalVar, GlobalVarCount); char t = GetTypeIDarray(x, $3); if(t != 'i') yyerror("Non integer value in integer expression!"); 
                                             struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root, $1, $3, -1, IDs, NULL, NULL); $$ = root; 
                                          }   
                  | ID '(' lista_apel ')' {char t = GetTypeIDfunction($1, $3); if(t != 'i') yyerror("Non integer value in integer expression!"); struct node* root = (struct node*)malloc(sizeof(struct node)); 
                                             buildAST(root,$1,-1,-1,OTHER,NULL,NULL); $$ = root; 
                                          }
                  | ID '(' ')'            {char t = GetTypeIDfunction($1, ""); if(t != 'i') yyerror("Non integer value in integer expression!"); struct node* root = (struct node*)malloc(sizeof(struct node)); 
                                             buildAST(root,$1,-1,-1,OTHER,NULL,NULL); $$ = root; 
                                          }
                  | NR_INT                {struct node* root = (struct node*)malloc(sizeof(struct node)); buildAST(root,"",-1,$1,NUMBER,NULL,NULL);  $$ = root;}     
                  ; 

bool_expression : var EQ var                           {if($1 == $3) $$ = 1; else $$ = 0;}
                | var NEQ var                          {if($1 != $3) $$ = 1; else $$ = 0;}
                | var GREATER var                      {if($1 > $3) $$ = 1; else $$ = 0;}
                | var LESS var                         {if($1 < $3) $$ = 1; else $$ = 0;}
                | var GEQ var                          {if($1 <= $3) $$ = 1; else $$ = 0;}
                | var LEQ var                          {if($1 <= $3) $$ = 1; else $$ = 0;}
                | '('bool_expression')'                {$$ = $2;} 
                | '!''('bool_expression')'             {$$ = ($3 + 1) % 2;} 
                | bool_expression AND bool_expression  {if($1 == 1 && $3 == 1) $$ = 1; else $$ = 0;}   
                | bool_expression OR bool_expression   {if($1 == 1 || $3 == 1) $$ = 1; else $$ = 0;}   
                ;

var : ID                 {$$ = GetIntValue($1, localVar, LocalVarCount, globalVar, GlobalVarCount);}    
    | ID '['NR_INT']'    {$$ = GetIntArrayValue($1, $3, localVar, LocalVarCount, globalVar, GlobalVarCount);}
    | int_expression     {$$ = evalAST($1, localVar, LocalVarCount, globalVar, GlobalVarCount); freeAST($1);}      
    | NR_INT             {$$ = $1;}
    ; 

%%
int main(int argc, char** argv){
yyin=fopen(argv[1],"r");
yyparse();
} 




	   