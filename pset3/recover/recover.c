// Program to recover jpeg images from raw file
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

bool is_beginning(char *cur_block);
void recover(FILE *inptr, char *cur_block,  int *jpeg_counter, int *read_result, char *outfile, FILE *outptr, char *f_name);

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: %s <file_name>.raw\n", argv[0]);
        return 1;
    }


    // remember filenames
    char *infile = argv[1];
    char *outfile = "000.jpg";

    // open input and output file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", outfile);
        return 2;
    }


    // Get pointer to memory block of 512 bytes
    char *cur_block = malloc(BLOCK_SIZE);
    if (cur_block == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }


    // Set variables
    int jpeg_counter = -1;
    int read_result = 0;
    char f_name[7];

    // Find beginning of jpeg
    do
    {
        read_result = fread(cur_block, 1, BLOCK_SIZE, inptr);
    }
    while (is_beginning(cur_block) != true);


    // Call recursive fn
    recover(inptr, cur_block, &jpeg_counter, &read_result, outfile, outptr, f_name);


    // free malloc()
    free(cur_block);

    // close infile and outfile
    fclose(inptr);
    fclose(outptr);

    // success
    return 0;

}


bool is_beginning(char *cur_block)
{
    char bg_bytes[3] = { 0xff, 0xd8, 0xff };
    if (cur_block[0] == bg_bytes[0] && cur_block[1] == bg_bytes[1] && cur_block[2] == bg_bytes[2] &&
        (cur_block[3] & 0xf0) == 0xe0)
    {
        return true;
    }
    else
    {
        return false;
    }
}


void recover(FILE *inptr, char *cur_block,  int *jpeg_counter, int *read_result, char *outfile, FILE *outptr, char *f_name)
{
// base case: end of file
    if (*read_result < BLOCK_SIZE)
    {
        printf("Reached the end of the file\n");
    }

// case for first: write from cur_block to corresponding file
    else
    {
        if (is_beginning(cur_block) == true)
        {
            // close previous outptr file
            fclose(outptr);

            // create new name of file
            *jpeg_counter += 1;
            // printf("jpeg_counter++: %i\n", *jpeg_counter);
            sprintf(f_name, "%03i.jpg", *jpeg_counter);
            // printf("f_name: %s\n", f_name);

            // open output file
            outptr = fopen(f_name, "w");
            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", outfile);
            }
        }

        // write cur_block to outptr file
        fwrite(cur_block, BLOCK_SIZE, 1, outptr);

        // read in the next block and get amount of bytes read
        *read_result = fread(cur_block, 1, BLOCK_SIZE, inptr);

// case for rest: recursion
        recover(inptr, cur_block, jpeg_counter, read_result, outfile, outptr, f_name);
    }
}