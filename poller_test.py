import pytest
from poller import *

def mock_opener(mock_file_input):
    class Opener:
        input = mock_file_input
        mock_file_output = []

        def __init__(self, file, mode=""):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_value, traceback):
            pass
        def __iter__(self):
            return iter(Opener.input)
        def write(self, text):
            Opener.mock_file_output.append(text)
    return Opener    
        
def test_participant():
    participant = Participant("Isabelle",5,3,1,1)
    assert str(participant) == "Isabelle,5,3,1,1"

def test_attempted():
    mock = mock_opener(["Isabelle,0,0,0,0"])
    p = Poller('participants.csv', mock)
    p.__enter__()
    p.__iter__()
    p.__next__()
    p.attempted()
    p.mock_writer()
    assert mock.mock_file_output == ['Isabelle,1,0,1,0'], "The attempted method didn't work"

def test_correct():
    mock = mock_opener(["Isabelle,0,0,0,0"])
    p = Poller('participants.csv', mock)
    p.__enter__()
    p.__iter__()
    p.__next__()
    p.correct()
    p.mock_writer()
    assert mock.mock_file_output == ['Isabelle,1,1,0,0'], "The correct method didn't work"

def test_excused():
    mock = mock_opener(["Isabelle,0,0,0,0"])
    p = Poller('participants.csv', mock)
    p.__enter__()
    p.__iter__()
    p.__next__()
    p.excused()
    p.mock_writer()
    assert mock.mock_file_output == ['Isabelle,1,0,0,1'], "The excused method didn't work"

def test_missing():
    mock = mock_opener(["Isabelle,0,0,0,0"])
    p = Poller('participants.csv', mock)
    p.__enter__()
    p.__iter__()
    p.__next__()
    p.missing()
    p.mock_writer()
    assert mock.mock_file_output == ['Isabelle,1,0,0,0'], "The missing method didn't work"

def test_total():
    mock = mock_opener(["Isabelle,0,0,0,0"])
    p = Poller('participants.csv', mock)
    p.__enter__()
    p.__iter__()
    p.__next__()
    p.attempted()
    p.__next__()
    p.missing()
    p.__next__()
    p.excused()
    p_total = p.total()
    assert p_total == 3, "The total method didn't work"

def test_iter_next_1():
    mock = mock_opener(["Isabelle,0,0,0,0", "Jesus,3,0,0,0", "Tidi,2,0,0,0"])
    p = Poller('participants.csv', mock)
    p.__enter__()
    p.__iter__()
    next_p = p.__next__()
    assert next_p == 'Isabelle,0,0,0,0', "The iter and next methods are not working"
