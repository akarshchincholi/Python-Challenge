import urllib.request                         # Basic HTTP simplifying module to open URLs           
from urllib.request import urlopen
import urllib.parse
import re                                     # re means Regular Expressions which is used for data manipulation in the HTML source code
import sqlite3                                # After collecting results of GEO IP lookups we store results in database table





'''  This module is used for GEO Ip lookup for a particular IP and fetch results such as Country, State, City, Zip Code '''

def GeoIP_Lookup(IP):

    url = 'http://ipinfodb.com/ip_locator.php'   #Chosen this website as it offers free GEO IP lookups 

    try:
        values = {'ip':IP, 'search':'GO'}        #The parameters needed to be passed to execute search in the website, the source code shows the parameters
        data = urllib.parse.urlencode(values)    #This is usually done to add %20 which is urlencoding for a 'space'
        data = data.encode('utf-8')              
        req = urllib.request.Request(url,data)   
        resp = urllib.request.urlopen(req)       #Fetching the source code in the given url with with our parameters as input
        respData = resp.read()
        #print (respData)

    except Exception as e:                       # Any sort of error is displayed in this code
        print (str(e))

    IP_Address = re.findall(r'IP address : <strong>(.*?)</strong>', str(respData))   # After analyzing the source code of results for several IPs we can see that the the
    Country = re.findall(r'Country :(.*?)<img', str(respData))                       # information we need always appears to be in between some patterns of characters
    State_Province = re.findall(r'State/Province :(.*?)</li>', str(respData))        # So we use Regular Expressions to fetch our required data from the massive data in source code
    City = re.findall(r'City :(.*?)</li>', str(respData))
    Zip_Code = re.findall(r'Zip or postal code :(.*?)</li>', str(respData))
    
    return (IP_Address, Country, State_Province, City, Zip_Code)                     # Return the required results







def create_table():                                                                                                     # We create a table to store our Data 
    conn = sqlite3.connect('Python.db')
    c = conn.cursor() # Cursor
    c.execute('CREATE TABLE IF NOT EXISTS GeoPlot_DB(IP TEXT, Country TEXT, State TEXT, City TEXT, Zip TEXT)')          # The table contains 5 columns - IP, Country, State, City, Zip



def data_entry(A1, A2, A3, A4, A5):                                                         # Data Entry in done in this module based on the result obtained from the source code 
    conn = sqlite3.connect('Python.db')
    c = conn.cursor() # Cursor
    c.execute ("""INSERT INTO GeoPlot_DB VALUES(?, ?, ?, ?, ?)""", [A1, A2, A3, A4, A5])
    conn.commit()
    c.close()
    conn.close()




def Enter_Full_Data(List_Of_IPS):                                                           # Iterates over the list of extracted IPs and collects GEO Ip lookup results and stores in databaase

    for i in range (0,len(List_Of_IPS)):                                                  
        IP_DB, Country_DB, State_DB, City_DB, Zip_DB = GeoIP_Lookup(List_Of_IPS[i])
        
        IP_DB = IP_DB[0]
        Country_DB = Country_DB[0]
        State_DB = State_DB[0]
        City_DB = City_DB[0]
        Zip_DB = Zip_DB[0]

        create_table()
        
        data_entry(IP_DB, Country_DB, State_DB, City_DB, Zip_DB)





''' This module is used to generate our custom Database Query and fetch the results based on the INPUTS given '''    

def Filter_From_DB(COUNTRY, STATE, CITY):

    if (COUNTRY != 'NO'):                                                   # We convert the raw input given by the user to the format in which we have stored in the databse
        COUNTRY = COUNTRY[:0] + ' ' + COUNTRY[0:] + ' '                     # Country is of the format ' XX '
                                                                            # State and City are of the format ' XXXX'     
    if (STATE != 'NO'):
        STATE = STATE[:0] + ' ' + STATE[0:]                                 # We are implying that we need to include appropriate spacing so that the filter matches the format in database    

    if (CITY != 'NO'):
        CITY = CITY[:0] + ' ' + CITY[0:]


    if (COUNTRY != 'NO') and (STATE != 'NO') and (CITY != 'NO'):            # Depending on which of the attributes we want to search, the following are the conditions and QUERY statements we build       
        c.execute("""SELECT * FROM GeoPlot_DB WHERE Country = (?) AND State = (?) AND City = (?)""", [COUNTRY, STATE, CITY])
        Count = 0
        for row in c.fetchall():
            print (row)
            Count = Count + 1
        print ("The number of Entries with given filters are: ", Count)
        print ('\n')

    if (COUNTRY != 'NO' and STATE != 'NO' and CITY == 'NO'):
        c.execute("""SELECT * FROM GeoPlot_DB WHERE Country = (?) AND State = (?)""", [COUNTRY, STATE])
        Count = 0
        for row in c.fetchall():
            print (row)
            Count = Count + 1
        print ("The number of Entries with given filters are: ", Count)
        print ('\n')
    
    if (COUNTRY != 'NO' and STATE == 'NO' and CITY != 'NO'):
        c.execute("""SELECT * FROM GeoPlot_DB WHERE Country = (?) AND City = (?)""", [COUNTRY, CITY])
        Count = 0
        for row in c.fetchall():
            print (row)    
            Count = Count + 1
        print ("The number of Entries with given filters are: ", Count)
        print ('\n')
        
    if (COUNTRY == 'NO' and STATE != 'NO' and CITY != 'NO'):
        c.execute("""SELECT * FROM GeoPlot_DB WHERE State = (?) AND City = (?)""", [STATE, CITY])
        Count = 0
        for row in c.fetchall():
            print (row)
            Count = Count + 1
        print ("The number of Entries with given filters are: ", Count)
        print ('\n')

    if (COUNTRY != 'NO' and STATE == 'NO' and CITY == 'NO'):
        c.execute("""SELECT * FROM GeoPlot_DB WHERE Country = (?) """, [COUNTRY])
        Count = 0
        for row in c.fetchall():
            print (row)
            Count = Count + 1
        print ("The number of Entries with given filters are: ", Count)
        print ('\n')
            

    if (COUNTRY == 'NO' and STATE != 'NO' and CITY == 'NO'):
        c.execute("""SELECT * FROM GeoPlot_DB WHERE State = (?) """, [STATE])
        Count = 0
        for row in c.fetchall():
            print (row)
            Count = Count + 1
        print ("The number of Entries with given filters are: ", Count)
        print ('\n')

    if (COUNTRY == 'NO' and STATE == 'NO' and CITY != 'NO'):
        c.execute("""SELECT * FROM GeoPlot_DB WHERE City = (?) """, [CITY])
        Count = 0
        for row in c.fetchall():
            print (row)
            Count = Count + 1
        print ("The number of Entries with given filters are: ", Count)
        print ('\n')






            


if __name__ == "__main__":
    
    List_Of_IPS = []                                                                    # Initialize at array to store all the extracted IPs from the unstrictured junk file                            
    with open('C:\\Users\\akars\\Desktop\\Python_Question\\List.txt') as F:             # Give the correction path to the File we want to extract IPs from
        for line in F:                                                                  # We parse the entire file, line by line and word by word
            for part in line.split():
                
                try:
                    a, b, c, d = part.split('.')                                        # Since we know that IPS are of the format  xxx.xxx.xxx.xxx
                    IP = (a+'.'+b+'.'+c+'.'+d)
                    if (IP[-1] == ','):                                                 # Handling unique cases which occur at end of every paragrahph in the file
                        IP = IP[:-1]
                    List_Of_IPS.append(IP)                                              # Append this extracted IP to the LIST
                    
                except ValueError:                                                      # Error detection
                    pass # not in the right format
                else:
                    pass
                    

    
    print (len(List_Of_IPS))                                                            # Print the size of the final list of extracted IPS from the FILE

    
    conn = sqlite3.connect('Python.db')
    c = conn.cursor()                                                                   # Cursor
    create_table()

    c.execute("SELECT * FROM GeoPlot_DB")                                               # we check if the database already has entries or not 
    Results = c.fetchall()
    Length = len(Results)
    print (Length)

    if (Length == 0):
        Enter_Full_Data(List_Of_IPS)

    elif (Length > 0):
        print ("Data Already Exists")
    
    


    S = True
    while (S):                                                                              # A loop is Started to continuously take inputs from the user and filter from the database

        Search = input ("Please type YES if you want to continue search or else type NO : ") # A YES/NO input is asked to continue search or not

        if (Search == 'YES'):
            Country = input("Enter The Country in two characters in UPPER Case or say NO : ")          # Our Custom Query language is defined in this section 
            State   = input("Enter the State with the first character in UPPER Case or say NO : ")     # We have an option to either give the input or enter NO to say that we dont want to search that attribute
            City    = input("Enter the City with the first character in UPPER Case or say NO : ")
            Filter_From_DB(Country, State, City)
            continue

        if (Search != 'YES') and (Search != 'NO'):
            print ("You have entered an invalid OPTION TYPE, please try again")
            continue

        if (Search == 'NO'):                                                                # If NO is entered, then the while loop exits and the program ends
            print ("You have chose to stop searching so the program ends here")
            S = False
             
        
        





