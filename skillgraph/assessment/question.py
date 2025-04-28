from enum import Enum
from itertools import combinations

from pydantic import BaseModel

from skillgraph.graph import Skill
from skillgraph.utils import load_prompt, parse_json_response


class QuestionType(str, Enum):
    NUMERICAL = "numerical"
    MULTIPLE_CHOICE = "multiple_choice"


class Question(BaseModel):
    skills: list[Skill]
    question_text: str
    type: QuestionType
    answer: str
    options: list[str] | None = None

    def check_answer(self, user_answer: str) -> bool:
        """Check if the user's answer is correct."""
        if self.type == QuestionType.NUMERICAL:
            try:
                return float(user_answer) == float(self.answer)
            except ValueError:
                return False
        else:  # MULTIPLE_CHOICE
            return user_answer.upper() == self.answer.upper()


def generate_skill_combinations(skills: list[Skill], k: int) -> list[tuple[Skill, ...]]:
    return list(combinations(skills, k))


def generate_question(skills: list[Skill], llm) -> Question:
    skill_names = ", ".join(skill.name for skill in skills)
    skill_descriptions = "\n".join(skill.description for skill in skills)

    prompt = load_prompt("generate_question").format(
        skill_names=skill_names, skill_descriptions=skill_descriptions
    )
    question_data = parse_json_response(llm, prompt)

    return Question(
        skills=skills,
        question_text=question_data["question"],
        type=question_data["type"],
        answer=question_data["answer"],
        options=question_data.get("options"),  # Optional for numerical questions
    )


def generate_assessment(skills: list[Skill], k: int, llm) -> list[Question]:
    skill_combinations = generate_skill_combinations(skills, k)
    questions = []

    for skill_combo in skill_combinations:
        question = generate_question(list(skill_combo), llm)
        questions.append(question)

    return questions
