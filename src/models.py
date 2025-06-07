from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Stage(BaseModel):
    id: int | str
    name: str
    image: Optional[str] = None


class Rule(BaseModel):
    key: str
    name: str


class Schedule(BaseModel):
    start_time: datetime
    end_time: datetime
    rule: Rule
    stages: List[Stage]
    is_fest: bool = False


class BattleSchedule(BaseModel):
    schedules: List[Schedule]


class WeaponCategory(BaseModel):
    key: str
    name: str


class Weapon(BaseModel):
    key: str
    name: str
    image: Optional[str] = None
    category: Optional[WeaponCategory] = None


class SalmonSchedule(BaseModel):
    start_time: datetime
    end_time: datetime
    stage: Stage
    weapons: List[Weapon]
    is_big_run: bool = False
    is_team_contest: bool = False


class SalmonRunSchedule(BaseModel):
    schedules: List[SalmonSchedule]


class CurrentBattlesResponse(BaseModel):
    regular: Optional[Schedule] = None
    bankara_open: Optional[Schedule] = None
    bankara_challenge: Optional[Schedule] = None
    x_match: Optional[Schedule] = None
    fest: Optional[Schedule] = None
