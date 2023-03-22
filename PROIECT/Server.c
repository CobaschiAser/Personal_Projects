#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <wait.h>




#define MAX 256
//#define HOST "127.0.0.1"
#define PORT  2807 // portul de conectare la server

#define LUNGIME_MAX_MESAJ 5
#define INCEPUT_JOC 8
#define IESIRE_JOC 9
//#define IESIRE_JOC_FORTAT 7

//chestii pentru client-server:
//int a[h][l]; //umplem cu 1 pentru primul jucator si cu 2 pentru al doilea
extern int errno;   //codul de eroare returnat de anumite apeluri */
struct sockaddr_in   server;	// structura folosita de server
struct sockaddr_in   from1;     // structura folosita de clientul 1
struct sockaddr_in   from2;     // structura folosita de clientul 2
int sd;			//descriptorul de socket
int mutare_coloana_veche;
int mutare_linie_veche;
int mutare_coloana_noua;
int mutare_linie_noua;
int sfarsit;
char mutare_piesa;
int mutare_introdusa_corecta;
int iesire_fortata;
int un_joc_nou;
int player;

char msgrasp[MAX];  //mesaj de raspuns pentru ambii clienti
char msg[MAX];      //mesaj universal citit
char tabla[8][8];





void pregatire_server();// vom pregati serverul pentru a putea realiza conexiuni cu clientii
int acceptare_client1();// 
int acceptare_client2();// 

//chestii de algoritmica

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

void actualizare_tabla(int lin_veche,int col_veche, int lin_noua, int col_noua,char piesa)
{
         fflush(stdout);
         tabla[lin_veche][col_veche]='0';
         tabla[lin_noua][col_noua]=piesa;
         //afisare_tabla();

}

int alege_clientul(int client1, int client2, int jucator )
{
    int client;
    if(jucator==1) client=client1;
    else if(jucator==2) client=client2;
    else {
        perror("[Eroare] Cod jucator invalid\n");
        exit(EXIT_FAILURE);
    }
    return client;
}

void raspunde_clientului(int client1, int client2, int jucator, char* mesaj)
{
    int client=alege_clientul(client1, client2, jucator);
    //printf("Trimitem mesajul ..%s..catre jucatorul %d\n",mesaj,jucator);
    fflush(stdout);

    if(write(client,mesaj,MAX)<=0)
    {
        perror("[Server] Eroare la transmiterea mesajului catre client\n");
        close(client);
        exit(EXIT_FAILURE);
    }

    //printf("Mesajul..%s.. a fost transmis cu succes catre jucatorul %d\n",mesaj ,jucator);
    fflush(stdout);
}

int mutare_turn ( int old_l, int old_c , int new_l, int new_c)
{
    if(new_l != old_l && new_c != old_c)// cu turnul ma pot deplasa doar pe aceeasi linie sau pe aceeasi coloana
                    return 0;
                if(new_l == old_l) //daca ma deplasez pe aceeasi linie
                {
                    if(new_c > old_c)
                    {
                        for(int i=old_c+1;i<new_c;i++)
                            if(tabla[new_l][i] != '0')
                                return 0;
                    }
                    if(new_c < old_c)
                    {
                        for(int i=old_c-1;i>new_c;i--)
                            if(tabla[new_l][i] != '0')
                                return 0;
                    }
                }
                if(new_c == old_c) //daca ma deplasez pe aceeasi linie
                {
                    if(new_l > old_l)
                    {
                        for(int i=old_l+1;i<new_l;i++)
                            if(tabla[i][new_c] != '0')
                                return 0;
                    }
                    if(new_l < old_l)
                    {
                        for(int i=old_l-1;i>new_l;i--)
                            if(tabla[i][new_c] != '0')
                                return 0;
                    }
                }
                return 1;
}

int mutare_nebun(int old_l, int old_c, int new_l, int new_c)
{
    if(new_l == old_l || new_c == old_c) return 0; // nebunul nu se poate deplasa pe aceeasi linie/coloana 

            if(abs(new_c-old_c) != abs(new_l-old_l)) return 0;// nebunul se poate deplasa doar pe diagonala in raport cu pozitia initiala

            // verifcam ca diagonalele pana la pozitia noua sa fie libere
            if(new_l > old_l) 
            {
                int dif = new_l - old_l;
                
                if(new_c < old_c)
                {
                    for(int i=1; i<dif; i++)
                        if(tabla[old_l+i][old_c-i] != '0')
                            return 0;
                    return 1;
                }
                if(new_c > old_c)
                {
                    for(int i=1; i<dif; i++)
                        if(tabla[old_l+i][old_c+i] != '0')
                            return 0;
                    return 1;
                }
            }
            if(new_l < old_l)
            {
                int dif=old_l - new_l;
                
                if(new_c < old_c)
                {
                    for(int i=1; i<dif; i++)
                    {
                        if(tabla[old_l-i][old_c-i] != '0')
                            return 0;
                    }
                  return 1;
                }
                if(new_c > old_c)
                {
                    for(int i=1;i<dif;i++)
                    {
                        if(tabla[old_l-i][old_c+i] != '0')
                            return 0;
                    }
                    return 1;
                }
            }
            return 1;
}

int ma_aflu_sub_atacul_pionului(int linie, int coloana, char piesa)
{
    if(strchr("tncpqk",piesa))
     {
            if(linie<7)
        {
            if(coloana-1>=0)
                if(tabla[linie+1][coloana-1]=='P')
                return 1;
            if(coloana+1<=7)
                if(tabla[linie+1][coloana+1]=='P')
                return 1;
        }
          return 0;  
     }
     else if(strchr("TNCPQK",piesa))
     {
        if(linie>0)
        {
            if(coloana-1>=0)
                if(tabla[linie-1][coloana-1]=='p')
                    return 1;
            if(coloana+1<=7)
                if(tabla[linie-1][coloana+1]=='p')
                    return 1;
        }
        return 0;
     }
     
}

int ma_aflu_sub_atacul_calului(int linie, int coloana, char piesa)
{
    if(strchr("tncpqk",piesa))
    {
        if(linie-2 >= 0 && coloana+1 <= 7 && tabla[linie-2][coloana+1] == 'C') return 1;
        if(linie-2 >= 0 && coloana-1 >= 0 && tabla[linie-2][coloana-1] == 'C') return 1;
        if(linie-1 >= 0 && coloana+2 <= 7 && tabla[linie-1][coloana+2] == 'C') return 1;
        if(linie-1 >= 0 && coloana-2 >= 0 && tabla[linie-1][coloana-2] == 'C') return 1;
        if(linie+2 <= 7 && coloana+1 <= 7 && tabla[linie+2][coloana+1] == 'C') return 1;
        if(linie+2 <= 7 && coloana-1 >= 0 && tabla[linie+2][coloana-1] == 'C') return 1;
        if(linie+1 <= 7 && coloana+2 <= 7 && tabla[linie+1][coloana+2] == 'C') return 1;
        if(linie+1 <= 7 && coloana-2 >= 0 && tabla[linie+1][coloana-2] == 'C') return 1;
        return 0;
    }
    else if(strchr("TNCPQK",piesa))
    {
        if(linie-2 >= 0 && coloana+1 <= 7 && tabla[linie-2][coloana+1] == 'c') return 1;
        if(linie-2 >= 0 && coloana-1 >= 0 && tabla[linie-2][coloana-1] == 'c') return 1;
        if(linie-1 >= 0 && coloana+2 <= 7 && tabla[linie-1][coloana+2] == 'c') return 1;
        if(linie-1 >= 0 && coloana-2 >= 0 && tabla[linie-1][coloana-2] == 'c') return 1;
        if(linie+2 <= 7 && coloana+1 <= 7 && tabla[linie+2][coloana+1] == 'c') return 1;
        if(linie+2 <= 7 && coloana-1 >= 0 && tabla[linie+2][coloana-1] == 'c') return 1;
        if(linie+1 <= 7 && coloana+2 <= 7 && tabla[linie+1][coloana+2] == 'c') return 1;
        if(linie+1 <= 7 && coloana-2 >= 0 && tabla[linie+1][coloana-2] == 'c') return 1;
        return 0;
    }
}


int ma_aflu_sub_atacul_turnului(int linie, int coloana, int piesa, int piesa2)
{
    int linie_nou, coloana_nou;
    if(strchr("tncpqk",piesa))
    {  
        linie_nou = linie-1;
        while(linie_nou > 0 && tabla[linie_nou][coloana] == '0')
            linie_nou--;
        if(tabla[linie_nou][coloana] == piesa2) return 1;
        
        linie_nou = linie+1;
        while(linie_nou < 7 && tabla[linie_nou][coloana] == '0')
            linie_nou++;
        if(tabla[linie_nou][coloana] == piesa2) return 1;

        coloana_nou = coloana-1;
        while(coloana_nou > 0 && tabla[linie][coloana_nou] == '0')
            coloana_nou--;
        if(tabla[linie][coloana_nou] == piesa2) return 1;
    
        coloana_nou = coloana+1;
        while(coloana_nou < 7 && tabla[linie][coloana_nou] == '0')
            coloana_nou++;
        if(tabla[linie][coloana_nou] == piesa2) return 1;

        return 0;
    }
    else if(strchr("TNCPQK",piesa))
    {
         linie_nou = linie-1;
        while(linie_nou > 0 && tabla[linie_nou][coloana] == '0')
            linie_nou--;
        if(tabla[linie_nou][coloana] == piesa2) return 1;
        
        linie_nou = linie+1;
        while(linie_nou < 7 && tabla[linie_nou][coloana] == '0')
            linie_nou++;
        if(tabla[linie_nou][coloana] == piesa2) return 1;

        coloana_nou = coloana-1;
        while(coloana_nou > 0 && tabla[linie][coloana_nou] == '0')
            coloana_nou--;
        if(tabla[linie][coloana_nou] == piesa2) return 1;
    
        coloana_nou = coloana+1;
        while(coloana_nou < 7 && tabla[linie][coloana_nou] == '0')
            coloana_nou++;
        if(tabla[linie][coloana_nou] == piesa2) return 1;

        return 0;
    }
}

int ma_aflu_sub_atacul_nebunului(int linie, int coloana, int piesa, int piesa2)
{
    int linie_nou;
    int coloana_nou;
    if(strchr("tncpqk",piesa))
    {
        linie_nou = linie-1;
        coloana_nou = coloana-1;
        while(linie_nou > 0 && coloana_nou > 0 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou--;
                coloana_nou--;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        linie_nou = linie-1;
        coloana_nou = coloana+1;
        while(linie_nou > 0 && coloana_nou < 7 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou--;
                coloana_nou++;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        linie_nou = linie+1;
        coloana_nou=coloana-1;
        while(linie_nou < 7 && coloana_nou > 0 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou++;
                coloana_nou--;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        linie_nou = linie+1;
        coloana_nou=coloana+1;
        while(linie_nou < 7 && coloana_nou < 7 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou++;
                coloana_nou++;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        return 0;
    }
    else if(strchr("TNCPQK",piesa))
    {
         linie_nou = linie-1;
        coloana_nou = coloana-1;
        while(linie_nou > 0 && coloana_nou > 0 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou--;
                coloana_nou--;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        linie_nou = linie-1;
        coloana_nou = coloana+1;
        while(linie_nou > 0 && coloana_nou < 7 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou--;
                coloana_nou++;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        linie_nou = linie+1;
        coloana_nou=coloana-1;
        while(linie_nou < 7 && coloana_nou > 0 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou++;
                coloana_nou--;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        linie_nou = linie+1;
        coloana_nou=coloana+1;
        while(linie_nou < 7 && coloana_nou < 7 && tabla[linie_nou][coloana_nou] == '0')
            {
                linie_nou++;
                coloana_nou++;
            }
            if(tabla[linie_nou][coloana_nou] == piesa2) return 1;
        return 0;
    }
    
}

int ma_aflu_sub_atacul_reginei(int linie, int coloana, int piesa)
{
    if(strchr("tncpqk", piesa))
    {
        if(ma_aflu_sub_atacul_nebunului(linie, coloana, piesa, 'Q')) return 1;
        if(ma_aflu_sub_atacul_turnului(linie, coloana, piesa, 'Q')) return 1;
        return 0;
    }
    if(strchr("TNCPQK", piesa))
    {
        if(ma_aflu_sub_atacul_nebunului(linie, coloana, piesa, 'q')) return 1;
        if(ma_aflu_sub_atacul_turnului(linie, coloana, piesa, 'q')) return 1;
        return 0;
    }
}

int ma_aflu_sub_atac(int linie, int coloana, char piesa)
{
    if(ma_aflu_sub_atacul_pionului(linie, coloana, piesa)) return 1;
    if(ma_aflu_sub_atacul_calului(linie, coloana, piesa)) return 1;
    if(ma_aflu_sub_atacul_reginei(linie, coloana, piesa)) return 1;
    if(strchr("tncpqk",piesa))
    {
        if(ma_aflu_sub_atacul_nebunului(linie, coloana, piesa, 'N')) return 1;
        if(ma_aflu_sub_atacul_turnului(linie, coloana, piesa, 'T')) return 1;
        return 0;       
    }
    else if(strchr("TNCPQK",piesa))
    {
        if(ma_aflu_sub_atacul_nebunului(linie, coloana, piesa, 'n')) return 1;
        if(ma_aflu_sub_atacul_turnului(linie, coloana, piesa, 't')) return 1;
        return 0;
    }
   
}

int mutare_poate_fi_facuta(int old_c, int old_l, int new_c, int new_l, char piesa)
{
    if(tabla[old_l][old_c]!=piesa)//verificam ca pe pozitia initiala sa afle piesa care se vrea mutata
    {
        printf("Pe pozitia specificata nu se gasea piesa respectiva!\n");
        fflush(stdout);
        return 0;
    }
    if(old_c > 7 || old_l > 7 || new_c >7 || new_l >7)//verificam ca pozitiile sa fie de pe tabla
        {
            printf("Ati introdus o pozitie afara din tabla!\n");
            fflush(stdout);
            return 0;
        }
    
    if(new_l==old_l && new_c==old_c)//verificam ca noua pozitie sa fie diferita dea cea initiala
      return 0;

    if(player==1) //verificam ca albul sa nu incerce sa mute piese negre
    {
        if(strchr("tncqkp",piesa))
            return 0;
    }

    if(player==2)//verificam ca negrul sa nu incerce sa mute piese albe
    {
        if(strchr("TNCQKP",piesa))
            return 0;
    }

    if(strchr("tncqkp",piesa))//verificam ca negrul sa nu poata muta peste o piesa neagra
    {
        if(strchr("tncqkp",tabla[new_l][new_c]))
            return 0;
    }
    if(strchr("TNCQKP",piesa))//verificam ca albul sa nu poata muta peste o piesa alba
    {
        if(strchr("TNCQKP",tabla[new_l][new_c]))
            return 0;
    }
    
    // incepem un fel de switch(piesa)
    
        if(piesa =='P') // pion alb
        {
                if( new_l == old_l-1 && new_c == old_c && tabla[new_l][new_c] == '0')//poate inainta pe aceeasi coloana o poz doar daca are liber 
                    return 1;
                if( old_l == 6 && new_l == old_l-2 && new_c == old_c && tabla[new_l][new_c] == '0' && tabla[new_l+1][new_c] == '0')//poate inainta pe aceeasi col 2 poz doar daca are liber tot pana acolo
                    return 1; 
                if(new_l == old_l-1 && (new_c == old_c-1 || new_c == old_c+1) && strchr("tncqkp",tabla[new_l][new_c]))//poate schimba coloana(vecina cu cea initiala) doar daca muta peste negru
                    return 1;
                return 0;//altfel, nu e mutare valida
        }
    
        else if (piesa == 'p')//pion negru
        {
                if(new_l == old_l+1 && new_c == old_c && tabla[new_l][new_c] == '0')//poate inainta pe aceeasi coloana o poz doar daca are liber
                    return 1;
                if(old_l == 1 && new_l == old_l+2 && new_c == old_c && tabla[new_l][new_c] == '0' && tabla[new_l-1][new_c] == '0')//poate inainta pe aceeasi col 2 poz doar daca are liber tot pana acolo
                    return 1;
                if(new_l == old_l+1 && (new_c == old_c-1 || new_c == old_c+1) && strchr("TNCQKP",tabla[new_l][new_c]))//poate schimba coloana(vecina cu)
                    return 1;
                return 0;//altfel, nu e mutare valida 
        }
        
        else if(piesa =='C' || piesa =='c' )// cal alb sau negru:
        {
                if(new_l == old_l-1 && (new_c == old_c-2 || new_c == old_c+2))
                    return 1;
                if(new_l == old_l-2 && (new_c == old_c-1 || new_c == old_c+1))
                    return 1;
                if(new_l == old_l+1 && (new_c == old_c-2 || new_c == old_c+2))
                    return 1;
                if(new_l == old_l+2 && (new_c == old_c-1 || new_c == old_c+1))
                    return 1;
                return 0;
        }
        else if(piesa == 'T' || piesa == 't') // turn alb sau negru
        {
               return mutare_turn(old_l, old_c, new_l, new_c);
        }

        else if(piesa == 'N' || piesa == 'n')
        {
            return mutare_nebun(old_l, old_c, new_l, new_c);
        }

        else if( piesa == 'Q' || piesa == 'q') // regina se poate misca ca o tura sau ca un nebun
        {
            
            if(new_l == old_l || new_c == old_c)
                return mutare_turn(old_l, old_c, new_l, new_c);
            if(new_l != old_l && new_c != old_c)
                return mutare_nebun(old_l, old_c, new_l, new_c);   
            return 0;
        }

       else if( piesa == 'K')
       {
        if(abs(old_l-new_l) > 1 || abs(old_c-new_c) > 1)//regele se poate deplasa doar pe o patrica vecina cu pozitia initiala
            return 0;
        // pt rege e necesar un set de verificari suplimentar, adica sa vedem daca nu cumva pozitia pe care se muta se afla sub atac inamic.
        return 1;
       }
    
    return 1;
}


int regele_e_atacat(int jucator)
{
    if(jucator==1)
    {
        for(int i=0;i<8;i++)
            for(int j=0;j<8;j++)
                if(tabla[i][j]=='K')
                {
                    return ma_aflu_sub_atac(i,j,'K');
                }
    }
    else
     {
        for(int i=0;i<8;i++)
            for(int j=0;j<8;j++)
                if(tabla[i][j]=='k')
                {
                    return ma_aflu_sub_atac(i,j,'k');
                }
     }
}

void analizeaza_msg_de_la_client(int jucator,char * mesaj)
{
   if(strlen(mesaj)>LUNGIME_MAX_MESAJ)
   {
    printf("Eroare..mesaj prea lung transmis de client");
    fflush(stdout);
    return;
   }
   
   else 
   {
     int first=mesaj[0]-'0';
     if(first!= IESIRE_JOC && first != INCEPUT_JOC /*&& first != IESIRE_JOC_FORTAT*/)
     {
        if(!strchr("0123456789",mesaj[0]) || !strchr("0123456789",mesaj[1]) ||
          !strchr("0123456789",mesaj[2]) || !strchr("0123456789",mesaj[3]) || 
        !strchr("pPtTnNcCqQkK",mesaj[4]))
        {
            printf("[server] Eroare: am primit un mesaj invalid, cu caractere necorespunzatoare\n");
            exit(EXIT_FAILURE);
            fflush(stdout);
        }
     

         mutare_coloana_veche=first;
         mutare_linie_veche=mesaj[1]-'0';
         mutare_coloana_noua=mesaj[2]-'0';
         mutare_linie_noua=mesaj[3]-'0';
         mutare_piesa=mesaj[4];
         bzero(msgrasp,MAX);
         mutare_introdusa_corecta=mutare_poate_fi_facuta(mutare_coloana_veche,mutare_linie_veche,mutare_coloana_noua,mutare_linie_noua,mutare_piesa);
         if(mutare_introdusa_corecta && !regele_e_atacat(jucator))
         {
            actualizare_tabla(mutare_linie_veche,mutare_coloana_veche, mutare_linie_noua, mutare_coloana_noua, mutare_piesa);
            if(regele_e_atacat(jucator))
            {
                mutare_introdusa_corecta=0;
                actualizare_tabla(mutare_linie_noua,mutare_coloana_noua, mutare_linie_veche, mutare_coloana_veche, mutare_piesa);
                msgrasp[0]=(char)('0'+IESIRE_JOC);
            msgrasp[1]='R';//regele e atacat, trebuie mutat neaparat regele
            msgrasp[2]='\0';
            return;
            }
            if(!regele_e_atacat(jucator))
            {
            actualizare_tabla(mutare_linie_noua,mutare_coloana_noua, mutare_linie_veche, mutare_coloana_veche, mutare_piesa);
            msgrasp[0]=mesaj[0];
            msgrasp[0]=mesaj[0];
            msgrasp[1]=mesaj[1];
            msgrasp[2]=mesaj[2];
            msgrasp[3]=mesaj[3];
            msgrasp[4]=mesaj[4];
            msgrasp[5]='\0';
            return;
            }
         }
         
         else if(mutare_introdusa_corecta && regele_e_atacat(jucator) && (mutare_piesa != 'k' && mutare_piesa != 'K'))
         {
            
            actualizare_tabla(mutare_linie_veche,mutare_coloana_veche, mutare_linie_noua, mutare_coloana_noua, mutare_piesa);
            if(regele_e_atacat(jucator))
            {
            mutare_introdusa_corecta=0;
            actualizare_tabla(mutare_linie_noua,mutare_coloana_noua, mutare_linie_veche, mutare_coloana_veche, mutare_piesa);
            msgrasp[0]=(char)('0'+IESIRE_JOC);
            msgrasp[1]='R';//regele e atacat, trebuie mutat neaparat regele
            msgrasp[2]='\0';
            return;
            }
            if(!regele_e_atacat(jucator))
            {

            actualizare_tabla(mutare_linie_noua,mutare_coloana_noua, mutare_linie_veche, mutare_coloana_veche, mutare_piesa);
            msgrasp[0]=mesaj[0];
            msgrasp[1]=mesaj[1];
            msgrasp[2]=mesaj[2];
            msgrasp[3]=mesaj[3];
            msgrasp[4]=mesaj[4];
            msgrasp[5]='\0';
            return;
            }

         }
         else if(mutare_introdusa_corecta && regele_e_atacat(jucator) && (mutare_piesa == 'k' || mutare_piesa == 'K') && ma_aflu_sub_atac(mutare_linie_noua,mutare_coloana_noua,mutare_piesa))
         {
            mutare_introdusa_corecta=0;
            msgrasp[0]=(char)('0'+IESIRE_JOC);
            msgrasp[1]='R';//regele e atacat, trebuie mutat neaparat regele
            msgrasp[2]='\0';
         }
         else if(mutare_introdusa_corecta && regele_e_atacat(jucator) && (mutare_piesa == 'k' || mutare_piesa == 'K') && !ma_aflu_sub_atac(mutare_linie_noua,mutare_coloana_noua,mutare_piesa))
         {
             msgrasp[0]=mesaj[0];
            msgrasp[1]=mesaj[1];
            msgrasp[2]=mesaj[2];
            msgrasp[3]=mesaj[3];
            msgrasp[4]=mesaj[4];
            msgrasp[5]='\0';
            return;
         }
         else
         {
            msgrasp[0]=(char)('0'+IESIRE_JOC);//trebuie ca in client sa putem citi usor si intelege la ce ne referim
            msgrasp[1]='I';//invalid
            msgrasp[2]='\0';
            return;
         }
     }

     if(first == IESIRE_JOC)
     {
        bzero(msgrasp, MAX);
        if(mesaj[1]=='N')// IESIRE_NORMALA
        {
            msgrasp[0]=(char)('0'+IESIRE_JOC);
            msgrasp[1]='N';
            msgrasp[2]=(char)('0'+jucator);
            msgrasp[3]='\0';
            return;
        }
        else if(mesaj[1]=='F') //IESIRE_FORTATA
        {
            iesire_fortata=1;
            msgrasp[0]=(char)('0'+IESIRE_JOC);
            msgrasp[1]='F';
            msgrasp[2]=(char)('0'+jucator);
            msgrasp[3]='\0';
        }
        
     }

     if(first == INCEPUT_JOC)
     {
            un_joc_nou = (int)(mesaj[1]-'0');
            return;
     }
     
   }
}

void citeste_mesajul_clientului(int client1, int client2, int jucator)
{
    printf("Asteptam mesajul de la client...\n");
    fflush(stdout);
    int client=alege_clientul(client1, client2, jucator);
    printf("clientul %d\n",client);
    int len=0;
    if(read(client,&len,sizeof(len))<=0)
    {
        printf("[Server] Eroare la citirea lungimii mesajului de la client\n");
        close(client);
        exit(EXIT_FAILURE);
    }
    int converted_len=ntohl(len);
    //printf("Am receptionat lungimea mesajului de la client:%d\n",converted_len);
    fflush(stdout);
    bzero(msg,MAX);
    if(read(client, msg, MAX)<=0)
    {
        printf("[Server] Eroare la citirea de la client\n");
        close(client);
        exit(EXIT_FAILURE);
    }
    //printf("Mesajul receptionat de la jucatorul %d este ..%s...urmeaza  analizarea lui \n", jucator, msg);
   analizeaza_msg_de_la_client(jucator, msg);
}

void asignare_tabla()
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
    //afisare_tabla();
}

void joc_nou(int client1, int client2)
{
    asignare_tabla();
    char *m1="8100K";//8= inceput de joc, 1= alb , 0 si R sunt random pt a umple 5 caractere dintre cele necesare
    char *m2="8200K";//8= inceput de joc, 2=negru , 0 si R analog ca mai sus
    
    raspunde_clientului(client1, client2, 1, m1);// jucatorul generat va juca cu alb
    raspunde_clientului(client1, client2, 2, m2);// jucatorul celalalt va juca cu negru
}

int un_singur_joc(int client1,int client2)
{
    joc_nou(client1, client2);
    player=1;
    int castigator=0;
    sfarsit=1000;
    int mutari_gresite_consecutive=0;
    while(sfarsit>0)
    {
       // printf("Inca o mutare: \n");
        citeste_mesajul_clientului (client1, client2, player);
        
        while(!mutare_introdusa_corecta && !iesire_fortata)
        {
            mutari_gresite_consecutive++;
            if(mutari_gresite_consecutive == 5)
            {
                sfarsit=0;
                castigator=3-player;
                break;
            }
            if(iesire_fortata)
            {
                sfarsit=0;
                break;
            }
            raspunde_clientului(client1, client2, player, msgrasp);
            citeste_mesajul_clientului(client1, client2, player);
            
           
            
        }
        mutari_gresite_consecutive=0;

     if(iesire_fortata==1)
     {
        castigator=3-player;
        sfarsit=0;
        printf("Iesire fortata\n");
        fflush(stdout);
        msgrasp[0]=(char)('0'+IESIRE_JOC);
        msgrasp[1]='F';
        msgrasp[2]=(char)('0' + castigator);
        msgrasp[3]='\0';
        
     } 

     if(sfarsit==0 && iesire_fortata == 0)
        {
            castigator=3-player;
            printf("Jocul e gata\n");
            //castigator=
            fflush(stdout);
            msgrasp[0]=(char)('0'+IESIRE_JOC);
            msgrasp[1]='N';
            msgrasp[2]=(char)('0'+castigator);
            msgrasp[3]='\0';
        }
       else
        actualizare_tabla(mutare_linie_veche, mutare_coloana_veche, mutare_linie_noua, mutare_coloana_noua, mutare_piesa);

        

        raspunde_clientului(client1, client2, 1, msgrasp);
        raspunde_clientului(client1, client2, 2, msgrasp);
        
        player=3-player;
        sfarsit--;
    }
    printf("S-a terminat..\n");
    printf("Castigator: jucatorul %d",castigator);
    return castigator;
}

int main()
{
   pregatire_server();
   while(1)
   {
    int client_1=acceptare_client1();
    int client_2=acceptare_client2();
    if(client_1==404 || client_2==404)// nu am gasit pereche
    {
        close(client_1);
        close(client_2);
        continue;
    }
    int pid=fork(); //cream un proces fiu
    if(pid==-1) //Eroare la fork
    {
        close(client_1);
        close(client_2);
        continue;
    }
    else if(pid>0) //parinte ->el continua sa accepte jucatori
    {
        close(client_1);
        close(client_2);
        while(waitpid(-1,NULL,WNOHANG)); //?
        continue;
    }
    else if(pid==0) //copil
    {
        close(sd);
        printf("[Server] Avem 2 jucatori si putem incepe partida\n");
        int CHAMP=un_singur_joc(client_1,client_2);
        close(client_1);
        close(client_2);
        exit(0);
    }
   }
}

void pregatire_server(){
   
   sd=socket(AF_INET, SOCK_STREAM, 0); //facem un socket, modalitate de comunicare in retea.
   if(sd==-1){
    perror("[Server] Eroare la creare socket!");
    return;
   }

   bzero(&server, sizeof(server));// pregatim structura pentru server
   bzero(&from1, sizeof(from1));// pregatim structura pentru client_1
   bzero(&from2, sizeof(from2));// pregatim structura pentru client_2

   server.sin_family = AF_INET;// stabilim familia de socketuri
   server.sin_addr.s_addr = htonl (INADDR_ANY);//acceptam orice adresa    ---  host-to-network long
   server.sin_port=htons(PORT); // utilizam un port     ---      host-to-network short

   if(bind(sd, (struct sockaddr *)  &server, sizeof(struct sockaddr)) ==-1)  // folosim bind pentru a atasa socketul
   {
       perror("[Server] Eroare la bind");
       return;
   }

   if(listen(sd,1)==-1)  // folosim listen pentru a astepta clienti
   {
     perror("[Server] Eroare la listen");
     return;
   }

}

int acceptare_client1(){
    int client_1; 
    unsigned int length1 = sizeof(from1);
   
   
    client_1 = accept(sd,(struct sockaddr *) &from1, &length1 );
    if(client_1 ==- 1){
    perror ("[Server] Eroare la acceptarea clientului 1");
    fflush(stdout);
    return 404;
    }

    printf ("[Server] Am acceptat la portul %d...clientul 1\n",PORT);
    fflush (stdout);
   

   return client_1;
}

int acceptare_client2(){
    int client_2;
    unsigned int length2=sizeof(from2);
    
    client_2=accept(sd,(struct sockaddr*) &from2, &length2);

    if(client_2==-1)
    {
        perror("[Server] Eroare la acceptarea clientului 2");
        fflush(stdout);
        return 404;
    }
    printf("[Server] Am acceptat la portul %d...clientul 2\n",PORT);
    fflush(stdout);

    return client_2;
}

