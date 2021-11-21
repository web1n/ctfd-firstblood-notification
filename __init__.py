from flask import current_app

from sqlalchemy.event import listen
from CTFd.models import Users, Solves, Challenges
from CTFd.utils.modes import get_model

def on_solve(mapper, conn, solve):
    Model = get_model()

    solve_count = (
        Solves.query.join(Model, Solves.account_id == Model.id)
            .filter(
            Solves.challenge_id == solve.challenge_id,
            Model.hidden == False,
            Model.banned == False,
        )
            .count()
    )

    if solve_count == 1:
        user = Users.query.filter_by(id=solve.user_id).first()
        challenge = Challenges.query.filter_by(id=solve.challenge_id).first()

        title = "First Blood!"
        message = "恭喜" + user.name + "解出题目: " + challenge.name + "并获得一血"

        current_app.events_manager.publish(data={"title": title, "content": message, "type": "toast"}, type="notification")


def load(app):
    listen(Solves, "after_insert", on_solve)
