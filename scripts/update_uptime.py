"""
Recalculates the "Uptime" field in dark-mode.svg based on a fixed date of birth,
so it always reflects the current age instead of being hardcoded.
"""
import re
from datetime import date, datetime, timezone

from dateutil.relativedelta import relativedelta

DOB = date(2004, 9, 2)
SVG_PATH = "dark-mode.svg"


def compute_uptime(today: date) -> str:
    rd = relativedelta(today, DOB)
    years = rd.years
    months = rd.months
    days = rd.days

    parts = []
    parts.append(f"{years} year{'s' if years != 1 else ''}")
    parts.append(f"{months} month{'s' if months != 1 else ''}")
    parts.append(f"{days} day{'s' if days != 1 else ''}")
    return ", ".join(parts)


def main():
    today = datetime.now(timezone.utc).date()
    uptime_str = compute_uptime(today)

    with open(SVG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Matches: <tspan class="key">Uptime</tspan>:<tspan class="cc"> ... </tspan><tspan class="value">OLD VALUE</tspan>
    pattern = re.compile(
        r'(<tspan class="key">Uptime</tspan>:<tspan class="cc">[^<]*</tspan><tspan class="value">)'
        r'[^<]*'
        r'(</tspan>)'
    )

    new_content, count = pattern.subn(rf"\g<1>{uptime_str}\g<2>", content)

    if count == 0:
        raise SystemExit("Could not find the Uptime field in the SVG — check the pattern.")

    if new_content != content:
        with open(SVG_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated Uptime to: {uptime_str}")
    else:
        print(f"Uptime already up to date: {uptime_str}")


if __name__ == "__main__":
    main()
