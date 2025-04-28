from skillgraph.assessment import Question, generate_assessment
from skillgraph.graph import Graph, Skill
from skillgraph.llm import AnthropicModel
from skillgraph.utils import load_prompt, parse_json_response


def generate_prerequisites(
    skill: Skill, llm: AnthropicModel, user_skill_level: str, max_retries: int = 3
) -> list[Skill]:
    prompt = load_prompt("generate_prerequisites").format(
        name=skill.name, description=skill.description, level=user_skill_level
    )
    prerequisites_data = parse_json_response(llm, prompt, max_retries)
    prerequisites = [
        Skill(name=prereq["name"], description=prereq["description"])
        for prereq in prerequisites_data
    ]
    return prerequisites


def print_question(question: Question):
    print(f"\nQuestion testing: {', '.join(skill.name for skill in question.skills)}")
    print(f"Q: {question.question_text}")
    if question.type == "multiple_choice":
        print("\nOptions:")
        for i, option in enumerate(question.options):
            print(f"{chr(65 + i)}) {option}")
    print(f"\nCorrect answer: {question.answer}")
    print("-" * 80)


def interactive_assessment(questions: list[Question]):
    score = 0
    total = len(questions)

    print("\nStarting Assessment")
    print("==================")
    print("For multiple choice questions, enter A, B, C, or D")
    print("For numerical questions, enter the number\n")

    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}/{total}")
        print(f"Testing skills: {', '.join(skill.name for skill in question.skills)}")
        print(f"\n{question.question_text}")

        if question.type == "multiple_choice":
            print("\nOptions:")
            for i, option in enumerate(question.options):
                print(f"{chr(65 + i)}) {option}")

        user_answer = input("\nYour answer: ").strip()

        if question.check_answer(user_answer):
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The answer was: {question.answer}")

    print(f"\nFinal Score: {score}/{total} ({score / total * 100:.1f}%)")
    return score / total


def main():
    root_skill = Skill(
        name="Gaussian Processes",
        description="Gaussian processes are a type of kernel method for non-parametric regression. They are a powerful tool for modeling complex, non-linear relationships in data.",
    )
    user_skill_level = "PhD student in computational neuroscience"
    system_prompt = load_prompt("system").format(
        root_skill=root_skill.name,
        root_skill_description=root_skill.description,
        user_skill_level=user_skill_level,
    )
    llm = AnthropicModel(system_prompt=system_prompt)

    graph = Graph(root=root_skill)
    skill_queue = [root_skill]
    processed_skills = set()
    while skill_queue:
        current_skill = skill_queue.pop(0)
        if current_skill.id in processed_skills:
            continue
        prerequisites = generate_prerequisites(current_skill, llm, user_skill_level)
        print(current_skill.name)
        for prereq in prerequisites:
            print(f"  {prereq.name}")
        processed_skills.add(current_skill.id)

        for prerequisite in prerequisites:
            graph.add_prerequisite(current_skill, prerequisite)
            skill_queue.append(prerequisite)

    print(f"\nProcessed {len(processed_skills)} skills in total")

    def print_hierarchy(skill_id: str, level: int = 0):
        node = graph._nodes[skill_id]
        indent = "  " * level
        print(f"{indent}- {node.skill.name}")
        for child_id in node.child_ids:
            print_hierarchy(child_id, level + 1)

    print("\nSkill Hierarchy:")
    print_hierarchy(root_skill.id)

    print("\nGenerating assessment...")
    questions = generate_assessment(graph.get_leaf_skills(), 2, llm)

    print("\nWould you like to:")
    print("1. Take the interactive assessment")
    print("2. Just view the questions and answers")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        proficiency = interactive_assessment(questions)
        print(f"\nOverall proficiency score: {proficiency:.2f}")
    else:
        for question in questions:
            print_question(question)


if __name__ == "__main__":
    main()
