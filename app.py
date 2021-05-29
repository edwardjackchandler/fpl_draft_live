from flask import Flask, render_template
from fpl import draft as draft

app = Flask(__name__)

@app.route('/live_scores/<league>/<game_week>')
def live_scores(league, game_week):
    fpl_draft_week = draft.ApiScraper(league, game_week)
    return render_template('index.html', result=fpl_draft_week.get_live_scores_call())

@app.route('/live_totals/<league>/<game_week>')
def live_totals(league, game_week):
    fpl_draft_week = draft.ApiScraper(league, game_week)
    df = fpl_draft_week.get_live_score_pdf_formatted()
    return render_template(
        "totals.html", 
        column_names=df.columns.values, 
        row_data=list(df.values.tolist()), 
        zip=zip
    )

if __name__ == "__main__":
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
