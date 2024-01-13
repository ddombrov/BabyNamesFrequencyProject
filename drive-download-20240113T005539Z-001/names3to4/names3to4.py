#!/usr/bin/env python3

# Libraries
import os
import sys
import getopt
import csv
import pandas as pd
import math

#main
def main ( argv ):

##COMMAND LINE INPUT SECTION########################################################################################################

    #make sure input not less than 4
    if len(argv) < 6:

        print ( "Usage: python3 names3to4 names3to4.py -f <input file name> -y <input file year> -s <input file sex>" )
        sys.exit(2)

    #check if input is valid
    try:
    
        (opts, args) = getopt.getopt ( argv,"f:y:s:",["inputF=","inputY=","inputS="] )
        
    except getopt.GetoptError:
    
        print ("Usage: python3 names3to4.py -f <input file name> -y <input file year> -s <input file sex>")
        sys.exit(2)

    #start a for loop
    for opt, arg in opts:

        #exit
        if opt == '-h':
            print ( "Usage: python3 names3to4.py -f <input file name> -y <input file year> - s <input file sex>" )
            sys.exit(2)

        #get an file name
        elif opt in ( "-f", "--inputF"):
            inputF = arg

        #get an year
        elif opt in ("-y", "--inputY"):
            inputY = int(arg)

        #get a sex
        elif opt in ("-s", "--inputS"):
            inputS = arg

    outputFileName = inputF
    
    print("Thank you for choosing us to fix your file. 1 moment please.")

##VARIABLE DECLARTION SECTION########################################################################################################
    headers      = ["Name", "Sex", "Rank", "Count", "Year"]
    name         = []
    nameH        = -1
    sex          = []
    sexH         = -1
    rank         = []
    rankH        = -1
    count        = []
    countH       = -1
    year         = []
    yearH        = -1
    tempHeader   = []
    columnMax    = 0

##DETERMINE HEADERS SECTION########################################################################################################
    #open the names file (and close it later)
    with open ( inputF ) as csvDataFile:

        #csvReader will iterate over lines in the file
        csvReader = csv.reader(csvDataFile, delimiter=',')

        columnMax = len(next(csvReader)) # Read first line and count columns
        csvDataFile.seek(0)  

        #start a for loop
        for row in csvReader:

            ##go through the header options
            #for i in range(0,columnMax-1):
            for i in range(0,columnMax):

                #if the row has content
                if row[i] != None and row[i] != "":

                    #read in each header
                    tempHeader=row[i].strip().title()
                
                #based on the content of that header decide what information is stored in the column
                if (tempHeader == "Name" or tempHeader == "Names" or tempHeader == "First Name"):
                    nameH=i
                  #  print("\nnameH: ")
                 #   print(nameH)
            
                if (tempHeader == "Sex" or tempHeader == "Sexes" or tempHeader == "Gender" or tempHeader == "Genders"):
                    sexH=i
                #    print("\nsexH: ")
                #    print(sexH)
            
                if (tempHeader == "Rank" or tempHeader == "Ranks" or tempHeader == "Position" or tempHeader == "Positions"):
                    rankH=i
                 #   print("\nrankH: ")
                 #   print(rankH)
            
                if (tempHeader == "Count" or tempHeader == "Counts" or tempHeader == "Frequency" or tempHeader == "Frequencies" or tempHeader == "Value" or tempHeader == "Values" or tempHeader == "Total" or tempHeader == "Totals" or tempHeader == "Number" or tempHeader == "Numbers"):
                    countH=i
                  #  print("\ncountH: ")
                  #  print(countH)

                if (tempHeader == "Year" or tempHeader == "Years"):
                    yearH=i
                  #  print("\nyearH: ")
                  #  print(yearH)

                #else:
                 #   print("Error because tempHeader is: ")
                 #   print(tempHeader)
                 #   print("An error has occured")
                 #   exit()

#            print("hellllllo")

##DATA COLLECTION SECTION########################################################################################################

            #save the name to an array
            tempName = row[nameH].strip()
            
            if (tempName != "Name" and tempName != "Names" and tempName != "First Name"):
                name.append(tempName)

            #if it's combined, save the sex to an array
            if (inputS == "C"):
            
                tempSex = row[sexH].strip() 
                
                if (tempSex != "Sex" and tempSex != "Sexes" and tempSex != "Gender" and tempSex != "Genders"):    
                    sex.append(tempSex)

            ##if it's all boys or all girls then fill with M or F 
            elif (inputS == "M"):          
                tempSex = "M"
                if (len(sex)<len(name)):
                    sex.append(tempSex)
                
            elif (inputS == "F"):        
                tempSex = "F"
                if (len(sex)<len(name)):
                    sex.append(tempSex)
            
            ##if there were enough names to get a rank
            if (rankH!=-1):
            
                ##not casted to int in case of tie with equals sign
                tempRank = row[rankH]
                
                if (tempRank!=None):
            
                    if (tempRank != "Rank" and tempRank != "Ranks" and tempRank != "Position" and tempRank != "Positions"):
   
                        #save the rank to an array
                        rank.append(tempRank)
                
                else:

                    if len(rank)<len(name):
                        rank.append("-")

            if (countH!=-1):

                tempCount=row[countH]
                
                if (tempCount != "Count" and tempCount != "Counts" and tempCount != "Frequency" and tempCount != "Frequencies" and tempCount != "Value" and tempCount != "Values" and tempCount != "Total" and tempCount != "Totals" and tempCount != "Number" and tempCount != "Numbers"):


                    #save the count to an array
#                    tempCount = int(row[countH])
                    count.append(tempCount)
                        
            else:
                if len(count)<len(name):
                    count.append("-")

            if (yearH!=-1):
            
                tempYear = row[yearH].strip()
                if (tempYear!="Year" and tempYear!="Years"):
                    year.append(tempYear)
            
            else:

                if (len(year)<len(name)):
                    tempYear = inputY
                    year.append(int(inputY))




#    print(name)
    #print(len(name))
 #   print(sex)
    #print(len(sex))
  #  print(rank)
   # print(len(rank))
   # print(count)
  #  print(len(count))
 #   print(year)
#    print(len(year))
   # print(headers)




    if len(name)!=0 :
#            print(name)
#            print(year)
            
            people = {'Year':year,'Sex':sex,'Name':name, 'Count': count}
            people_df = pd.DataFrame(people)

#Year,Sex,Rank,Name,Count
            people_df.sort_values(["Count","Name"], axis = 0, ascending=[False,True], inplace=True)

            rankedPeople_df = people_df.assign(Rank=rank)
            
            print("All done. The file has been fixed. Have a wonderful day.")

            ##print ( rankedPeople_df.head(10) )

            rankedPeople_df.to_csv(outputFileName, sep=',', index=False, encoding='utf-8')
            
    else:
        print("Unfortunatly, your file has no names")





if __name__ == "__main__":
    main ( sys.argv[1:] )

#
#   End of names3to4.py
#
