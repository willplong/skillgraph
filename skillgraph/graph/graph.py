from __future__ import annotations

from dataclasses import dataclass, field

from .types import Skill


@dataclass
class Node:
    skill: Skill
    parent_id: str | None = None
    child_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "skill": self.skill.model_dump(),
            "parent_id": self.parent_id,
            "child_ids": self.child_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Node:
        skill = Skill(**data["skill"])
        node = cls(skill=skill)
        if data["parent_id"] is not None:
            node.parent_id = data["parent_id"]
        node.child_ids = data["child_ids"]
        return node


class Graph:
    def __init__(self, root: Skill):
        self._root = Node(root)
        self._nodes: dict[str, Node] = {root.id: self._root}

    def add_prerequisite(self, skill: Skill, prerequisite: Skill) -> None:
        if skill.id not in self._nodes:
            raise ValueError(f"Skill with ID {skill.id} not found")
        node = self._nodes[skill.id]
        prerequisite_node = Node(prerequisite)
        self._nodes[prerequisite.id] = prerequisite_node

        node.child_ids.append(prerequisite.id)
        prerequisite_node.parent_id = skill.id
