typedef struct function{
    char name[100];
    char type[100];
    int lineDeclare;
    int param_count;
    struct variable params[100];
    int variable_count;
    struct variable variables[100];
}function;

typedef struct variable{
    char name[100];
    char type[100];
    enum CONSTANT constant;
    enum DOMAINS domain;
    int vectorCount;
    int lineDeclare;
    int int_val;
    float float_val;
    int bool_val;
    char char_val;
    char string_val[100];
    int int_vec[100];
    float float_vec[100];
    int bool_vec[100];
    char char_vec[100];
    char (string_vec[100])[100];
}variable;

struct variable variables[100];
int varCount = 0;

struct function functions[100];
int funcCount = 0;

void afisare_variabila(FILE* fptr,int index)
{
   fprintf(fptr," nume: %s,",variables[index].nume);
   switch(variables[index].constant)
   {
    case "CONSTANT" :{
		fprintf(fptr,"este constant,");	
    }break;
    case "NCONSTANT":{
        fprintf(fptr," nu este constant,");
    }break;
   }

    if(strcmp(variables[index].type,"int") == 0){
        if(variables[index].vectorCount > 0)
        {       
            fprintf(fptr," tipul intreg, este vector, si are valoarea: ");
            for(int i=0;i<variables[index].vectorCount;i++)
                fprintf(fptr,"%d ",variables[index].int_vec[i]);
        }
        else 
        {
            fprintf(fptr," tipul intreg, si are valoarea: %d", variables[index].int_val);
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
            fprintf(fptr,"tipul float, si are valoarea: %f", variables[index].float_val);
        }
    }
    else if(strcmp(variables[index].type,"bool") == 0){
        if(variables[index].vectorCount > 0)
        {       
            fprintf(fptr,"tipul bool, este vector, si are valoarea: ");
            for(int i=0;i<variables[index].vectorCount;i++)
                fprintf(fptr,"%s ", variables[index].bool_vec[i] ? "true" : "false");
        }
        else 
        {
            fprintf(fptr,"tipul bool, si are valoarea: %s", variables[index].bool_val ? "true" : "false");
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
            fprintf(fptr,"tipul float, si are valoarea: %c", variables[index].char_val);
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
            fprintf(fptr,"tipul string, si are valoarea: %s", variables[index].string_val);
        }
    }
   
}

void afisare_tabel_variabile()
{
    FILE *fptr;
    fptr = fopen("symbol_tabel_variables.txt","w");

	for(int i=0; i<varCount; i++)
	 {
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
    fprintf(fptr,"are %d parametrii ",functions[index].param_count);
    if(functions[index].param_count > 0)
    {
        for(int i=0;i<functions[index].param_count;i++)
            fprintf(fptr,"parametru: %d , nume_param: %s, tip_param: %d", i+1, functions[index].params[i].name, functions[index].params[i].type);
    }
}

void afisare_tabel_functii()
{
    FILE *fptr;
    fptr = fopen("symbol_tabel_functions.txt","w");

	for(int i=0; i<funcCount; i++)
	 {
	  fprintf(fptr,"Functia:%i:", i+1); 
        afisare_functie(fptr,i);
        fprintf(fptr,"\n"); 
	 }
    fclose(fptr);
}