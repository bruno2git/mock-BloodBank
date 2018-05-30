#-*- coding: utf-8 -*-

from Questions import *
from DBmanager import Database



def retrieve_donor_routine( database ):
    while True:
        try:
            name_or_num = raw_input('>>> Insira o Numero, o SNS ou o Nome (completo) do dador: ').strip()
            if name_or_num != '':
                if len(name_or_num) >= 3:  #Assume tres caracteres como o minimo para um nome (completo) - (Num Dador => 6, Num SNS => 9)
                    if name_or_num.isdigit():
                        number = name_or_num
                        if len( number ) == 6:
                            if database.donor_Map.has_key( number ):
                                donor = database.Retrieve_Donor_by_number( number )
                                return donor
                            else:
                                print '< numero de dador nao atribuido >'
                        elif len( number ) == 9:
                            if database.sns_to_donor.has_key( number ):
                                donor = database.Retrieve_Donor_by_SNS( number )
                                return donor
                            else:
                                print '< numero do SNS nao encontrado >'
                        else:
                            print '< formato incorrecto - ex: SNS=123456789, N#=123456 >'
                    else:
                        name = name_or_num.upper().replace(' DE ',' ').replace(' DA ',' ').replace(' DO ',' ').replace(' DOS ',' ').replace(' DAS ',' ')
                        if database.name_to_number.has_key( name ):
                            raw_input('< o nome foi detectado >')
                            number_list = database.name_to_number[ name ]
                            if len(number_list) == 1:
                                number = number_list[0]
                                donor = database.Retrieve_Donor_by_number( number )
                                return donor
                            else:
                                raw_input('< ha mais de um dador registado com este nome >') 
                                line_list = []
                                for number in number_list:
                                    line_list.append( database.donor_Map[ number ] )
                                donor_list = database.Retrieve_Donor_from_Line_List( line_list )
                                raw_input('< os dadores de nome "%s" serao listados >' %name_or_num)
                                for i, donor in enumerate( donor_list ):
                                    raw_input('< continuar >')
                                    print '\n#================[%s]================#' %(i+1)
                                    print donor
                                    print '#====================================#'
                                while True:
                                    option = raw_input('>>> seleccione o dador pretendido (ctrl+c para cancelar): ').strip().replace(' ','')
                                    if option != '':
                                        if option.isdigit():
                                            option = int( option )
                                            if option <= len(donor_list) and option > 0:
                                                donor = donor_list[ option - 1 ]
                                                return donor
                                            else:
                                                print '< insira um numero entre 1 e %s (ctrl+c para cancelar) >' %len(donor_list)
                                        else:
                                            print '< insira o numero correspondente ao dador (ctrl+c para cancelar) >'
                        else:
                            print '< o nome "%s" nao foi encontrado >' % name_or_num
        except KeyboardInterrupt as Error:
            raise Error



def new_donation_routine( database ):
    try:
        donor = retrieve_donor_routine( database )
        print '\n====================================\n', donor
        print '===================================='
        raw_input('>>> Prosseguir com a operacao (ctrl+c para anular)? ')
        if donor.age() <= 65:
            donation = database.create_donation( donor )
            if donation != None:
                database.store_donation( donation )
                print '\n#-----------------#\n', donation, '\n#-----------------#\n'
                raw_input('>>> Registo adicionado com sucesso.')
        else:
            print '\n< A idade do dador N#%s nao lhe permite doar sangue - %s anos >' %(donor.number.num, donor.age())
            raw_input('>>> Operacao abortada.')
    except KeyboardInterrupt:
        print '< operacao cancelada pelo utilizador >'
        pass



def new_donor_routine( database ):
    name = define_name()
    while True:
        sns = define_sns()
        if database.sns_to_donor.has_key( sns.num ):
            print '< numero do SNS ja atribuido >'
        else:
            break
    ABO = define_ABO()
    Rh = define_Rh()
    bloodtype = Bloodtype( ABO, Rh )
    gender = define_gender()
    birthdate = define_birthdate()
    if birthdate != None:
        street = define_street()
        postcode = define_postcode()
        city = define_city()
        country = define_country()
        address = Address( street, postcode, city, country )
        phone = define_phone()
        mobile = define_mobile()
        email = define_email()
        contacts = Contacts( address, email, phone, mobile )
        return name, sns, bloodtype, gender, birthdate, contacts
    else:
        return None, None, None, None, None, None



def remove_from_stock_routine( database ):
    while True:
        try:
            while True:
                bloodtype = raw_input('>>> Insira o grupo sanguineo (ABO Rh): ').upper().replace(' ','')
                if bloodtype != '':
                    if match('(A\-|A\+|AB\+|AB\-|O\+|O\-)$', bloodtype):
                        break
                    else:
                        print '< grupo sanguineo nao reconhecido - insira: ABO Rh >'
            while True:
                number_of_units = raw_input('>>> Insira o numero de unidades a levantar: ').replace(' ','')
                if number_of_units != '':
                    if number_of_units.isdigit():
                        try:
                            number_of_units = int( number_of_units )
                            if number_of_units > 0:
                                break
                            else:
                                print '< numero minimo aceite: 1 >'
                        except ValueError:
                            print '< insira um numero inteiro >'
                    else:
                        print '< insira um numero >'
            donations = database.Remove_Blood_from_Stock ( bloodtype , number_of_units )
            if donations != None:
                print '>>> Foram removidas as seguintes unidades:'
                for donation in donations:
                    print 'doacao N#:', donation
                break
        except KeyboardInterrupt:
            print '< processo cancelado pelo utilizador >'
            break



def last_donation_routine( database ):
    try:
        donor = retrieve_donor_routine( database )
        donor_number = donor.number.num
        last_donation_dates = database.Get_Last_Donation_Dates_from_Donor_number( donor_number )
        if last_donation_dates != None:
            raw_input('\n>>> Data da ultima doacao do dador N#%s: (%s)' %( donor_number, last_donation_dates[0]) )
        else:
            raw_input('\n>>> o dador N#%s nao efectuou qualquer doacao' % donor_number )
    except KeyboardInterrupt:
        pass



def full_Donor_report_routine( database ):
    try:
        print '            <LEGENDA>'
        print '------------------------------------'
        print '[1] Numero de Dador'
        print '[2] Nome'
        print '[3] Numero SNS'
        print '[4] Grupo ABO'
        print '[5] Grupo Rh'
        print '[6] Sexo'
        print '[7] Data de Nascimento'
        print '[8] Rua'
        print '[9] Codigo postal'
        print '[10] Localidade'
        print '[11] Pais'
        print '[12] E-mail'
        print '[13] Telefone'
        print '[14] Telemovel'
        print '------------------------------------'
        print '(ctrl+c) >> Retroceder'
        print '------------------------------------'
        while True:
            rawInput = raw_input('>>> Insira os campos a imprimir, pela ordem pretendida, separados por ",": ').strip().replace(' ','')
            if rawInput != '':
                if rawInput[ len(rawInput) -1 ] == ',':
                    rawInput = rawInput[ : len(rawInput) -1 ]
                raw_list = rawInput.split(',')
                field_list = []
                try:
                    valid = True
                    for char in raw_list:
                        char = int(char)
                        field_list.append( char )
                        if char < 1 or char > 14:
                            valid = False
                            break
                    if valid == True:
                        break
                    else:
                        print '< insira numeros entre 1 e 14 >'
                except ValueError:
                    print '< insira os numeros separados por virgulas - ex: 1,2,3 >'
        while True:
            print_on_screen = raw_input('>>> Mostrar a listagem no ecra (S/N)? ').upper().strip()
            if print_on_screen != '':
                if print_on_screen == 'S':
                    print_on_screen = True
                    break
                elif print_on_screen == 'N':
                    print_on_screen = False
                    break
                else:
                    print '< insira "S" para Sim e "N" para Nao >'
        raw_input('< o processo de listagem tera inicio >')
        database.full_Donor_report( field_list, print_on_screen )
        raw_input('< listagem concluida com sucesso - consulte o relatorio na pasta Reports >')
    except KeyboardInterrupt:
        print '< processo cancelado pelo utilizador >'
        


def full_Donation_report_routine ( database ):
    try:
        print '             <LEGENDA>'
        print '------------------------------------'
        print '[1] Numero da Doacao'
        print '[2] Data de Entrada'
        print '[3] Numero do Dador'
        print '[4] Grupo ABO'
        print '[5] Grupo Rh'
        print '[6] Centro de Colheita'
        print '[7] Data de Saida'
        print '------------------------------------'
        print '(ctrl+c) >> Retroceder'
        print '------------------------------------'
        while True:
            rawInput = raw_input('>>> Insira os campos a imprimir, pela ordem pretendida, separados por ",": ').strip().replace(' ','')
            if rawInput != '':
                if rawInput[ len(rawInput) -1 ] == ',':
                    rawInput = rawInput[ : len(rawInput) -1 ]
                raw_list = rawInput.split(',')
                field_list = []
                try:
                    valid = True
                    for char in raw_list:
                        char = int(char)
                        field_list.append( char )
                        if char < 1 or char > 7:
                            valid = False
                            break
                    if valid == True:
                        break
                    else:
                        print '< insira numeros entre 1 e 7 >'
                except ValueError:
                    print '< insira os numeros separados por virgulas - ex: 1,2,3 >'
        while True:
            print_on_screen = raw_input('>>> Mostrar a listagem no ecra (S/N)? ').upper().strip()
            if print_on_screen != '':
                if print_on_screen == 'S':
                    print_on_screen = True
                    break
                elif print_on_screen == 'N':
                    print_on_screen = False
                    break
                else:
                    print '< insira "S" para Sim e "N" para Nao >'
        raw_input('< o processo de listagem tera inicio >')
        database.full_Donation_report( field_list, print_on_screen )
        raw_input('< listagem concluida com sucesso - consulte o relatorio na pasta Reports >')
    except KeyboardInterrupt:
        print '< processo cancelado pelo utilizador >'



def get_stock_routine( database ):
    while True:
        try:
            bloodtype = raw_input('>>> Insira grupo sanguineo (ABO+Rh): ').upper().strip().replace(' ','')
            if bloodtype != '':
                stock = database.Get_Stock_from_bloodtype( bloodtype )
                if stock != None:
                    raw_input('\n>>> Dispomos de %s unidades de sangue %s Rh%s.' %( stock, bloodtype[ : len(bloodtype)-1 ], bloodtype[ len(bloodtype)-1 ]) )
                    break
        except KeyboardInterrupt:
            break



def donation_count_between_dates_routine( database ):
    try:
        while True:
            date_input = raw_input('>>> Insira a data de Inicio (dd-mm-aaaa): ').strip().replace(' ','')
            if date_input != '':
                try:
                    Ini_Date = datetime.strptime( date_input , '%d-%m-%Y').date()
                    break
                except ValueError:
                    print '< data e/ou formato invalidos >'
        while True:
            date_input = raw_input('>>> Insira a data de Fim (dd-mm-aaaa): ').strip().replace(' ','')
            if date_input != '':
                try:
                    End_Date = datetime.strptime( date_input , '%d-%m-%Y').date()
                    if End_Date >= Ini_Date:
                        break
                    else:
                        print '< limite superior deve ser maior que ou igual a limite inferior >'
                except ValueError:
                    print '< data e/ou formato invalidos >'
        Count = database.Count_Donations_between_dates( Ini_Date, End_Date )
        raw_input( '\n>>> Foram efectuadas %s doacoes entre %s e %s' %( Count, Ini_Date.strftime('%d-%m-%Y'), End_Date.strftime('%d-%m-%Y') ) )
    except KeyboardInterrupt:
        print '< operacao abortada pelo utilizador >'



def donation_numbers_between_dates_routine( database ):
    try:
        while True:
            date_input = raw_input('>>> Insira a data de Inicio (dd-mm-aaaa): ').strip().replace(' ','')
            if date_input != '':
                try:
                    Ini_Date = datetime.strptime( date_input , '%d-%m-%Y').date()
                    break
                except ValueError:
                    print '< data e/ou formato invalidos >'
        while True:
            date_input = raw_input('>>> Insira a data de Fim (dd-mm-aaaa): ').strip().replace(' ','')
            if date_input != '':
                try:
                    End_Date = datetime.strptime( date_input , '%d-%m-%Y').date()
                    if End_Date >= Ini_Date:
                        break
                    else:
                        print '< limite superior deve ser maior que ou igual a limite inferior >' 
                except ValueError:
                    print '< data e/ou formato invalidos >'
        Donation_list = database.Get_Donation_List_between_dates( Ini_Date, End_Date )
        if Donation_list != []:
            raw_input('\n>>> Entre %s e %s foram efectuadas as doacoes N#%s a N#%s ' %(Ini_Date.strftime('%d-%m-%Y'), End_Date.strftime('%d-%m-%Y'), Donation_list[0], Donation_list[ len(Donation_list)-1 ]))
            while True:
                print_list = raw_input('>>>Imprimir lista de doacoes (S/N)? ').upper()
                if print_list != '':
                    if print_list == 'S':
                        print '------------------------------------'
                        for donation in Donation_list:
                            print donation
                        print '------------------------------------'
                        break
                    elif print_list == 'N':
                        break
                    else:
                        print '< insira "S" para Sim e "N" para Nao >'
        else:
            print '\n< nao foram feitas doacoes entre %s e %s >' %(Ini_Date.strftime('%d-%m-%Y'), End_Date.strftime('%d-%m-%Y'))
    except KeyboardInterrupt:
        print '< operacao abortada pelo utilizador >'



def global_Donor_stat_routine( database ):
    try:
        headlines = ['[Grupo sanguineo]', '[Sexo]', '[Localidade]', '[Pais]']
        lengths = [0, 0, 0, 0]
        Dict_list = database.Global_Donor_stats( [[4,5],[6],[10],[11]], concat_sep='' )
        for i in xrange( len(Dict_list) ):
            for key in Dict_list[i].iterkeys():
                if len(key) > lengths[i]:
                    lengths[i] = len(key)
            print '\n------------------------------------'
            print '%s' %headlines[i].center(36)
            raw_input('------------------------------------')
            for value, frequency in Dict_list[i].iteritems():
                Global = '%.2f%%' %frequency
                string = '%s:%s' %( value.ljust(lengths[i]), Global.rjust(8))
                print '%s' %string.center(36)
            print '------------------------------------'
    except KeyboardInterrupt:
        print '< operacao interrompida pelo utilizador >'



def global_Donation_stat_routine( database ):
    try:
        headlines = ['[Grupo sanguineo]', '[Centro]']
        lengths = [0, 0]
        Dict_list = database.Global_Donation_stats( [[4,5],[6]], concat_sep='' )
        for i in xrange( len(Dict_list) ):
            for key in Dict_list[i].iterkeys():
                if len(key) > lengths[i]:
                    lengths[i] = len(key)
            print '\n------------------------------------'
            print '%s' %headlines[i].center(36)
            raw_input('------------------------------------')
            for value, frequency in Dict_list[i].iteritems():
                Global = '%.2f%%' %frequency
                string = '%s:%s' %( value.ljust(lengths[i]), Global.rjust(8))
                print '%s' %string.center(36)
            print '------------------------------------'
    except KeyboardInterrupt:
        print '< operacao interrompida pelo utilizador >'



def Donation_Stats_within_interval_routine( database ):
    try:
        while True:
            date_input = raw_input('>>> Insira a data de Inicio (dd-mm-aaaa): ').strip().replace(' ','')
            if date_input != '':
                try:
                    Ini_Date = datetime.strptime( date_input , '%d-%m-%Y').date()
                    break
                except ValueError:
                    print '< data e/ou formato invalidos >'
        while True:
            date_input = raw_input('>>> Insira a data de Fim (dd-mm-aaaa): ').strip().replace(' ','')
            if date_input != '':
                try:
                    End_Date = datetime.strptime( date_input , '%d-%m-%Y').date()
                    if End_Date >= Ini_Date:
                        break
                    else:
                        print '< limite superior deve ser maior que ou igual a limite inferior >'
                except ValueError:
                    print '< data e/ou formato invalidos >'
        headlines = ['[Grupo sanguineo]', '[Centro]']
        lengths = [0, 0]
        Dict_list = database.Donation_Stats_within_interval( [[4,5],[6]], Ini_Date, End_Date )
        for i in xrange( len(Dict_list) ):
            for key in Dict_list[i].iterkeys():
                if len(key) > lengths[i]:
                    lengths[i] = len(key)
            print '\n------------------------------------'
            print '%s' %headlines[i].center(36)
            raw_input('------------------------------------')
            for value, frequency in Dict_list[i].iteritems():
                local = '%.2f%%' %frequency[0]
                globl = '(%.2f%%)' %frequency[1] #frequency[1] corresponde à percentagem face ao total
                string = '%s:%s%s' %( value.ljust(lengths[i]), local.rjust(8), globl.rjust(9))
                print '%s' %string.center(36)
            print '------------------------------------'
    except KeyboardInterrupt:
        print '< operacao interrompida pelo utilizador >'



def Donor_Stats_within_interval_routine( database ):
    try:
        while True:
            age_input = raw_input('>>> Insira a idate limite inferior: ').strip().replace(' ','')
            if age_input != '':
                try:
                    ini_age = int( age_input )
                    if ini_age >= 18:
                        break
                    else:
                        print '< idade minima = 18 >' #não defini limite maximo porque os registos dos dadores permanecem na DB após a idade máxima
                except ValueError:
                    print '< insira um numero inteiro >'
        while True:
            age_input = raw_input('>>> Insira a idate limite superior: ').strip().replace(' ','')
            if age_input != '':
                try:
                    end_age = int( age_input )
                    if end_age >= 18:
                        if end_age >= ini_age:
                            break
                        else:
                            print '< limite superior deve ser maior que ou igual a limite inferior >' 
                    else:
                        print '< idade minima = 18 >'
                except ValueError:
                    print '< insira um numero inteiro >'
        headlines = ['[Grupo sanguineo]', '[Sexo]', '[Localidade]', '[Pais]']
        lengths = [0, 0, 0, 0]
        Dict_list = database.Donor_Stats_within_interval( [[4,5],[6],[10],[11]], ini_age, end_age )
        for i in xrange( len(Dict_list) ):
            for key in Dict_list[i].iterkeys():
                if len(key) > lengths[i]:
                    lengths[i] = len(key)
            print '\n------------------------------------'
            print '%s' %headlines[i].center(36)
            raw_input('------------------------------------')
            for value, frequency in Dict_list[i].iteritems():
                local = '%.2f%%' %frequency[0]
                globl = '(%.2f%%)' %frequency[1] #frequency[1] corresponde à percentagem face ao total
                string = '%s:%s%s' %( value.ljust(lengths[i]), local.rjust(8), globl.rjust(9))
                print '%s' %string.center(36)
            print '------------------------------------'
    except KeyboardInterrupt:
        print '< operacao interrompida pelo utilizador >'



def donation_list_routine( database ):
    try:
        donor = retrieve_donor_routine( database )
        if database.donor_to_donation.has_key( donor.number.num ):
            raw_list = database.donor_to_donation[ donor.number.num ]
            int_list = []
            for raw_number in raw_list:
                int_list.append( int(raw_number) )
            donation_list = database.Retrieve_Donation_from_Line_List( int_list )
            raw_input('\n>>> O dador N#%s efectuou %s doacoes >' %( donor.number.num, len(donation_list) ))
            raw_input('>>> Iniciar listagem (ctrl+c para cancelar) >')
            for i, donation in enumerate( donation_list ):
                raw_input('< continuar >')
                print '\n#==========[%s]==========#' %(i+1)
                print donation
                print '#=======================#'
        else:
            print '\n>>> O dador N#%s nao efectuou qualquer doacao >' %donor.number.num
    except KeyboardInterrupt:
        print '< operacao abortada pelo utilizador >'



####################=<WORK IN PROGRESS>=####################

def edit_donor_info( database, donor ): 
    pass


def has_donor_number_routine( database ):
    pass


def has_sns_number_routine( database ):
    pass


def stock_life( database ):
    pass


def age_stats( database ):
    pass


def retrieve_donor_by_field_value_routine( database ):
    pass


def retrieve_donation_by_field_value_routine( database ):
    pass


def retrieve_donation_by_number_routine( database ):
    pass


############################################################
