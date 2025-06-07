from typing import Optional, Dict, Any, List

try:
    from .splatoon_api import Splatoon3API
    from .models import Schedule
except ImportError:
    from splatoon_api import Splatoon3API
    from models import Schedule


def _format_battle_info(schedule: Schedule) -> Dict[str, Any]:
    """バトル情報を辞書形式に変換"""
    return {
        "rule": schedule.rule.name,
        "stages": [stage.name for stage in schedule.stages],
        "start_time": schedule.start_time.isoformat(),
        "end_time": schedule.end_time.isoformat(),
    }


async def _get_battles_by_index(mode: str, index: int) -> Dict[str, Any]:
    """指定されたインデックスのバトル情報を取得"""
    api = Splatoon3API()
    
    try:
        result = {}
        mode_map = {
            "regular": ("regular", api.get_regular_schedule),
            "bankara-open": ("bankara_open", api.get_bankara_open_schedule),
            "bankara-challenge": ("bankara_challenge", api.get_bankara_challenge_schedule),
            "x": ("x_match", api.get_x_match_schedule),
        }
        
        if mode == "all":
            modes_to_fetch = mode_map.keys()
        else:
            modes_to_fetch = [mode] if mode in mode_map else []
        
        for mode_key in modes_to_fetch:
            result_key, get_schedule = mode_map[mode_key]
            schedule = await get_schedule()
            
            if schedule.schedules and len(schedule.schedules) > index:
                result[result_key] = _format_battle_info(schedule.schedules[index])
        
        return result
    
    finally:
        await api.close()


async def get_current_battles(mode: Optional[str] = "all") -> Dict[str, Any]:
    """
    現在のバトル情報を取得します。

    Args:
        mode: 取得するモード ("regular", "bankara-open", "bankara-challenge", "x", "all")

    Returns:
        現在のバトル情報
    """
    return await _get_battles_by_index(mode, 0)


async def get_next_battles(mode: Optional[str] = "all") -> Dict[str, Any]:
    """
    次のバトル情報を取得します。

    Args:
        mode: 取得するモード ("regular", "bankara-open", "bankara-challenge", "x", "all")

    Returns:
        次のバトル情報
    """
    return await _get_battles_by_index(mode, 1)


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
            current = schedule.schedules[0]
            result["current"] = {
                "stage": current.stage.name,
                "weapons": [weapon.name for weapon in current.weapons],
                "start_time": current.start_time.isoformat(),
                "end_time": current.end_time.isoformat(),
                "is_big_run": current.is_big_run,
                "is_team_contest": current.is_team_contest,
            }

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