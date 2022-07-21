#include <stdlib.h>
#include "super_system.h"


const char *help =
  "\nSupported commands:\n"
  "  h\t\tPrints this help information\n"
  "  id\t\tReturns the ID of the device\n"
  "  v\t\tReturns the version number of the device software\n"
;

#define VERSION "0.0.1"
#define ID "IBEXSS_01"
#define MAXSERIALBUF 128
char SerialBuf[MAXSERIALBUF];
#define MAXSERIALBUFITEMS MAXSERIALBUF/2
char *SerialBufItems[MAXSERIALBUFITEMS];

const char EOT='\x04';
const char *CNF="Command not found";
const char CMD_DELIMS[] = " (),";


int my_abs(int value) {
    if (value < 0) {
        return -value;
    }
    else {
        return value;
    }
}

void swap(char *x, char *y) {
    char t = *x; *x = *y; *y = t;
}

char* reverse(char *buffer, int i, int j)
{
    while (i < j) {
        swap(&buffer[i++], &buffer[j--]);
    }
     return buffer;
}

char* my_itoa(int value, char* buffer, int base)
{
    if (base < 2 || base > 32) {
        return buffer;
    }
    int n = my_abs(value);
    int i = 0;
    while (n)
    {
        int r = n % base;
        if (r >= 10) {
            buffer[i++] = 65 + (r - 10);
        }
        else {
            buffer[i++] = 48 + r;
        }
        n = n / base;
    }
    if (i == 0) {
        buffer[i++] = '0';
    }
    if (value < 0 && base == 10) {
        buffer[i++] = '-';
    }
    buffer[i] = '\0'; 
    return reverse(buffer, 0, i - 1);
}

int my_atoi(char* str) {
    int res = 0;
    for (int i = 0; str[i] != '\0'; ++i) {
        res = res * 10 + str[i] - '0';
    }
    return res;
}

int my_strcmp(const char* s1, const char* s2) {
    while(*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return *(const unsigned char*)s1 - *(const unsigned char*)s2;
}

unsigned int is_delim(char c, const char *delim) {
    while(*delim != '\0') {
        if(c == *delim)
            return 1;
        delim++;
    }
    return 0;
}

char *my_strtok(char *srcString, const char *delim)
{
    static char *backup_string;
    if(!srcString) {
        srcString = backup_string;
    }
    if(!srcString) {
        return NULL;
    }
    while(1) {
        if(is_delim(*srcString, delim)) {
            srcString++;
            continue;
        }
        if(*srcString == '\0') {
            return NULL; 
        }
        break;
    }
    char *ret = srcString;
    while(1) {
        if(*srcString == '\0') {
            backup_string = srcString;
            return ret;
        }
        if(is_delim(*srcString, delim)) {
            *srcString = '\0';
            backup_string = srcString + 1;
            return ret;
        }
        srcString++;
    }
}

uint16_t fetch_cmd(char *input) {
    uint16_t NoChars = 0;
    char char_in = getchar();
    while (char_in != EOT) {
        if (is_char_waiting()) {
            input[NoChars++] = char_in;
            char_in = getchar();
        }
    }
    input[NoChars++]='\0';
    return NoChars;
}

uint16_t proc_cmd(char *input, char **input_items) {
    uint16_t NoItems = 0;
    char *cmd_item = my_strtok(input, CMD_DELIMS);
    while (cmd_item != NULL) {
        input_items[NoItems++]=cmd_item;
        cmd_item = my_strtok(NULL, CMD_DELIMS);
    }
    return NoItems;
}

void exec_cmd(char **input_items, const uint16_t NoItems) {
    int32_t res = 0;
    char res_str[10];
    if (((my_strcmp(input_items[0], "h")==0) || (my_strcmp(input_items[0], "?")==0)) && (NoItems==1)) {
        puts(help);
    }
    else if ((my_strcmp(input_items[0], "id")==0) && (NoItems==1)) {
        puts(ID);
    }
    else if ((my_strcmp(input_items[0], "v")==0) && (NoItems==1)) {
        puts(VERSION);
    }
    else if ((my_strcmp(input_items[0], "add")==0) && (NoItems>1)) {
        for (int i=1; i<NoItems; i++) {
            res += my_atoi(input_items[i]);
        }
        my_itoa(res, res_str, 10);
        puts(res_str);
    }
    else if ((my_strcmp(input_items[0], "min1")==0) && (NoItems==2)) {
        my_itoa(my_atoi(input_items[1])-1, res_str, 10);
        puts(res_str);
    }
    else if ((my_strcmp(input_items[0], "pitems")==0) && (NoItems>1)) {
        for (int i=1; i<NoItems; i++) {
            puts(input_items[i]);
        }
    }
    else {
        puts(CNF);
        puts("\n\n");
        puts(help);
    }
    putchar(EOT);
}

int main(void) {
    while(1) {
        if (is_char_waiting()) {
            fetch_cmd(SerialBuf);
            uint16_t NoItems = proc_cmd(SerialBuf, SerialBufItems);
            exec_cmd(SerialBufItems, NoItems);
        }
    }
}
