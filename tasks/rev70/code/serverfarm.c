#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void handle_task(int i, const char *input);

int main(int argc, char **argv) {
	char *input = (char*) malloc(sizeof(char)*100 +1);

	for(int i=0; i < argc -1; i++) {
		printf("Enter Solution for task %d:",i);
		scanf("%s", input);
		handle_task(i, input);
	}
	free(input);
}

void handle_task(int i, const char *input) {
	int sum = 0;
	switch(i) {
		case 0:
			//1. block: IW{S.E
			for(int j = 0; j < strlen(input); j++) {
				sum += (int) input[j];
			}
			sum /= strlen(input);
			printf("%s", "Here's your 1. block:");
			if(! (sum <= 35)) {
				printf("I{WAQ3\n");
				return;
			}
			printf("%s","IW{");
			printf("%c", 0x50 + 0x3);
			printf("%c%c\n", 0134/2, (2<<5) + 5);
			break;
		case 1:
			//2. block: .R.V.E
			printf("%s", "Here's your 2. block:");
			if(! strlen(input) == 2) {
				printf("I{WAQ3\n");
				return;
			}
			if( ((int)input[0]) % ((int)input[1]) == 65) {
				printf("%s",".R.");
				printf("%c", 0x56);
				printf("%c%c\n", 0134/2, (2<<5) + 5);
			} else {
				printf("WI{QA3\n");
			}
			break;
		case 2:
			//2. block: .R>=F:
			printf("%s", "Here's your 3. block:");
			if(strcmp(input,"1337") == 0) {
				printf("%s\n",".R>=F:");
			} else {
				printf("%c%s%c\n",'.',"Q.D.Q",'!');
			}
			break;
		case 3:
			//2. block: A:R:M}
			if(strlen(input) > 0) {
				printf("%c%s%c\n",'A',":R:M",'}');
			}
			break;
		default:
			return;
	}
	return;
}