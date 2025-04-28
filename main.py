import json

from skillgraph.config import PROJECT_ROOT
from skillgraph.graph import Graph, Skill
from skillgraph.llm import AnthropicModel


def load_prompt(name: str) -> str:
    prompt_path = PROJECT_ROOT / "prompts" / f"{name}.md"
    return prompt_path.read_text()


def generate_prerequisites(skill: Skill, llm: AnthropicModel) -> list[Skill]:
    prompt = load_prompt("generate_prerequisites")
    prompt = prompt.format(name=skill.name, description=skill.description)
    response = llm.get_response(prompt)
    try:
        if response.startswith("```json"):
            response = response[len("```json") :]
        if response.endswith("```"):
            response = response[: -len("```")]
        prerequisites_data = json.loads(response)
        prerequisites = [
            Skill(name=prereq["name"], description=prereq["description"])
            for prereq in prerequisites_data
        ]
        return prerequisites
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Failed to parse LLM response: {e}") from e


def main():
    system_prompt = load_prompt("system")
    llm = AnthropicModel(system_prompt=system_prompt)

    root_skill = Skill(
        name="Gaussian Processes",
        description="Gaussian processes are a type of kernel method for non-parametric regression. They are a powerful tool for modeling complex, non-linear relationships in data.",
    )

    graph = Graph(root=root_skill)

    prerequisites = generate_prerequisites(root_skill, llm)

    for prerequisite in prerequisites:
        graph.add_prerequisite(root_skill, prerequisite)

        sub_prerequisites = generate_prerequisites(prerequisite, llm)
        for sub_prerequisite in sub_prerequisites:
            graph.add_prerequisite(prerequisite, sub_prerequisite)

    def print_hierarchy(skill_id: str, level: int = 0):
        node = graph._nodes[skill_id]
        indent = "  " * level
        print(f"{indent}- {node.skill.name}")
        for child_id in node.child_ids:
            print_hierarchy(child_id, level + 1)

    print("\nSkill Hierarchy:")
    print_hierarchy(root_skill.id)


if __name__ == "__main__":
    main()
