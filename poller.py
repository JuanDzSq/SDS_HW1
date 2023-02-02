import csv
import random

class Poller:
    def __init__(self, file):
        self.filename = file
        self.csvp = None
    
    def __enter__(self):
        self.csvp = open(self.filename)
        self.fieldnames = ['name','polled','correct','attempted','excused']
        excess = []
        f_reader = csv.DictReader(self.csvp, fieldnames=self.fieldnames, restkey=excess, restval='Missing')
        self.f_writer = csv.DictWriter(self.csvp, fieldnames=self.fieldnames, delimitir=',')

        if len(excess):
            # Throw ValueError
            pass
        self.f_dict_list = []
        for line in f_reader:
            if any(val in ('Missing') for val in line.values()):    # From https://stackoverflow.com/questions/1278749/how-do-i-detect-missing-fields-in-a-csv-file-in-a-pythonic-way
                # Throw ValueError
                pass
            self.f_dict_list.append(line)                
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.csvp.close()

    def __iter__(self):
        return self
    
    def __next__(self):
        polled_list = []
        for dictionary in self.f_dict_list:
            polled_list.append(int(dictionary['polled']))
        lowest_num = min(polled_list)
        #del polled_list
        low_polled = []
        for dictionary in self.f_dict_list:
            if int(dictionary['polled']) == lowest_num:
                low_polled.append(dictionary)
        rando_int = random.randint(0, len(low_polled) - 1)
        self.current_participant = low_polled[rando_int]
        current_participant_str = Participant(self.current_participant['name'], int(self.current_participant['polled']), int(self.current_participant['correct']), 
                        int(self.current_participant['attempted']), int(self.current_participant['excused']))
        return current_participant_str
    
    def attempted(self):
        # Use self.current_participant
        # Modify self.f_dict_list only
        for dictionary in self.f_dict_list:
            if dictionary['name'] == self.current_participant['name']:
                dictionary['attempted'] = str(1 + int(self.current_participant['attempted']))
                dictionary['polled'] = str(1 + int(self.current_participant['polled']))
            break
        for line in self.f_dict_list:
            self.f_writer.writerow(line)

    #def correct():

    #def excused():

    #def missing():

    #def stop():

    #def total():
        

class Participant:
    def __init__(self, name: str, polled: int, correct: int, attempted: int, excused: int):
        self.name = name
        self.polled = polled
        self.correct = correct
        self.attempted = attempted
        self.excused = excused
    
    def __str__(self):
        return ','.join([self.name, str(self.polled), str(self.correct), str(self.attempted), str(self.excused)])