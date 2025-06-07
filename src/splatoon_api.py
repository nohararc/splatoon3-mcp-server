import httpx
from datetime import datetime
from typing import Optional, Dict, Any

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
        stages = []
        for stage_data in data.get("stages", []):
            stage = Stage(
                id=stage_data["id"],
                name=stage_data["name"],
                image=stage_data.get("image"),
            )
            stages.append(stage)

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

        weapons = []
        for weapon_data in data.get("weapons", []):
            weapon = Weapon(
                key=weapon_data.get("key", ""),
                name=weapon_data["name"],
                image=weapon_data.get("image"),
            )
            weapons.append(weapon)

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

    async def get_regular_now(self) -> Optional[Schedule]:
        data = await self._request("/regular/now")
        results = data.get("results", [])
        if results:
            return self._parse_schedule(results[0])
        return None

    async def get_bankara_open_now(self) -> Optional[Schedule]:
        data = await self._request("/bankara-open/now")
        results = data.get("results", [])
        if results:
            return self._parse_schedule(results[0])
        return None

    async def get_bankara_challenge_now(self) -> Optional[Schedule]:
        data = await self._request("/bankara-challenge/now")
        results = data.get("results", [])
        if results:
            return self._parse_schedule(results[0])
        return None

    async def get_x_match_now(self) -> Optional[Schedule]:
        data = await self._request("/x/now")
        results = data.get("results", [])
        if results:
            return self._parse_schedule(results[0])
        return None

    async def get_regular_schedule(self) -> BattleSchedule:
        data = await self._request("/regular/schedule")
        schedules = []
        for item in data.get("results", []):
            schedules.append(self._parse_schedule(item))
        return BattleSchedule(schedules=schedules)

    async def get_bankara_open_schedule(self) -> BattleSchedule:
        data = await self._request("/bankara-open/schedule")
        schedules = []
        for item in data.get("results", []):
            schedules.append(self._parse_schedule(item))
        return BattleSchedule(schedules=schedules)

    async def get_bankara_challenge_schedule(self) -> BattleSchedule:
        data = await self._request("/bankara-challenge/schedule")
        schedules = []
        for item in data.get("results", []):
            schedules.append(self._parse_schedule(item))
        return BattleSchedule(schedules=schedules)

    async def get_x_match_schedule(self) -> BattleSchedule:
        data = await self._request("/x/schedule")
        schedules = []
        for item in data.get("results", []):
            schedules.append(self._parse_schedule(item))
        return BattleSchedule(schedules=schedules)

    async def get_salmon_run_schedule(self) -> SalmonRunSchedule:
        data = await self._request("/coop-grouping/schedule")
        schedules = []
        for item in data.get("results", []):
            schedules.append(self._parse_salmon_schedule(item))
        return SalmonRunSchedule(schedules=schedules)
