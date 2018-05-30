#-*- coding: utf-8 -*-

from re import match, search
from datetime import date



class Donor_num:
    '''
    Instantiates the donor's national donor number
    '''
    def __init__(self, num):
        self.num = num  #[num] is a string

    def __repr__(self):
        return str(self.num)

    def valid (self):
        '''
        Ascertains the validity of [num] as a national donor number
        Returns True if [num] is composed of 6 digits; False otherwise
        '''
        #Note: we could not determine the number of digits in a donor number
        #      so we assumed 6 digits (as in our own cards).
        if match('[0-9]{6}$', self.num) != None:
            return True
        else:
            return False #E01



class SNS_num:
    '''
    Instantiates the donor's national health system number (SNS)
    '''
    def __init__(self, num):
        self.num = num  #[num] is a string

    def __repr__(self):
        return str(self.num)

    def valid (self):
        '''
        Ascertains the validity of [num] as a portuguese health system number
        Returns True if [num] is composed of 9 digits; False otherwise
        '''
        if match('[0-9]{9}$', self.num) != None and self.num != '000000000':
            return True
        else:
            return False #E02



class Name:
    '''
    Instantiates the donor's name
    '''
    def __init__(self, name):
        self.name = name  #[name] is a string

    def __repr__(self):
        return str(self.name)

    def valid (self):
        '''
        Verifies if [name] contains digits, commas or new lines
        Returns True if it doesn't and False otherwise
        '''
        if search('[0-9]|;', self.name) == None:
            return True
        else:
            return False #E03



class Gender:
    '''
    Instantiates the donor's gender (M/F)
    '''
    def __init__(self, gender):
        self.gender = gender  #[gender] is a string 

    def __repr__(self):
        return str(self.gender)

    def valid (self):
        '''
        Ascertains the validity of [gender]
        Returns True if [gender] is "M" or "F"; False otherwise
        '''
        if self.gender == 'M' or self.gender == 'F':
            return True
        else:
            return False #E04



class Birthdate:
    '''
    Instantiates the donor's birth date
    '''
    def __init__(self, birth_date):
        self.birth_date = birth_date  #[birth_date] is a datetime.date instance

    def __str__(self):
        return self.birth_date.strftime('%d-%m-%Y')

    def year(self):
        '''Returns year of [birth_date]'''
        return self.birth_date.year

    def month(self):
        '''Returns month of [birth_date]'''
        return self.birth_date.month

    def day(self):
        '''Returns day of [birth_date]'''
        return self.birth_date.day

    def age(self): #age < 18 => E05
        '''Returns the age with reference to [birth_date]'''
        today = date.today()
        try:
            birth_day = self.birth_date.replace(year = today.year) #keeps day and month of [birth_date] and takes present year
        except ValueError as Error:
            if self.birth_date.month == 2 and self.birth_date.day == 29: #catches the exception raised when the birth day is 29, the birth month is February and the present year is not a leap year (ano bissexto)
                birth_day = self.birth_date.replace(year = today.year, day = self.birth_date.day-1) #assumes 28/02 as the birthday
            else:
                raise Error
        if birth_day > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year



class Phone:
    '''
    Instantiates a portuguese local phone number
    '''
    def __init__(self, num):
        self.num = num  #[num] is a string

    def __repr__(self):
        return str(self.num)

    def valid (self):
        '''
        Ascertains the validity of [num] as a local phone number
        Returns True if [num] starts with 2 and is composed by 9 digits; False otherwise
        '''
        if match('2[0-9]{8}$', self.num) != None:
            return True
        else:
            return False #E06



class Mobile:
    '''
    Instantiates a portuguese mobile phone number
    '''
    def __init__(self, num):
        self.num = num  #[num] is a string

    def __repr__(self):
        return str(self.num) #in case [num] is not <str>

    def valid (self):
        '''
        Ascertains the validity of [num] as a mobile phone number
        Returns True if [num] starts with 9 and is composed by 9 digits; False otherwise
        '''
        if match('9[0-9]{8}$', self.num) != None:
            return True
        else:
            return False #E07
        


class Email:
    '''
    Instantiates an email account
    '''
    def __init__(self, email):
        self.email = email  #[email] is a string

    def __repr__(self):
        return str(self.email)

    def valid(self):
        '''
        Ascertains the validity of [email] as an email account
        Returns True if only authorized characters are found and the domain extension length is between two and six characters; False otherwise
        '''
        if match('[a-z0-9\._%+-]+@[a-z0-9.-]+\.[a-z]{2,6}$', self.email) != None: #regex adapted from http://www.webmonkey.com/2008/08/four_regular_expressions_to_check_email_addresses/ and http://stackoverflow.com/questions/201323/using-a-regular-expression-to-validate-an-email-address
            return True
        else:
            return False #E08
        '''
        Note1: [Email.valid()] does not filter new lines '\n' after [email]
               This does not constitute problem for raw_input() does not insert new lines
               and they are filtered when parsed from file.
        Note2: [Email.valid()] only accepts lower case; str.lower() will be applied to input.
        '''



class Address:
    '''
    Instantiates an portuguese address
    '''
    def __init__(self, street = None, postcode = None, city = None, country = None):
        self.street = street
        self.city = city
        self.postcode = postcode
        self.country = country
        #all attributes are strings

    def __repr__(self):
        return '%s\n%s %s, %s' %(self.street, self.postcode, self.city, self.country)

    def valid_postcode(self):
        '''
        Ascertains the validity of [postcode] as a portuguese postal code
        Returns True if 'four-three' digit format is verified, False if not, and None if not defined
        '''
        if self.postcode != None:
            if match('[0-9]{4}-[0-9]{3}$', self.postcode):
                return True
            else:
                return False #E09
        else:
            return None
        


class Contacts:
    '''
    Instantiates the donor's contacts
    '''
    def __init__(self, address = None, email = None, phone = None, mobile = None):
        self.address = address  #[address] is an instance of Address class
        self.email = email      #[email] is an instance of Email class
        self.phone = phone      #[phone] is an instance of Phone class
        self.mobile = mobile    #[mobile] is an instance of Mobile class

    def __repr__(self):
        return 'Endereco:\n%s\nEmail: %s\nTel.: %s\nTelm.: %s' %(self.address, self.email, self.phone, self.mobile)



class Bloodtype:
    '''
    Instantiates donor's blood type referring to ABO and Rh systems
    '''
    def __init__(self, ABO, Rh):
        self.ABO = ABO          #[ABO] is a string
        self.Rh = Rh            #[Rh] is a string

    def __repr__(self):
        return '%s Rh%s' %(self.ABO, self.Rh)

    def valid (self):
        '''
        Ascertains the validity of [ABO] and [Rh] as a blood type
        '''
        if match('(A|B|AB|O)$', self.ABO) and match('(\+|\-)$', self.Rh):
            return True
        else:
            return False #E10




'''
Address('Rua Dr. Jose Sousa Machado N51, R/C','4710-383','Braga','Portugal')
Email('bruno.phoenix@gmail.com')
Phone('253104152')
Mobile('932847455')
C = Contacts(Address('Rua Dr. Jose Sousa Machado N51, R/C','4710-383','Braga'),Email('bruno.phoenix@gmail.com'),Phone('253104152'),Mobile('932847455'))
'''
