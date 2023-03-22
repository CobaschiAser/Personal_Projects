#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "Types.h"

struct variable variables[100];
int varCount = 0;

struct function functions[20];
int funcCount = 0;

struct User_class classTypes[20];
int classCount = 0;
struct variable classes[20];
int classVarCount=0;

int yyerror(char *ERRORmsg) {
    printf("Error at line %d : %s\n", yylineno, ERRORmsg);
    fflush(stdout);
    exit(-1);
    return 0;
}

void NumberToString(int n,char number[100]){
    int reverseNumber=0;
    while(n>0){
        reverseNumber *= 10;
        reverseNumber += n%10;
        n /= 10;
    }
    int count=0;
    while(reverseNumber>0){
        char x = reverseNumber % 10 + '0';
        number[count] = x;
        count++;
        reverseNumber /= 10;
    }
    number[count]='\0';
}

void AddVariable(struct variable x){
    variables[varCount] = x;
    varCount++;
}

void AddLocalVariables(struct variable *localVar,int LocalVarCount){
    for(int i = 0; i < LocalVarCount; ++i){
        AddVariable(localVar[i]);
    }
}

void AddLocalVariablesMain(struct variable *localVar,int LocalVarCount){
    for(int i = 0; i < LocalVarCount; ++i){
        strcpy(localVar[i].domainName,"Main");
        AddVariable(localVar[i]);
    }
}

void VariableExists(int line){
    char msg[100]="";
    strcpy(msg,"Variable already defined at line: ");
    char number[100];
    NumberToString(line,number);
    strcat(msg,number);
    yyerror(msg);
}

char GetTypeIDarray(struct variable* poz,int index){
    if(poz==NULL){
        yyerror("Variable does not exist!");
    }
    if(poz->vectorCount<=index){
        yyerror("Array is too small!");
    }
    if(poz->vectorCount<0){
        yyerror("Negative index!");
    }
    return poz->type[0];
}

struct variable* VarInDomain(char* id,struct variable* varList,int localVarCount,struct variable* globalVariable,int globalVarCount){
    for(int i = 0; i < localVarCount; ++i){
        if(strcmp(id, varList[i].name) == 0){
            return &varList[i];
        }
    }
    for(int i = 0; i < globalVarCount; ++i){
        if(strcmp(id, globalVariable[i].name) == 0){
            return &globalVariable[i];
        }
    }
    return NULL;
}

int GetIntArrayValue(char* name,int index,struct variable* localVariables,int localVar_count,struct variable* GlobalVar,int GlobalVarCount){
    struct variable* x = VarInDomain(name, localVariables, localVar_count, GlobalVar, GlobalVarCount);
    if(x->vectorCount==0){
        yyerror("Variable is not an array!");
    }
    if(strcmp(x->type,"int")!=0){
        yyerror("Variable is not an integer!");
    }
    if(x->vectorCount<=index){
        yyerror("Array is too small!");
    }
    if(x->vectorCount<0){
        yyerror("Negative index!");
    }
    return x->int_vec[index];
}

int GetIntValue(char* name,struct variable* localVariables,int localVar_count,struct variable* GlobalVar,int GlobalVarCount){
    struct variable* x = VarInDomain(name, localVariables, localVar_count, GlobalVar, GlobalVarCount);
    if(x->vectorCount!=0){
        yyerror("Variable is an array!");
    }
    if(strcmp(x->type,"int")!=0){
        yyerror("Variable is not an integer!");
    }
    return x->int_val;
}

char GetTypeIDfunction(char* functionName,char* Lista_apel){
    int functionExists=0;
    for(int i = 0; i < funcCount; ++i){
        if(strcmp(functionName,functions[i].name)==0){
            functionExists=1;
            if(strcmp(Lista_apel, functions[i].paramID) == 0){
                return functions[i].type[0];
            }
        }
    }
    if(functionExists==0){
        yyerror("Function does not exist!");
    }
    yyerror("Parameters dont match the functions parameters!");
}

struct variable declareVar(char* name, char* t, enum CONSTANT c, enum DOMAINS d, int VectorCount, int line,struct variable* LocalVar, int LocalVarCount,struct variable* GlobalVar,int GlobalVarCount){
    struct variable* poz = VarInDomain(name,LocalVar,LocalVarCount,GlobalVar,GlobalVarCount);
    if(poz == NULL){
        struct variable x;
        strcpy(x.name, name);
        strcpy(x.type, t);
        x.constant = c;
        x.domain=d;
        x.vectorCount=VectorCount;
        x.lineDeclare=line;
        if(d==GLOBAL){
            strcpy(x.domainName,"Global");
        }
        if(VectorCount < 0){
            yyerror("Size of array cant be a negative number!");
        }
        if(VectorCount > 0){
            if(VectorCount>20){
                yyerror("Array is too big!");
            }
            if(strcmp(t,"int")==0){
                x.int_vec=(int *) malloc(VectorCount * sizeof(int));
                for(int i = 0;i<VectorCount;++i){
                    x.int_vec[i]=0;
                }
            }
            else if(strcmp(t,"float")==0){
                x.float_vec=(float *) malloc(VectorCount * sizeof(float));
                for(int i = 0;i<VectorCount;++i){
                    x.float_vec[i]=0.0;
                }
            }
            else if(strcmp(t,"bool")==0){
                x.bool_vec=(int *) malloc(VectorCount * sizeof(int));
                for(int i = 0;i<VectorCount;++i){
                    x.bool_vec[i]=0;
                }
            }
            else if(strcmp(t,"char")==0){
                x.char_vec=(char *) malloc(VectorCount * sizeof(char));
                for(int i = 0;i<VectorCount;++i){
                    x.char_vec[i]='0';
                }
            }
            else if(strcmp(t,"string")==0){
                for(int i = 0;i<VectorCount;++i){
                    strcpy(x.string_vec[i],"0");
                }
            }
        }
        else if(VectorCount==0){
           if(strcmp(t,"int")==0){
                x.int_val=0;
            }
            else if(strcmp(t,"float")==0){
                x.float_val=0.0;
            }
            else if(strcmp(t,"bool")==0){
                x.bool_val=0;
            }
            else if(strcmp(t,"char")==0){
                x.char_val='0';
            }
            else if(strcmp(t,"string")==0){
                strcpy(x.string_val,"0");
            } 
        }
        return x;
    }
    else{
        VariableExists(poz->lineDeclare);
    }
}

struct variable initVarINT_BOOL(char* name, char* t, enum CONSTANT c, enum DOMAINS d, int value, int line,struct variable* LocalVar, int LocalVarCount,struct variable* GlobalVar,int GlobalVarCount){
    if(strcmp(t, "bool") != 0 && strcmp(t, "int") != 0 ){
        char msg[100] = "";
        strcpy(msg,"Invalid conversion for variable ");
        strcat(msg,name);
        yyerror(msg);
    }
    struct variable* poz = VarInDomain(name,LocalVar,LocalVarCount,GlobalVar,GlobalVarCount);
    if(poz == NULL){
        struct variable x;
        strcpy(x.name, name);
        strcpy(x.type,t);
        x.constant = c;
        x.domain=d;
        if(strcmp(t, "int") == 0){
            x.int_val = value;
        }
        else {
            x.bool_val = value;
        }
        x.lineDeclare=line;
        x.vectorCount = 0;
        return x;
    }
    else{
        VariableExists(poz->lineDeclare);
    }
} //INT and BOOL

struct variable initVarFLOAT(char* name, char* t, enum CONSTANT c, enum DOMAINS d, float value, int line,struct variable* LocalVar, int LocalVarCount,struct variable* GlobalVar,int GlobalVarCount){
    if(strcmp(t, "float") != 0){
        char msg[100] = "";
        strcpy(msg,"Invalid conversion for variable ");
        strcat(msg,name);
        yyerror(msg);
    }
    struct variable* poz = VarInDomain(name,LocalVar,LocalVarCount,GlobalVar,GlobalVarCount);
    if(poz == NULL){
        struct variable x;
        strcpy(x.name, name);
        strcpy(x.type,t);
        if(d==GLOBAL){
            strcpy(x.domainName,"Global");
        }
        x.vectorCount=0;
        x.constant = c;
        x.domain=d;
        x.float_val = value;
        return x;
    }
    else{
        VariableExists(poz->lineDeclare);
    }
}

struct variable initVarCHAR(char* name, char* t, enum CONSTANT c, enum DOMAINS d, char value, int line,struct variable* LocalVar, int LocalVarCount,struct variable* GlobalVar,int GlobalVarCount){
    if(strcmp(t, "char") != 0){
        char msg[100] = "";
        strcpy(msg,"Invalid conversion for variable ");
        strcat(msg,name);
        yyerror(msg);
    } 
    struct variable* poz = VarInDomain(name,LocalVar,LocalVarCount,GlobalVar,GlobalVarCount);
    if(poz == NULL){
        struct variable x;
        strcpy(x.name, name);
        strcpy(x.type,t);
        if(d==GLOBAL){
            strcpy(x.domainName,"Global");
        }
        x.constant = c;
        x.domain=d;
        x.vectorCount=0;
        x.char_val = value;
        x.lineDeclare=line;
        x.vectorCount = 0;
        return x;
    }
    else{
        VariableExists(poz->lineDeclare);
    }
}   

struct variable initVarSTRING(char* name, char* t, enum CONSTANT c, enum DOMAINS d, char* value, int line,struct variable* LocalVar, int LocalVarCount,struct variable* GlobalVar,int GlobalVarCount){
    if(strcmp(t, "string") != 0){
        char msg[100] = "";
        strcpy(msg,"Invalid conversion for variable ");
        strcat(msg,name);
        yyerror(msg);
    }
    struct variable* poz = VarInDomain(name,LocalVar,LocalVarCount,GlobalVar,GlobalVarCount);
    if(poz == NULL){
        struct variable x;
        strcpy(x.name, name);
        strcpy(x.type,t);
        if(d==GLOBAL){
            strcpy(x.domainName,"Global");
        }
        x.constant = c;
        x.domain=d;
        x.vectorCount=0;
        strcpy(x.string_val,value);
        x.lineDeclare = line;
        x.vectorCount = 0;
        return x;
    }
    else{
        VariableExists(poz->lineDeclare);
    }
}

struct variable initiClassItem(char* name,char* className,enum DOMAINS d,int line,struct variable* LocalVar, int LocalVarCount,struct variable* GlobalVar,int GlobalVarCount){
    int classtypeExists=0;
    for(int i = 0;i < classCount;++i){
        if(strcmp(className,classTypes[i].name)==0){
            classtypeExists=1;
            break;
        }
    }
    if(classtypeExists==0){
        yyerror("Class is not defined!");
    }
    struct variable* poz = VarInDomain(name,LocalVar,LocalVarCount,GlobalVar,GlobalVarCount);
    if(poz == NULL){
        struct variable x;
        strcpy(x.name, name);
        strcpy(x.type,className);
        if(d==GLOBAL){
            strcpy(x.domainName,"Global");
        }
        x.constant = NCONSTANT;
        x.domain=d;
        x.lineDeclare=line;
        x.vectorCount = 0;
        classes[classVarCount]=x;
        classVarCount++;
        return x;
    }
    else{
        VariableExists(poz->lineDeclare);
    }
}

int CheckParam(char* name, struct variable *param, int param_count){
    for(int i = 0; i < param_count; ++i){
        if(strcmp(name, param[i].name) == 0){
            return i;
        }
    }
    return -1;
}

int AddParam(char* name, char* t, enum CONSTANT c, int VectorCount, struct variable *param, int param_count){
    int pozParam = CheckParam(name,param,param_count);
    if(pozParam == -1){
        struct variable x;
        strcpy(x.name, name);
        strcpy(x.type,t);
        x.constant = c;
        if(VectorCount < 0){
            yyerror("Size of array is a negative number!");
        }
        x.vectorCount=VectorCount;
        param[param_count] = x;
        return 1;
    }
    else {
        yyerror("Parameter already defined in this function!");
    }
}

int CheckFuncExistence(char* name){
    for(int i = 0; i < funcCount; ++i){
        if(strcmp(name, functions[i].name) == 0){
            return i;
        }
    }
    return -1;
}

void FunctionExists(int line){
    char msg[100]="";
    strcpy(msg,"Function already defined at line: ");
    char number[100];
    NumberToString(line,number);
    strcat(msg,number);
    yyerror(msg);
}

void checkReturn(char* type,char* returnType){
    if(type[0]==returnType[0]){
        return;
    }
    else{
        yyerror("Return type does not match the functions type!");
    }
}

struct function declareFunction(char* name,char* t,int line,struct variable* param_list, int param_count,struct variable* localVar,int LocalVarCount){
    function f;
    f.param_count=param_count;
    for(int i = 0; i < param_count; ++i){
        f.params[i]=param_list[i];
        f.paramID[i]=param_list[i].type[0];
    }
    f.paramID[param_count]='\0';
    for(int i = 0; i < funcCount; ++i){
        if(strcmp(name,functions[i].name)==0){
            if(strcmp(f.paramID, functions[i].paramID) == 0){
                FunctionExists(functions[i].lineDeclare);
            }
        }
    }
    strcpy(f.name,name);
    strcpy(f.type,t);
    f.lineDeclare=line;
    f.inClass=0;
    f.param_count=param_count;
    f.variable_count=LocalVarCount;
    for(int i = 0; i < LocalVarCount; ++i){
        strcpy(localVar[i].domainName,name);
        f.variables[i]=localVar[i];
        AddVariable(localVar[i]);
    }
    functions[funcCount]=f;
    funcCount++;
    return f;
}

struct function declareClassFunction(char* name,char* t,int line,struct variable* param_list, int param_count,struct variable* localVar,int LocalVarCount,struct function* ClassFunctions,int ClassFunctionsCount){
    function f;
    f.param_count=param_count;
    for(int i = 0; i < param_count; ++i){
        f.params[i]=param_list[i];
        f.paramID[i]=param_list[i].type[0];
    }
    f.paramID[param_count]='\0';
    for(int i = 0; i < ClassFunctionsCount; ++i){
        if(strcmp(name,ClassFunctions[i].name)==0){
            if(strcmp(f.paramID, ClassFunctions[i].paramID) == 0){
                FunctionExists(ClassFunctions[i].lineDeclare);
            }
        }
    }
    strcpy(f.name,name);
    strcpy(f.type,t);
    f.lineDeclare=line;
    f.inClass=1;
    f.param_count=param_count;
    f.variable_count=LocalVarCount;
    for(int i = 0; i < LocalVarCount; ++i){
        strcpy(localVar[i].domainName,name);
        f.variables[i]=localVar[i];
        AddVariable(localVar[i]);
    }
    return f;
}

void ClassExists(int line){
    char msg[100]="";
    strcpy(msg,"Class already defined at line: ");
    char number[100];
    NumberToString(line,number);
    strcat(msg,number);
    yyerror(msg);
}

void declareClass(char* name,struct variable* ClassVar, int ClassVarCount,struct function* ClassFunctions,int ClassFunctionsCount,int line){
    for(int i = 0;i<classCount;++i){
        if(strcmp(name,classTypes[i].name)==0){
            ClassExists(classTypes[i].lineDeclare);
        }
    }
    strcpy(classTypes[classCount].name,name);
    for(int i = 0; i < ClassVarCount; ++i){
        classTypes[classCount].ClassVariables[i]=ClassVar[i];
        strcpy(ClassVar[i].domainName,name);
        variables[varCount]=ClassVar[i];
        varCount++;
    }
    for(int i = 0; i < ClassFunctionsCount; ++i){
        strcpy(ClassFunctions[i].className,name);
        classTypes[classCount].ClassFunctions[i]=ClassFunctions[i];
        functions[funcCount]=ClassFunctions[i];
        funcCount++;
    }
    classCount++;
}

void checkLista_Apel(char* functionName, char* Lista_apel){
    int functionExists=0;
    for(int i = 0; i < funcCount; ++i){
        if(strcmp(functionName,functions[i].name)==0){
            functionExists=1;
            if(strcmp(Lista_apel, functions[i].paramID) == 0){
                return;
            }
        }
    }
    if(functionExists==0){
        yyerror("Function does not exist!");
    }
    yyerror("Parameters dont match the functions parameters!");
}

char GetTypeIDvar(struct variable* poz){
    if(poz==NULL){
        yyerror("Variable does not exist!");
    }
    return poz->type[0];
}

void assign(struct variable* poz1,int index1,enum VAR_TYPE type1,struct variable* poz2,int index2,enum VAR_TYPE type2){
    if(poz1==NULL){
        yyerror("Variable 1 does not exist!");
    }
    if(poz2==NULL){
        yyerror("Variable 2 does not exist!");
    }
    if(strcmp(poz1->type,poz2->type)!=0){
        yyerror("Variables have different types!");
    }
    if(type1==ARRAY && poz1->vectorCount<=index1){
        yyerror("Array 1 too small!");
    }
    if(type2==ARRAY && poz2->vectorCount<=index2){
        yyerror("Array 2 too small!");
    }
    if(poz1->constant==CONSTANT){
        yyerror("Cannot reassign the value of a constant variable!");
    }

    if(strcmp(poz1->type,"int")==0){
        if(type2 == VARIABLE){
            if(type1 == VARIABLE){
                poz1->int_val=poz2->int_val;
            }
            if(type1 == ARRAY){
                poz1->int_vec[index1]=poz2->int_val;
            }
        }
        else if(type2 == ARRAY){
            if(type1 == VARIABLE){
                poz1->int_val=poz2->int_vec[index2];
            }
            if(type1 == ARRAY){
                poz1->int_vec[index1]=poz2->int_vec[index2];
            }
        }
    }

    if(strcmp(poz1->type,"float")==0){
        if(type2 == VARIABLE){
            if(type1 == VARIABLE){
                poz1->float_val=poz2->float_val;
            }
            if(type1 == ARRAY){
                poz1->float_vec[index1]=poz2->float_val;
            }
        }
        else if(type2 == ARRAY){
            if(type1 == VARIABLE){
                poz1->float_val=poz2->float_vec[index2];
            }
            if(type1 == ARRAY){
                poz1->float_vec[index1]=poz2->float_vec[index2];
            }
        }
    }

    if(strcmp(poz1->type,"bool")==0){
        if(type2 == VARIABLE){
            if(type1 == VARIABLE){
                poz1->bool_val=poz2->bool_val;
            }
            if(type1 == ARRAY){
                poz1->bool_vec[index1]=poz2->bool_val;
            }
        }
        else if(type2 == ARRAY){
            if(type1 == VARIABLE){
                poz1->bool_val=poz2->bool_vec[index2];
            }
            if(type1 == ARRAY){
                poz1->bool_vec[index1]=poz2->bool_vec[index2];
            }
        }
    }

    if(strcmp(poz1->type,"char")==0){
        if(type2 == VARIABLE){
            if(type1 == VARIABLE){
                poz1->char_val=poz2->char_val;
            }
            if(type1 == ARRAY){
                poz1->char_vec[index1]=poz2->char_val;
            }
        }
        else if(type2 == ARRAY){
            if(type1 == VARIABLE){
                poz1->char_val=poz2->char_vec[index2];
            }
            if(type1 == ARRAY){
                poz1->char_vec[index1]=poz2->char_vec[index2];
            }
        }
    }

    if(strcmp(poz1->type,"string")==0){
        if(type2 == VARIABLE){
            if(type1 == VARIABLE){
                strcpy(poz1->string_val,poz2->string_val);
            }
            if(type1 == ARRAY){
                strcpy(poz1->string_vec[index1],poz2->string_val);
            }
        }
        else if(type2 == ARRAY){
            if(type1 == VARIABLE){
                strcpy(poz1->string_val,poz2->string_vec[index2]);
            }
            if(type1 == ARRAY){
                strcpy(poz1->string_vec[index1],poz2->string_vec[index2]);
            }
        }
    }
}

void assignINT(struct variable* poz,int index,enum VAR_TYPE type,int value){
    if(poz==NULL){
        yyerror("Variable does not exist!");
    }
    if(strcmp(poz->type,"int")!=0){
        yyerror("Variables have different types!");
    }
    if(type==ARRAY && poz->vectorCount<=index){
        yyerror("Array is too small!");
    }
    if(poz->constant==CONSTANT){
        yyerror("Cannot reassign the value of a constant variable!");
    }
    if(type == VARIABLE){
        poz->int_val=value;
    }
    if(type == ARRAY){
        poz->int_vec[index]=value;
    }
}

void assignFLOAT(struct variable* poz,int index,enum VAR_TYPE type,float value){
    if(poz==NULL){
        yyerror("Variable does not exist!");
    }
    if(strcmp(poz->type,"float")!=0){
        yyerror("Variables have different types!");
    }
    if(type==ARRAY && poz->vectorCount<=index){
        yyerror("Array is too small!");
    }
    if(poz->constant==CONSTANT){
        yyerror("Cannot reassign the value of a constant variable!");
    }
    if(type == VARIABLE){
        poz->float_val=value;
    }
    if(type == ARRAY){
        poz->float_vec[index]=value;
    }
}

void assignBOOL(struct variable* poz,int index,enum VAR_TYPE type,int value){
    if(poz==NULL){
        yyerror("Variable does not exist!");
    }
    if(strcmp(poz->type,"bool")!=0){
        yyerror("Variables have different types!");
    }
    if(type==ARRAY && poz->vectorCount<=index){
        yyerror("Array is too small!");
    }
    if(poz->constant==CONSTANT){
        yyerror("Cannot reassign the value of a constant variable!");
    }
    if(type == VARIABLE){
        poz->bool_val=value;
    }
    if(type == ARRAY){
        poz->bool_vec[index]=value;
    }
}

void assignCHAR(struct variable* poz,int index,enum VAR_TYPE type,char value){
    if(poz==NULL){
        yyerror("Variable does not exist!");
    }
    if(strcmp(poz->type,"char")!=0){
        yyerror("Variables have different types!");
    }
    if(type==ARRAY && poz->vectorCount<=index){
        yyerror("Array is too small!");
    }
    if(poz->constant==CONSTANT){
        yyerror("Cannot reassign the value of a constant variable!");
    }
    if(type == VARIABLE){
        poz->char_val=value;
    }
    if(type == ARRAY){
        poz->char_vec[index]=value;
    }
}

void assignSTRING(struct variable* poz,int index,enum VAR_TYPE type,char* value){
    if(poz==NULL){
        yyerror("Variable does not exist!");
    }
    if(strcmp(poz->type,"string")!=0){
        yyerror("Variables have different types!");
    }
    if(type==ARRAY && poz->vectorCount<=index){
        yyerror("Array is too small!");
    }
    if(poz->constant==CONSTANT){
        yyerror("Cannot reassign the value of a constant variable!");
    }
    if(type == VARIABLE){
        strcpy(poz->string_val,value);
    }
    if(type == ARRAY){
        strcpy(poz->string_vec[index],value);
    }
}

void buildAST(struct node* root,char* name,int index,int value,enum NodeType type,struct node* left,struct node* right){
    strcpy(root->name,name);
    root->value=value;
    root->index=index;
    root->type=type;
    root->left=left;
    root->right=right;
}

int evalAST(struct node* root,struct variable* localVariables,int localVar_count,struct variable* GlobalVar,int GlobalVarCount){
    switch(root->type){
        case OP : {
            if(strcmp(root->name,"+")==0){
                return evalAST(root->left,localVariables,localVar_count,GlobalVar,GlobalVarCount)+evalAST(root->right,localVariables,localVar_count,GlobalVar,GlobalVarCount);
            }
            else if(strcmp(root->name,"-")==0){
                return evalAST(root->left,localVariables,localVar_count,GlobalVar,GlobalVarCount)-evalAST(root->right,localVariables,localVar_count,GlobalVar,GlobalVarCount);
            }
            else if(strcmp(root->name,"/")==0){
                int n2=evalAST(root->right,localVariables,localVar_count,GlobalVar,GlobalVarCount);
                if(n2==0){
                    yyerror("Dividing by 0!");
                }
                return evalAST(root->left,localVariables,localVar_count,GlobalVar,GlobalVarCount)/n2;
            }
            else if(strcmp(root->name,"*")==0){
                return evalAST(root->left,localVariables,localVar_count,GlobalVar,GlobalVarCount)*evalAST(root->right,localVariables,localVar_count,GlobalVar,GlobalVarCount);
            }
            else if(strcmp(root->name,"%")==0){
                return evalAST(root->left,localVariables,localVar_count,GlobalVar,GlobalVarCount)%evalAST(root->right,localVariables,localVar_count,GlobalVar,GlobalVarCount);
            }
        }break;
        case NUMBER : {
            return root->value;
        }break;
        case IDs: {
            if(root->index==-1){
                return GetIntValue(root->name,localVariables,localVar_count,GlobalVar,GlobalVarCount);
            }
            else{
                 return GetIntArrayValue(root->name,root->index,localVariables,localVar_count,GlobalVar,GlobalVarCount);
            }

        }break;
        case OTHER: {
            return 0;
        }
    }
}

void freeAST(struct node* root) {
    if(root==NULL)
        return;
    freeAST(root->left);
    freeAST(root->right);
    free(root);
}

void afisare_variabila(FILE* fptr,int index)
{
   fprintf(fptr," nume: %s, ",variables[index].name);
   switch(variables[index].constant)
   {
    case CONSTANT :{
		fprintf(fptr,"este constant, ");	
    }break;
    case NCONSTANT :{
        fprintf(fptr," nu este constant, ");
    }break;
   }
    fprintf(fptr," Domeniul este : %s ",variables[index].domainName);
    if(strcmp(variables[index].type,"int") == 0){
        if(variables[index].vectorCount > 0)
        {       
            fprintf(fptr," tipul intreg, este vector, si are valoarea: ");
            for(int i=0;i<variables[index].vectorCount;i++)
                fprintf(fptr,"%d ",variables[index].int_vec[i]);
        }
        else 
        {
            fprintf(fptr," tipul intreg, si are valoarea: %d ", variables[index].int_val);
        }
    }
    else if(strcmp(variables[index].type,"float") == 0){
        if(variables[index].vectorCount > 0)
        {       
            fprintf(fptr," tipul float, este vector, si are valoarea: ");
            for(int i=0;i<variables[index].vectorCount;i++)
                fprintf(fptr,"%f ",variables[index].float_vec[i]);
        }
        else 
        {
            fprintf(fptr,"tipul float, si are valoarea: %f ", variables[index].float_val);
        }
    }
    else if(strcmp(variables[index].type,"bool") == 0){
        if(variables[index].vectorCount > 0)
        {       
            fprintf(fptr,"tipul bool, este vector, si are valoarea: ");
            for(int i=0;i<variables[index].vectorCount;i++)
                fprintf(fptr,"%s ", variables[index].bool_vec[i] ? "true " : "false ");
        }
        else 
        {
            fprintf(fptr,"tipul bool, si are valoarea: %s ", variables[index].bool_val ? "true" : "false");
        }
    }
    else if(strcmp(variables[index].type,"char") == 0){
        if(variables[index].vectorCount > 0)
        {       
            fprintf(fptr,"tipul char, este vector, si are valoarea: ");
            for(int i=0;i<variables[index].vectorCount;i++)
                fprintf(fptr,"%c ", variables[index].char_vec[i]);
        }
        else 
        {
            fprintf(fptr,"tipul float, si are valoarea: %c ", variables[index].char_val);
        }
    }
    else if(strcmp(variables[index].type,"string") == 0){
        if(variables[index].vectorCount > 0)
        {       
            fprintf(fptr,"tipul string, este vector, si are valoarea: ");
            for(int i=0;i<variables[index].vectorCount;i++)
                fprintf(fptr,"%s ", variables[index].string_vec[i]);
        }
        else 
        {
            fprintf(fptr,"tipul string, si are valoarea: %s ", variables[index].string_val);
        }
    }
   
}

void afisare_tabel_variabile()
{
    FILE *fptr;
    fptr = fopen("symbol_tabel_variables.txt","w");

	for(int i=0; i<varCount; i++){
	    fprintf(fptr,"Variabila:%i:", i+1); 
        afisare_variabila(fptr,i);
        fprintf(fptr,"\n"); 
	}
    fclose(fptr);
}

void afisare_functie(FILE* fptr,int index)
{
    fprintf(fptr,"nume: %s,",functions[index].name);
    fprintf(fptr,"tipul : %s, ", functions[index].type);
    if(functions[index].inClass==1){
        fprintf(fptr,"Functia face parte din clasa : %s, ", functions[index].className);
    }
    fprintf(fptr,"are %d parametrii ",functions[index].param_count);
    if(functions[index].param_count > 0)
    {
        for(int i=0;i<functions[index].param_count;i++)
            fprintf(fptr,"parametru: %d , nume_param: %s, tip_param: %s", i+1, functions[index].params[i].name, functions[index].params[i].type);
    }
}

void afisare_tabel_functii()
{
    FILE *fptr;
    fptr = fopen("symbol_tabel_functions.txt","w");

	for(int i=0; i<funcCount; i++){
	    fprintf(fptr,"Functia:%i:", i+1); 
        afisare_functie(fptr,i);
        fprintf(fptr,"\n"); 
	}
    fclose(fptr);
}


