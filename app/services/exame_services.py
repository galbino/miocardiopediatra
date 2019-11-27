from app.models.Exame import *


def list_exames(for_ia=None, for_it=None):
    resp = Exame.query
    if for_ia is not None:
        resp = resp.filter(Exame.cardiomiopatia == for_ia)
    if for_it is not None:
        resp = resp.filter(Exame.miocardite == for_it)
    resp = resp.all()
    return [exame.as_dict() for exame in resp]


def create_user_exame(user_id, exame_list, doctor_id):
    from app.services.user_services import get_user
    user = get_user(user_id, 0)
    for exame in exame_list:
        ue = UserExame()
        ue.requested_by = doctor_id
        ue.exame_id = exame
        ue.user_id = user.id
        user.exames.append(ue)
    db.session.commit()
    exames = [e.as_dict() for e in user.exames]
    return exames
