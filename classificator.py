import csv
import math
from collections import defaultdict


# BEGIN Screener Class ----------------------------------------------------------------------------------------------- #

class Screener:

    @staticmethod
    def set_present(present):
        Screener.present = present

    # Konstruktor des Screeners
    # 'name' enthaelt den Namen als String (Bsp. "Screener 15")
    # 'correct' enthaelt die Antworten als Liste von Zahlen (0: falsch, 1: richtig)
    def __init__(self, name, correct):
        self.name = str(name)
        self.correct = list(correct)

        # berechne alle relevanten Werte des Screeners
        self.accuracy = self.accuracy()
        self.hit_rate = self.hit_rate()
        self.miss_rate = self.miss_rate()
        self.false_alarm_rate = self.false_alarm_rate()
        self.correct_rejection_rate = self.correct_rejection_rate()
        self.sensitivity = self.sensitivity()
        self.criterion = self.criterion()

    # Berechnung der Accuracy
    # diese Methode ist als Beispiel fertig implementiert
    def accuracy(self):
        # initialisiere die Anzahl richtiger Antworten 'num_correct' mit 0
        num_correct = 0

        # gehe durch alle Antworten (entry) in der Liste 'correct'
        for entry in self.correct:

            # falls die Antwort richtig ist, erhoehe die Anzahl richtiger Antworten
            if int(entry) == 1:
                num_correct += 1
        # teile die Anzahl richtiger Antworten durch die Gesamtanzahl von Antworten
        return num_correct / len(self.correct)

    # todo: Berechnung der Hitrate
    def hit_rate(self):
        num_present=0 
        num_hit=0 
        #Anz Hits
        for entry, entry2 in zip(self.present, self.correct):
            if int(entry) == int(entry2) == 1 :
                num_hit +=1
        #Anz gefaehrlicher Koffer
        for entry in self.present:
            if int(entry) == 1:
                num_present += 1
        return num_hit / num_present

    # todo: Berechnung der Missrate
    def miss_rate(self):
        return 1 - self.hit_rate

    # todo: Berechnung der False-Alarm-Rate 
    def false_alarm_rate(self):
        num_present=0 
        num_far=0 
        #Anz False-Alarms
        for entry, entry2 in zip(self.present, self.correct):
            if int(entry) == int(entry2) == 0 :
                num_far +=1
        #Anz ungefaehrlicher Koffer
        for entry in self.present:
            if int(entry) == 0:
                num_present += 1
        return num_far / num_present

    # todo: Berechnung der Correct-Rejection-Rate
    def correct_rejection_rate(self):
        return 1 - self.false_alarm_rate

    # todo: Berechnung der Sensitivity
    def sensitivity(self):
        rate_far = self.normsinv(self.false_alarm_rate)
        rate_hit = self.normsinv(self.hit_rate)
        
        #Rueckgabe Sensitivity
        return rate_hit - rate_far

    # todo: Berechnung des Criterion
    def criterion(self):
        rate_far = self.normsinv(self.false_alarm_rate)
        rate_hit = self.normsinv(self.hit_rate)
        
        #Rueckgabe Criterion
        return -0.5*(rate_far + rate_hit)

    # Signum-Funktion
    def sign(self, x):
        if x < 0:
            return -1
        elif x == 0:
            return 0
        else:
            return 1

    # z-Werte:
    # Approximation der inversen kumulierten Standardnormalverteilung
    # Quelle: http://en.wikipedia.org/wiki/Normal_distribution#Quantile_function
    def normsinv(self, p):
        # Approximation der inversen Fehlerfunktion
        # Quelle: http://en.wikipedia.org/wiki/Error_function#Approximation_with_elementary_functions
        def erfinv(x):
            a = 0.147
            tmp = 2 / (math.pi*a) + math.log(1-x**2)/2
            return self.sign(x) * math.sqrt(math.sqrt(tmp**2 - math.log(1-x**2)/a) - tmp)

        if not (0 <= p <= 1):
            raise ValueError("p must be between 0 and 1")

        return math.sqrt(2) * erfinv(2*p-1)

    # Ausgabe der Screener Attribute als formatierter String
    def get_string(self):
        result = self.name + "\n"
        result += "  A .... accuracy ................ %3.1f \n" % (self.accuracy * 100)
        result += "  HR ... hit rate ................ %3.1f \n" % (self.hit_rate * 100)
        result += "  MR ... miss rate ............... %3.1f \n" % (self.miss_rate * 100)
        result += "  FAR .. false alarm rate ........ %3.1f \n" % (self.false_alarm_rate * 100)
        result += "  CRR .. correct rejection rate .. %3.1f \n" % (self.correct_rejection_rate * 100)
        result += "  d' ... sensitivity ............. %+1.3f \n" % self.sensitivity
        result += "  c .... criterion ............... %+1.3f \n" % self.criterion

        return result

# END   Screener Class ----------------------------------------------------------------------------------------------- #


# BEGIN Classificator Class ------------------------------------------------------------------------------------------ #

class Classificator:

    # Konstruktor der classificator-Klasse
    # 'data_path' und 'columns' dienen dem Erstellen der Screener
    # 'screeners' enthaelt alle Screener in einer Liste
    def __init__(self, data_path):
        self.data_path = data_path
        self.columns = defaultdict(list)
        self.screeners = []

        self.read_data()
        self.create_screeners()
        self.rank_screeners()

    def read_data(self):
        # read data into dictionary
        with open(self.data_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for (key, value) in row.items():
                    self.columns[key].append(value)

        # target presence is set as class attribute to the screener class (independent of instances of that class)
        Screener.set_present(self.columns['Target Presence'])

    def create_screeners(self):
        # for each column of the csv file
        for title in self.columns:
            # if it contains screener results ...
            if str(title).startswith('Screener '):
                # ... then create screener with column-title as name and column-content as results
                self.screeners.append(Screener(str(title), self.columns[title]))

    # todo: Implementierung der Berechnung von Durchschnittswerten (HR, MR, FAR, CRR) und Darstellung in Matrix-Form
    def average(self):
        #hr
        for screener in self.screeners:
            av_hr += screener.hit_rate
        av_hr = av_hr / len(self.screeners)

        #mr
        for screener in self.screeners:
            av_mr += screener.miss_rate
        av_mr = av_mr / len(self.screeners)

        #far
        for screener in self.screeners:
            av_far += screener.false_alarm_rate
        av_far = av_far / len(self.screeners)

        #crr
        for screener in self.screeners:
            av_crr += screener.correct_rejection_rate
        av_crr = av_crr / len(self.screeners)

        # ausgabe in matrix
        print("%.2f" % av_hr + " * " + "%.2f" % av_crr)
        print("    *    ")
        print("%.2f" % av_mr + " * " + "%.2f" % av_far)


    # todo: gestalte die Reihenfolge der Screener-Liste in Abhaengigkeit von der Aufgabenstellung
    def rank_screeners(self, ):
        # die Reihenfolge wird durch eine Sortierweise festgelegt: derzeit wird das Attribut "name" eines
        # Screeners verwendet, um die Liste zu sortieren. Die Sortierung wird durch die Angabe "reverse=True"
        # umgekehrt
        #rank accruacy
        print("Reihung nach der Accuracy")
        self.screeners.sort(key=lambda x: x.accuracy, reverse=True)
        """#rank hit-rate
        print("Reihung nach der Hit-Rate")
        self.screeners.sort(key=lambda x: x.hit_rate, reverse=True)
        #rank false-alarm-rate
        print("Reihung nach der False-Alarm-Rate")
        self.screeners.sort(key=lambda x: x.false_alarm_rate)
        #rank hit-rate and sensitivity
        print("Reihung nach der Hit-Rate und der Sensititvity")
        self.screeners.sort(key=lambda x: (x.accuracy, x.hit_rate), reverse=True)"""

    def get_top_five(self):
        return self.screeners[:15]

# END   Classificator Class ------------------------------------------------------------------------------------------ #


# BEGIN Main Program ------------------------------------------------------------------------------------------------- #

c = Classificator("sdt-data.csv")
top = c.get_top_five()

for element in top:
    print(element.get_string())

# END   Main Program ------------------------------------------------------------------------------------------------- #
