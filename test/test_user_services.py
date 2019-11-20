import pytest
from app.services import user_services


class TestUserServices:
    def test_fill_question(self):
        val = {1: 1, 2: 0, 3: 1}
        resp = user_services.fill_questions(val)
        for r in resp:
            assert r.question_id in val.keys()
            assert r.answer == val.get(r.question_id)
