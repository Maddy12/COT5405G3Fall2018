/*Divide Big Integers by Jack P. Oakley
This program takes signed integers of any size in the form of a string and
divides them to give integer division*/
import java.util.Random;
import java.util.Scanner;

public class DivideBigInt
{
   public static final Random gen = new Random();
   private static final int NUMLOOPS = 1000;
   //Due to overflow errors, the MAXDIVISOR had to be restricted to less digits
   //10 or more Digits crashes, 9 digits gets negatives in the middle of numbers
   private static final int MAXDIVISOR = 8;
   
   public static void main(String[] args)
   {
      final int nStart = 4;
      final int nStop = 512;
      final int nMult = 2;
   
      generalCase();
      runCases(nStart, nStop, nMult);
   }//End main()
   
   //This method runs the general case and test numbers
   public static void generalCase()
   {
      //This bigInt is a string of numbers exactly 1000 digits long
      String bigInt = "1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000";
      String medInt = "85276";
      String smallInt = "12";
      String output;
      
      output = getSign(bigInt, smallInt);
      medInt = stripSign(bigInt);
      smallInt = stripSign(smallInt);
      output = output + divide(bigInt, smallInt);
      System.out.println(output);
   }//End generalCase()
    
   //This method determines the sign for the output and returns it in a string
   public static String getSign(String str1, String str2)
   { 
     char sign1 = str1.charAt(0);
     char sign2 = str2.charAt(0);

     if((sign1 == '-' && sign2 != '-') || (sign1 != '-' && sign2 == '-'))
        return "-";
     else
        return "+";  
   }//End getSign()
   
   //This method strips any signs out of the string number
   public static String stripSign(String str)
   {
      if(str.charAt(0) == '-' || str.charAt(0) == '+')
         return str.substring(1,str.length());
      else
         return str;
   }
   
   //This method builds a string of the integer division result
   public static String divide(String str1, String str2)
   {
      String answer = "";
      int num1;
      int num2 = Integer.parseInt(str2);
      int carry = 0;
      
      while(str1.length() > 0)
      {
         num1 = Integer.parseInt(str1.substring(0,1));
         str1 = str1.substring(1, str1.length());
         carry = carry * 10 + num1;
         if(num2 == 0)
            answer = "0";
         else
         {
            answer = answer + carry / num2;
            if(carry >= num2)
               carry = carry % num2;
         }
      }
      return answer;
   }//End divide()
   
   //This method returns a random string of numbers of the given size
   public static String buildStringNum(int size)
   {
      StringBuilder s = new StringBuilder();

      // Sign
      if(gen.nextBoolean())
         s.append('+');
      else
         s.append('-');

      // First digit should be in [1, 9] range
      s.append((char)((gen.nextInt(9) + 1) + '0'));

      // Digits other than the first one in [0, 9] range
      for(int i = 0; i < size - 1; i++)
      {
         s.append((char)(gen.nextInt(10) + 48));
      }

      return s.toString();
   }//End buildStringNum()
   
   //This method runs the case with numLoops random inputs of size n
   public static void repeatCases(int n)
   {
      String s1, s2, output;
      for(int i = 0; i < NUMLOOPS; i++)
      {
         s1 = buildStringNum(n);
         if(n <= MAXDIVISOR)
            s2 = buildStringNum(n);
         else
            s2 = buildStringNum(MAXDIVISOR);
         output = getSign(s1, s2);
         s1 = stripSign(s1);
         s2 = stripSign(s2);
         output = output + divide(s1, s2);
         System.out.println(output);
      }
   }//End repeatCases()
   
   //This method runs all of the cases
   public static void runCases(int nStart, int nStop, int nMult)
   {
      Scanner kb = new Scanner(System.in);

      for(int n = nStart; n <= nStop; n *= nMult)
      {
         System.out.println("n= " + n);
         repeatCases(n);
         if(n < nStop)
         {
            System.out.println("Enter any letter and press enter to continue " +
               "onto n= " + n * nMult);
            kb.next();
         }
      }

      kb.close();
   }//End runCases()
   
}//End DivideBigInt class
