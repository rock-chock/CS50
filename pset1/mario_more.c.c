// Print 2 pyramids of hashtags
#include <cs50.h>
#include <stdio.h>

int get_height(string prompt);
void make_pyramid(int height);

// Ask user for height of a pyramid, then render 2 pyramids of #
int main(void)
{
    int height = get_height("Input height of a pyramid (between 1 and 8 inclusive): ");
    make_pyramid(height);
}

// Get height of pyramid from user. Height is an integer between 1 and 8, inclusive
int get_height(string prompt)
{
    int height;
    do
    {
        height = get_int("%s", prompt);
    }
    while ((height < 1) || (8 < height));
    return (height);
}


// Render two pyramids composed of given (height) rows and given (height) columns of #
void make_pyramid(int height)
{
    for (int i = 1; i <= height; i++)
    {
        // Render right oriented part of image
        for (int j = height; j >= 1; j--)
        {
            if (j > i)
            {
                printf(" ");
            }
            else 
            {
                printf("#"); 
            }   
        }
        // Render a space;
        printf("  ");
        //  Render left oriented part of image
        for (int j = height; j >= 1; j--)
        {
            if (j > (height - i))
            {
                printf("#");
            }
        }
        printf("\n");
    }
}


