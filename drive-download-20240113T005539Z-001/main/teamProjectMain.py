import pandas as pd
from subprocess import call
from ethnicolr import census_ln
import matplotlib.pyplot as plt
import csv

#dataframes that hold the data of california and australia
californiaDf = pd.read_csv('California 1960-2021 M.csv', delimiter=',', encoding='latin1')
australiaDf = pd.read_csv('Australia 1952-2021 M.csv', delimiter=',', encoding='latin1')
scotland2019FDf = pd.read_csv('Scotland2019F.csv', delimiter=',', encoding='latin1')
scotland2019MDf = pd.read_csv('Scotland2019M.csv', delimiter=',', encoding='latin1')
Newfoundland2003FDf = pd.read_csv('Newfoundland2003F.csv', delimiter=',', encoding='latin1')
Newfoundland2003MDf = pd.read_csv('Newfoundland2003M.csv', delimiter=',', encoding='latin1')


def headerChange(data):

  for header in data.columns:
    NHeader = header
    if (header.title() == "Gender" or header.title() == "Genders" or header.title() == "Sexes"):
      NHeader = "Sex"
    if (header.title() == "First Name" or header.title() == "Names" or header.title() == "Names"):
      NHeader = "Name"
    if (header.title() == "Frequency" or header.title() == "Count" or header.title() == "Frequencies" or header.title() == "Value" or header.title() == "Counts" or header.title() == "Total" or header.title() == "Totals" or header.title() == "Number" or header.title() == "Numbers"):
      NHeader = "Count"
    if (header.title() == "Position" or header.title() == "Positions" or header.title() == "Ranks"):
      NHeader = "Rank"
    if (header.title() == "Years"):
      NHeader = "Year"

    data = data.rename(columns = {header: NHeader})

  cols = ["Year", "Sex", "Rank", "Name", "Count"]
  data = data.reindex(columns = cols)
  data.sort_values("Year", ascending = True)
  return data

def topNames(year, filename):
    # Load data from file
    df = pd.read_csv(filename)

    # Filter by year
    df = df[df['Year'] == year]

    # Group by name and sum the counts
    name_counts = df.groupby('Name')['Count'].sum()

    # Sort by count in descending order and get top 10
    topNames = name_counts.sort_values(ascending=False)[:10]

    # Print the top 10 names
    print(topNames.to_string())

def searchCalifornia():
    # Get user input for the search term
    search_term = input("Enter search term: ")

    # Filter the California dataframe based on the search term
    filtered_df = californiaDf.loc[californiaDf['Name'].str.contains(search_term, case=False)]

    # Print the filtered dataframe
    print(filtered_df.to_string(index=False))

def search_australia():
    # Get user input for the search term
    search_term = input("Enter search term: ")

    # Filter the California dataframe based on the search term
    filtered_df = australiaDf.loc[australiaDf['Name'].str.contains(search_term, case=False)]

    # Print the filtered dataframe
    print(filtered_df.to_string(index=False))

#names for the files
df2 = australiaDf[['Name']].copy()
#print(df2.to_string(index=False))

#if user searches for 'top 10 australia names' print out the top 10 names of df2

df3 = californiaDf[['Name']].copy()
#print(df3.to_string(index=False))

def searchCaliforniaGraph():
    # Get user input for the search term
    search_term = input("Enter search term: ")

    # Filter the California dataframe based on the search term
    filtered_df = californiaDf.loc[californiaDf['Name'].str.contains(search_term, case=False)]

    # Print the filtered dataframe
    print(filtered_df.to_string(index=False))

    # Plot the frequency of the name over the years
    filtered_df.groupby('Year')['Count'].sum().plot(kind='line')
    plt.title(f"Frequency of {search_term} in California")
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.show()

def SearchAustraliaGraph():
    # Get user input for the search term
    search_term = input("Enter search term: ")

    # Filter the Australia dataframe based on the search term
    filtered_df = australiaDf.loc[australiaDf['Name'].str.contains(search_term, case=False)]

    # Print the filtered dataframe
    print(filtered_df.to_string(index=False))

    # Plot the frequency of the name over the years
    filtered_df.groupby('Year')['Count'].sum().plot(kind='line')
    plt.title(f"Frequency of {search_term} in Australia")
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.show()

def alphabetNames(filename):
    df = pd.read_csv(filename)

    topNames = df.sort_values(["Name"], ascending=[True])

    print(topNames.to_string())


def processFile():
    while True:
        file_path = input('Enter the name of the file: ')
        try:
            df = pd.read_csv(file_path, header=None, usecols=[0, 1, 2, 3, 4], names=["Year", "Sex", "Rank", "Name", "Count"])
            break
        except FileNotFoundError:
            print('Invalid file name entered. Please enter a valid file name.')
    
    while True:
        yearInput = input('Enter the year (either 2000 or 2010): ')
        if yearInput not in ['2000', '2010']:
            print('Invalid year entered. Please enter either 2000 or 2010.')
        else:
            year = int(yearInput)
            break
    
    census_ln(df, 'Name')

    call(["census_ln", "-y", str(year), "-o", "output-census" + str(year) + ".csv", "-l", "3", file_path])

    # read the output file and print its contents
    df_output = pd.read_csv('output-census' + str(year) + '.csv', skiprows=[1])
    
    df_output = df_output.dropna()
    
    return df_output.to_string(index=False, float_format='%.2f')


def printCsv(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            print(row)

def menu():
    while True:
        print("1. Track ethnicity")
        print("2. Search for keywords in the files")
        print("3. Search for the top 10 in any given year in any location")
        print("4. Print graphs based off name data")
        print("5. Print out the names alphabetically")
        print("6. Print out the data")
        print("7. Exit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("The headers stand for pctwhite (percent white), pctblack(percent black), pctapi (percentage chance asian), pctaian, (percentage American Indian and Alaskan Native), pct2prace (Percentage 2+ races), pcthispanic (percentage hispanic)")
            processFileOutput = processFile()
            print(processFileOutput)
        elif choice == '2':
            location_choice = input("Would you like to search through California or Australia? ")
            if location_choice.lower() == 'california':
                searchCalifornia()
            elif location_choice.lower() == 'australia':
                search_australia()
            else:
                print("Invalid location. Please enter 'California' or 'Australia'.")
        elif choice == "3":
            filename = input("Enter filename: ")
            year = int(input("Enter year: "))
            topNames(year, filename)
        elif choice == "4":
            location_choice = input("Would you like to search through California or Australia? ")
            if location_choice.lower() == 'california':
                searchCaliforniaGraph()
            elif location_choice.lower() == 'australia':
                SearchAustraliaGraph()
            else:
                print("Invalid location. Please enter 'California' or 'Australia'.")
        elif choice == "5":
            alphaFilename = input("Enter filename: ")
            sorted_names = alphabetNames(alphaFilename)
            print(sorted_names)
        elif choice == "6":
            printCsvFilename = input("Enter filename: ")
            printCsv(printCsvFilename)
        elif choice == "7":
            break
        else:
            print("Invalid choice!")

menu()