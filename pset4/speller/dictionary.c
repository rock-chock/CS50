// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents index of 'z' (assuming that 'a' is 0)
#define IND_Z 25

// Represents number of letters
#define LTRS 26

// Represents number of buckets in a hash table
#define N (IND_Z * LTRS * LTRS * LTRS + IND_Z * LTRS * LTRS + IND_Z * LTRS + LTRS + 1)

// Represents counter for words in dictionary
unsigned int cntr;

// Represent key produced by hashtag
unsigned long key;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];


// Hashes word to a number between 0 and IND_Z*LTRS*LTRS (25*26*26), inclusive, based on its first and second letters
unsigned long hash(const char *word)
{
    int second = (strlen(word) < 2) ? 'a' : word[1];
    int third = (strlen(word) < 3) ? 'a' : word[2];
    int fourth = (strlen(word) < 4) ? 'a' : word[3];
    return (tolower(word[0]) - 'a') * LTRS * LTRS * LTRS + (tolower(second) - 'a') * LTRS * LTRS +
           (tolower(third) - 'a') * LTRS + (tolower(fourth) - 'a');
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Make a new node for the word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Copy word into node.word
        strcpy(new_node->word, word);

        // Get new value of key by hashing a word
        key = hash(word);

        // Copy head of bucket(hashtable[key]) to node->next
        new_node->next = hashtable[key];

        // Allocate a word in the head of hashtable[key]
        hashtable[key] = new_node;

        // Advance counter for words
        cntr++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}



// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return cntr;
}


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash the given word and store value in key
    key = hash(word);

    // Set pointer "trav" to the beginning of the corresponding bucket
    node *trav = hashtable[key];

    // Compare given word to value of current node's "word"
    while (trav != NULL)
    {
        // return true if found the word in dictionary
        if (strcasecmp(word, trav->word) == 0)
        {
            return true;
        }
        trav = trav->next;
    }
    return false;
}




// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Declare ptrs to traverse linked lists
    node *trav, *deletion;
    trav = hashtable[0];

    // alternative
    // Access each bucket
    for (int i = 0; i < N; i++)
    {
        trav = hashtable[i];
        // Delete each element of a linked list starting from the first
        while (trav != NULL)
        {
            // Copy trav
            deletion = trav;
            // Advance trav
            trav = trav->next;
            // Free abandoned element
            free(deletion);
        }
    }
    // Assume that free() was done correctly
    return true;
}
