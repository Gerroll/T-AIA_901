import celery
from naturalLanguageProcessing import Nlp
import os

app = celery.Celery('iliketrainsbot')

app.conf.update(BROKER_URL=os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))

@app.task
def init():
    NLP = Nlp()
    # NLP.reset()
    NLP.train()

    return True
