#-*- coding: utf-8 -*-

from DBmanager import *
from Routines import *



def Main():
    print '=================< BANCO DE SANGUE >================='
    print '*****************************************************'
    print '********** BEM VINDO A ESTA BASE DE DADOS ***********'
    print '*****************************************************'
    #Instantiating database
    database = Database()
    #Loading database (mounting some information into memory)
    database.load_donorDB()
    database.load_donationDB()
    database.load_approved_centers()
    #Presenting list of approved centers to user
    print 'Lista de centros aprovados:'
    print '------------------------------------'
    for i, center in enumerate( database.approved_centers ):
        print ' [%s] Centro de %s' %(i+1, center)
    print '------------------------------------'
    while True:
        option = raw_input('>>> Centro de colheitas: ').strip().replace(' ','')
        if option != '':
            if option.isdigit():
                try:
                    option = int(option)
                    if option > 0 and option <= len(database.approved_centers):
                        database.center = database.approved_centers[ option -1 ]
                        raw_input( '>>> Seleccionado o Centro de: [%s]' % database.center )
                        #raw_input('< este centro estara associado a todas as doacoes >')
                        break
                    else:
                        print '< insira um numero entre 1 e %s >' % len(database.approved_centers)
                except ValueError:
                    print '< insira o numero correspondente ao centro >'
            else:
                print '< insira um numero >'
    try:
        returned = True   #indica se o menu deve ser impresso (se o utilizador esta a retornar de algum sub-menu)
        while True:
            if returned:
                print '\n=========< MENU PRINCIPAL >=========' #podia ficar tudo num so print, separando com "\n" mas assim le-se melhor.
                print '# [1] Registar doacao              #'
                print '# [2] Registar novo dador          #'
                print '# [3] Retirar unidades do stock    #'
                print '# [4] Pesquisas                    #'
                print '# [5] Relatorios                   #'
                print '# [6] Estatisticas                 #'
                print '#----------------------------------#'
                print '# [0] Sair                         #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                try:
                    option = int( option ) #passo desnecessario; podia comparar com "1", "2", etc.
                    if option == 1:
                        print '\n=========[REGISTO DE DOACAO]========'
                        new_donation_routine ( database )
                        returned = True    
                    elif option == 2:
                        try:
                            print '\n========[ REGISTO DE DADOR ]========'
                            name, sns, bloodtype, gender, birthdate, contacts = new_donor_routine( database )
                            if name != None:
                                donor = database.create_donor( name, sns, bloodtype, gender, birthdate, contacts )
                                print '\n===========< Novo dador >==========='
                                print donor                                        #falta editar antes de guardar
                                print '===================================='
                                database.store_donor( donor )
                                raw_input('\n>>> Dador registado com sucesso' )
                        except KeyboardInterrupt:
                            pass
                        returned = True
                    elif option == 3:
                        print '\n=====[ LEVANTAMENTO DE SANGUE ]====='
                        remove_from_stock_routine( database )
                        returned = True
                    elif option == 4:
                        sub_menu_queries( database )
                        returned = True
                    elif option == 5:
                        sub_menu_reports( database )
                        returned = True
                    elif option == 6:
                        sub_menu_stats( database )
                        returned = True
                    elif option == 0:
                        raise KeyboardInterrupt
                    else:
                        print '< insira o numero da operacao pretendida >'
                        
                except ValueError:
                    print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt as Error:
        raise Error




def sub_menu_queries( database ):
    try:
        returned = True
        while True:
            if returned:
                print '\n===========< PESQUISAS >============'
                print '# [1] Data da ultima doacao        #'
                print '# [2] Lista de doacoes do dador    #'
                print '# [3] Stock por Grupo              #'
                print '# [4] Stock completo               #'
                print '# [5] Doacoes no Intervalo         #'
                print '# [6] ID Doacoes no Intervalo      #'
                print '#----------------------------------#'
                print '# [0] Retorno                      #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                if not option.isdigit():
                    print '< insira o numero da operacao pretendida >' 
                else:
                    option = int(option)
                    if option == 1:
                        print '\n=======[Data da ultima doacao]======'
                        last_donation_routine( database )
                        returned = True
                    elif option == 2:
                        print '\n====[Lista de doacoes do dador]====='
                        donation_list_routine( database )
                        raw_input('continuar >>>')
                        returned = True
                    elif option == 3:
                        print '\n==========[Stock por Grupo]========='
                        get_stock_routine( database )
                        returned = True
                    elif option == 4:
                        print '\n===========[Stock completo]========='
                        database.blood_stock_report()
                        raw_input('continuar >>>')
                        returned = True
                    elif option == 5:
                        print '\n========[Doacoes no Intervalo]======'
                        donation_count_between_dates_routine( database )
                        raw_input('continuar>>>')
                        returned = True
                    elif option == 6:
                        print '\n======[ID Doacoes no Intervalo]====='
                        donation_numbers_between_dates_routine( database )
                        raw_input('continuar>>>')
                        returned = True
                    elif option == 0:
                        return
                    else:
                        print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt:
        return



def sub_menu_reports( database ):
    try:
        returned = True
        while True:
            if returned:
                print '\n===========< RELATORIOS >==========='
                print '# [1] Listagem completa            #'
                #print '# [2] Listagem por intervalo       #' #######
                #print '# [3] Listagem diaria              #' #######
                print '#----------------------------------#'
                print '# [0] Retorno                      #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                if not option.isdigit():
                    print '< insira o numero da operacao pretendida >' 
                else:
                    option = int(option)
                    if option == 1:
                        sub_menu_full_report( database )
                        returned = True
                        '''
                        elif option == 2:
                            sub_menu_report_by_interval( database )
                            returned = True
                        '''
                    elif option == 0:
                        return
                    else:
                        print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt:
        return


def sub_menu_full_report( database ):
    try:
        returned = True
        while True:
            if returned:
                print '\n========< LISTAGEM COMPLETA >======='
                print '# [1] Dadores                      #'
                print '# [2] Doacoes                      #'
                print '#----------------------------------#'
                print '# [0] Retorno                      #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                if not option.isdigit():
                    print '< insira o numero da operacao pretendida >' 
                else:
                    option = int(option)
                    if option == 1:
                        print '\n=======[ LISTAGEM - DADORES ]======='
                        full_Donor_report_routine( database )
                        returned = True
                    elif option == 2:
                        print '\n=======[ LISTAGEM - DOACOES ]======='
                        full_Donation_report_routine( database )
                        returned = True
                    elif option == 0:
                        return
                    else:
                        print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt:
        return



'''
def sub_menu_report_by_interval( database ):
    try:
        returned = True
        while True:
            if returned:
                print '\n=====< LISTAGEM POR INTERVALO >====='
                print '# [1] Dadores                      #'
                print '# [2] Doacoes                      #'
                print '#----------------------------------#'
                print '# [0] Retorno                      #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                if not option.isdigit():
                    print '< insira o numero da operacao pretendida >' 
                else:
                    option = int(option)
                    if option == 1:
                        print '\n=======[ LISTAGEM - DADORES ]======='
                        ( database )
                        returned = True
                    elif option == 2:
                        print '\n=======[ LISTAGEM - DOACOES ]======='
                        full_Donation_report_routine( database )
                        returned = True
                    elif option == 0:
                        return
                    else:
                        print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt:
        return
'''




def sub_menu_stats( database ):
    try:
        returned = True
        while True:
            if returned:
                print '\n==========< Estatisticas >=========='
                print '# [1] Estatistica global           #'
                print '# [2] Estatistica por intervalo    #'
                #print '# [4] Estatistica por idade        #' #######
                print '#----------------------------------#'
                print '# [0] Retorno                      #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                if not option.isdigit():
                    print '< insira o numero da operacao pretendida >' 
                else:
                    option = int(option)
                    if option == 1:
                        sub_menu_global_stat( database )
                        returned = True
                    elif option == 2:
                        sub_menu_stat_by_interval( database )
                        returned = True
                    elif option == 0:
                        return
                    else:
                        print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt:
        return



def sub_menu_global_stat( database ):
    try:
        returned = True
        while True:
            if returned:
                print '\n=======< ESTATISTICA GLOBAL >======='
                print '# [1] Dadores                      #'
                print '# [2] Doacoes                      #'
                print '#----------------------------------#'
                print '# [0] Retorno                      #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                if not option.isdigit():
                    print '< insira o numero da operacao pretendida >' 
                else:
                    option = int(option)
                    if option == 1:
                        print '\n=====[ ESTATISTICA - DADORES ]======'
                        global_Donor_stat_routine( database )
                        raw_input('continuar >>>')
                        returned = True
                    elif option == 2:
                        print '\n=====[ ESTATISTICA - DOACOES ]======'
                        global_Donation_stat_routine( database )
                        raw_input('continuar >>>')
                        returned = True
                    elif option == 0:
                        return
                    else:
                        print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt:
        return





def sub_menu_stat_by_interval( database ):
    try:
        returned = True
        while True:
            if returned:
                print '\n===< ESTATISTICA POR INTERVALO >===='
                print '# [1] Dadores                      #'
                print '# [2] Doacoes                      #'
                print '#----------------------------------#'
                print '# [0] Retorno                      #'
                print '===================================='
                returned = False
            option = raw_input('>>> Operacao numero: ').strip()
            if option != '':
                if not option.isdigit():
                    print '< insira o numero da operacao pretendida >' 
                else:
                    option = int(option)
                    if option == 1:
                        print '\n=====[ ESTATISTICA - DADORES ]======'
                        Donor_Stats_within_interval_routine( database )
                        raw_input('continuar >>>')
                        returned = True
                    elif option == 2:
                        print '\n=====[ ESTATISTICA - DOACOES ]======'
                        Donation_Stats_within_interval_routine( database )
                        raw_input('continuar >>>')
                        returned = True
                    elif option == 0:
                        return
                    else:
                        print '< insira o numero da operacao pretendida >'
    except KeyboardInterrupt:
        return



def trabalho_realizado_por():
    print '             Bruno Silva        PG25220'
    print '             Catarina Correia   PG19643'
    print '             Dora Henriques      ID4893'
    print '             Sara Martins       PG23820'


if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        try:
            print '\n*****************************************************'
            print '************ << IAP @Bioinfo @UMinho >> *************'
            print '*****************************************************'
            trabalho_realizado_por()
            raw_input('*****************************************************')
        except KeyboardInterrupt:
            pass
