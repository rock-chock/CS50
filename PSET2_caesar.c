/* caesar.c
 *
 * https://docs.cs50.net/2018/x/psets/2/pset2.html
 * 
 * Author: rock-chock */

// Caesar encrypting algorithm

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Alphabet length
const int LENGTH = 'z' - 'a' + 1;

// Encrypt a text by using Caesar's algorithm 
int main(int argc, string argv[])
{
    // Check if user gave 2 words at a command prompt (1. to start program, 2. key). If not 2, exit the program.
    if (argc != 2)
    {
        printf("\nUsage: %s key\n", argv[0]);
        return 1;
    } 
    // Check if a given key is natural number. If not, exit the program.
    string s_key = argv[1];
    for (int i = 0, n = strlen(s_key); i < n; i++)
    {
        if (isdigit(s_key[i]) == false)
        {
            printf("\nUsage: %s key\n", argv[0]);
            return 2; 
        }
    }
    // Convert a string key to an integer
    int key = atoi(s_key);
    printf("Success!\n");
    // Prompt user for plaintext
    string plain_text = get_string ("\nplaintext: ");
    // Encrypt plain text
    string cipher_text = plain_text;
    char cur;
    for (int i = 0, n = strlen(plain_text); i < n; i++)
    {
        cur = plain_text[i];
        if isupper(cur)
        {
            cur = (cur - 'A' + key) % LENGTH + 'A';
        }
        else if islower(cur)
        {
            cur = (cur - 'a' + key) % LENGTH + 'a';
        }
        cipher_text[i] = cur;
    }
    // Output ciphertext
    printf("\nciphertext: %s\n", cipher_text);
}
