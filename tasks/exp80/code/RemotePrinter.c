#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

void print(char *ip, int port);
void print_flag();

int main() {
	setbuf(stdout, NULL);
	char ip[16];
	int port = 0;
	printf("This is a remote printer!\n");
	printf("Enter IPv4 address:");
	scanf("%15s", ip);
	printf("Enter port:");
	scanf("%d", &port);
	printf("Thank you, I'm trying to print %s:%d now!\n", ip, port);

	print(ip, port);

	return 0;
}

void print(char *ip, int port) {
	int s;
	struct sockaddr_in sv;
	char m[8192];
	
	s = socket(AF_INET , SOCK_STREAM , 0);
	if (s == -1)
	{
		printf("No socket :(\n");
		return;
	}
	
	sv.sin_addr.s_addr = inet_addr(ip);
	sv.sin_family = AF_INET;
	sv.sin_port = htons(port);

	if (connect(s , (struct sockaddr *)&sv , sizeof(sv)) < 0)
	{
		perror("No communication :(\n");
		return ;
	}

	if( recv(s , m , sizeof(m) , 0) < 0)
	{
		puts("No data :(");
		return ;
	}
	
	printf(m);

	close(s);
	
	return ;
}

void print_flag() {
	FILE *f = fopen("flag.txt", "r");
	char flag[50];
	fgets(flag, sizeof(flag), f);
	fclose(f);
	printf("YAY, FLAG: %s\n", flag);
	return;
}