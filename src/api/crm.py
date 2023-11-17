from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path
import re
import string

from tinydb import TinyDB, where, table


@dataclass
class User:
    first_name: str
    last_name: str
    phone_number: str = ''
    address: str = ''

    DB: ClassVar = TinyDB(Path(__file__).resolve().parent.parent.parent / 'db.json', indent=4)

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def db_instance(self) -> table.Document | list[table.Document] | None:
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    def __str__(self) -> str:
        return f'{self.full_name}\n{self.phone_number}\n{self.address}'

    def _checks(self):
        self._check_phone_number()
        self._check_names()

    def _check_phone_number(self):
        phone_number = re.sub(r"^\+33|[()\s*]", "", self.phone_number)

        if len(phone_number) == 9 and not phone_number.startswith('0'):
            phone_number = '0' + phone_number

        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f'Numéro de téléphone {phone_number} invalide.')

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError('Le prénom et le nom de famille ne peuvent pas être vides.')

        special_characters = string.punctuation + string.digits
        for character in self.full_name.strip():
            if character in special_characters:
                raise ValueError(f'Nom "{self.full_name}" invalide')

    def exists(self) -> bool:
        return bool(self.db_instance)

    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])  # type: ignore
        return []

    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()

        if self.exists():
            return -1
        else:
            return User.DB.insert(self.__dict__)


def get_all_users():
    return [User(**user) for user in User.DB.all()]


if __name__ == '__main__':
    adrien = User('Adrien', 'Klein')
    print(adrien.delete())
