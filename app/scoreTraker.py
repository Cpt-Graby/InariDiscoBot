import os
import csv
from collections import defaultdict
import datetime

class ScoreTracker:
    def __init__(self):
        # Utilisation d'un dictionnaire pour stocker les scores par date
        self.scores = defaultdict(dict)

    def add_score(self, participant: str, score: int, date=None):
        if date is None:
            date = str(datetime.date.today())
        # Conserve le dernier score pour chaque participant chaque jour
        self.scores[date][participant] = score

    def get_scores(self, date=None):
        if date is None:
            date = str(datetime.date.today())
        # Récupère les scores pour une date donnée
        return self.scores.get(date, {})

    def get_last_score(self, participant: str, date=None):
        scores = self.get_scores(date)
        return scores.get(participant, None)

    def calculate_total_score_by_participant(self):
        total_scores = defaultdict(int)
        for date_scores in self.scores.values():
            for participant, score in date_scores.items():
                total_scores[participant] += score
        return dict(total_scores)

    def print_scores_for_participant(self, participant: str):
        result = f"Scores pour {participant}:\n"
        for date, scores in self.scores.items():
            if participant in scores:
                result += f"{date}: {scores[participant]}\n"
        return result

    def save_scores_to_csv(self, participant: str):
        if not os.path.exists("resultat"):
            os.makedirs("resultat")
        file_name = f"resultat/{participant}.csv"
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['Date', 'Score']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for date, score in self.scores.items():
                if participant in score:
                    writer.writerow({'Date': date, 'Score': score[participant]})

    def get_current_ranking(self, date=None):
        if date is None:
            date = str(datetime.date.today())
        scores = self.get_scores(date)
        ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print(ranking)
        return ranking


if __name__ == "__main__":
    # Exemple d'utilisation :
    tracker = ScoreTracker()

    tracker.add_score("Participant 1", 100, "2023-09-02")
    tracker.add_score("Participant 2", 100, "2023-09-02")
    tracker.add_score("Participant 1", 100)
    tracker.add_score("Participant 2", 150)
    tracker.add_score("Participant 1", 120)  # Le score précédent de Participant 1 est écrasé
    tracker.add_score("Participant 2", 200)  # Le score précédent de Participant 2 est écrasé

    print("Scores pour aujourd'hui :")
    print(tracker.get_scores())
    print("Dernier score de Participant 1 aujourd'hui :", tracker.get_last_score("Participant 1"))
    print("Dernier score de Participant 2 aujourd'hui :", tracker.get_last_score("Participant 2"))

    total_scores_by_participant = tracker.calculate_total_score_by_participant()
    print("Somme totale des scores par participant :", total_scores_by_participant)
    tracker.print_scores_for_participant("Participant 1")
    tracker.save_scores_to_csv("Participant 1")
    current_ranking = tracker.get_current_ranking()
    print("Classement actuel des participants :", current_ranking)
