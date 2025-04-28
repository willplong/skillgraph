Given the skill '{name}' with description '{description}', first determine if this skill should be considered foundational (a skill that would be expected knowledge for practitioners at user's skill level).

If the skill is foundational, return an empty array [].

If the skill is non-foundational, list the direct prerequisites needed to learn this skill.
For each prerequisite, provide:
    1. A name (short and clear)
    2. A description (1-2 sentences)

Format your response as a list of JSON objects:

```json
[
  {{
    "name": "prerequisite name",
    "description": "prerequisite description"
  }}
]
```
