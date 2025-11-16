from datetime import datetime, date, timedelta
import re

def get_current_quarter(today: date = None) -> str:
    if today is None:
        today = date.today()
    year = today.year
    quarter = (today.month - 1) // 3 + 1
    return f"{year}-Q{quarter}"

def get_quarter_dates(quarter_str: str):
    match = re.match(r"(\d{4})-Q(\d)", quarter_str)
    if not match:
        return None, None
    
    year = int(match.group(1))
    quarter = int(match.group(2))
    
    start_month = (quarter - 1) * 3 + 1
    start_date = date(year, start_month, 1)
    
    end_month = quarter * 3
    if end_month == 12:
        end_date = date(year, 12, 31)
    else:
        end_date = date(year, end_month + 1, 1) - timedelta(days=1)
    
    return start_date, end_date

def render_template_string(template: str, variables: dict) -> str:
    result = template
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        result = result.replace(placeholder, str(value))
    return result

def days_since(dt: datetime) -> int:
    if dt is None:
        return None
    delta = datetime.utcnow() - dt
    return delta.days

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M") -> str:
    if dt is None:
        return "Never"
    return dt.strftime(format_str)
