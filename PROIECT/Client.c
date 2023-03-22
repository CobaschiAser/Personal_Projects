#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <string.h>
#include <stdbool.h>


#define h 8
#define MAX 256

#define LUNGIME_MAX_MESAJ 5
#define INCEPUT_JOC 8
#define IESIRE_JOC 9
//#define IESIRE_JOC_FORTAT 7

//chestii pentru client-server:
struct sockaddr_in server;	// structura folosita pentru conectare
extern int errno; // codul de eroare returnat de anumite apeluri
char msg[MAX];    // mesajul trimis
char mutare[MAX]; //mutarea data ca input de clienti
int sd;			  // descriptorul de socket
int port; //portul de conectare la server
int jucator;//primul sau al doilea dintr-ul joc
int iesire_normala;
int iesire_fortata;
int egalitate;
int mutare_introdusa_gresita;
int castigator;
int un_joc_nou;

int mutare_linie_veche;
int mutare_coloana_veche;
int mutare_coloana_noua;
int mutare_linie_noua;
char mutare_piesa;

void conectare();
void verificare_parametrii();

//algoritmica

char tabla[h][h];// aici vom umple tabla de sah.

void ajutor()
{
    printf("Instructiunile jocului sunt urmatoarele:...Mult succes!\n");
    fflush(stdout);
    return;
}

int cuvant_cheie_iesire(char * mesaj_mutare) // hard-codam un set de cuvinte prin care un jucator/client poate renunta la joc
{
    if(strcmp(mesaj_mutare, "ies") == 0) return 1;
    if(strcmp(mesaj_mutare, "renunt") == 0) return 1;
    if(strcmp(mesaj_mutare, "exit") == 0) return 1;
    if(strcmp(mesaj_mutare, "quit") == 0) return 1;
    return 0;
}

int cuvant_cheie_help(char * mesaj_mutare) // hard-codam un set de cuvinte prin care un jucator/client poate renunta la joc
{
    if(strcmp(mesaj_mutare, "ajutor") == 0) return 1;
    if(strcmp(mesaj_mutare, "help") == 0) return 1;
    if(strcmp(mesaj_mutare, "nustiu") == 0) return 1;
    if(strcmp(mesaj_mutare, "cefac") == 0) return 1;
    if(strcmp(mesaj_mutare, "unde") == 0) return 1;
    if(strcmp(mesaj_mutare, "cand") == 0) return 1;
    if(strcmp(mesaj_mutare, "cum") == 0) return 1;
    if(strcmp(mesaj_mutare, "ce") == 0) return 1;
    return 0;
}

void afisare_tabla()
{
   printf("Tabla actuala arata in felul urmator:\n"); 
   for(int i=0;i<8;i++)
     {
        for(int j=0;j<8;j++)
         printf("%c  ",tabla[i][j]);
         printf("\n");
     }
     printf("\n");
}

void actualizare_tabla(int lin_veche, int col_veche, int lin_noua, int col_noua, char piesa)
{
         fflush(stdout);
         tabla[lin_veche][col_veche]='0';
         tabla[lin_noua][col_noua]=piesa;
         afisare_tabla();
}


void joc_nou()
    
{
for(int i=0;i<8;i++)
        for(int j=0;j<8;j++)
            tabla[i][j]='0';
    for(int i=0;i<8;i++)
      {
        tabla[1][i]='p';
        tabla[6][i]='P';
      }
    tabla[0][0]='t';
    tabla[0][7]='t';
    tabla[0][1]='c';
    tabla[0][6]='c';
    tabla[0][2]='n';
    tabla[0][5]='n';
    tabla[0][3]='q';
    tabla[0][4]='k';
    tabla[7][0]='T';
    tabla[7][7]='T';
    tabla[7][1]='C';
    tabla[7][6]='C';
    tabla[7][2]='N';
    tabla[7][5]='N';
    tabla[7][3]='Q';
    tabla[7][4]='K';
    
   
}          


void citeste_mesajul_serverului()
{
    if (read (sd, msg, MAX) <= 0) //(apel blocant pina cind serverul raspunde)
    {
        perror ("[client] Eroare la read() de la server.\n");
        fflush(stdout);
        return;
    }
    //printf("Am citit de la [server]: %s\n", msg);
    //fflush(stdout);
    
}

void transmite_serverului(char* raspuns)
{
    int len=strlen(raspuns);
    int len_converted=htonl(len);
    if(write(sd,&len_converted,sizeof(len_converted))<=0)
    {
        perror("[client] Eroare la write() catre server (lungimea mesajului)");
        fflush(stdout);
        return;
    }
    //printf("Am transmis catre server un mesaj de lungime: %d\n", len);
    fflush(stdout);
    if(write(sd,raspuns,MAX)<=0) 
    {
        perror("[client] Eroare la write() catre server.\n");
        fflush(stdout);
        return;
    }
    //printf("Am transmis catre server: %s\n",raspuns);
    fflush(stdout);
}

int validare_input_jucator(char* mesaj_mutare) // stabilim daca mesajul trece de la client la server
{
    if(cuvant_cheie_iesire(mesaj_mutare))
    {
        mutare[0]=(char)('0'+IESIRE_JOC);
        mutare[1]='F';
        mutare[2]='\0';
        return 1;
    }
    else if(cuvant_cheie_help(mesaj_mutare))
    {
        ajutor();
        return 0;
    }
    else if(strlen(mesaj_mutare)>LUNGIME_MAX_MESAJ)
    {
        printf("Mesaj prea lung\n");
        fflush(stdout);
        return 0;
    }
    else if(!strchr("01234567",mesaj_mutare[0]) || !strchr("01234567",mesaj_mutare[1])||
    !strchr("01234567",mesaj_mutare[2]) || !strchr("01234567",mesaj_mutare[3]) ||
    !strchr("pPtTnNcCqQkK",mesaj_mutare[4]))
    {
        printf("Caractere nepermise : %s\n",mesaj_mutare);
        fflush(stdout);
        return 0;
    }
    return 1;
}

char * mutare_valida()
{
    int valid=0;
    
    while(!valid)
    {
        printf("Introduceti pozitia initiala(coloana,linie) , pozitia finala(coloana linie) si tipul piesei\n");
        fflush(stdout);
        scanf("%s",mutare);
        if(validare_input_jucator(mutare))
            valid=1;
    }
    return mutare;
   
}

void analizeaza_msg_de_la_server(char* mesaj) //un mesaj primit de la server trebuie sa fie de forma [cifra][cifra][cifra][cifra][caracter]
{
    if(strlen(mesaj)>LUNGIME_MAX_MESAJ)//mesaj prea lung 
    {
        printf("[client] Eroare, am primit un mesaj invalid, prea lung\n");
        fflush(stdout);
        return;
    }

    

    int first=mesaj[0]-'0';
    
    if(first!=INCEPUT_JOC && first!=IESIRE_JOC /*&& first!=IESIRE_JOC_FORTAT*/ ) // e mutare normala
    {
        if(!strchr("0123456789X",mesaj[0]) || !strchr("0123456789X",mesaj[1]) || 
    ! strchr("0123456789X",mesaj[2]) || !strchr("0123456789X",mesaj[3]) || !strchr("pPtTnNcCqQkK",mesaj[4])) //mesaj cu caractere invalide 
    {
        printf("[Client] Eroare, am primit un mesaj cu caractere invalide\n");
        fflush(stdout);
        return;
    }
        mutare_introdusa_gresita=0;
        mutare_coloana_veche=first;
        mutare_linie_veche=mesaj[1]-'0';
        mutare_coloana_noua=mesaj[2]-'0';
        mutare_linie_noua=mesaj[3]-'0';
        mutare_piesa=mesaj[4];
        return;
    }
    if(first==INCEPUT_JOC)
    {
        printf("Jocul incepe acum...\n");
        fflush(stdout);
        iesire_normala=0;
        iesire_fortata=0;
        jucator=(int)(mesaj[1]-'0');
        un_joc_nou=(int)(mesaj[1]-'0');
        if(jucator==1)
        {
            printf("Sunt jucatorul 1.Eu joc cu alb -litere mari- si incep primul..\n");
            fflush(stdout);
        }
        else 
        {
            printf("Sunt jucatorul 2.Eu joc cu negru -litere mici-si incep al doilea..\n");
            fflush(stdout);
        }
    }    

    if(first == IESIRE_JOC) // s-a terminat jocul
    {
        if(mesaj[1]=='N')//Jocul s-a terminat normal
        {
            printf("[admin]: Jocul s-a terminat normal\n");
            fflush(stdout);
            iesire_normala=1;
            castigator=(int)(mesaj[2] - '0');
        }
        else if(mesaj[1]=='F')
        {
            printf("[admin]: Jocul s-a terminat fortat\n");
            fflush(stdout);
            iesire_fortata=1;
            castigator=(int)(mesaj[2]-'0');
        }

        else if(mesaj[1]=='I')
        {
            printf("[admin]: Mutarea introdusa nu poate fi efectuata. Va rugam introduceti alta mutare:\n");
            fflush(stdout);
            mutare_introdusa_gresita=1;
        }
        else if(mesaj[1]=='R')
        {
            printf("[admin]: Regele e atacat.Trebuie scapat de atac!\n");
            fflush(stdout);
            mutare_introdusa_gresita=1;
        }
        else if(mesaj[1]=='4')
        {
            un_joc_nou=4;
            printf("[admin]: Va scot de tot.\n");
        }
        
        return;
    }

}

void stabileste_regulile_jocului()
{
    joc_nou();
    citeste_mesajul_serverului();
    analizeaza_msg_de_la_server(msg);
    afisare_tabla();
}

void un_singur_joc()
{
    stabileste_regulile_jocului();
    int randul=2;
    if(jucator==1)
    {
        char* rasp=mutare_valida();
        transmite_serverului(rasp);
   }
   int xx=2000;
 while(xx){
        citeste_mesajul_serverului();
        analizeaza_msg_de_la_server(msg);
       while(mutare_introdusa_gresita)
       {
        char*rasp=mutare_valida();
        transmite_serverului(rasp);
        citeste_mesajul_serverului();
        analizeaza_msg_de_la_server(msg);
        if(iesire_normala || iesire_fortata)
        break;
       }
       mutare_introdusa_gresita=0;
        system("clear");
        actualizare_tabla(mutare_linie_veche,mutare_coloana_veche,mutare_linie_noua,mutare_coloana_noua,mutare_piesa);
        if(iesire_normala==1)
        {
           
            if(jucator == castigator)
            {
                printf("Felicitari! Ati castigat!\n");
                fflush(stdout);
                close(sd);
                return;
            }
            else
            {
                 printf("Ati pierdut...\n");
                fflush(stdout);
                close(sd);
                return;
            }
        }
        if(iesire_fortata==1)
        {
            
            if(jucator == castigator)
            {
                printf("Felicitari! Ati castigat!\n");
                fflush(stdout);
                close(sd);
                return;
            }
            else
            {
                 printf("Ati pierdut...\n");
                fflush(stdout);
                close(sd);
                return;
            }
        }
        if(randul==jucator ) // e randul lui sa mute si poate face asta
        {
            char* rasp= mutare_valida();
           transmite_serverului(rasp);

        }
        randul=3-randul;
        xx--;
}
    
}

int main(int argc, char *argv[])
{
    if(argc!=3) //verificam existenta tuturor parametrilor in linia de comanda
  {
    printf("Sintaxa corecta: %s, <adresa_server>, <port>\n",argv[0]);
    return -1;
  }

    port=atoi(argv[2]);//stabilim portul

    sd=socket(AF_INET, SOCK_STREAM, 0); //cream socketul
    
    if(sd==-1)
    {
        perror("[Client] Eroare la creare socket");
        return;
    }
    server.sin_family=AF_INET;//stabilim familia socketului
    server.sin_addr.s_addr=inet_addr(argv[1]);//adresa IP a serverului
    server.sin_port=htons(port); //portul de conectare

    if(connect(sd,(struct sockaddr*) &server, sizeof(struct sockaddr))==-1) //ne conectam la server
    {
        perror("[Client] Eroare la conectarea la server.Reincercati...");
        return;
    }
    printf("M-am conectat la server...\n");

    un_singur_joc();

   return 0;
}
