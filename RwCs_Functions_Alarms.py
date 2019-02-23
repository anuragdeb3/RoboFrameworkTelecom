#!/user/bin/python

import re
import sys
import time
import os
import csv
import itertools
import ast

#***************************************************************************************
# Global values
#***************************************************************************************
Default_path = ""
Executable_path = ""
dir_path = ""
#dir_path = os.getcwd()

bold_red_start = "\033[1;31m"
bold_end = "\033[0m"
bold_green_start = "\033[1;32m"

global csv_columns
csv_columns = ['action', 'operation', 'tag', 'value']
global csv_file
csv_file = 'input.csv'

# *****************************************************************************************************
# Defining a function to take the service trace sent as parameter from RIDE and return it back as LIST.
# Ride doesn't understand List directly when fetching it from file, whole list will be considered as single entity.
# That's why using below function to return it to RIDE as LIST.
# *****************************************************************************************************

def Execute_Clear(ListClear):
    print(ListClear)
    for item in ListClear:
        print(item)
    return ListClear



# *****************************************************************************************************
# Defining a function to set working directory path for access.
# *****************************************************************************************************
def SetPathToFile(path, exe_path):
    # dir_path = path.replace(':\\','://').replace('\\','/')+'/utility/'
    dir_path = path + '\utility\\'

    global Default_path
    Default_path = dir_path

    global Executable_path
    Executable_path = exe_path + '\\'

# *****************************************************************************************************
#Defining af function for fetching a currrent working directory
# *****************************************************************************************************
def fetch_path():
    dir_paths = dir_path.replace(':\\','://').replace('\\','/')+'/'
    return dir_paths



# *****************************************************************************************************
# Compare list of lists
# Can be used to compare any two list of list
# Takes 2 arguments, 1- Data from Trace File, 2- Data given by User
# *****************************************************************************************************
def CmplistOfList(tracedata,userdata):
    result = 0
    for tralst, userlst in itertools.izip(tracedata, userdata):
        print(tralst)
        
        print(userlst)
        
        print("******************")
        for element1, element2 in itertools.izip(tralst, userlst):
            if element1.strip() == element2.strip():
                print("Match ------ Expected : "+str(element2) + "  Actual : "+str(element1))
                print(element1)
                print(element2)
                pass
            else:
                result += 1
                print("Expected : " + str(element2))
                print("Actual : " + str(element1) + "------ Mismatch  ")
    
                
    if result == 0:
       return("Pass")
    else:
       return("Fail")

# *****************************************************************************************************

# Defining a function for converting list to string .(argument - list type)
# *****************************************************************************************************
def listToString(list):
    str = ""
    for line in list:
        str = str + line + "\n"

    return str

        
#*********************************************
# FOR RETURNING Trace name
#*********************************************
def fetch_trace_name():
    TRACE_FILE_NAME = "ccf_sep.119.tra"
    return TRACE_FILE_NAME


#*****************************************************
# FOR Calculating MSISDN length and updating in the LST
#*****************************************************


def update_lst(noa,msisdn):
    print("#################################################################UPDATE MSISDN")
    data = noa + msisdn
    lenpara =len(data)/2
    if lenpara < 10:
       para = '0'+ str(lenpara)
    #print(para+data)
    count = 1
    #print(os.getcwd())
    lststr = ""
    
    with open(Default_path+"output.lst", 'r') as handler:
         line = handler.readline()
         while line:
           if count == 4:
              line = line.replace('\n','')
              line = line + para+data + "\n"
           count+=1
           lststr += line
           line = handler.readline()
    #print"After update"
    #print lststr

    with open(Default_path+"output.lst", 'w') as handler:           
           handler.write(lststr) 
    #print (Default_path)         










# *****************************************************************************************************
#Aim-To capture a 'service.object.name' and their parameters with a value and search in reference file & update that TOC command corresponding to value of
#    a TOC Command read from a file.(for Global commands read from a file)
#Defining a function that matches the expression in file
# *****************************************************************************************************
def global_operation2(ref_filename, to_update_commands_file):  # to_update_commands_file (before updation)
    global Executable_path
    global Default_path
    print("*****************  TOC COMMNANDS  ***********************************************")
    global pattern
    global new_cmnd
    new_cmnd = []
    global param
    final_output_list = []
    ref_found_flg = 0
    to_update_commands_file = to_update_commands_file.replace("\"","")
    with open(Default_path+to_update_commands_file,'r') as update_file:
        update_commands = update_file.readlines()
        print("file Given:")
        print(update_commands)
        if update_commands is not None:
            for i in range(len(update_commands)):
                # new_cmnd.clear()
                del new_cmnd[:]
                ref_found_flg = 0
                pattern_list = update_commands[i].split(',')
                print("Pattern For Toc command :")
                print(pattern_list[0])
                pattern = pattern_list[0]
                for k in range(1, len(pattern_list)):
                    new_cmnd.append(pattern_list[k].replace("\n","").replace(";",""))
                print("Parameter List from User")
                print(new_cmnd)
                print(len(new_cmnd))
                print("#############################################")
                param = new_cmnd

                print("Reading from reference file")
                with open(Default_path+ref_filename, 'r') as f1:
                    counter = 0
                    final_command = ""
                    commands_list = f1.readlines()
                    final_string = ""

                    for line in commands_list:
                        line = line.replace('\n', '')
                        # print(line)
                        if line.startswith(pattern):

                            final_command = final_command + str(pattern) + ","
                            print("      " + final_command)
                            print("      Found match going for splitting on Delimiter ,(Comma) ")
                            print("Got a Matching Toc Command from reference File ")
                            ref_found_flg = 1
                            print("      "+line)
                            ref_cmd_list = line.split(',')
                            ref_list = ref_cmd_list[1:]

                            final_command = ""
                            print("####################### User Given parameter list :\n")
                            print(param)
                            print("####################### Reference List :\n")
                            print(ref_list)
                            ref_dict = {}
                            usr_dict = {}

                            for item in ref_list:
                                itemstr = item.split('=')
                                ref_dict.update({itemstr[0]: itemstr[1]})

                            for element in param:
                                elestr = element.split('=')
                                usr_dict.update({elestr[0]: elestr[1]})

                            print("####################### Dictionary :")
                            print(usr_dict)
                            print(ref_dict)

                            finallst = []
                            print("\n        #######################")

                            for parakey in ref_dict:
                                if parakey in usr_dict:
                                    final_command = str(parakey) + "=" + str(usr_dict[parakey])
                                    finallst.append(final_command)
                                else:
                                    final_command = str(parakey) + "=" + str(ref_dict[parakey]).replace(';', '')

                                    finallst.append(final_command)

                            final_command1 = pattern + ',' + ','.join(finallst) + ';'

                            print("        "+final_command1)
                            final_output_list.append(final_command1)
                            final_command1 = ""

                    if ref_found_flg == 0:
                        print("Couldn't find the Pattern in the Reference File")

    final_file = "Toc_commands_generated.txt"
    with open(Executable_path + final_file, 'w+') as f:
            f.write('\n'.join(final_output_list) + '\n')
            print("COMMANDS GENERATED IN FILE:")
            print('\n'.join(final_output_list) + '\n')
    print("\n")


# *****************************************************************************************************
#Aim-To capture a 'service.object.name' and their parameters with a value and search in reference file & update that TOC command corresponding to value of
#    a TOC Command read from a file.
#Defining a function that matches the expression in file
# *****************************************************************************************************

def operation1(ref_filename,toc_command_list):  #to_update_commands_file (before updation)
    global Executable_path
    print("*****************  TOC COMMNANDS  ***********************************************")
    global pattern
    global new_cmnd
    new_cmnd = []
    global param
    final_output_list = []
    update_commands = toc_command_list
    ref_found_flg = 0
    ints_list = []
    if update_commands is not None:
        for i in range(len(update_commands)):
        #new_cmnd.clear()
            del new_cmnd[:]
            pattern_list = update_commands[i].split(',')
            print("Pattern for toc command :")
            print(pattern_list[0])
            pattern = pattern_list[0]
            for k in range(1,len(pattern_list)):
                new_cmnd.append(pattern_list[k])
            print("Parameter List from User")
            print(new_cmnd)
            print("#############################################")
            param = new_cmnd

            print("Reading from reference file")
            with open(Default_path+ref_filename, 'r') as f1:
                counter = 0
                final_command = ""
                commands_list = f1.readlines()
                final_string = ""

                for line in commands_list:
                    line = line.replace('\n', '')
                    #print(line)
                    if line.startswith(pattern):

                        final_command = final_command + str(pattern) + ","
                        print("      " + final_command)
                        print("      Found match going for splitting on Delimiter ,(Comma) ")
                        print("Got a Matching Toc Command from reference File \n")
                        ref_found_flg = 1
                        print(line)
                        ref_cmd_list = line.split(',')
                        ref_list = ref_cmd_list[1:]

                        final_command = ""
                        print("\n####################### User Given parameter list :")
                        print(param)
                        print("\n####################### Reference List :")
                        print(ref_list)
                        ref_dict = {}
                        usr_dict = {}

                        for item in ref_list:
                            itemstr = item.split('=')
                            ref_dict.update({itemstr[0]:itemstr[1]})


                        for element in param:
                            elestr = element.split('=')
                            usr_dict.update({elestr[0]: elestr[1]})

                        print("\n#######################\n")
                        print(usr_dict)
                        print(ref_dict)

                        finallst = []
                        print("\n#######################\n")

                        for parakey in ref_dict:
                            if parakey in usr_dict:
                                final_command = str(parakey) + "=" + str(usr_dict[parakey])
                                finallst.append(final_command)
                            else:
                                final_command = str(parakey) + "=" + str(ref_dict[parakey]).replace(';','')

                                finallst.append(final_command)
    

                        final_command1 = pattern + ',' + ','.join(finallst) + ';'

                        print(final_command1)
                        final_output_list.append(final_command1)
                        final_command1=""


                if ref_found_flg == 0:
                    print("Couldn't find the Pattern in the Reference File")
########### FOR INTS UPDATE COMMANDS FOR SPECIFIC TABLE #########
            '''temp_ints = pattern.split(".")
            ints_pattern = temp_ints[0]+" "+temp_ints[1]
            #print(ints_pattern)
            if ints_pattern not in ints_list:
                ints_list.append(ints_pattern)
            #print("INTS")
                
    for x in range(len(ints_list)):
        ints_list[x] = "//osp/local/bin/ints psmf " + ints_list[x]
    print("INTS COMMANDS :")
    #print(ints_list)
    with open(Executable_path + "INTS_UPDATE_FILE.sh", 'w+') as ifile: #ints UPDATE FILE CREATION
       ifile.write("#!/bin/sh"+'\n')
       ifile.write('\n'.join(ints_list) + '\n')
       print('\n'.join(ints_list) + '\n')'''


    final_file = "Toc_commands_generated.txt"                # TOC COMMANDS FILE CREATION
    with open(Executable_path + final_file,'w+') as f:
        f.write('\n'.join(final_output_list) + '\n')
        print("COMMANDS GENERATED IN FILE:")
        print('\n'.join(final_output_list) + '\n')
    print("\n")
#***************************************************older  one **************************************************
def operation(ref_filename,toc_command_list):  #to_update_commands_file (before updation)
    global Executable_path
    print("*****************  TOC COMMNANDS  ***********************************************")
    global pattern
    global new_cmnd
    new_cmnd = []
    global param
    final_output_list = []
    global final_string
    final_string = "temprory"
    i = 1
    if i==1:
    #with open(to_update_commands_file,'r') as update_file:
       # update_commands = update_file.readlines()
        update_commands = toc_command_list
        list = []
        for i in range(len(update_commands)):
            #new_cmnd.clear()
            del new_cmnd[:]
            pattern_list = update_commands[i].split(',')
            #print("list 0th value=")
            #print(pattern_list[0])
            pattern = pattern_list[0]
            for k in range(1,len(pattern_list)):
                new_cmnd.append(pattern_list[k])
            #print("nnew parameter list")
            #print(new_cmnd)
            param = new_cmnd



            with open(ref_filename, 'r') as f1:
                counter = 0
                final_command = ""
                commands_list = f1.readlines()
                #print("COMMANDS LIST:")
                #print(commands_list)
                #print("pattern")
                #print(pattern)
                #print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                #print(final_string)
                final_string = ""
                #print("empty" + final_string)

                for line in commands_list:
                    line = line.replace('\n', '')
                    #print(line)
                    if line.startswith(pattern):
                        #print("$$$$$" + final_command)
                        final_command = final_command + str(pattern) + ","
                        #print("$$$$$" + final_command)
                        #print("found match going for splitting on , ")
                        #print(line)
                        list = line.split(',')
                        #print(list[0])
                        #print(list[1])
                        equal_list = []
                        #print("####################### list:::")
                        #print(param)
                        for token in range(len(param)):
                            if '\n' in param[token]:
                                param[token] =param[token].rstrip('\n').replace('\n', '')
                            param_value = param[token].split('=')
                            #print("PPPPPPPPPPPPPPPPPPPPPP")
                            #print(param[token])
                            #print("vvvvvvvvvvvvvvv")
                            #print(param_value[0])
                            #print(param_value[1])
                            #print("going for '='")
                            if token == 0:
                                #print("token first=" + str(token))
                                global flag
                                flag = 0
                                for index in range(1, len(list)):
                                    #print("@@@@@@@@@@@@@@@@@@@")
                                    #print(list[index])
                                    # print(list[index].split("="))
                                    #print("**************************")
                                    equal_list = list[index].split("=")
                                    # yoge=list[index].split("=")
                                    # print("%%%%%%%%%%%%%%%%%%%%%%%")
                                    # print(yoge[0],yoge[1])
                                    #print(equal_list)
                                    #print("first equal para before=")
                                    #print(equal_list[0])
                                    #print("second equal paara before=")
                                    #print(equal_list[1])
                                    if ';' in param_value[1]:
                                        param_value[1] = param_value[1].replace(';','')
                                   # print(param_value[1])
                                    final_command = final_command.rstrip('\n')
                                    if equal_list[0] == param_value[0]:
                                        flag = 1
                                        equal_list[1] = param_value[1]
                                        #print("first equal para =" + equal_list[0])
                                        #print("second equal paara =" + equal_list[1])
                                        final_command += equal_list[0] + '=' + equal_list[1]
                                        #print("final=" + final_command)
                                        # print("x"+x)
                                    else:
                                        if flag == 0:
                                            final_command += equal_list[0] + '=' + equal_list[1]+','
                                        else:
                                            final_command += ',' + equal_list[0] + '=' + equal_list[1]
                                     #   print("final2" + final_command)
                                        # print("y"+y)
                                    #equal_list.clear()
                                    del equal_list[:]
                                    final_strings = final_command.split('\n')
                                    #print("nnnnnnnnLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                                    #print(final_strings)
                                    #print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                                    final_string = final_strings[0].replace('\n','')
                                    #print(final_string)
                                    #print(type(final_string))
                            else:
                                final_command_new = str(pattern) + ","
                                #print("Token second=" + str(token))
                                #print("+++++++++++++")
                                #print(final_string)
                                #print(type(final_string))
                                string = final_string
                                #print("token 2 string:" + string)
                                list2 = string.split(',')
                                #print("LIST 2")
                                #print(list2)
                                for index in range(1, len(list2)-1):
                                    #print("@@@@@@@@@@@@@@@@@@@")
                                    #print(list2[index])
                                    # print(list[index].split("="))
                                    #print("**************************")
                                    equal_list2 = list2[index].split("=")
                                    # yoge=list[index].split("=")
                                    # print("%%%%%%%%%%%%%%%%%%%%%%%")
                                    # print(yoge[0],yoge[1])
                                   # print(equal_list2)
                                    #print("first equal para before=")
                                    #print(equal_list2[0])
                                    #print("second equal paara before=")
                                    #print(equal_list2[1])
                                    # final_command_new = final_command_new.rstrip('\n')
                                    if equal_list2[0] == param_value[0]:
                                        equal_list2[1] = param_value[1]
                                        #print("first equal para =" + equal_list2[0])
                                        #print("second equal paara =" + equal_list2[1])
                                        final_command_new += equal_list2[0] + '=' + equal_list2[1] + ','
                                        #print("final=" + final_command_new)
                                        # print("x"+x)
                                    else:
                                        final_command_new += equal_list2[0] + '=' + equal_list2[1] + ','
                                        #print("final 2=" + final_command_new)
                                        # print("y"+y)
                                    #print("TTTTTTTTTTTTTTTTT")
                                    #print(final_command_new.replace(';,', ';'))
                                    #equal_list2.clear()
                                    #equal_list.clear()
                                    del equal_list[:]
                                    del equal_list2[:]
                                    final_string = final_command_new.replace(';,', ';')
                                    '''final_string = final_command_new.split('\n')
                                    print("^^^^^^^^^^^^")
                                    print(final_string)
                                    equal_list.clear()
                                    #final_string = final_command.split('\n')
                                    print("#################################################")
                                    print(final_string)'''

                        counter += 1
                        # final_string = final_command.split('\n')
                        #print("#######################")
                        #print(final_string)
                        #print("#########################")
                        # url = re.sub('\.;,$', '*****', final_string)
                       # print("/////////////////")
                        final_string = final_string.replace(';,', ';')
                        # print(str(final_string).replace(';,',';'))
                        #print(final_string)
                        #print(type(final_string))
                        #print("//////////////////")
                        final_output_list.append(final_string)

    #print("All commands")
    #print(final_output_list)
    final_file = "Toc_commands_generated.txt"
    with open(Executable_path + final_file,'w+') as f:
        f.write('\n'.join(final_output_list) + '\n')
        print("COOMMANDS GENERATED IN FILE:")
        print('\n'.join(final_output_list) + '\n')
    print("\n")

        #or token in range(len(final_output_list)):
           #f.writelines(final_output_list[token]+"\n")

    '''
                    url = 'abcdc.com'
    if url.endswith('.com'):
        url = url[:-4]

                    """
            print("Total lines founded are :" + str(counter))

            print("done")
        """

                        if list[0]==pattern:
                            for item in range(1,len(list)):
                                temp = p for p in
                                temp = ite
                                if temp[0]==pattern


                        print("read data")
                            print(read_data)
                            # pattern = input("enter the 'service name.object.operation' to be search all matching  commands  in file:" )
                            #pattern = "d2frc.webuser.create"
                            print("pattern to be searched for matching:")
                            print(pattern)
                            print("total lines in read data:" + str(len(read_data)))
                            buffer = []
                            for line in read_data:
                                print("first 1 ")
                                line.replace('\n','************')
                                print(line)
                                #line.replace('\n','**')
                                #line.rstrip('\n')
                                print(line)
                                if line.startswith(pattern):
                                    line.replace(';',',')
                                    line.rstrip('\n')
                                    new_line = line+update
                                    print("UPDATED LINE : "+new_line)
                                    buffer.append(new_line)
                print("Total lines added in buffer:" + str(len(buffer)))
                print("ADDED LINES IN BUFFER:")
                print(buffer)
                with open('y.txt','w+')as y:
                    for final_commnad in buffer:
                        y.write(final_commnad)'''





# *****************************************************************************************************
# For writing list data to CSV File
# *****************************************************************************************************

def Write_List_To_CSV(data_list):
    global Default_path
    print("DEFAULT_PATH :"+Default_path + csv_file)
    with open(Default_path+csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(csv_columns)
        for data in data_list:
            data = str(data)
            data = data.split(',')
            writer.writerow(data)
        #           df = pd.read_csv('C:\\Users\\gur15277\\.spyder-py3\\csv\\Names.csv')
        #          df.to_csv('C:\\Users\\gur15277\\.spyder-py3\\csv\\Names.csv', index=False)

        return




# *****************************************************************************************************
# For creating LST File using XMl & other arguments.
# ****************************************************************************************************
def Create_LST_File(INAP_SI8, serviceRI,ACN):
    global Default_path
    print("value is ", INAP_SI8)
    if "Map_ussd" in INAP_SI8:
        command = 'python ' + Default_path + 'Asn_parser_v0.3_map.py -c ' + Default_path + 'input.csv -i ' + Default_path + '{}.xml -o '.format(INAP_SI8) + Default_path + 'output.xml'
    else:
        command = 'python ' + Default_path + 'Asn_parser_v0.3.py -c ' + Default_path + 'input.csv -i ' + Default_path + '{}.xml -o '.format(INAP_SI8) + Default_path + 'output.xml'
    print("type",type(command) ,command)
    #command = unicodedata.normalize('NFKD', command).encode('ascii','ignore')
    print("After Normalize Type of command:" , type(command),command)
    # command="python3 D:\\Python\\Python37-32\\AsnParser\\Asn_parser_v0.3.py -c C:\\Users\\gur15277\\.spyder-py3\\csv\\input.csv -i D:\\Python\\Python37-32\\AsnParser\\{}.xml -o D:\\Python\\Python37-32\\AsnParser\\output.xml".format(INAP_SI8)
    # os.system('python3 D:\\Python\\Python37-32\\AsnParser\\Asn_parser_v0.3.py -c C:\\Users\\gur15277\\.spyder-py3\\csv\\input.csv -i D:\\Python\\Python37-32\\AsnParser\\SI8.xml -o D:\\Python\\Python37-32\\AsnParser\\output.xml')
    result = os.system(command)
    print("Result=")
    print(result)
    with open(Default_path +'output.lst', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('ACTT 55 ' + '\n')
        f.write('DEST_RT SEP,{} '.format(serviceRI) + '\n')
        f.write('TRP ROUTER' + '\n')
        f.write('TDE DIAL1,{}'.format(ACN) + '\n')
        f.write(content)



# *****************************************************************************************************
# Defining a function to remove the files created on the fly from windows
# *****************************************************************************************************
def Remove_InterGenerated_Files():
    # Default_pathsss = "D:\\FunctionalAuto\\utilities\\"
    # print(Default_pathsss)

    # file not sure to delete = "xml2lst.pl.log"
    global Default_path
    print("Deleting files...")

    delete_files = ["input.csv", "output.xml", "output.lst","xml2lst.pl.log"]
    for file in delete_files:
        #path = os.getcwd() + "\\utility\\"
        path = Default_path
        print(path)
        if os.path.isfile(path + file):
            os.remove(path + file)
            print("File Deleted::= " + path + file)
        else:  ## Show an error ##
            print("Error:''%s''file not found" % file) 





# *****************************************************************************************************
# Defining a function to remove the files created on the fly from windows
# *****************************************************************************************************
def USSDRemove_InterGenerated_Files():
    # Default_pathsss = "D:\\FunctionalAuto\\utilities\\"
    # print(Default_pathsss)

    # file not sure to delete = "xml2lst.pl.log"
    global Default_path
    print("Deleting files...")

    delete_files = ["input.csv", "output.xml", "output.lst","xml2lst_Map.pl.log"]
    for file in delete_files:
        #path = os.getcwd() + "\\utility\\"
        path = Default_path
        print(path)
        if os.path.isfile(path + file):
            os.remove(path + file)
            print("File Deleted::= " + path + file)
        else:  ## Show an error ##
            print("Error:''%s''file not found" % file) 





#**************************************************
# For Verifying Alarms In Trace
#**************************************************

def verify_alarm(tracefile,alarm_test_data):
    print("\n\n******************  ALARMS  ***********************************************\n")
    current_milli_time = lambda: int(round(time.time() * 1000))
    millis = current_milli_time()
    regex = r"\s+(\d{1,2}/\d{1,2}/\d{4})\s(\d{1,2}:\d{1,2}:\d{1,2})\s(\[.*\])(.*)"
    with open(tracefile, 'r') as f:
        txt = f.read()

    match = re.findall(regex, txt, re.M | re.I)
    flag = 0
    alarm = ""
    final_alarms = []
    for i in range(len(match)):
        #print("match:" + str(i))
        t = match[i]
        level_state = re.search(r"LEVEL=(.*)\sSTATE:\s\d*", t[3]).group()

        data = t[3].split(":")
        n = data[2]
        n = n.split(',')
        #print(n[0])
        #print(level_state)

        temp = ""
        for t in data[5:12]:
            temp = temp + " " + t
        #print(temp)
        #alarm = n[0] + "," + level_state + "," + temp # for full comparison
        alarm = n[0]
        print("ALARM:" + alarm)
        final_alarms.append(alarm)
    #print("********")
    #print(type(alarm_test_data))
    print("User Given Alarms:")
    print(alarm_test_data)
    #print(type(final_alarms))
    print("Alarms in Trace:")
    print(final_alarms)
    #print("---------")
    res = 0
    if len(alarm_test_data) == 0 and len(final_alarms) == 0:
        res += 5

    else:
        #print("Going for comparison")
        for item_a in final_alarms:
            for item_b in alarm_test_data:
                if item_b in item_a:
                    print "Alarm Matched :" + str(item_b)
                    res += 1
                else:
                    flag = 99
                    res = 0
                    print "Alarm not Matched: ",item_b

    millis1 = current_milli_time()
    #print("End Time is {}".format(millis1))
    print("Execution time in miliseconds is ::  " + str(millis1 - millis), "Miliseconds")
    #print(res)
    #print("alarm_test_data:"+str(len(alarm_test_data)))
    #print("Final Alarms:" + str(len(final_alarms)))

    if flag == 99:
        return "Fail"
    elif res == 0:
        return "Fail"
    else:
        return "Pass"


# *****************************************************************************************************
# For Fetching message and Verify MAP
# *****************************************************************************************************
def Verify_AccessCode(trace,Expected_Message):
    # This Function is for verify Access Code.
    #Expected_Message = '2 Follow Me deactivated'

    trace_extract = fetchData(trace)
    res =0
    str1 = ": CV_USSDATA ="
    if str1 in trace_extract:
         result1 = trace_extract.index(str1)
         result2 = result1 + 115
         block=trace_extract[result1:result2]
         print ("********************  USSD Message  ***************************")
         #print (block)
         #print ("******************** Block End **************************************")
         block_list = block.split("\n")
         #print (block_list)
         block_list_first = block_list[0].split("=")
         #print (block_list_first)
         print ("MESSAGE IN TRACE (ACTUAL) : ", block_list_first[1])
         print (" MESSAGE BY USER (EXPECTED) : ", Expected_Message)
         if (Expected_Message == block_list_first[1].strip(" ")):
               #print ("************** Testcase  : PASS *****************")
               pass
         else:
               res += 1
               #print ("************** Testcase  : FAIL *****************")

    else:
        res = 100
        print ("MESSAGE NOT FOUND")

    if res == 0:
       print("USSD Message Validation PASSED")
       return "Pass"
    else:
       print("!!!!!! USSD Message Validation FAILED !!!!!")
       return "Fail"

#print ( verify_ussdstring(trace_file))

# *****************************************************************************************************
# For Fetching USSDString and Verify MAP
# *****************************************************************************************************

def Verify_USSDstring(trace,Expected_USSD_string):
    # This Function is for verify USSD string.
    Expected_USSD_string = Expected_USSD_string.lower()
    trace_extract = fetchData(trace)
    res =0
    str1 = "pussr_msg->ussdDataCodingScheme'0f'H"
    #print (str1)

    if str1 in trace_extract:
         result1 = trace_extract.index(str1)
         result2 = result1 + 600
         block=trace_extract[result1:result2]
         print ("******************** USSD String  ***************************")
         #print (block)
         #print ("******************** INAP::Encode Block End **************************************")
         ussd_string_value = re.search(r'ussdString\s(\')(\d*\w*)(\')',block).group().replace("'","").lower().split()
         print( ussd_string_value[0], "IN TRACE (ACTUAL) :" , ussd_string_value[1])
         print("ussdString BY USER (EXPECTED) :" , Expected_USSD_string )
         if (Expected_USSD_string == ussd_string_value[1]):
               #print ("************** Testcase  : PASS *****************")
               pass
         else:
               res += 1
               print ("************** Testcase  : FAIL *****************")

    else:
        print ("USSD STRING NOT FOUND")

    if res == 0:
       print("USSD String Validated PASSED")
       return "Pass"
    else:
       print("!!!!!! USSD String Validation FAILED !!!!!")
       return "Fail"









# *****************************************************************************************************
# For Fetching operation parameters in dictionary
# *****************************************************************************************************
def fetchList(data):
    #print("type of data" + str(type(data)))
    compo_value = data.find(" Component : { -- SEQUENCE --")
    data = data[compo_value:]

    exp = re.compile(r'\s(--)\s(.*)\s(--)')
    parameter = re.compile(r'(\n)\s*(\w*)(\W?)(\w*)\s')
    parameter_value = re.compile(r'(\')(\d*\w*)(\')')

    parameter_dictionary = {}

    #print("*****************************************************")
    #print(re.sub(exp," ",data))
    string_list = (re.sub(exp," ",data)).split(',')
    print("string_list")
    print(string_list)
    for i in range(len(string_list)):
        #print("********************************************************")
        string_list[i].replace('\n',"")
        #print(string_list[i].replace('\n'," "))
        n,v = "",""
        #print((re.search(parameter,string_list[0]).group()).replace('\n',"").strip()) # name
        if re.search(parameter,string_list[i]) is not None:
            n = (re.search(parameter,string_list[i]).group()).replace('\n',"").strip()
            #print(n)
        #print((re.search(parameter_value,string_list[0]).group()).replace('\'','')) #  value
        if re.search(parameter_value,string_list[i]) is not None:
            #print("only if it has value")
            v = (re.search(parameter_value,string_list[i]).group()).replace('\'','')
            #print(v)


        if len(n) == 0:
            continue
        elif len(v) == 0:
            #parameter_dictionary[n] = None
            pass
        else:
            parameter_dictionary[n] = v
        n,v = "",""
        #print("---------------------------------------")
        #print(n)
        #print(v)
    #print(re.sub(exp," ",data))# change --void-- to space
    print(type(parameter_dictionary))
    print("\n****************************************************************")# type of variable

    for key in sorted(parameter_dictionary):
        print(str(key) + " : " + str(parameter_dictionary[key]) + "    ")
    print("******Dictionary End********")
    return parameter_dictionary




# *****************************************************************************************************
# Verify Stat/ CDR Dictionary
# *****************************************************************************************************


def Verify_Statscdr(user_stat,Tracecdrstat,DateDict):   
    print (" CDR/Stats In Trace(Actual):")
    #print(type(Tracecdrstat))
    print (Tracecdrstat, "\n")
    print(" CDR/Stats By User (Expected):")
    #print(type(user_stat))
    print (user_stat, "\n")
    key = 0
    res = 0
    ress = 0
    if len(user_stat) == len(Tracecdrstat):
        for key in user_stat:
            if key in Tracecdrstat:
                  if key in DateDict.keys():
                      frmat = DateDict[key]
                      datelist = re.findall(frmat, Tracecdrstat[key])
                      if not datelist:
                          #print("Invalid Format for Key " + key)
                          print ("Invalid Format " + key +" Expected :" +user_stat[key] + " Actual :"+Tracecdrstat[key])
                          ress = 100  
                      else:
                          #print("Valid Format for Key " + key)
                          print ("Valid Format "+ key + " Expected :" + user_stat[key] + " Actual :" + Tracecdrstat[key])
                  elif user_stat[key].strip() == Tracecdrstat[key].strip():
                      print ("Value matched for "+ key + " Expected :" + user_stat[key] + " Actual :" + Tracecdrstat[key])
                      res = res + 1
                  else:
                      print ("Value not matched for " + key +" Expected :" +user_stat[key] + " Actual :"+Tracecdrstat[key])
                      print ("Tag/Event Value failed")
                      ress = 100   

    else :
         ress = 100
         print("Testcase FAIL : !!!!! Number of Tags/Events are Different")
         print("Expected (User Given) Length : ", str(len(user_stat)))
         print("Actual (In Trace) Length : " + str(len(Tracecdrstat)))

        #print(ress)
    if ress == 100:
         print("Testcase FAIL : !!!!! Value not matched for Some Tag/Event  !!!!!")
         return "Fail"
    else:
         print("Testcase PASS : !!!!! All Values matched!!!!! ")
         return "Pass"
            

# *****************************************************************************************************
# For Comparing Dictionary
# **********************************dict*******************************************************************

def compDict(userpara,tracepara):
    print("                  ACTUAL         ->      EXPECTED/USER")
    for key in userpara:
        if tracepara[key] != tracepara[key]:
            print("Difference for "+str(key)+":"+str(tracepara[key])+"->"+str(userpara[key]))
            result = 100
        else:
            print("Match for"+str(key)+":", str(tracepara[key])+ "->"+str(userpara[key]))

#******************************************************************************************************
# For validating the operation parameters.(using Dictionary)
#******************************************************************************************************
def validatePara(tracepara, userpara):
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    UserParaDict = {}
    print(len(userpara))
    print(str(userpara))

    stralm = str(userpara).replace("[u'", "").replace("']", "")
    strlst = stralm.split(",")
    for item in strlst:
        dictstr = item.split("=")
        UserParaDict.update({dictstr[0].strip(): dictstr[1].strip()})

    print("#####################################\nFinal Expected Data in Format for Parameters")
    print(UserParaDict)


    print("################################################################")
    print("Trace data")
    print(tracepara)


    print("########################Compare#############################")
    result = 0
    tmpdict = {}
#######################################################################
#Added to handle extra parameters in Operation

    for key in tracepara:
        if key in UserParaDict: 
            if tracepara[key] != UserParaDict[key]:
                print("Difference for "+str(key)+":"+str(tracepara[key])+"->"+str(UserParaDict[key]))
                result = 100
            elif tracepara[key] == UserParaDict[key]:
                print("Match for "+str(key)+":"+str(tracepara[key])+"->"+str(UserParaDict[key]))
        else:
            tmpdict[key] = tracepara[key] 
        
    if len(tmpdict) > 0:
        print("Extra Parameters from Traces")
        for item in tmpdict:
            print(str(item)+ "=" + str(tmpdict[item]))         
            
        

    if result == 0:
        return ("Pass")
    else:
        return ("Fail")





# *****************************************************************************************************
# Fetch OPERATION PARAMETERS
# *****************************************************************************************************


def fetchOPpara(trace,userpara):
    opera = ""
    data = fetchData(trace)
    datalist = data.split("\n")

    for ln in range(0, len(datalist), 1):
        
        # ************************************************Connect Operation*************************
        if "->  14   " in datalist[ln]:
            print("Line Number: " + str(ln))

            opera = datalist[ln - 50:ln]
            TraceDict = fetchList(listToString(opera))
            print(TraceDict)
            result = validatePara(TraceDict, userpara)

            if result == "Pass":
                return "Pass"
            else:
                return "Fail"


        # ***********************************************Service Release Operation**********************

        elif "->  16   " in datalist[ln]:
            print("Got 16")
            opera = datalist[ln - 130:ln]

            for line in opera[::-1]:
                if "context.release_cause" in line:
                    result_code = str(line).split("=")[1].strip()
                    print("Release Cause is :" + result_code)
                    TraceDict = {"release_cause" : result_code}
                    break


            result = validatePara(TraceDict, userpara)

            if result == "Pass":
                return "Pass"
            else:
                return "Fail"

        # ***********************************************3E Operation*******************************
        elif "->  3E   " in datalist[ln]:
            print("Line Number: " + str(ln))

            opera = datalist[ln - 50:ln]
            fetchList(listToString(opera))




#*************************************************************************************************
# Extract the operation code from trace & validate it for the given set of operation codes
#*************************************************************************************************
def Extract_Op_Code(trace,oplist):
    print("\n\n******************  OPERATION CODE   ***********************************************\n")
    res = 0
    print("OPERATION CODE BY USER(Expected) :")
    print(oplist) 
    opcode_list = []
    with open(trace, "r") as ifile:
        for line in ifile:
            if line.startswith("OPERATION :"):
                tmp =next(ifile, '').strip().split("->")
                opcode_list.append(tmp[1].replace(".","").replace(";","").replace("<","").replace(">","").strip())
    print("OPERATION CODE IN TRACE(Actual):")
    print(opcode_list)  

#******************* comparison of OP Codes ******************************
    if oplist is not None:
        if len(oplist) != len(opcode_list):
            res = 1
            print("NUMBER OF OPERATION CODES ARE DIFFRENT IN TRACE FILE FOR GIVEN DATA!!!! ")
        else:
            for index in range(len(opcode_list)):
                if oplist[index] ==  opcode_list[index]:
                    pass
                else:
                    print("OPERATION CODE NOT MATCHED: "+opcode_list[index])
                    res = 2
        if res == 0:
            print("SEQUENCE OF OPERATION CODE MATCHED")
            return "Pass"
        else:
            print("FAILED !!!!!")
            return "Fail"
        

#





#****************************************************************************************************
# For extracting/fetching stats & cdr from trace.
#****************************************************************************************************
def fetchStatCdr(trace, user_stat, DateDict):
    
    #trace_extract = fetchData(trace)
    print("*****************************STAT & CDR*********************")

    # Realizing the tags to be skipped.






    handle = open(trace, 'r')
    trace_extract = handle.read()
    #print(type(trace_extract))
    count = 0
    start = 0
    end = 0
    starttag = 'Tag:'
    endtag = 'Dump:'
    startEvent = 'Event:'
    endEvent = ' Value:'

    cdrstatDic = {}


    Ticket_Count = trace_extract.count("* Stat_ticket **")  # Searching the pattern for tickets and counting for multiple occurences
    print("Ticket Count =" + str(Ticket_Count))
    if "\n" in trace_extract:
        dataticket = trace_extract.split("\n")
    else:
        dataticket = trace_extract

    #print(len(dataticket))
    #print(type(dataticket))
    
    for i in range(0, len(dataticket) - 1):  # Fetching the last occurence of stat Ticket
        if "* Stat_ticket **" in dataticket[i]:
            count += 1
            if count == Ticket_Count:
                start = i
                for j in range(start, len(dataticket) - 1):
                    if "Entry" in dataticket[j]:
                        end = j
                        break

    cdrstatextract = dataticket[start:end]  # CDR Stats Extract
    #print (type(cdrstatextract))
    for index in cdrstatextract:
        print(index)
    print("******************")
    for item in cdrstatextract:
        if "Tag" in item:
            cdrstatDic.update({(item.split(starttag))[1].split(endtag)[0].strip(): item.split(endtag)[1].strip()})  # Enable for Dictionary

        if "Event" in item:
            if "Dump: stat separator" in item:
                pass
            else:
                cdrstatDic.update({(item.split(startEvent))[1].split(endEvent)[0].strip(): item.split(endEvent)[1].strip() })  # Enable for Dictionary

    cdrstatDic

    print("**************Stats & CDR***********************************************")
    if user_stat is not None:
        result = Verify_Statscdr(user_stat, cdrstatDic, DateDict)
        #print(result)
        if result == "Pass":
            return "Pass"
        else :
            return "Fail"     


#*****************************************************************************************************
# For validating Alarms
#*****************************************************************************************************
def validateAlarm(alarmlist, useralarmData):
    if len(alarmlist) == len(useralarmData):
        print("*************************Alarms Comparison*****************")
        return(CmplistOfList(alarmlist,useralarmData))
        

    else :
        print("Difference in Expected and Actual !!!")
        print("Expected Alarms")
        print(useralarmData)
        print("Actual Alarms")
        print(alarmlist)
        return("Fail")
                                                                           
# **********************************************************************************************************

# User format should be [['Description', 'Type', 'Level', 'State', 'Dump']'['Description', 'Type', 'Level', 'State', 'Dump']]
def fetchAlarm1(tracedata, useralarm):
    print("%%%%%%%%%%%%%%%%Alarms%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    
    #print(useralarm)
    # print(len(useralarm))
    UserAlmDict = {}
    UserArlmLst = []
    #print("LENGTH OF USER ALARM")
    #print(len(useralarm))
    #print(useralarm)
    
    if str(useralarm).replace("[u'", "").replace("']", "") != "NA":
        for count in range(0, len(useralarm)):
            #print(useralarm[count])
            stralm = str(useralarm[count]).replace("[u'", "").replace("']", "")
            strlst = stralm.split(",")
            for item in strlst:
                dictstr = item.split("=")
                UserAlmDict.update({dictstr[0].strip(): dictstr[1].strip()})
            UserArlmLst.append(UserAlmDict)
            UserAlmDict = {}

        print("##################################### \nUser Alarms in Expected Data Format:")
        print(UserArlmLst)
    else:
        print("Expected Alarms is Empty")    

    print("################################################################")
    # print("Trace data")
    handler = open(tracedata, 'r')

    printline = False

    DictDump = {}
    ListAlarm = []

    for alarmline in handler.readlines():
        #print alarmline
        # printline = '*=*=' in alarmline
        if printline:
            print("Alarm from Trace : " + str(alarmline))
            alarmline = alarmline.split(",")
            DictDump.update({'Desc': (alarmline[0].split(":")[-1].strip())})
            # print('Desc='+(alarmline[0].split(":")[-1].strip()))
            DictDump.update({'Type': (alarmline[1].replace("TYPE=", "").strip())})
            # print(alarmline[1])
            DictDump.update({'Level': (alarmline[2].replace("LEVEL=", "").strip())})
            # print(alarmline[2])
            DictDump.update({'State': (alarmline[3].replace("STATE:", "").replace("(Script main", "").strip())})
            # print(alarmline[3])
            if ")(" in alarmline[-1].replace("DUMP:", ""):
                tempDumpDict = (alarmline[-1].replace("DUMP:", "").strip()).split(")(")
                lentemp = len(tempDumpDict) - 1
                count = 0
    
    
                for item in tempDumpDict:
                    if count == lentemp:
                        itemlast = item.split(')')
                        item = itemlast[0].split(':')
                        t = item[-1].split('=')
                        # print(t[0].strip().replace('(', '').replace(')', ''))
                        DictDump.update({t[0].strip().replace('(', '').replace(')', ''): t[1].strip().replace('(', '').replace(')', '')})
                        if len(itemlast[1]) > 0:
                            print("Last Item :" + str(itemlast[1]))
                    else:
                        item = item.split(':')
                        t = item[-1].split('=')
                        # print(t[0].strip().replace('(', '').replace(')', ''))
                        DictDump.update(
                            {t[0].strip().replace('(', '').replace(')', ''): t[1].strip().replace('(', '').replace(')', '')})
                    count += 1
            else:
                print(alarmline[-1].replace("DUMP:", ""))
    
    
    
    
    
            # print ("*************Alarms************************************************")
            # print(type(DictDump))
            print("Actual Alarm")
            print(DictDump)
            ListAlarm.append(DictDump)
            DictDump = {}
            # print(type(ListAlarm))
            # print(ListAlarm)
    
        else:
            pass
    
            # print("in else")
    
        # print("alarm line  "+str(alarmline))
        printline = '*=*=' in alarmline

    # print(ListAlarm)

    print("########################Compare#############################")
    result = 0
    
    if len(ListAlarm) == len(UserArlmLst):

        for tralst, userlst in itertools.izip(ListAlarm, UserArlmLst):
            # print(tralst)
            # print(userlst)
            print("************************************")
            print("              ACTUAL ->  EXPECTED  ")
            for key in userlst:
                if tralst[key] != userlst[key]:
                    print("Difference for "+str(key)+":"+str(tralst[key])+"->"+str(userlst[key]))
                    result = 100
                else:
                    print("Match for "+str(key)+":"+str(tralst[key])+"->"+str(userlst[key]))

    else:
        print("Difference in Length of Actual & Expected")
        print("Actual Alarm from Traces")
        print(ListAlarm)
        print("Expected Alarms")
        print(UserArlmLst)
        result = 100
    
    if result == 0:
        return "Pass"
    else:
        return "Fail"


#**********************************************************************************

def fetchData(trace):
    # Below solution will reduce the need of opening and reading a file again and again
    # We will be reading the file once and then store it into a String varible

    handle = open(trace, 'r')
    data = handle.read()

    handle.close()
    return(data)
    #fetchOPpara(data)
    #fetchStatCdr(data)

#*********************************************************************************************************************


'''
# start point to
if __name__=="__main__":
	#fetch_path()
    toc_list = ['ccf_p6.access_matrix.create,AM_MN="access_matrix1",DUMMY07="1",FN_MSID_F1="2",MSID1="123456789";','ccf_p6.rel_cs_ann.modify,REL1="12";']
    operation('D:\FunctionalAuto\Demo_RwCs_1\utility\\rwcs_cmnd_reference.txt',toc_list)
'''

