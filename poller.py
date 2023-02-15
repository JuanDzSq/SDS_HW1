import csv
import random

class Poller:
    def __init__(self, _file, opener=open):
        self._filename = _file
        self._opener = opener
        self.csvp = None
        self.total_polled = 0
        self.f_participant_list = []
    def __enter__(self):
        self.csvp = self._opener(self._filename, 'r')
        self.fieldnames = ['name','polled','correct','attempted','excused']
        excess = []
        f_reader = csv.DictReader(self.csvp, fieldnames=self.fieldnames, restkey=excess, restval='Missing')
        if len(excess):
            # TO DO (Juan) Add a throw ValueError
            pass
        for line in f_reader:
            if any(val in ('Missing') for val in line.values()):    # From https://stackoverflow.com/questions/1278749/how-do-i-detect-missing-fields-in-a-csv-_file-in-a-pythonic-way
                # TO DO (Juan) Add a throw ValueError
                pass
            self.f_participant_list.append(Participant(line['name'], line['polled'], line['correct'], line['attempted'], line['excused']))
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.csvp = self._opener(self._filename, 'w')
        self.f_writer = csv.writer(self.csvp)
        for participant in self.f_participant_list:
            self.f_writer.writerow([participant.name, participant.polled, participant.correct, participant.attempted, participant.excused])
        self.csvp.close()
    def __iter__(self):
        return self
    def __next__(self):
        polled_list = [participant.polled for participant in self.f_participant_list]
        lowest_num = min(polled_list)
        low_polled = []
        for participant in self.f_participant_list:
            if participant.polled == lowest_num:
                low_polled.append(participant)
        rando_int = random.randint(0, len(low_polled) - 1)
        self.current_participant = low_polled[rando_int]
        return str(self.current_participant)
    def update(self, method_name):
        for i in range(len(self.f_participant_list)):
            if self.f_participant_list[i].name == self.current_participant.name:
                self.f_participant_list[i].polled = 1 + self.current_participant.polled
                self.total_increase()
                if method_name != 'missing':
                    setattr(self.f_participant_list[i], method_name, 1 + getattr(self.f_participant_list[i], method_name)) 
                break
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
    def total_increase(self):
        self.total_polled += 1
    def total(self):
        return self.total_polled
    
    def mock_writer(self):
        with self._opener(self._filename, 'w') as f:
            for participant in self.f_participant_list:
                f.write(str(participant))
class Participant:
    def __init__(self, name: str, polled, correct, attempted, excused):
        self.name = name
        self.polled = int(polled)
        self.correct = int(correct)
        self.attempted = int(attempted)
        self.excused = int(excused)
    
    def __str__(self):
        return ','.join([self.name, str(self.polled), str(self.correct), str(self.attempted), str(self.excused)])
        
# Write down comments