from typing import Optional, Dict, Any

try:
    from .splatoon_api import Splatoon3API
except ImportError:
    from splatoon_api import Splatoon3API


async def get_current_battles(mode: Optional[str] = "all") -> Dict[str, Any]:
    """
    現在のバトル情報を取得します。

    Args:
        mode: 取得するモード ("regular", "bankara-open", "bankara-challenge", "x", "all")

    Returns:
        現在のバトル情報
    """
    api = Splatoon3API()

    try:
        result = {}

        if mode == "all" or mode == "regular":
            regular = await api.get_regular_now()
            if regular:
                result["regular"] = {
                    "rule": regular.rule.name,
                    "stages": [stage.name for stage in regular.stages],
                    "start_time": regular.start_time.isoformat(),
                    "end_time": regular.end_time.isoformat(),
                }

        if mode == "all" or mode == "bankara-open":
            bankara_open = await api.get_bankara_open_now()
            if bankara_open:
                result["bankara_open"] = {
                    "rule": bankara_open.rule.name,
                    "stages": [stage.name for stage in bankara_open.stages],
                    "start_time": bankara_open.start_time.isoformat(),
                    "end_time": bankara_open.end_time.isoformat(),
                }

        if mode == "all" or mode == "bankara-challenge":
            bankara_challenge = await api.get_bankara_challenge_now()
            if bankara_challenge:
                result["bankara_challenge"] = {
                    "rule": bankara_challenge.rule.name,
                    "stages": [stage.name for stage in bankara_challenge.stages],
                    "start_time": bankara_challenge.start_time.isoformat(),
                    "end_time": bankara_challenge.end_time.isoformat(),
                }

        if mode == "all" or mode == "x":
            x_match = await api.get_x_match_now()
            if x_match:
                result["x_match"] = {
                    "rule": x_match.rule.name,
                    "stages": [stage.name for stage in x_match.stages],
                    "start_time": x_match.start_time.isoformat(),
                    "end_time": x_match.end_time.isoformat(),
                }

        return result

    finally:
        await api.close()


async def get_next_battles(mode: Optional[str] = "all") -> Dict[str, Any]:
    """
    次のバトル情報を取得します。

    Args:
        mode: 取得するモード ("regular", "bankara-open", "bankara-challenge", "x", "all")

    Returns:
        次のバトル情報
    """
    api = Splatoon3API()

    try:
        result = {}

        if mode == "all" or mode == "regular":
            schedule = await api.get_regular_schedule()
            if schedule.schedules and len(schedule.schedules) > 1:
                next_battle = schedule.schedules[1]
                result["regular"] = {
                    "rule": next_battle.rule.name,
                    "stages": [stage.name for stage in next_battle.stages],
                    "start_time": next_battle.start_time.isoformat(),
                    "end_time": next_battle.end_time.isoformat(),
                }

        if mode == "all" or mode == "bankara-open":
            schedule = await api.get_bankara_open_schedule()
            if schedule.schedules and len(schedule.schedules) > 1:
                next_battle = schedule.schedules[1]
                result["bankara_open"] = {
                    "rule": next_battle.rule.name,
                    "stages": [stage.name for stage in next_battle.stages],
                    "start_time": next_battle.start_time.isoformat(),
                    "end_time": next_battle.end_time.isoformat(),
                }

        if mode == "all" or mode == "bankara-challenge":
            schedule = await api.get_bankara_challenge_schedule()
            if schedule.schedules and len(schedule.schedules) > 1:
                next_battle = schedule.schedules[1]
                result["bankara_challenge"] = {
                    "rule": next_battle.rule.name,
                    "stages": [stage.name for stage in next_battle.stages],
                    "start_time": next_battle.start_time.isoformat(),
                    "end_time": next_battle.end_time.isoformat(),
                }

        if mode == "all" or mode == "x":
            schedule = await api.get_x_match_schedule()
            if schedule.schedules and len(schedule.schedules) > 1:
                next_battle = schedule.schedules[1]
                result["x_match"] = {
                    "rule": next_battle.rule.name,
                    "stages": [stage.name for stage in next_battle.stages],
                    "start_time": next_battle.start_time.isoformat(),
                    "end_time": next_battle.end_time.isoformat(),
                }

        return result

    finally:
        await api.close()


async def get_salmon_run() -> Dict[str, Any]:
    """
    サーモンラン情報を取得します。

    Returns:
        現在と次回のサーモンラン情報
    """
    api = Splatoon3API()

    try:
        schedule = await api.get_salmon_run_schedule()
        result = {"current": None, "next": None}

        if schedule.schedules:
            # 現在のシフト
            current = schedule.schedules[0]
            result["current"] = {
                "stage": current.stage.name,
                "weapons": [weapon.name for weapon in current.weapons],
                "start_time": current.start_time.isoformat(),
                "end_time": current.end_time.isoformat(),
                "is_big_run": current.is_big_run,
                "is_team_contest": current.is_team_contest,
            }

            # 次のシフト
            if len(schedule.schedules) > 1:
                next_shift = schedule.schedules[1]
                result["next"] = {
                    "stage": next_shift.stage.name,
                    "weapons": [weapon.name for weapon in next_shift.weapons],
                    "start_time": next_shift.start_time.isoformat(),
                    "end_time": next_shift.end_time.isoformat(),
                    "is_big_run": next_shift.is_big_run,
                    "is_team_contest": next_shift.is_team_contest,
                }

        return result

    finally:
        await api.close()
