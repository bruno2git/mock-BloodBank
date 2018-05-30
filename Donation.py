#-*- coding: utf-8 -*-

from Elements import *



class Donation:
    '''
    Instantiates a blood donation record
    '''
    def __init__(self, donation_num, IN_date, donor_num, bloodtype, center, OUT_date = None):
        self.number = donation_num    #(str)
        self.IN = IN_date             #(datetime.date instance)
        self.donor = donor_num        #(str)
        self.type = bloodtype         #(Bloodtype instance)
        self.ABO = bloodtype.ABO      #(str)
        self.Rh = bloodtype.Rh        #(str)
        self.center = center          #(str)
        self.OUT = OUT_date           #(datetime.date instance or None)



    def __repr__(self):
        return 'Donation: %s\nDate: %s\nDonor: %s\nBlood type: %s\nCenter: %s\nOut date: %s' %(self.number, self.IN.strftime('%d-%m-%Y'), self.donor, self.type, self.center, self.OUT.strftime('%d-%m-%Y') if self.OUT != None else self.OUT)



    def encode(self):
        return '%s;%s;%s;%s;%s;%s;%s\n' %(self.number, self.IN.strftime('%d-%m-%Y'), self.donor, self.ABO, self.Rh, self.center, self.OUT.strftime('%d-%m-%Y') if self.OUT != None else self.OUT)



'''
D = Donation( '1', date.today(), '123456', Bloodtype('O','+'), 'Braga')
'''
