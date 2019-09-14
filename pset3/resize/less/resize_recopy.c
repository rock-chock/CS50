// Makes a resized copy of a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        printf("Usage: %s n <file_to_be_resized>.bmp <resized_file_name>.bmp\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);

    // check if 1 <= n <= 100. If 1, just return copy.c (?)
    if (n < 1 || n > 100)
    {
        printf("input n that is 1 <= n <= 100");
        return 1;

    }


    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }


    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf_in;
    fread(&bf_in, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi_in;
    fread(&bi_in, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf_in.bfType != 0x4d42 || bf_in.bfOffBits != 54 || bi_in.biSize != 40 ||
        bi_in.biBitCount != 24 || bi_in.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // get output buffers
    BITMAPFILEHEADER bf_out = bf_in;
    BITMAPINFOHEADER bi_out = bi_in;


   // if n != 1, change 2 essential fields.
    if (n != 1)
    {
        // get new width (pixels)
         bi_out.biWidth = bi_in.biWidth * n;

        // get new height (pixels)
        bi_out.biHeight = bi_in.biHeight * n;
    }


    // determine padding for scanlines
    int in_padding = (4 - (bi_in.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // determine padding for outptr line
    int out_padding = (4 - (bi_out.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;


    // if n != 1, change 2 other fields.
    if (n != 1)
    {
        // get new image size (bytes)
        bi_out.biSizeImage = bi_out.biWidth * abs(bi_out.biHeight) * sizeof(RGBTRIPLE) + out_padding * abs(bi_out.biHeight);

        // new value of file size (bytes)
        bf_out.bfSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + bi_out.biSizeImage;
    }


    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_out, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_out, sizeof(BITMAPINFOHEADER), 1, outptr);



    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi_in.biHeight); i < biHeight; i++)
    {
        // iterate the same line n times
        for (int m = 0; m < n; m++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi_in.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile n times
                for (int k = 0; k < n; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // add out_padding bytes to outptr
            for (int l = 0; l < out_padding; l++)
            {
                fputc(0x00, outptr);
            }


            // if m is not last step, go to the beginning of inptr line
            if (m != n - 1)
            {
                int back_offset = bi_in.biWidth * sizeof(RGBTRIPLE) * -1;
                printf("back_offset: %i\n", back_offset);
                fseek(inptr, back_offset, SEEK_CUR);
            }
        }
        // skip over in_padding bytes inside inptr
        fseek(inptr, in_padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}