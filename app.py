from flask import Flask, render_template, request
import random

app = Flask(__name__)



# Creating  classes for the players, team, bowlers, etc.
class Player:
    def __init__(self, name, bowling, batting, fielding, running, experience):
        self.name = name
        self.bowling = bowling
        self.batting = batting
        self.fielding = fielding
        self.running = running
        self.experience = experience


class Team:
    # Selecting the name of the players
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.captain = None
        self.current_batsmen = []
        self.current_bowler = None

    # Selecting the captain but with random draw
    def select_captain(self):
        self.captain = random.choice(self.players)

    # Selecting the batsmen but with random draw
    def choose_batsmen(self):
        self.current_batsmen = random.sample(self.players, 2)

    # Selecting the bowler but with random draw
    def choose_bowler(self):
        self.current_bowler = random.choice(self.players)


class Field:
    def __init__(self, size, fan_ratio, pitch_conditions, home_advantage):
        self.size = size
        self.fan_ratio = fan_ratio
        self.pitch_conditions = pitch_conditions
        self.home_advantage = home_advantage


class Umpire:
    def __init__(self):
        self.score = 0
        self.wickets = 0
        self.overs = 0

    def predict_outcome(self, batsman, bowler):
        # Calculating the probabilities based on player stats, field conditions, etc.

        batting_probability = batsman.batting * random.uniform(0.8, 1.2)
        bowling_probability = bowler.bowling * random.uniform(0.8, 1.2)
        outcome_probability = batting_probability / \
            (batting_probability + bowling_probability)

        # To determine the outcome of the ball
        if random.random() < outcome_probability:
            return 'Out'
        else:
            return 'Not Out'

    def make_decision(self, decision):
        pass


class Commentator:
    def __init__(self):
        self.commentary = []

    def add_commentary(self, comment):
        self.commentary.append(comment)

    def get_commentary(self):
        return "\n".join(self.commentary)


class Match:
    def __init__(self, team1, team2, field):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.umpire = Umpire()
        self.commentator = Commentator()

    def simulate_match(self):
        # Initializing the match parameters

        # To select captains for both teams
        self.team1.select_captain()
        self.team2.select_captain()

        # To choose batting order and bowler for the first over
        self.team1.choose_batsmen()
        self.team2.choose_batsmen()
        self.team1.choose_bowler()
        self.team2.choose_bowler()

        # Simulating the match ball by ball
        for ball in range(120):
            batsman = self.team1.current_batsmen[0]
            bowler = self.team2.current_bowler

            outcome = self.umpire.predict_outcome(batsman, bowler)

            if outcome == 'Out':
                self.umpire.make_decision('Out')
                self.commentator.add_commentary(f"{batsman.name} is out!")

                # To update wickets and select the next batsman
                self.umpire.wickets += 1
                self.team1.current_batsmen[0] = random.choice(
                    self.team1.players)

                # To check if all players are out
                if self.umpire.wickets == len(self.team1.players):
                    break
            else:
                self.commentator.add_commentary(f"{batsman.name} scores runs!")

                # Updating scores and overs
                runs = random.randint(0, 6)
                self.umpire.score += runs
                self.umpire.overs += 0.1

                # Checking if the over is completed
                if self.umpire.overs % 1 == 0:
                    # Switching bowler and batsmen for the next over
                    self.team1.current_batsmen.reverse()
                    self.team2.choose_bowler()

        # To determine the winner based on the scores
        if self.umpire.score > self.umpire.score:
            winner = self.team1.name
        elif self.umpire.score < self.umpire.score:
            winner = self.team2.name
        else:
            winner = "Draw"

        match_result = {
            "team1": self.team1.name,
            "team2": self.team2.name,
            "score1": self.umpire.score,
            "score2": self.umpire.score,
            "winner": winner,
            "commentary": self.commentator.get_commentary()
        }

        return match_result


# Flask routes

@app.route('/')
def home():
    return render_template('home.html')  # Home page


@app.route('/simulate', methods=['POST', 'GET'])
def simulate_match():
    # Creating players
    player1 = Player("MS Dhoni", 0.2, 0.8, 0.99, 0.8, 0.9)
    player2 = Player("Virat Kohli", 0.3, 0.9, 0.95, 0.7, 0.8)
    player3 = Player("Rohit Sharma", 0.1, 0.85, 0.9, 0.75, 0.7)
    player4 = Player("Jasprit Bumrah", 0.9, 0.2, 0.8, 0.6, 0.9)
    player5 = Player("Ravindra Jadeja", 0.5, 0.7, 0.9, 0.8, 0.8)

    # Creating teams
    team1 = Team("India", [player1, player2, player3, player4, player5])
    team2 = Team("Australia", [player1, player2, player3, player4, player5])

    # Creating field
    field = Field("Large", 0.8, "Dry", 0.1)

    # Creating a match and simulate it
    cricket_match = Match(team1, team2, field)
    result = cricket_match.simulate_match()

    return render_template('simulation_result.html', match_result=result)


@app.route('/result')   # Route to showcase result
def match_result():

    return render_template('match_result.html', match_result=match_result)


if __name__ == '__main__':
    app.run(debug=True) # Keeping debug true to check the any bugs and solve it.
