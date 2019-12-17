import pytest
from app.services import user_services


class TestUserServices:
    def test_fill_question(self):
        val = {1: 1, 2: 0, 3: 1}
        resp = user_services.fill_questions(val)
        for r in resp:
            assert r.question_id in val.keys()
            assert r.answer == val.get(r.question_id)

    def test_calc_taxa_one(self):
        questions = [
            {"weight_miocardite": 5, "weight_miocardiopatia": 10, "value_weight_miocardiopatia": 1,
                      "value_weight_miocardite": 1, "answer": 1},
            {"weight_miocardite": 5, "weight_miocardiopatia": 20, "value_weight_miocardiopatia": 1,
              "value_weight_miocardite": 1, "answer": 1},
            {"weight_miocardite": 10, "weight_miocardiopatia": 20, "value_weight_miocardiopatia": 0,
              "value_weight_miocardite": 1, "answer": 0}
        ]
        assert user_services.calc_taxa_from_questions(questions) == (0.5, 1)

    def test_calc_taxa_two(self):
        questions = [
            {"weight_miocardite": 5, "weight_miocardiopatia": 10, "value_weight_miocardiopatia": 1,
                      "value_weight_miocardite": 1, "answer": 0},
            {"weight_miocardite": 5, "weight_miocardiopatia": 20, "value_weight_miocardiopatia": 1,
              "value_weight_miocardite": 1, "answer": 1},
            {"weight_miocardite": 10, "weight_miocardiopatia": 20, "value_weight_miocardiopatia": 0,
              "value_weight_miocardite": 1, "answer": 1}
        ]
        assert user_services.calc_taxa_from_questions(questions) == (0.75, 0.4)

    def test_password_encrypt(self):
        password = 'g00gle33'
        actual_resp = "47e73f97f21771864e83813b6b801122e8e5051c29dd65c818bc33d7e0937fc0"
        resp = user_services.encrypt_password(password)
        assert resp != password
        assert resp == actual_resp

    def test_password_encrypt_two(self):
        password = 'teste'
        actual_resp = "a481b165a7e751b7be74d129cda4e2337cb089f2953b232836d2ac78763e1558"
        resp = user_services.encrypt_password(password)
        assert resp != password
        assert resp == actual_resp
