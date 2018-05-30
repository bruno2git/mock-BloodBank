#-*- coding: utf-8 -*-

from Donor import *
from Donation import *
from os import stat, remove, rename, path
from shutil import move
from calendar import monthrange
from datetime import datetime, timedelta, date
from random import randint



class Database:

    '''
    Database manager.
    WARNING: apart from [store_donor] and [store_donation] all methods require that [load_donor] and [load_donation] have been previously run once.
    '''

    #/!\ for some reason, Python terminal requires an absolute (complete) path... /!\
    #def __init__(self, donor_path = r'D:\Dropbox\Bioinformática\myPythonFiles\IAP\Trabalho\Database\Donor_record.csv', donation_path = r'D:\Dropbox\Bioinformática\myPythonFiles\IAP\Trabalho\Database\Donation_record.csv', center_path = r'D:\Dropbox\Bioinformática\myPythonFiles\IAP\Trabalho\System\Centers.txt'):

    def __init__(self, donor_path = 'Database/Donor_record.csv', donation_path = 'Database/Donation_record.csv', center_path = 'System/Centers.txt'):
        self.donor_path = donor_path        #[donor_file] is the path to the text file where donor records are stored
        self.donation_path = donation_path  #[donation_file] is the path to the text file where donation records are stored
        self.center_path = center_path      #[center_file] this it the path to the file storing approved donation centers
        self.donor_Map = {}                 #{[donor_number]: line in donor_file (int)}
        #self.donation_Map = {}             #{[donation_number]: line in donation_file (int)} (#Sendo a atribuicao dos numeros de doacao sequencial e a comecar em 1, este mapa torna-se obsoleto pois a o numero da linha e igual ao numero da doacao.)
        self.name_to_number = {}            #{[donor name]: donor number(s) (list)}
        self.donor_to_donation = {}         #{[donor number]: donation(s) (list)}
        self.blood_to_donor = {}            #{[bloodtype]: donors (list)}
        self.sns_to_donor = {}              #{[sns]: donor_number}
        self.bloodtype_to_stock = {}        #{[bloodtype]: donation not out (list)}  #stock follows FIFO (as in a Queue)
        #self.date_to_donation = {}         #{[date]: donation(s) (list)}
        self.donation_to_date = {}          #{[donation number]: (dateIN, dateOUT) (tuple)}
        self.donor_count = 0                #[donor_count] keeps track of the (global) number of donors
        self.donation_count = 0             #[donation_count] keeps track of the (global) number of donations
        self.approved_centers = []          #[approved_centers] (list) is a list of approved donation centers from which the user muct choose one  #apenas simulado (Braga, Lisboa, Porto e Coimbra) "(por falta de tempo) Nao serao feitos metodos para adicao ou remocao de centros aprovados";
        self.center = None                  #[center] is meant to keep a string with the name of the blood donation center; set once per session, will be associated with all donations made



    #=============================================< Data mounting >================================================#

    def load_donorDB(self):
        '''
        Accesses Donor_record.csv to assemble [donor_Map], [name_to_number], [blood_to_donor] and [donor_count].
        Note1: This method is meant to be run once (and only once) at begining of the main program.
        Note2: The intention of the dictionaries is to keep essential info (only) in memory in order to speed most common queries.
        Note3: Data could be assembled into Donor objects and Donor.valid() could be run but it would be more time consuming.
        WARNING: If run more than once it duplicates the information contained in the assembled dictionaries.
        '''
        try:
            #path = self.donor_path.encode(encoding='UTF-8')
            if stat( self.donor_path )[6] != 0: #os.stat(file_path)[6] gives file's number of lines
                with open( self.donor_path ) as donor_file:
                    for i, line in enumerate(donor_file):
                        if i > 0: #ignores headline
                            field = disassemble(line)
                            #==========<"decode" of field>=========#
                            number = field[0]
                            name = field[1].upper().replace(' DE ',' ').replace(' DA ',' ').replace(' DO ',' ').replace(' DOS ',' ').replace(' DAS ',' ')
                            SNS = field[2]
                            ABO = field[3]
                            Rh = field[4]
                            bloodtype = ABO+Rh
                            #gender = field[5]
                            #birthdate = field[6]
                            #street = field[7]
                            #postcode = field[8]
                            #city = field[9]            #Not necessary (so far)
                            #country = field[10]
                            #email = field[11]
                            #phone = field[12]
                            #mobile = field[13]
                            #==========<mounts donor_Map>==========#
                            self.donor_Map[number] = i
                            #=======<mounts name_to_number>========#
                            if self.name_to_number.has_key(name):
                                self.name_to_number[name].append(number)
                            else:
                                self.name_to_number[name] = [number]
                            #=======<mounts blood_to_donor>========#
                            if self.blood_to_donor.has_key(bloodtype):
                                self.blood_to_donor[bloodtype].append(number)
                            else:
                                self.blood_to_donor[bloodtype] = [number]
                            #========<mounts sns_to_donor>=========#
                            self.sns_to_donor[ SNS ] = number
                            #=======<donor_count increment>========#
                            self.donor_count += 1
        except WindowsError as error:
            raw_input('%s' %error)
            


        
    def load_donationDB(self):
        '''
        Accesses Donor_record.csv to assemble [donation_Map], [name_to_number], [blood_to_donor] and [donor_count].
        Note1: This method is meant to be run once at begining of the main program.
        Note2: The intention of the dictionaries is to keep essential info (only) in memory in order to speed most common queries.
        Note3: Data could be assembled into Donation objects but it would be more time consuming.
        WARNING: If run more than once it duplicates the information contained in the assembled dictionaries.
        '''
        try:
            #path = self.donation_path.encode(encoding='UTF-8')
            if stat( self.donation_path )[6] != 0: #os.stat(file_path)[6] gives file's number of lines
                with open( self.donation_path ) as donation_file:
                    for i, line in enumerate(donation_file):
                        if i > 0: #ignores headline
                            field = disassemble(line)
                            #===========<"decode" of field>============#
                            number = field[0]  #refers to donation number
                            IN = field[1]
                            donor = field[2]
                            ABO = field[3]
                            Rh = field[4]
                            bloodtype = ABO+Rh
                            #center = field[5]       #Not necessary (so far)
                            OUT = field[6]
                            #===========<mounts donation_Map>==========#
                            #self.donation_Map[number] = i  #(obsoleto nas condicoes presentes)
                            #=========<mounts donor_to_donation>=======#
                            if self.donor_to_donation.has_key(donor):
                                self.donor_to_donation[donor].append(number)
                            else:
                                self.donor_to_donation[donor] = [number]
                            #========<mounts bloodtype_to_stock>=======#
                            if OUT == 'None':
                                if self.bloodtype_to_stock.has_key(bloodtype):
                                    self.bloodtype_to_stock[bloodtype].append(number)
                                else:
                                    self.bloodtype_to_stock[bloodtype] = [number]
                            #=========<mounts date_to_donation>========#
                            '''
                            if self.date_to_donation.has_key(IN):
                                self.date_to_donation[IN].append(number)
                            else:
                                self.date_to_donation[IN] = [number]
                            '''
                            #=========<mounts donation_to_date>========#
                            if self.donation_to_date.has_key(number):
                                self.donation_to_date[number].append( (IN, OUT) )
                            else:
                                self.donation_to_date[number] = (IN, OUT)
                            #========<donation_count increment>========#
                            self.donation_count += 1
        except WindowsError as error:
            raw_input('%s' %error)



    def load_approved_centers (self):
        '''
        Creates a list of approved donation centers stored in <Database.approved_center_list>
        from which the user must choose one in the begining of the session.
        The chosen center will be stored in <Database.center> and will be assocated with all donations registered during the session.
        '''
        try:
            with open(self.center_path) as center_file:
                for line in center_file:
                    if line != '\n':
                        self.approved_centers.append( line.replace('\n','') )
        except IOError as error:
            print error



    #========================================< Create Donor and Donation >=========================================#

    def create_donor (self, name, sns_num, bloodtype, gender, birthdate, contacts):
        '''
        Returns an instance of Donor class with an previously unassigned donor number.
        Assumes that all arguments are valid (validated during input procedure).
        Generates a valid unassigned donor number.
        Note: Assumes that all donor numbers have 6 digits.
        '''
        #Warning:
        # We are aware that this method of generating donor's numbers imply that:
        #  1) The available numbers will eventually run out and the program will enter an infinite loop;
        #  2) Number generation will get slower as numbers available decrease.
        #  For the purpose of this exercise we considered those limitations acceptable.
        #==================<Notes>=====================
        #[name] is an instance of Name class
        #[sns_num] is an instance of SNS_num class
        #[bloodtype] is an instance of Bloodtype class
        #[ABO] is an attribute of Bloodtype class
        #[Rh] is an attribute of Bloodtype class
        #[gender] is an instance of Gender class
        #[birthdate] is an instance of Birthdate class
        #[contacts] is an instance of Contacts class
        #[address] is an instance of Address class
        #[street] is an attribute of Address class
        #[postcode] is an attribute of Address class
        #[city] is an attribute of Address class
        #[country] is an attribute of Address class
        #[email] is an instance of Email class
        #[phone] is an instance of Phone class
        #[mobile] is an instance of Mobile class
        #==============================================
        while True:
            intNumber = randint(1, 999999) #at most 6 digits
            strNumber = str( intNumber )
            rawNumber = strNumber.zfill(6) #assures 6 digits by filling the remainder with zeros to the left
            if rawNumber not in self.donor_Map:
                donorNumber = Donor_num(rawNumber) #[donorNumber] is an instance of Donor_num class
                break
        return Donor(donorNumber, name, sns_num, bloodtype, gender, birthdate, contacts)



    def create_donation (self, donor):
        '''
        Receives as input an instance of Donor [donor] and [center] (a string).
        Returns an instance of Donation if conditions are met; returns None otherwise.
        Note: Assumes [donor.valid() == True] (because validation criteria will be met prior to this method implementation).
        Note2: Assumes forbidden character verification on [center] has been performed on input.
        Note3: store_donation() is meant to be run on this method's output before this method is runned again.
        '''
        #====<verification of minimum time lapse between donations>====# 
        last_dates = self.Get_Last_Donation_Dates_from_Donor_number( donor.number.num )
        time_since_last = 0
        if last_dates != None: #Tem pelo menos uma doacao
            last_date = last_dates[0] #(IN_date, OUT_date)
            last_date = datetime.strptime(last_date, '%d-%m-%Y').date()
            time_since_last = month_delta( last_date ) #number of months passed since last donation
        if donor.gender.gender == 'M' and time_since_last >= 3 or donor.gender.gender == 'F' and time_since_last >= 4 or last_dates == None:
            donation_number = str(self.donation_count + 1)
            IN_date = date.today()
            new_donation = Donation( donation_number, IN_date, donor.number.num, donor.bloodtype, self.center )
            #Note: [donation_count] will only be incremented on store donation method
            return new_donation
        else:
            raw_input('< intervalo entre doacoes insuficiente (%s meses) - operacao abortada >' %time_since_last)




    #=============================================< Storage methods >==============================================#

    def store_donor (self, donor): #[donor] is an instance of Donor class
        '''
        Adds a new donor record to the donor database.
        Assumes valid donor.
        '''
        #if donor.valid():  (verification of individual elements runs on input)
        while True:
            try:
                with open(self.donor_path, 'a') as donor_file:
                    donor_file.write(donor.encode())
                    break
            except IOError as Error:
                if Error.errno == 13:
                    print '\n< %s >' %Error.strerror
                    raw_input('>>> Feche o ficheiro "%s".' %Error.filename)
                else:
                    raise Error
        #==========<mounts donor_Map>=================================#
        self.donor_Map[ donor.number.num ] = self.donor_count + 1
        #=======<mounts name_to_number>===============================#
        name = donor.name.name.upper().replace(' DE ',' ').replace(' DA ',' ').replace(' DO ',' ').replace(' DOS ',' ').replace(' DAS ',' ')
        if self.name_to_number.has_key( name ):
            self.name_to_number[ name ].append( donor.number.num )
        else:
            self.name_to_number[ name ] = [ donor.number.num ]
        #=======<mounts blood_to_donor>===============================#
        bloodtype = donor.ABO + donor.Rh
        if self.blood_to_donor.has_key( bloodtype ):
            self.blood_to_donor[ bloodtype ].append( donor.number.num )
        else:
            self.blood_to_donor[ bloodtype ] = [ donor.number.num ]
        #========<mounts sns_to_donor>================================#
        self.sns_to_donor[ donor.sns.num ] = donor.number.num
        #=======<donor_count increment>===============================#
        self.donor_count += 1



    def store_donation (self, donation): #[donation] is an instance of Donation class
        '''
        Adds a new donation record to the donation database.
        Assumes [donation] as valid.
        '''
        while True:
            try:
                with open(self.donation_path, 'a') as donation_file:
                    donation_file.write(donation.encode())
                    break
            except IOError as Error:
                if Error.errno == 13:
                    print '\n< %s >' %Error.strerror
                    raw_input('>>> Feche o ficheiro "%s".' %Error.filename)
                else:
                    raise Error
        #=========<Adds to donor_to_donation>==============================#
        if self.donor_to_donation.has_key( donation.donor ):
            self.donor_to_donation[ donation.donor ].append(donation.number)
        else:
            self.donor_to_donation[ donation.donor ] = [donation.number]
        #========<Adds to bloodtype_to_stock>==============================#
        bloodtype = donation.ABO + donation.Rh
        if self.bloodtype_to_stock.has_key( bloodtype ):
            self.bloodtype_to_stock[ bloodtype ].append(donation.number)
        else:
            self.bloodtype_to_stock[ bloodtype ] = [donation.number]
        #=========<Adds to date_to_donation>===============================#
        IN_date = donation.IN.strftime('%d-%m-%Y')
        '''
        if self.date_to_donation.has_key( IN_date ):
            self.date_to_donation[ IN_date ].append( donation.number )
        else:
            self.date_to_donation[ IN_date ] = [donation.number]
        '''
        #=========<Adds to donation_to_date>===============================#
        OUT_date = donation.OUT.strftime('%d-%m-%Y') if donation.OUT != None else str(donation.OUT)
        if self.donation_to_date.has_key(donation.number):
            self.donation_to_date[ donation.number ].append( (IN_date, OUT_date) )
        else:
            self.donation_to_date[ donation.number ] = (IN_date, OUT_date)
        #========<Increments donation_count>===============================#
        self.donation_count += 1



    def Remove_Blood_from_Stock ( self, bloodtype , number_of_units ):
        '''
        Removes [number_of_units] of a determined [bloodtype] from stock.
        '''
        stock = self.Get_Stock_from_bloodtype( bloodtype )
        if stock != None:
            if stock >= number_of_units:
                OUT_list = []
                for i in xrange( number_of_units ):
                    OUT_list.append( int( self.bloodtype_to_stock[ bloodtype ].pop(0) ) )
                OUT_date = date.today().strftime('%d-%m-%Y')
                edit_field_in_line( self.donation_path, OUT_list, 7, OUT_date )
                return OUT_list
            else:
                print '< stock insuficiente - ha %s unidades de sangue %s >' %(stock, bloodtype)
                return None
        else:
            print '< nao ha qualquer unidade em stock desse grupo >'
            return None



    #===========================================< Edition methods >==============================================#

    def Edit_Donor_field_by_line(self, line_number, field_number, field_value):
        '''
        Sets [field_number](int) to specified [field_value](str) for [line_number](int).
        Note0: This method constitutes a limitation of "edit_field_in_line()" external function
               which accepts a list of lines to edit in the same field and with the same value.
        Note1: Assumes the existence of a "temp" folder in the execution directory.
        Note2: Assumes file_path as a valid file path (and extension).
        Note3: Assumes the line has at least [field_number] fields.
        Note4: To edit a value in the first line line_number must be zero.
        '''
        edit_field_in_line ( self.donor_path, [line_number], field_number, field_value )

    '''
    Note: A method to edit donation records (asside from OUT_date)
          have not been developed since there are no mutable fields in donation.
          The donation record must remain unaltered.
    '''

    #===========================================< Retrieval methods >==============================================#

    def Retrieve_Donor_from_Line (self, line_number):
        '''
        Retrieve_Donor_from_Line( [line_number] ) --> donor (Donor class)
        Returns the donor (instance of Donor class) corresponding to [line_number] in Donor_record.csv.
        Note: get_Lines_by_line_Numbers() can be used to retrieve multiple lines but here it is meant to return only one.
        WARNING: [line_number = 0] attempts to mount Donor with header line.
        '''
        raw_donor = get_Lines_by_line_Numbers(self.donor_path, [line_number])
        if raw_donor != []:
            return mount_Donor( raw_donor[0] )



    def Retrieve_Donation_from_Line (self, line_number):
        '''
        Retrieve_Donation_from_Line( [line_number] ) --> donation (Donation class)
        Returns the donation (instance of Donation class) corresponding to [line_number] in Donation_record.csv.
        Note: get_Lines_by_line_Numbers() can be used to retrieve multiple lines but here it is meant to return only one.
        WARNING: [line_number = 0] attempts to mount Donation with header line.
        '''
        raw_donation = get_Lines_by_line_Numbers(self.donation_path, [line_number])
        if raw_donation != []:
            return mount_Donation( raw_donation[0] )



    def Retrieve_Donor_from_Line_List (self, line_list):
        '''
        Retrieve_Donor_from_Line_List( [line_list] ) --> [donor_list] (Donor class)
        Returns a list with donors (instances of Donor class) corresponding to [line_list].
        Note: The order of the returned donors is that of Donor_record.csv.
        WARNING: [line_number = 0] attempts to mount Donor with header line.
        '''
        raw_list = get_Lines_by_line_Numbers( self.donor_path, line_list )
        if raw_list != []:
            donor_list = []
            for raw_donor in raw_list:
                donor_list.append( mount_Donor( raw_donor ) )
            return donor_list



    def Retrieve_Donation_from_Line_List (self, line_list):
        '''
        Retrieve_Donation_from_Line_List( [line_list] ) --> [donation_list] (Donation class)
        Returns a list with donations (instances of Donation class) corresponding to [line_list].
        Note: The order of the returned donations is that of Donation_record.csv.
        WARNING: [line_number = 0] attempts to mount Donation with header line.
        '''
        raw_list = get_Lines_by_line_Numbers( self.donation_path, line_list )
        if raw_list != []:
            donation_list = []
            for raw_donation in raw_list:
                donation_list.append( mount_Donation( raw_donation ) )
            return donation_list



    def Retrieve_Donor_by_number (self, donor_number):
        '''
        Retrieve_Donor_by_number( [donor_number] ) --> donor (Donor class)
        Returns the donor (instance of Donor class) corresponding to [donor_number] in Donor_record.csv
        Note1: [donor_number] is a string.
        '''
        #if self.donor_Map.has_key( donor_number ):
        line_number = self.donor_Map[ donor_number ]
        donor = self.Retrieve_Donor_from_Line( line_number )
        return donor



    def Retrieve_Donor_by_SNS (self, SNS_number):
        '''
        Retrieve_Donor_by_SNS( [SNS_number] ) --> donor (Donor class)
        Returns the donor (instance of Donor class) corresponding to [SNS_number] in Donor_record.csv
        Note1: [SNS_number] is a string.
        '''
        #if self.sns_to_donor.has_key( SNS_number ):
        donor_number = self.sns_to_donor[ SNS_number ]
        donor = self.Retrieve_Donor_by_number( donor_number )
        return donor



    #=============================================< Query methods >================================================#    

    #=====================< "Get_..." methods >=======================#
        
    def Get_Donation_list_from_Donor_number (self, donor_number):
        '''Returns a <list> with all donations (donation numbers) made by the donor with such [donor_number].'''
        if self.donor_to_donation.has_key(donor_number):
            return self.donor_to_donation[donor_number]



    def Get_Last_Donation_from_Donor_number (self, donor_number):
        '''Returns a <string> with the last donation (number) made by the donor with such [donor_number].'''
        Donation_list = self.Get_Donation_list_from_Donor_number( donor_number )
        if Donation_list != None:
            return Donation_list[len(Donation_list)-1] #Indice [0] da lista corresponde a doacao mais antiga; o ultimo indice a mais recente.



    def Get_Last_Donation_Dates_from_Donor_number (self, donor_number):
        '''
        Returns a <tuple> with (IN_date, OUT_date) of donation with such [donation_number].
        Note: IN_date and OUT_date are <string>; OUT_date can have value "None" (also a string). #Estas "datas" podem ser convertidas em objectos datetime.date()
        '''
        Last_Donation = self.Get_Last_Donation_from_Donor_number( donor_number )
        return self.Get_donationDates_from_donationNumber( Last_Donation )



    def Get_donationDates_from_donationNumber (self, donation_number):
        '''
        Returns a <tuple> with (IN_date, OUT_date) of donation with such [donation_number].
        Note: IN_date and OUT_date are <string>; OUT_date can have value "None" (also a string). #Estas "datas" podem ser convertidas em objectos datetime.date()
        '''
        if self.donation_to_date.has_key(donation_number):
            return self.donation_to_date[donation_number]



    def Get_Stock_from_bloodtype( self, bloodtype ):
        '''
        Returns the number of units in stock of a specified [bloodtype].
        '''
        if not self.bloodtype_to_stock.has_key( bloodtype ):
            print '< tipo sanguineo "%s" nao reconhecido >' % bloodtype
            print '< use o formato (ABO+Rh) - ex: A+/AB-/O+ >'
        else:
            return len( self.bloodtype_to_stock[ bloodtype ] )



    def Get_Donation_List_between_dates(self, from_date, to_date):
        '''
        Returns a list with all donations (donation numbers) between <from_date> and <to_date> (both dates are included).
        <from_date> and <to_date> are datetime.date() instances.
        Note: Assumes dates are valid.
        '''
        donation_list = []
        end_of_interval = False
        start_of_interval = False
        try:
            with open(self.donation_path) as File:
                File.readline() #cabecalho
                while not end_of_interval:                    
                    line = File.readline()
                    if not line: break
                    field_list = disassemble(line)
                    line_date = datetime.strptime( field_list [1], '%d-%m-%Y' ).date()
                    if line_date <= to_date and line_date >= from_date:
                        donation_list.append(field_list[0])
                        start_of_interval = True
                    elif start_of_interval:
                        end_of_interval = True
            return donation_list
        except IOError as error:
            print error



    def Count_Donations_between_dates(self, from_date, to_date):
        '''
        Returns the number of donations (int) between <from_date> and <to_date> (both dates are included).
        <from_date> and <to_date> are datetime.date() instances.
        Note: Assumes dates are valid.
        '''
        donation_counter = 0
        end_of_interval = False
        start_of_interval = False
        try:
            with open(self.donation_path) as File:
                File.readline() #cabecalho
                while not end_of_interval:                    
                    line = File.readline()
                    if not line: break
                    field_list = disassemble(line)
                    line_date = datetime.strptime( field_list [1], '%d-%m-%Y' ).date()
                    if line_date <= to_date and line_date >= from_date:
                        donation_counter += 1
                        start_of_interval = True
                    elif start_of_interval:
                        end_of_interval = True
            return donation_counter
        except IOError as error:
            print error



    #=====================< "Has_..." methods >=======================#

    def Has_Donor_number(self, donor_number):
        '''
        Has_Donor_number([donor_number](str)) --> True or False
        '''
        if self.donor_Map.has_key( donor_number ):
            return True
        else:
            return False



    def Has_SNS_number(self, SNS_number):
        '''
        Has_SNS_number([SNS_number](str)) --> True or False
        '''
        if self.sns_to_donor.has_key( SNS_number ):
            return True
        else:
            return False



    #===============================================< Reports >====================================================#

    def full_Donor_report (self, field_list, print_on_screen):
        '''
        Saves a full report of the specified fields in [field_list]
        '''
        create_report_file_by_fields ( self.donor_path, [], field_list, 'full_Donor_report', None, print_on_screen)



    def full_Donation_report (self, field_list, print_on_screen):
        '''
        Saves a full report of the specified fields in [field_list]
        '''
        create_report_file_by_fields ( self.donation_path, [], field_list, 'full_Donation_report', None, print_on_screen)



    def blood_stock_report ( self ):
        '''
        Returns the number of units in stock for every bloodtype.
        '''
        print '\n-------------< STOCK >--------------'
        length = 0
        for value in self.bloodtype_to_stock.itervalues():
            stock = len( value )
            stock = str( stock )
            if len( stock ) >= length:
                length = len( stock )
        for bloodtype in self.bloodtype_to_stock.iterkeys():
            blood_str = '%s' %bloodtype
            stock_str = '%s' %len(self.bloodtype_to_stock[ bloodtype ])
            string = 'Sangue Tipo %s:  %s unidades' %(blood_str.ljust(3), stock_str.rjust( length ))
            print string.center(36)
        print'------------------------------------'



    #================================================< Stats >=====================================================#

    def Global_Donor_stats ( self, query_field_list, concat_sep='' ):
        '''
        Global_Donor_stats( [[4,5],[6],[10]], concat_sep=' ') --> [ {['ABO Rh']:%%}, {['Gender']:%%}, {['City']:%%} ]
        Returns a list of dictionaries with the percentage of each value (or joint value) in each field (or joint field) specified in <query_field_list>.
        Joint field sintaxe: ( query_field_list=[[1,3],[4,2],[1]], concat_sep='.') --> ['field1.field3','field4.field2','field1']
        Note1: Assumes that every field number in <query_field_list> is within range.
        Note2: Assumes that the first field is field number 1.
        '''
        return global_stat_by_field (self.donor_path, query_field_list, concat_sep='')



    def Global_Donation_stats ( self, query_field_list, concat_sep='' ):
        '''
        Global_Donation_stats( [[4,5],[6]], concat_sep=' ') --> [ {['ABO Rh']:%%}, {['Center']:%%} ]
        Returns a list of dictionaries with the percentage of each value (or joint value) in each field (or joint field) specified in <query_field_list>.
        Joint field sintaxe: ( query_field_list=[[1,3],[4,2],[1]], concat_sep='.') --> ['field1.field3','field4.field2','field1']
        Note1: Assumes that every field number in <query_field_list> is within range.
        Note2: Assumes that the first field is field number 1.
        '''
        return global_stat_by_field (self.donation_path, query_field_list, concat_sep='')



    def Donation_Stats_within_interval ( self, query_field_list, from_date, to_date, concat_sep=''):
        '''
        Donation_stats_within_interval( [[4,5],[6]], <from_date>, <to_date>, concat_sep=' ') --> [ {['ABO Rh']:[local%, global%]}, {['Center']:[local%, global%]} ]
        Returns a list of dictionaries with the percentage of each value (or joint value) in each field (or joint field)
        specified in <query_field_list> between <from_date> and <to_date> (both dates are included).
        Joint field sintaxe: ( query_field_list=[[1,3],[4,2],[1]], concat_sep='.') --> ['field1.field3','field4.field2','field1']
        Note0: <from_date> and <to_date> are <datetime.date> instances.
        Note1: Assumes that every field number in <query_field_list> is within range.
        Note2: Assumes that the first field is field number 1.
        '''
        interval_counter = 0.0   #conta as doações dentro do intervalo especificado
        Field_value_frequency = []   #cada campo da lista vai conter um dicionário com a frequência de cada valor no campo 'query' correspondente.
        for i in xrange( len(query_field_list) ):
            Field_value_frequency.append( {} )   #abertura dos dicionários necessários
        end_of_interval = False
        start_of_interval = False
        try:
            with open( self.donation_path ) as File:
                File.readline() #cabecalho
                while not end_of_interval:
                    line = File.readline()
                    if not line: break
                    fields_in_line = disassemble( line )
                    line_date = datetime.strptime( fields_in_line[1], '%d-%m-%Y' ).date()
                    if line_date <= to_date and line_date >= from_date:
                        interval_counter += 1
                        joint_fields = join_fields( fields_in_line, query_field_list, concat_sep )
                        for i in xrange( len(query_field_list) ):
                            value = joint_fields[i].upper()
                            if Field_value_frequency[i].has_key( value ):
                                Field_value_frequency[i][ value ] += 1
                            else:
                                Field_value_frequency[i][ value ] = 1
                        start_of_interval = True
                    elif start_of_interval:
                        end_of_interval = True
            for Dict in Field_value_frequency:
                for value in Dict.iterkeys():
                    global_percent = round( Dict[ value ] / float(self.donation_count) * 100, 2 ) #dá erro se [donation_count == 0]
                    Dict [value] = [ round( Dict[ value ]/interval_counter * 100, 2 ) ]
                    Dict [value].append( global_percent )
            return Field_value_frequency
        except IOError as Error:
            raw_input('IOError: %s' %Error)



    def Donor_Stats_within_interval ( self, query_field_list, from_age, to_age, concat_sep=''):
        '''
        Donor_stats_within_interval( [[4,5],[6],[10]], <from_age>, <to_age>, concat_sep=' ') --> [ {['ABO Rh']:[local%, global%]}, {['Gender']:[local%, global%]}, {['City']:[local%, global%]} ]
        Returns a list of dictionaries with the percentage of each value (or joint value) in each field (or joint field)
        specified in <query_field_list> between <from_age> and <to_age> (both are included).
        Joint field sintaxe: ( query_field_list=[[1,3],[4,2],[1]], concat_sep='.') --> ['field1.field3','field4.field2','field1']
        Note1: Assumes that every field number in <query_field_list> is within range.
        Note2: Assumes that the first field is field number 1.
        '''
        interval_counter = 0.0   #conta as doações dentro do intervalo especificado
        Field_value_frequency = []   #cada campo da lista vai conter um dicionário com a frequência de cada valor no campo 'query' correspondente.
        for i in xrange( len(query_field_list) ):
            Field_value_frequency.append( {} )   #abertura dos dicionários necessários
        try:
            with open( self.donor_path ) as File:
                File.readline() #cabecalho
                for line in File:
                    fields_in_line = disassemble( line )
                    birth_date = datetime.strptime( fields_in_line[6], '%d-%m-%Y' ).date()
                    Age = Birthdate( birth_date ).age()
                    if Age <= to_age and Age >= from_age:
                        interval_counter += 1
                        joint_fields = join_fields( fields_in_line, query_field_list, concat_sep )
                        for i in xrange( len(query_field_list) ):
                            value = joint_fields[i].upper()
                            if Field_value_frequency[i].has_key( value ):
                                Field_value_frequency[i][ value ] += 1
                            else:
                                Field_value_frequency[i][ value ] = 1
            for Dict in Field_value_frequency:
                for value in Dict.iterkeys():
                    global_percent = round( Dict[ value ] / float(self.donor_count) * 100, 2 ) #dá erro se [donor_count == 0]
                    Dict [value] = [ round( Dict[ value ]/interval_counter * 100, 2 ) ]
                    Dict [value].append( global_percent )
            return Field_value_frequency
        except IOError as Error:
            raw_input('IOError: %s' %Error)



#==============================================< Auxiliar functions >==============================================#

def mount_Donor( line ):
    '''
    Mounts and returns a Donor object from a [line] (string) that meets Donor.encode() sintaxe.
    Note: No verification is run on this procedure.
    '''
    field = disassemble(line)
    #==========< "decode" of field >=========#
    number = field[0]
    name = field[1]
    SNS = field[2]
    ABO = field[3]
    Rh = field[4]
    gender = field[5]
    birthdate = datetime.strptime( field[6], '%d-%m-%Y').date()
    #==< contacts >==# (optional fields)
    street = field[7] if field[7] != 'None' else None
    postcode = field[8] if field[8] != 'None' else None
    city = field[9] if field[9] != 'None' else None
    country = field[10] if field[10] != 'None' else None
    email = field[11] if field[11] != 'None' else None
    phone = field[12] if field[12] != 'None' else None
    mobile = field[13] if field[13] != 'None' else None
    #=========< Assembly of Donor >=========#
    donor = Donor( Donor_num( number ), Name( name ), SNS_num( SNS ), Bloodtype( ABO, Rh ), Gender( gender ), Birthdate( birthdate ),\
                   Contacts( Address( street, postcode, city, country), Email( email ), Phone( phone ), Mobile( mobile )))
    return donor



def mount_Donation( line ):
    '''
    Mounts and returns a Donation object from a [line] (string) that meets Donation.encode() sintaxe.
    Note: No verification is run on this procedure.
    '''
    field = disassemble(line)
    #==========< "decode" of field >=========#
    number = field[0]
    IN_date = datetime.strptime( field[1], '%d-%m-%Y').date()
    donor = field[2]
    ABO = field[3]
    Rh = field[4]
    center = field[5]
    OUT_date = datetime.strptime( field[6], '%d-%m-%Y').date() if field[6] != 'None' else None
    #=========< Assembly of Donation >=========#
    donation = Donation( number, IN_date, donor, Bloodtype( ABO, Rh ), center, OUT_date )
    return donation



def get_Lines_by_line_Numbers(file_path, line_number): #[line_number] is a <list> with the numbers of the lines to retrieve
    '''
    Takes as input a path to a file [file_path] and a list of integers [line_number]
    Returns a list [line_list] with the lines of the file whose numbers are in [line_number]
    If line numbers are out of range for the file, returns an empty list [].
    WARNING: [line_number = 0] retrieves header line.
    '''
    line_list = []
    with open(file_path) as File:
        for i, line in enumerate(File):
            if i in line_number: #assumes first line as number 1
                line_list.append(line)
    return line_list



def get_Lines_by_field_Value(file_path, field_number, field_value, sep = ';'):
    '''
    Returns a list with the lines of File in [file_path] whose value in field number [field_number] match value [field_value].
    Note: get_Lines_by_field_Value is slower than get_Lines_by_line_Numbers.
    '''
    if type(field_value) != str:
        field_value = str(field_value)
    line_list = []
    with open(file_path) as File:
        for line in File:
            fields = disassemble(line)
            if field_number <= len(fields):
                if fields[field_number-1] == field_value: #assumes first field as number 1
                    line_list.append(line)
    return line_list



def disassemble(line, sep = ';'):
    '''Removes new lines '\n' and splits [line] by [sep]'''
    return line.replace('\n','').split(sep)



def assemble(field_list, sep = ';'):
    new_line = ''
    for field in field_list[ : len(field_list) -1 ]:
        new_line += field + sep
    new_line += field_list[ len(field_list) -1 ] + '\n'
    return new_line



def month_delta(last_date): #[last_date] e um objecto datetime.date()
    '''
    Counts the number of months past since donor's last donation.
    Increments date1 month by month until it is greater than or equal to present date.
    '''
    delta = 0
    today = date.today()
    while True: #processo iterativo de contagem dos meses
        month_days = monthrange(last_date.year, last_date.month)[1] #retorna o numero de dias no mes da data1
        last_date += timedelta(days = month_days) #Soma a data1 o numero de dias do mes1  
        if last_date <= today: #se a data1 ainda e inferior a data2 incrementa delta
            delta += 1
        else:
            break
    return delta



def edit_field_in_line (file_path, line_list, field_number, field_value, sep = ';'):
    '''
    Sets [field_number](int) to specified [field_value](str) for lines in [line_list](list) of [file_path](str) .
    Note1: Assumes the existence of a "temp" folder in the execution directory.
    Note2: Assumes file_path as a valid file path (and extension).
    Note3: Assumes the line has at least [field_number] fields.
    Note4: To edit a value in the first line line_number must be zero.
    '''
    temp_file = 'temp' + file_path[ file_path.rfind('.') : ] #Assumes the existence of a "temp" folder in the execution directory.
    temp_path = 'temp/' + temp_file                          #This could be done in the same directory since the files have different names,
    if file_path.rfind('/') != -1:                           #that way it wouldn't require shutil.move() method.
        folder = file_path [ : file_path.rfind('/') +1 ]
    else:
        folder = file_path [ : file_path.rfind('\\') +1 ]
    try:
        with open( file_path, 'r' ) as ori_file, open( temp_path, 'w' ) as tmp_file:
            for i, line in enumerate(ori_file):
                if i in line_list:
                    field_list = disassemble( line, sep )
                    if field_number <= len(field_list):
                        field_list [ field_number -1 ] = field_value
                        new_line = assemble ( field_list, sep )
                        tmp_file.write( new_line )
                else:
                    tmp_file.write( line )
        move( temp_path , folder + temp_file ) #Moves temp_file out of temp folder
        while True:
            try:
                remove( file_path )
                break
            except WindowsError as Error:
                if Error.errno == 13 and Error.winerror == 32:
                    print '\n< %s >' %Error.strerror
                    raw_input('>>> Feche o ficheiro "%s".' %Error.filename)
                else:
                    raise Error
        rename( folder + temp_file, file_path )
    except IOError as Error:
        raw_input ('IOError %s' %Error)
        raise Error



def create_report_file_by_fields (read_path, line_list, field_list, report_name = 'Report', report_extension = None, print_on_screen = False, sep = ';'):
    '''
    Sets [field_number](int) to specified [field_value](str) for lines in [line_list](list) of [file_path](str) .
    Note1: Assumes the existence of a "Reports" folder in the execution directory (where all reports will be saved).
    Note2: Assumes file_path as a valid file path (and extension).
    Note3: Assumes that no value in field_list exceeds the number of fields in line.
    Note4: To edit a value in the first line line_number must be zero.
    Note5: The order of fields in field_list indicates the order of fields in output report.
    '''
    if not 0 in line_list and line_list != []:
        line_list.insert(0,0)
    if report_extension == None:  #vai usar a mesma extensao do ficheiro de origem
        report_file = report_name + read_path[ read_path.rfind('.') : ]
    else:
        report_file = report_name + report_extension
    report_path = 'Reports/' + report_file  #Assumes the existence of a "Reports" folder in the execution directory
    report_path = dont_overwrite( report_path )
    try:
        with open( read_path ) as ori_file, open( report_path, 'w' ) as new_file:
            for i, line in enumerate(ori_file):
                if i in line_list or line_list == []:
                    broken_line = disassemble( line, sep )
                    new_line = []
                    for field_number in field_list:
                        new_line.append( broken_line [ field_number -1 ] )
                    if i == 0:
                        justification = []
                        for field in new_line:
                            justification.append( len(field) )
                    assembled_new_line = assemble ( new_line, sep )
                    new_file.write( assembled_new_line )
                    if print_on_screen:
                        for i, field in enumerate( new_line ):
                            print field.ljust( justification[ i ] ),
                        print '\n',
    except IOError as Error:
        print Error



def dont_overwrite (filename):
    '''
    Checks if <filename.ext> exists in directory and replaces it with <filename(z).ext>
    where "z" is an integer which is iteratively incremented until filename(z).ext does not exist in the directory.
    '''
    z = 1
    while path.exists(filename):
        E = filename.rfind('.')
        Y = filename.rfind(')')
        if Y == E-1:
            X = filename.rfind('(')
            filename = filename[:X] + '(%s)' %str(z) + filename[E:]
        else:
            filename = filename[:E] + '(%s)' %str(z) + filename[E:]            
        z += 1
    return filename



def global_stat_by_field (file_path, query_field_list, concat_sep='', field_sep=';'):
    '''
    Returns a list of dictionaries with the percentage of each value (or joint value) in each field (or joint field) specified in <query_field_list>.
    Joint field sintaxe: ( query_field_list=[[1,3],[4,2],[1]], concat_sep='.') --> ['field1.field3','field4.field2','field1']
    Note1: Assumes that every field number in <query_field_list> is within range.
    Note2: Assumes that the first field is field number 1.
    '''
    global_counter = 0.0
    Field_value_frequency = []   #cada campo da lista vai conter um dicionário com a frequência de cada valor no campo 'query' correspondente.
    for i in xrange( len(query_field_list) ):
        Field_value_frequency.append( {} )   #abertura dos dicionários necessários
    try:
        with open(file_path) as File:
            File.readline()   #ignora o cabeçalho
            for line in File:
                global_counter += 1
                fields_in_line = disassemble( line, field_sep )
                joint_fields = join_fields( fields_in_line, query_field_list, concat_sep )
                for i in xrange( len(query_field_list) ):
                    value = joint_fields[i].upper()
                    if Field_value_frequency[i].has_key( value ):
                        Field_value_frequency[i][ value ] += 1
                    else:
                        Field_value_frequency[i][ value ] = 1
        for Dict in Field_value_frequency:
            for value in Dict.iterkeys():
                Dict [value] = round( Dict[ value ]/global_counter * 100, 2 ) 
        return Field_value_frequency
    except IOError as Error:
        raw_input('IOError: %s' %Error)



def join_fields (field_list, instructions, concat_sep=''):
    '''
    join_fields( ['a','b','c','d'], [[1,3],[4,2],[1]], '.' ) --> ['a.c','d.b','a']
    Input: Receives a list with strings <field_list> and a set of instructions on how to concatenate them <instructions>.
    Output: Returns a list of strings with the concatenation result.
    Note1: Assumes that every field number in <instructions> is within range for the fields of <field_list>.
    Note2: Assumes that first field is number 1.
    '''
    result = []
    for instruction in instructions:
        new_string = ''
        for number in instruction[ : len(instruction)-1 ]:
            new_string += field_list[ number -1 ] + concat_sep
        new_string += field_list[ instruction[ len(instruction)-1 ] -1 ]
        result.append( new_string )
    return result


