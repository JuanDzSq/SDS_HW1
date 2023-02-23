import csv
import random

"""Contains the classes Poller and Participant to be used in randopoll.py.

Poller has the functionality of reading a given csv file, and randomly polls participants that have the smallest
amount of polled count. Based on command input in the randopoll.py program, it increases corresponding counts by one.
When the quit method is called, the randopoll.py program ends and the csv file is re-written with the new data.
The Participant class is a container for each participant information in the csv file.
"""
class Poller:
    """Randomly polls participants from a csv file, and has methods to change its data.
    
    With the purpose of randomly polling participants, and recording their reaction, 
    it reads a given csv file with participantion count data and randomly polls those 
    with the least polled count. A method is used depending on the reaction of the 
    participant, them being: attempted, answered correctly, excused, and missing.
    The quit method serving to end the program that is using a Poller instance.

    Attributes:
        _filename: name of the csv file to be manipulated.
        _opener: optional file mock opener.
        csvp: contains the open csv file.
        total_polled: an integer count of how many polls has been made by the instance.
        f_participant_list: a list containing the read contents of the csv file.
        fieldnames: the names of the required fields for each line of the csv file.
        current_participant: a randomly chosen participant by the poller.
    """
    def __init__(self, _file, opener=open):
        """Initializes a Poller instance for a corresponding file.

        Args:
            _file: a csv file name.
            opener: optional mock opener, used for testing.
        """
        self._filename = _file
        self._opener = opener
        self.csvp = None
        self.total_polled = 0
        self.f_participant_list = []

    def __enter__(self):
        """Opens the csv file _file, and if it has the correct format for each line,
        it copies the contents to f_participant_list. 

        The csv file must have the correct format for each line. There must not be any 
        excess or missing fields, else an error will be raised.
        Example of correct format: "Jesus,3,0,0,0".
        Example of incorrect format: "Jesus,3,0,0".

        Raises:
            ValueError: the csv file does not have the required formating for the program.
              It either has missing or excess fields in one of its lines.
        """
        self.csvp = self._opener(self._filename, 'r')
        self.fieldnames = ['name','polled','correct','attempted','excused']
        excess = []
        f_reader = csv.DictReader(self.csvp, fieldnames=self.fieldnames, 
                                  restkey=excess, restval='Missing')
        if len(excess):  # True if there are excess fields in the csv file.
            raise ValueError()
        for line in f_reader:
            if any(val in ('Missing') for val in line.values()):  # True if there are any missing fields in the csv file.
                                                                  # From https://stackoverflow.com/questions/1278749/how-do-i-detect-missing-fields-in-a-csv-_file-in-a-pythonic-way
                raise ValueError()
            self.f_participant_list.append(Participant(line['name'], line['polled'], 
                                           line['correct'], line['attempted'], line['excused']))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Re-writes the csv file to reflect the changes submited during the running of randopoll.py"""
        with self._opener(self._filename, 'w') as csvp:
            f_writer = csv.writer(csvp)
            for participant in self.f_participant_list:
                f_writer.writerow([participant.name, participant.polled, participant.correct, 
                                        participant.attempted, participant.excused])
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Chooses the next participant for the program.

        Randomly picks a participant in f_participant_list from those that have the least amount
        of polled count. For example, with two participants with 3 polls and one with 5, it will randomly pick 
        from the ones with 3 polls.

        Returns:
            A string formatted Participant object that corresponds with the randomly chosen participant.
            For example: "Isabelle,3,2,0,0,1"
        """
        poll_count_list = [participant.polled for participant in self.f_participant_list]
        lowest_poll_count = min(poll_count_list)  # Gets the lowest polled count among all participants.
        lowest_polled_participants = []
        for participant in self.f_participant_list:
            if participant.polled == lowest_poll_count:
                lowest_polled_participants.append(participant)  # Added to list if the participant has lowest polled count.
        random_int = random.randint(0, len(lowest_polled_participants) - 1)
        self.current_participant = lowest_polled_participants[random_int]  # Gets random participant with the lowest polled count.
        return str(self.current_participant)
    
    """
    I like your idea to use a helper method for each of the methods that share functionality! Here is some feedback:
    Having to loop through our participants list every time we update an individual can get costly if we have a lot of
    participants. We could consider updating our self.current_particpant attribute directly bc it is 
    the same object (more technically it "points to" see https://www.pythonmorsels.com/variables-are-pointers/)
    as the current participant found in the list.
    """
    def update(self, method_name):
        """Updates the randomly polled participant in f_participant_list with a corresponding given command.

        This method is used by the program command methods (except quit()) to increase the corresponding count,
        and the count of polled, to the current participant chosen by random polling.

        Args:
            method_name: string of the method name submited as a command in the program (except for quit()).
        """
        for i in range(len(self.f_participant_list)):
            if self.f_participant_list[i].name == self.current_participant.name:
                self.f_participant_list[i].polled = 1 + self.current_participant.polled  # Increases poll count by 1. # try "+=" syntax here.
                self.total_increase()
                if method_name != 'missing':
                    setattr(self.f_participant_list[i], method_name, 
                            1 + getattr(self.f_participant_list[i], method_name))  # Increases chosen method's count by 1.
                break
    
    def attempted(self):
        """Increases the polled and attempted count of corresponding participant by one with the update method."""
        self.update('attempted')
    
    def correct(self):
        """Increases the polled and correct count of corresponding participant by one with the update method."""
        self.update('correct')
    
    def excused(self):
        """Increases the polled and excused count of corresponding participant by one with the update method."""
        self.update('excused')
    
    def missing(self):
        """Increases only the polled count of corresponding participant by one with the update method."""
        self.update('missing')
    
    def stop(self):
        """Ends the randopoll.py program."""
        return True
    
    def total_increase(self):
        """Keeps track of the total amount of random polling done in the program."""
        self.total_polled += 1
    
    def total(self):
        return self.total_polled
    
class Participant:
    """Contains the data of a participant from a csv file.

    Attributes:
        name: string of name of participant.
        polled: integer number count of times the participant has been polled.
        correct: integer number count of times the participant was correct.
        attempted: integer number count of times the participant attempted, but wasn't correct.
        excuesed: integer number count of times the participant has been excuesed. 
    """
    def __init__(self, name: str, polled, correct, attempted, excused):
        self.name = name
        self.polled = int(polled)
        self.correct = int(correct)
        self.attempted = int(attempted)
        self.excused = int(excused)
    
    def __str__(self):
        """Formats Participant object as: 'Name,poll count,correct count,attempted count,excused count'."""
        return ','.join([self.name, str(self.polled), str(self.correct),
                         str(self.attempted), str(self.excused)])
        