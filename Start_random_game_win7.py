from pathlib import Path
import subprocess
import random

def find_acf_files(directory):
    p = Path(directory)
    return list(p.rglob('*.acf'))

print('Введите путь до всех steamapps, которые у вас установлены через ";"\nПример:\n        C:/Program Files (x86)/Steam/steamapps ; D:/Steam/steamapps        ')
directorys = input()
directorys_list = directorys.split(';')
print('\n\n\nИщу игры, установленные в указанных директориях\n\n\n')
all_games = {}

for i in directorys_list:
    start_directory = "{}\\".format(i.strip())
    acf_files = find_acf_files(start_directory)
    
    for acf_file in acf_files:
        with open(str(acf_file), "r", encoding='utf-8-sig') as f:  # Преобразуем acf_file в строку
            string = f.read()
            #print('string={}'.format(string))
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
                    if game_name == '' or game_name == 'Borderless Gaming':
                        break
                    id_a = string.find('appid')
                    id_b = string.find('Universe')
                    id1 = string[id_a:id_b-1].strip()
                    print('id1={}'.format(id1))
                    id_c = id1[:-1]
                    game_id = id_c[id1[:-1].rfind('"')+1:]
                    all_games[game_name] = game_id
                    print('Добавил в список игру {}, id={}'.format(game_name, game_id))
            except ValueError as err:
                print(err)

names_games = list(all_games.keys())

if names_games:
    game_for_play = random.choice(names_games)
    start = 'steam://run/{}'.format(all_games[game_for_play])
    print('\nВсего найдено игр: {} шт.'.format(len(all_games)))
    print('\nИгра, в которую ты будешь играть, называется: {}\nПриятной игры!\n\n\n'.format(game_for_play))
    input('Нажми Enter чтобы начать!')
    subprocess.run(['start', start], shell=True)
else:
    print("Игры не найдены.")
