#include <stdio.h>
#include "flag.h"

int main() {
	setbuf(stdout, NULL);
	printf("Solve the following equations:\n");
	printf("X > 1337\n");
	printf("X * 7 + 4 = 1337\n");
	
	unsigned int leet = 1337;
	unsigned int x = 0;
	unsigned int seven = 7;

	printf("Enter the solution X: ");
	scanf("%d", &x);

	printf("You entered: %d\n", x);
	if(x <= leet) {
		printf("%d is not bigger than %d\n", x, leet);
		printf("WRONG!!!\n");
		printf("Go to school and learn some math!\n");
		return 1;
	}
	printf("%d is bigger than %d\n", x, leet);

	x *= 7;
	x += 4;

	if(x == 1337) {
		printf("%d is equal to %d\n", x, leet);
		printf("Well done!\n");
		printf(FLAG);
		return 0;
	}

	printf("%d is not equal to %d\n", x, leet);
	printf("WRONG!!!\n");
	printf("Go to school and learn some math!\n");
	return 1;
}