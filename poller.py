import csv
import random

class Poller:
    def __init__(self, file):
        self.filename = file
        self.csvp = None
        self.total_polled = 0
    def __enter__(self):
        self.csvp = open(self.filename, 'r')
        self.fieldnames = ['name','polled','correct','attempted','excused']
        excess = []
        f_reader = csv.DictReader(self.csvp, fieldnames=self.fieldnames, restkey=excess, restval='Missing')
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
        #self.csvp = open(self.filename, 'w')
        #self.f_writer = csv.DictWriter(self.csvp, fieldnames=self.fieldnames)
        #self.f_writer.writerows(self.f_dict_list)
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
    def update(self, method_name):
        for i in range(len(self.f_dict_list)):
            if self.f_dict_list[i]['name'] == self.current_participant['name']:
                self.f_dict_list[i]['polled'] = str(1 + int(self.current_participant['polled']))
                self.total()
                if method_name != 'missing':
                    self.f_dict_list[i][method_name] = str(1 + int(self.current_participant[method_name]))
                break
        self.csvp = open(self.filename, 'w')
        self.f_writer = csv.DictWriter(self.csvp, fieldnames=self.fieldnames)
        self.f_writer.writerows(self.f_dict_list)
    def attempted(self):
        self.update('attempted')
    def correct(self):
        self.update('correct')
    def excused(self):
        self.update('excused')
    def missing(self):
        self.update('missing')
    def stop(self):
        return True
    def total(self):
        self.total_polled += 1
class Participant:
    def __init__(self, name: str, polled: int, correct: int, attempted: int, excused: int):
        self.name = name
        self.polled = polled
        self.correct = correct
        self.attempted = attempted
        self.excused = excused
    
    def __str__(self):
        return ','.join([self.name, str(self.polled), str(self.correct), str(self.attempted), str(self.excused)])