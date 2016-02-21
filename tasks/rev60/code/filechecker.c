#include <stdio.h>
#include <stdlib.h>
#define PASSWORDFILE ".password"

typedef enum { false, true } bool;
bool password_file_exists();
void check_password_char(int i, int *c);

int main(int argc, char **argv) {

	if(! password_file_exists()) {
		printf("Fatal error: File does not exist");
		return 1;
	}

	FILE *pw_file = fopen(PASSWORDFILE, "r");
	if(! pw_file) {
		printf("Error: Could not read file\n");
		return 1;
	}

	int data_len = (2 << 3) - 1;

	int c;
	int is_wrong = 0;
	for(int i = 0; i < data_len; i++) {
		c = fgetc(pw_file);

		if(feof(pw_file)) {
			is_wrong |= 0x1337;
			break;
		}

		check_password_char(i, &c);
		is_wrong = is_wrong | c;
	}

	if(is_wrong > 0) {
		printf("Error: Wrong characters\n");
		return 1;
	}

	fclose(pw_file);

	printf("Congrats!\n");
	return 0;
}

bool password_file_exists() {
	FILE *password_file;

	password_file = fopen(PASSWORDFILE, "r");

	if(! password_file) {
		return false;
	}

	fclose(password_file);
	return true;
}

void check_password_char(int i, int *c) {
	const int lookup[15] = {4846, 4832, 4796, 4849, 4846, 4843, 4850, 4824, 4852, 4847, 4818, 4852, 4844, 4822, 4794};

	*c = (lookup[i] + *c) % 0x1337;
}