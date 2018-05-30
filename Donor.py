#-*- coding: utf-8 -*-

from Elements import *



class Donor:
    '''
    Instantiates a blood donor
    '''
    def __init__(self, donor_num, name, sns_num, bloodtype, gender, birthdate, contacts):
        self.number = donor_num                    #[donor_num] is an instance of Donor_num class
        self.name = name                           #[name] is an instance of Name class
        self.sns = sns_num                         #[sns_num] is an instance of SNS_num class
        self.bloodtype = bloodtype                 #[bloodtype] is an instance of Bloodtype class
        self.ABO = bloodtype.ABO                   #[ABO] is an attribute of Bloodtype class
        self.Rh = bloodtype.Rh                     #[Rh] is an attribute of Bloodtype class
        self.gender = gender                       #[gender] is an instance of Gender class
        self.birthdate = birthdate                 #[birthdate] is an instance of Birthdate class
        self.contacts = contacts                   #[contacts] is an instance of Contacts class
        self.address = contacts.address            #[address] is an instance of Address class
        self.street = contacts.address.street      #[street] is an attribute of Address class
        self.postcode = contacts.address.postcode  #[postcode] is an attribute of Address class
        self.city = contacts.address.city          #[city] is an attribute of Address class
        self.country = contacts.address.country    #[country] is an attribute of Address class
        self.email = contacts.email                #[email] is an instance of Email class
        self.phone = contacts.phone                #[phone] is an instance of Phone class
        self.mobile = contacts.mobile              #[mobile] is an instance of Mobile class



    def __repr__(self):
        return 'Dador N#: %s\nNome: %s\nSNS: %s\nTipo sanguineo: %s\nGenero: %s\nData de nascimento: %s\nIdade: %s\n-------------<Contactos>------------\n%s' \
               %(self.number, self.name, self.sns, self.bloodtype, self.gender, self.birthdate, self.age(), self.contacts)


    
    def age(self):
        return self.birthdate.age()



    def valid(self):
        '''
        Ascertains the validity of the Donor instance, performing multiple individual verifications
        '''
        if not self.number.valid():
            print 'Erro: Dador N# %s, N# de dador invalido.' %self.number
            return 'E01'
        elif not self.sns.valid():
            print 'Erro: Dador N# %s, N# do SNS invalido (%s).' %(self.number, self.sns)
            return 'E02'
        elif not self.name.valid():
            print 'Erro: Dador N# %s, Nome invalido (%s).' %(self.number, self.name)
            return 'E03'
        elif not self.gender.valid():
            print 'Erro: Dador N# %s, sexo invalido (%s).' %(self.number, self.gender)
            return 'E04'
        elif self.age() < 18:
            print 'Erro: Dador N# %s, idade inferior a legal (%s).' %(self.number, self.age())
            return 'E05'
        elif self.age() > 65:
            print 'Erro: Dador N# %s, idade superior ao limite (%s).' %(self.number, self.age())
            return 'E06'
        elif self.phone != None and not self.phone.valid():
            print 'Erro: Dador N# %s, n# de telefone invalido (%s).' %(self.number, self.phone)
            return 'E07'
        elif self.mobile != None and not self.mobile.valid():
            print 'Erro: Dador N# %s, n# de telemovel invalido (%s).' %(self.number, self.mobile)
            return 'E08'
        elif self.email != None and not self.email.valid():
            print 'Erro: Dador N# %s, email invalido (%s).' %(self.number, self.email)
            return 'E09'
        elif self.address != None and self.address.valid_postcode() == False:
            print 'Erro: Dador N# %s, codigo postal invalido (%s).' %(self.number, self.address.postcode)
            return 'E10'
        elif not self.bloodtype.valid():
            print 'Erro: Dador N# %s, grupo sanguineo invalido (%s).' %(self.number, self.bloodtype)
            return 'E11'
        else:
            return True



    def encode(self):
        return '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(self.number, self.name, self.sns, self.ABO, self.Rh, self.gender, self.birthdate, \
                                                             self.street, self.postcode, self.city, self.country, self.email, self.phone, self.mobile)


'''
U = Donor(Donor_num('123456'), Name('Bruno Miguel Machado Silva'), SNS_num('123456789'), Bloodtype('O','+'), Gender('m'), Birthdate(date(1986,06,25)), Contacts(Address('Rua Dr. Jose Sousa Machado N51, R/C','4710-383','Braga','Portugal'), Email('bruno.phoenix@gmail.com'), Phone('253104152'), Mobile('932847455')))
'''
