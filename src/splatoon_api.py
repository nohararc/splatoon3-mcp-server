import httpx
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

try:
    from .models import (
        Schedule,
        BattleSchedule,
        SalmonRunSchedule,
        Stage,
        Rule,
        Weapon,
        SalmonSchedule,
    )
except ImportError:
    from models import (
        Schedule,
        BattleSchedule,
        SalmonRunSchedule,
        Stage,
        Rule,
        Weapon,
        SalmonSchedule,
    )


class BattleMode(Enum):
    REGULAR = "regular"
    BANKARA_OPEN = "bankara-open"
    BANKARA_CHALLENGE = "bankara-challenge"
    X_MATCH = "x"


class Splatoon3API:
    def __init__(self):
        self.base_url = "https://spla3.yuu26.com/api"
        self.client = httpx.AsyncClient(
            timeout=30.0, headers={"User-Agent": "Splatoon3-MCP-Server/1.0"}
        )

    async def close(self):
        await self.client.aclose()

    async def _request(self, endpoint: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"API request failed: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def _parse_schedule(self, data: Dict[str, Any]) -> Schedule:
        stages = [
            Stage(
                id=stage_data["id"],
                name=stage_data["name"],
                image=stage_data.get("image"),
            )
            for stage_data in data.get("stages", [])
        ]

        rule = Rule(key=data["rule"]["key"], name=data["rule"]["name"])

        return Schedule(
            start_time=datetime.fromisoformat(
                data["start_time"].replace("Z", "+00:00")
            ),
            end_time=datetime.fromisoformat(data["end_time"].replace("Z", "+00:00")),
            rule=rule,
            stages=stages,
            is_fest=data.get("is_fest", False),
        )

    def _parse_salmon_schedule(self, data: Dict[str, Any]) -> SalmonSchedule:
        stage = Stage(
            id=data["stage"]["id"],
            name=data["stage"]["name"],
            image=data["stage"].get("image"),
        )

        weapons = [
            Weapon(
                key=weapon_data.get("key", ""),
                name=weapon_data["name"],
                image=weapon_data.get("image"),
            )
            for weapon_data in data.get("weapons", [])
        ]

        return SalmonSchedule(
            start_time=datetime.fromisoformat(
                data["start_time"].replace("Z", "+00:00")
            ),
            end_time=datetime.fromisoformat(data["end_time"].replace("Z", "+00:00")),
            stage=stage,
            weapons=weapons,
            is_big_run=data.get("is_big_run", False),
            is_team_contest=data.get("is_team_contest", False),
        )

    async def _get_battle_now(self, mode: BattleMode) -> Optional[Schedule]:
        """指定されたモードの現在のバトル情報を取得"""
        data = await self._request(f"/{mode.value}/now")
        results = data.get("results", [])
        return self._parse_schedule(results[0]) if results else None

    async def _get_battle_schedule(self, mode: BattleMode) -> BattleSchedule:
        """指定されたモードのスケジュールを取得"""
        data = await self._request(f"/{mode.value}/schedule")
        schedules = [self._parse_schedule(item) for item in data.get("results", [])]
        return BattleSchedule(schedules=schedules)

    async def get_regular_now(self) -> Optional[Schedule]:
        return await self._get_battle_now(BattleMode.REGULAR)

    async def get_bankara_open_now(self) -> Optional[Schedule]:
        return await self._get_battle_now(BattleMode.BANKARA_OPEN)

    async def get_bankara_challenge_now(self) -> Optional[Schedule]:
        return await self._get_battle_now(BattleMode.BANKARA_CHALLENGE)

    async def get_x_match_now(self) -> Optional[Schedule]:
        return await self._get_battle_now(BattleMode.X_MATCH)

    async def get_regular_schedule(self) -> BattleSchedule:
        return await self._get_battle_schedule(BattleMode.REGULAR)

    async def get_bankara_open_schedule(self) -> BattleSchedule:
        return await self._get_battle_schedule(BattleMode.BANKARA_OPEN)

    async def get_bankara_challenge_schedule(self) -> BattleSchedule:
        return await self._get_battle_schedule(BattleMode.BANKARA_CHALLENGE)

    async def get_x_match_schedule(self) -> BattleSchedule:
        return await self._get_battle_schedule(BattleMode.X_MATCH)

    async def get_salmon_run_schedule(self) -> SalmonRunSchedule:
        data = await self._request("/coop-grouping/schedule")
        schedules = [
            self._parse_salmon_schedule(item) for item in data.get("results", [])
        ]
        return SalmonRunSchedule(schedules=schedules)