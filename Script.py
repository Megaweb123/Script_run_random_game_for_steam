from pathlib import Path
import subprocess
import random

def find_acf_files(directory):
    p = Path(directory)
    return list(p.rglob('*.acf'))
print('Введите название дисков, на которых у вас установленны игры Steam через ";"\nПример:\nC:\Program Files (x86)\Steam\steamapps;D:\Steam\steamapps')
directorys = input()
directorys_list = directorys.split(';')
print('\n\n\nТеперь ждем запуска игры и радуемся 😉\n\n\n')
all_games = {}
print(directorys_list)
for i in directorys_list:
    start_directory = f"{i}\\"
    acf_files = find_acf_files(start_directory)

    for acf_file in acf_files:
        with open(acf_file, "r", encoding='utf-8-sig') as f:
            string = f.read()
        try:
            BytesToDownload = string.find('BytesToDownload')
            BytesDownloaded = string.find('BytesDownloaded')
            BytesToStage = string.find('BytesToStage')
            BytesToDownload_bytes = string[BytesToDownload-1:BytesDownloaded-1].strip()[:-1].rfind('"')
            BytesDownloaded_bytes = string[BytesDownloaded-1:BytesToStage-1].strip()[:-1].rfind('"')
            a = string[BytesToDownload-1:BytesDownloaded-1].strip()[BytesToDownload_bytes + 1:-1].strip()
            b = string[BytesDownloaded-1:BytesToStage-1].strip()[BytesToDownload_bytes + 1:-1].strip()

            if a == b:
                name_a = string.find('name')
                name_b = string.find('StateFlags')
                name = string[name_a:name_b-1].strip()
                name_c = name[:-1]
                game_name = name_c[name[:-1].rfind('"')+1:]
                id_a = string.find('appid')
                id_b = string.find('universe')
                id = string[id_a:id_b-1].strip()
                id_c = id[:-1]
                game_id = id_c[id[:-1].rfind('"')+1:]
                all_games[game_name] = game_id
                print(f'Добавил в список игру {game_name}')
        except ValueError as err:
            print(err)


names_games = []
for i in all_games.keys():
    if i != '':
        names_games.append(i)

random.choice(names_games)
start = f'steam://rungameid/{all_games[random.choice(names_games)]}'
print(f'Всего найдено игр: {len(all_games)} шт.')
# Выполнение команды и получение результата
subprocess.run(['start', start], shell=True)

