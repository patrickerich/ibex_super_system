#include <stdlib.h>
#include <string.h>
#include "super_system.h"


const char *help =
  "\nSupported commands:\n"
  "  h\t\tPrints this help information\n"
  "  id\t\tReturns the ID of the device\n"
  "  v\t\tReturns the version number of the device software\n"
;

#define VERSION "0.0.2"
#define ID "IBEXSS_01"
#define MAXSERIALBUF 128
char SerialBuf[MAXSERIALBUF];
#define MAXSERIALBUFITEMS MAXSERIALBUF/2
char *SerialBufItems[MAXSERIALBUFITEMS];

const char EOT='\x04';
const char *CNF="Command not found";
const char CMD_DELIMS[] = " (),";

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
    char *cmd_item = strtok(input, CMD_DELIMS);
    while (cmd_item != NULL) {
        input_items[NoItems++]=cmd_item;
        cmd_item = strtok(NULL, CMD_DELIMS);
    }
    return NoItems;
}

void exec_cmd(char **input_items, const uint16_t NoItems) {
    int32_t res = 0;
    char res_str[10];
    if (((strcmp(input_items[0], "h")==0) || (strcmp(input_items[0], "?")==0)) && (NoItems==1)) {
        puts(help);
    }
    else if ((strcmp(input_items[0], "id")==0) && (NoItems==1)) {
        puts(ID);
    }
    else if ((strcmp(input_items[0], "v")==0) && (NoItems==1)) {
        puts(VERSION);
    }
    else if ((strcmp(input_items[0], "add")==0) && (NoItems>1)) {
        for (int i=1; i<NoItems; i++) {
            res += atoi(input_items[i]);
        }
        itoa(res, res_str, 10);
        puts(res_str);
    }
    else if ((strcmp(input_items[0], "min1")==0) && (NoItems==2)) {
        itoa(atoi(input_items[1])-1, res_str, 10);
        puts(res_str);
    }
    else if ((strcmp(input_items[0], "pitems")==0) && (NoItems>1)) {
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
