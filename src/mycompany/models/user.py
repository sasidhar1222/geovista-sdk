from dataclasses import dataclass


@dataclass
class User:

    id: int
    name: str
    email: str

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"]
        )