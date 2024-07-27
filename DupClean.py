#######################################################################################################
#   Import Statement :  
#######################################################################################################
import os
import sys
import time
import hashlib

#######################################################################################################
#   Function Name   :   Delete_File
#   Input           :   FileName
#   Output          :   HexaDigit
#   Description     :   Delete duplicate file
#   Author          :   Rushikesh Hemant Gholap
#   Date/Time       :   11/05/2024
#######################################################################################################
def Delete_File(Dict1):

    Results = list(filter(lambda x : len(x) >1 ,Dict1.values()))
    
    Cnt = 0

    if len(Results) > 0:
        for Result in Results:     
            for SubResult in Result:         
                Cnt = Cnt + 1
                if Cnt >= 2:
                    os.remove(SubResult)
            Cnt = 0
    else:
        print("No duplicate file found")

#######################################################################################################
#   Function Name   :   Calculate_CheckSum
#   Input           :   FileName
#   Output          :   HexaDigit
#   Description     :   Find check sum of file
#   Author          :   Rushikesh Hemant Gholap
#   Date/Time       :   11/05/2024
#######################################################################################################
def Calculate_CheckSum(Path, Blocksize=1024):

    Open_File = open(Path, 'rb')

    Read_File = Open_File.read(Blocksize)

    MD5 = hashlib.md5()

    while len(Read_File) > 0:
        MD5.update(Read_File)
        Read_File = Open_File.read(Blocksize)

    Open_File.close()

    return MD5.hexdigest()

#######################################################################################################
#   Function Name   :   DirectoryWatcher
#   Input           :   Connamd Line Argument
#   Output          :   In Log File
#   Description     :   Copy all files from first directory into second directory
#   Author          :   Rushikesh Hemant Gholap
#   Date/Time       :   11/05/2024
#######################################################################################################
def DirectoryWatcher(DirName):

    Flag = os.path.isabs(DirName)

    if (Flag == False):

        DirName = os.path.abspath(DirName)

    Exist = os.path.isdir(DirName)

    if (Exist == True):

        print("Directory is exits.....!")

        Duplicate = {}
         
        for FolderName, SubFolderName, FileName in os.walk(DirName):
            for Name in FileName:
                Path = os.path.join(DirName, Name)
                HashFile = Calculate_CheckSum(Path)

                # Find Duplicate
                if HashFile in Duplicate:
                    Duplicate[HashFile].append(Path)
                     
                else:
                    Duplicate[HashFile] = [Path]
        
        return Duplicate
                  
    else:
        
        print("Directory does not exits")
        
#######################################################################################################
#   Function Name   :   Print_Result
#   Input           :   Directoty
#   Output          :   In Log File
#   Description     :   Print result
#   Author          :   Rushikesh Hemant Gholap
#   Date/Time       :   11/05/2024
#######################################################################################################
def Print_Result(Dict1):
    
    Results = list(filter(lambda x : len(x) >1 ,Dict1.values()))
    
    if len(Results) > 0:
  
        print("Duplicate Found ")
        print("The following files are duplicate")
        for Result in Results:
            for SubResult in Result:
                print('%s'% SubResult)
                
    else:
        print("No duplicate found")


#######################################################################################################
#   Entery Point Function
#######################################################################################################
def main():

    print("------------------------------ Directory Watcher ------------------------------")

    if (len(sys.argv) == 2):

        if ((sys.argv[1] == "--h") or (sys.argv[1] == "--H")):
            print("This script is used to perform Directory traversal")
            exit()

        if ((sys.argv[1] == "--u") or (sys.argv[1] == "--U")):
            print("Usage of the script : ")
            print("Name_Of_File  Name_Of_Directory  Name_Of_Directory  File_extension")
            exit()

        try:
            
            Arr = {}
            Starttime = time.time()
            Arr = DirectoryWatcher(sys.argv[1])
            Print_Result(Arr)
            Delete_File(Arr)
            Endtime = time.time()
            print("Time required to execute the script is : ", Starttime - Endtime)

        except Exception as Obj:
            print("Exception for : ", Obj)

    else:
        print("Invalid input")
        print("Use --h option to get the help and use --u option to get the usage of application")
        exit()

    print("------------------------------ Directory Watcher ------------------------------")

    return 0

#######################################################################################################
#   Starter
#######################################################################################################
if __name__ == "__main__":
    main()

