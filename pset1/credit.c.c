/* credit.c
 * 
 * https://docs.cs50.net/problems/credit/credit.html
 * Author: rock-chock */

// Fn for credit card number validation

#include <stdio.h>
#include <cs50.h>

//    Card Name is one of:
string C_NAME_AMEX = "AMEX\n";
string C_NAME_MASTERCARD = "MASTERCARD\n";
string C_NAME_VISA = "VISA\n";
string C_NAME_INVALID = "INVALID\n";
 
//    Card_Length_Standart is one of:
int C_LENGTH_AMEX = 15;
int C_LENGTH_MASTC_OR_VISA = 16;
int C_LENGTH_VISA = 13;

// Maximum length of credit card number
const int C_LENGTH_MAX = 16;

//    First_2_Digits_Standart is one of:
// FIRST_2_AMEX          34 || 37;
// FIRST_2_MASTERCARD    [51, 55];
// FIRST_2_VISA          [40, 49];

int c_num_to_array (long c_number, int *digits);
string get_name(int *digits, int c_length, int first_2);
int check_luhn(int *digits, int c_length);

// Output name of credit card 
int main(void)
{
    long c_number;					                             
    do
    {
        c_number = get_long("Number: ");
    }
    while (c_number < 1);
    // Get length of c_number and convert c_number to array
    int digits[C_LENGTH_MAX];                                             
    int c_length = c_num_to_array (c_number, digits);
    // Check c_number for validity and produce credit card name 
    int first_2 = (10 * (digits[(c_length - 1)])) + digits[(c_length - 2)]; 
    string c_name = get_name(digits, c_length, first_2); 
    printf("%s", c_name);                          
}

// Convert given card number to an array and produce card number's length
// Digits order in array is reversed relatively to card number
int c_num_to_array(long c_number, int *digits)
{
    int length_counter = 0;
    while (((c_number / 10) > 0) || ((c_number % 10) > 0))       
    {   
        // Put digit into current index in array
        *digits = (c_number % 10);                                
        c_number = (c_number / 10);   
        length_counter++;
        // Increase pointer value to access the next index of array
        digits++;                                                  
    }
    return length_counter;
}

// Check credit card number for validity and produce corresponding credit card name 
string get_name(int *digits, int c_length, int first_2)
{  
    int result_luhn = check_luhn(digits, c_length);
    if ((c_length == C_LENGTH_AMEX) &&                            
       ((first_2 == 34) || (first_2 == 37)) &&
       (result_luhn == 0)) 
    {
        return C_NAME_AMEX;       
    }
    else if ((c_length == C_LENGTH_MASTC_OR_VISA) &&        
            ((first_2 >= 51) && (first_2 <= 55)) &&
            (result_luhn == 0))  
    {
        return C_NAME_MASTERCARD; 
    }
    else if (((c_length == C_LENGTH_VISA) || (c_length == C_LENGTH_MASTC_OR_VISA)) && 
            ((first_2 >= 40) && (first_2 <= 49)) &&         
            (result_luhn == 0))
    {
        return C_NAME_VISA;
    }     
    else                                                    
    {
        return C_NAME_INVALID;
    }
}

// Produce modulo of card digits sum using Luhn's algorithm
int check_luhn(int *digits, int c_length)
{
    int sum_first = 0;                                       
    int sum_mult_second = 0;
    int mult_num = 0; 
    int num;
    for (int i = 0; i < c_length; i = i + 1)
    {
        // Access to each item of array
        num = *digits;
        // Sum of multiplication of every other digit, starting with the array's second digit
        if ((i % 2) == 1)                                    
        {
            mult_num = 2 * num;
            // If mult_num consists of 2 digits, add those digits together
            if (mult_num > 9)                                
            {
                sum_mult_second += (mult_num % 10) + (mult_num / 10);
            }
            else
            {
                sum_mult_second += mult_num;
            }            
        }
        
        // Sum of every other digit, starting with the array's first digit
        else                                                 
        {
            sum_first += num;
        }
        // Increase pointer to provide access to the next item
        digits++;                                            
    }
    // Find modulo of sum
    int result_luhn = (sum_first + sum_mult_second) % 10;    
    return result_luhn;
}