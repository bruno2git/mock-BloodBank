#-*- coding: utf-8 -*-

from Elements import *
from datetime import datetime



'''
These are individual "questions" (controled user inputs) to be assembled into routines (Routines module).
Routines will be called by the main program (Main module).
'''



def define_donor_number():
    while True:
        num_input = raw_input('>>> Insira o numero de Dador: ').strip().replace(' ','')
        if num_input != '':
            donor_num = Donor_num( num_input )
            if donor_num.valid(): #requires 6 digits
                return donor_num
            else:
                print '< Numero de dador invalido >'

#print define_donor_number()



def define_sns():
    while True:
        sns_input = raw_input('>>> Insira numero do SNS: ').strip().replace(' ','')
        if sns_input != '':
            sns = SNS_num( sns_input )
            if sns.valid():
                return sns
            else:
                print '< numero do SNS invalido >'

#print define_sns()



def define_name():
    while True:
        name_input = raw_input('>>> Insira o Nome: ').strip()
        if name_input != '':
            name = Name( name_input )
            if name.valid():
                return name
            else:
                print '< detectado caracter nao aceite - nao insira ";" ou digitos >'

#print define_name()



def define_gender():
    while True:
        gender_input = raw_input('>>> Insira o Genero (M/F): ').upper().strip()
        if gender_input != '':
            gender = Gender( gender_input )
            if gender.valid():
                return gender
            else:
                print '< genero nao reconhecido - insira "M" para masculino ou "F" para feminino >'

#print define_gender()



def define_birthdate():
    while True:
        date_input = raw_input('>>> Insira data de Nascimento (dd-mm-aaaa): ').strip().replace(' ','')
        if date_input != '':
            try:
                Date_obj = datetime.strptime( date_input , '%d-%m-%Y').date()
                birthdate = Birthdate( Date_obj )
                age = birthdate.age()
                if 18 <= age <= 60:  #Para uma primeira doacao a idade limite e de 60 anos.
                    return birthdate
                else:
                    print '< idade incompativel com a doacao de sangue (%s anos) >' % age
                    while True:
                        try:
                            is_true_birthdate = raw_input('>>> (%s) e a data de nascimento correcta (S/N)? ' %birthdate).upper().strip()
                        except ValueError:
                            is_true_birthdate = raw_input('>>> A data que inseriu esta correcta (S/N)? ').upper().strip()
                        if is_true_birthdate != '':
                            if is_true_birthdate == 'S':
                                raw_input('\n< este utente nao pode ser registado como dador - operacao abortada >')
                                birthdate = None
                                return birthdate
                            elif is_true_birthdate == 'N':
                                break
                            else:
                                print '< comando nao reconhecido - "S" para Sim, "N" para Nao >'
            except ValueError: #as Error:
                    print '< data e/ou formato invalidos >' #Error
                    #Nota: E levantado ValueError para anos inferiores a 1900 pois strftime() nao os aceita.

#print define_birthdate()



def define_phone():
    while True:
        phone_input = raw_input('>>> Insira numero de Telefone (opc.): ').strip().replace(' ','')
        if phone_input != '':
            phone = Phone( phone_input )
            if phone.valid():
                return phone
            else:
                print '< numero nao reconhecido - aceita tel. fixo PT (s/ indicativo) >'
        else:
            phone = None
            return phone

#print define_phone()



def define_mobile():
    while True:
        mobile_input = raw_input('>>> Insira numero de Telemovel (opc.): ').strip().replace(' ','')
        if mobile_input != '':
            mobile = Mobile( mobile_input )
            if mobile.valid():
                return mobile
            else:
                print '< numero nao reconhecido - aceita telm. PT (s/ indicativo) >'
        else:
            mobile = None
            return mobile

#print define_mobile()



def define_email():
    while True:
        email_input = raw_input('>>> Insira o E-mail (opc.): ').lower().strip().replace(' ','') #Nota: strip() tambem remove tabs no inicio e no fim
        if email_input != '':
            email = Email ( email_input )
            if email.valid():
                return email
            else:
                print '< endereco e-mail nao reconhecido >'
        else:
            email = None
            return email

#print define_email()



def define_ABO():
    while True:
        ABO = raw_input('>>> Insira grupo ABO: ').upper().strip()
        if ABO != '':
            if match('(A|B|AB|O)$', ABO ):
                return ABO
            else:
                print '< grupo ABO nao reconhecido - aceita (A/B/AB/O) >'

#print define_ABO()



def define_Rh():
    while True:
        Rh = raw_input('>>> Insira grupo Rh: ').strip()
        if Rh != '':
            if match('(\+|\-)$', Rh):
                return Rh
            else:
                print '< grupo Rh nao reconhecido - aceita (+/-) >'

#print define_Rh()



def define_street():
    while True:
        street = raw_input('>>> Insira a Rua: ').strip()#.upper()
        if street != '':
            #street = street.replace(' DE ',' ').replace(' DA ',' ').replace(' DO ',' ').replace(' DOS ',' ').replace(' DAS ',' ')
            if street.find(';') == -1:
                return street
            else:
                print '< detectado caracter nao aceite - nao insira ";" >'

#print define_street()



def define_postcode():
    while True:
        postcode = raw_input('>>> Insira o Codigo Postal: ').strip().replace(' ','')
        if postcode != '':
            if match('[0-9]{4}-[0-9]{3}$', postcode):
                return postcode
            else:
                print '< codigo postal nao reconhecido - aceita formato "XXXX-XXX" >'

#print define_postcode()



def define_city():
    while True:
        city = raw_input('>>> Insira a Localidade: ').strip()#.upper()
        if city != '':
            #city = city.replace(' DE ',' ').replace(' DA ',' ').replace(' DO ',' ').replace(' DOS ',' ').replace(' DAS ',' ')
            if city.find(';') == -1:
                return city
            else:
                print '< detectado caracter nao aceite - nao insira ";" >'

#print define_city()



def define_country():
    while True:
        country = raw_input('>>> Insira o Pais (Portugal por omissao): ').strip()#.upper()
        if country != '':
            if country.find(';') == -1:
                return country
            else:
                print '< detectado caracter nao aceite - nao insira ";" >'
        else:
            country = 'Portugal'
            return country

#print define_country()


