/* vigenere.c
 * 
 * https://docs.cs50.net/2018/x/psets/2/vigenere/vigenere.html
 * Author: rock-chock */

// Vigenere encrypting algorithm
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

// Alphabet length
const int LETTERS = 'z' - 'a' + 1;

bool is_valid(int argc, string key);
void make_array(string s_key, int keys[]);
string encrypt(int keys[], int length, string plain_text);

// Encrypt a text by using Caesar's algorithm 
int main(int argc, string argv[])
{
    // Check amount of given words and if the key is made of letters
    string s_key = argv[1];
    if (!is_valid(argc, s_key))
    {
        printf("\nUsage: %s keyword\n", argv[0]);
        return 1;
    }
    printf("Success!\n");
    
    // Convert a string key to array of keys
    int length = strlen(s_key);
    int keys[length];
    make_array(s_key, keys);
    // Encrypt given string using key text
    string plain_text = get_string("\nplaintext: ");
    string cipher_text = encrypt(keys, length, plain_text); 
    printf("\nciphertext: %s\n", cipher_text);
}

// Produce true if user gave 2 words at command prompt and if a given key consists of letters. Otherwise false. 
bool is_valid(int argc, string key)
{
    if (argc != 2)
    {
        return false;
    }
    else
    {
        for (int i = 0, n = strlen(key); i < n; i++)
        {
            if (!isalpha(key[i]))
            {
                return false; 
            }
        }
    }
    return true;
}

// Save each char of s_key to array keys[];
void make_array(string s_key, int keys[])
{
    for (int i = 0, n = strlen(s_key); i < n; i++)
    {
        keys[i] = tolower(s_key[i]) - 'a';
    }
}

// Encrypt given string using Vigenère algorithm 
string encrypt(int keys[], int key_length, string plain_text)
{
    string cipher_text = plain_text;
    char cur_c;
    int cur_key;
    // key_count is -1 in case if the 1st given char of plaintext is not a letter
    int key_count = -1;
    for (int i = 0, n = strlen(plain_text); i < n; i++)
    {
        cur_c = plain_text[i];
        // If cur_c is a letter, advance key_count. Otherwise let it stay the same.
        if isalpha(cur_c)
        {
            key_count = (key_count + 1) % key_length;
        }
        cur_key = keys[key_count];
        if isupper(cur_c)
        {
            cur_c = (cur_c - 'A' + cur_key) % LETTERS + 'A';
        }
        else if islower(cur_c)
        {
            cur_c = (cur_c - 'a' + cur_key) % LETTERS + 'a';
        }
        cipher_text[i] = cur_c;
    }
    return cipher_text;
}
