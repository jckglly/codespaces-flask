from flask import Flask, render_template, request
from wtforms import Form, IntegerField, validators, StringField
import statistics

app = Flask(__name__)

class InputForm(Form):
    scores = StringField(validators=[validators.required()])
    slope = IntegerField(validators=[validators.required()])
    rating = IntegerField(validators=[validators.required()])


def calculate_handicap(scores, slope, rating):
    """
    Calculates a player's handicap using the World Handicap System (WHS) logic.
    :param scores: A list of the player's recent round scores.
    :param slope: The slope of the course played
    :param rating: The course rating
    :return: The player's handicap.
    """
    scores = list(map(int, scores.split(',')))
    scores = scores[-20:]
    scores.sort()
    scores = scores[:10]
    handicap_differentials = []
    for score in scores:
        handicap_differential = (score - rating) * 113 / slope
        handicap_differentials.append(handicap_differential)
    handicap_differentials.sort()
    handicap_differentials = handicap_differentials[1:-1]
    handicap_index = statistics.mean(handicap_differentials)
    handicap_index = round(handicap_index, 1)
    return handicap_index

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        scores = form.scores.data
        slope = form.slope.data
        rating = form.rating.data
        handicap = calculate_handicap(scores, slope, rating)
        return render_template('result.html', form=form, handicap=handicap)
    return render_template('input.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
