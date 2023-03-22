#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylineno;

enum CONSTANT{
    CONSTANT,
    NCONSTANT
};

enum DOMAINS{
    GLOBAL,
    LOCAL
};

enum VAR_TYPE{
    VARIABLE,
    ARRAY,
    CLASS_ITEM
};

typedef struct variable{
    char name[20];
    char type[20];
    enum CONSTANT constant;
    enum DOMAINS domain;
    char domainName[100];
    int vectorCount;
    int lineDeclare;

    union {
        int int_val;
        float float_val;
        int bool_val;
        char char_val;
    };

    char string_val[20];
    char string_vec[20][20];

    union{
        int* int_vec;
        float* float_vec;
        int* bool_vec;
        char* char_vec;
        void* vec;
    };
    
}variable;

typedef struct function{
    char name[20];
    char type[20];
    int lineDeclare;
    int param_count;
    int inClass;
    char className[20];
    char paramID[20];
    struct variable params[20];
    int variable_count;
    struct variable variables[20];
}function;

typedef struct User_class{
    char name[20];
    int lineDeclare;
    int variable_count;
    struct variable ClassVariables[20];
    int function_count;
    struct function ClassFunctions[20];
}User_class;

enum NodeType{
    OP,
    NUMBER,
    IDs,
    OTHER
};

typedef struct node{
    char name[20];
    int index;
    int value;
    enum NodeType type;
    struct node* left;
    struct node* right;
}node;