from datetime import datetime

process_date = lambda s: [int(n) for n in s.replace("-", " ").replace(":", " ").split()]
convert_to_date = lambda s: datetime(*process_date(s))
subtract_date = lambda s, d: convert_to_date(s) - d
convert_to_hours = lambda d: d.seconds // 3600