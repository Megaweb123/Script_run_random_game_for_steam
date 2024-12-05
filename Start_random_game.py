from pathlib import Path
import subprocess
import random
import time

def find_acf_files(directory):
    p = Path(directory)
    return list(p.rglob('*.acf'))
print('Введите путь до всех steamapps, которые у вас установленны через ";"\n\nПример:\n        C:\Program Files (x86)\Steam\steamapps ; D:\Steam\steamapps        ')
directorys = input()
directorys_list = directorys.split(';')
print('\n\n\nИщу игры, устанновленые в указанных дирикториях\n\n\n')
all_games = {}
for i in directorys_list:
    start_directory = f"{i.strip()}\\"
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
                if game_name == '':
                    break
                id_a = string.find('appid')
                id_b = string.find('universe')
                id = string[id_a:id_b-1].strip()
                id_c = id[:-1]
                game_id = id_c[id[:-1].rfind('"')+1:]
                all_games[game_name] = game_id
                print(f'Добавил в список игру {game_name}, id = {game_id}')
        except ValueError as err:
            print(err)


names_games = []
for i in all_games.keys():
    if i != '':
        names_games.append(i)
game_for_play = random.choice(names_games)
start = f'steam://rungameid/{all_games[game_for_play]}'
print(f'\nВсего найдено игр: {len(all_games)} шт.')
print(f'\nИгра, в которую ты будешь играть, называется: {game_for_play}\nПриятной игры!\n\n\n')
print(f'Нажни Enter чтобы начать!')
go = input()
# Выполнение команды и получение результата
subprocess.run(['start', start], shell=True)

