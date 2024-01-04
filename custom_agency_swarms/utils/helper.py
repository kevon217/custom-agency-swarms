from datetime import datetime


def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError("Invalid date format. Use 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'")


def filter_fobjs_by_date_range(file_objs, start_date, end_date):
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    return [f for f in file_objs if start_timestamp <= f.created_at < end_timestamp]
