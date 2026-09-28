import re
try:
    with open("log.txt", encoding="windows-1251") as log:
        log_text = log.read()
except:
    print("Ошибка при работе с файлом")

print("Строки с ERROR или WARN:")
# регулярка для поиска уровня warn илт error
pattern_w = r'^(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<level>ERROR|WARN)\s+(?P<message>.*)$'
#вывод
for m in re.finditer(pattern_w, log_text, re.MULTILINE):
    print(f"{m.group('time')}  {m.group('level')}  {m.group('message')}")

print("Строки, где упоминаются IP-адреса:")
# регулярка для нахождения IP
ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
# проходим по каждой строке и проверяем, есть ли в ней IP
for line in log_text.split('\n'):
    if re.search(ip_pattern, line):
        # вывод
        parts = line.split(' ', 3)
        time = f"{parts[0]} {parts[1]}"
        level = parts[2]
        message = parts[3]
        print(f"{time}  {level}  {message}")
