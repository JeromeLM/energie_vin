from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Wine:
    _name: str
    _type: str
    _winery: str
    _appellation: str
    _vintage: int
    _ratings: List[int]
    _price: float

    def get_data(self) -> Dict:
        return {
            "name": self._name,
            "type": self._type,
            "winery": self._winery,
            "appellation": self._appellation,
            "vintage": self._vintage,
            "ratings": self._ratings.copy(),
            "price": self._price,
        }

    @classmethod
    def create_from_data(cls, data: Dict):
        return cls(
            _name=data["name"],
            _type=data["type"],
            _winery=data["winery"],
            _appellation=data["appellation"],
            _vintage=data["vintage"],
            _ratings=data["ratings"],
            _price=data["price"],
        )
