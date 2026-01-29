#!/usr/bin/env python3
"""Обогащение данных солдат статусами с pamyat-naroda.ru"""

import requests
import time
import json
from pathlib import Path

# Подтверждённые записи из make_excel_full.py
confirmed = [
    {"f":"Аверин","n":"Михаил","p":"Кондратьевич","y":"1903","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК, Удмуртская АССР, Кизнерский р-н, 6 зап.","u":"https://pamyat-naroda.ru/heroes/isp-chelovek_spisok18314620/"},
    {"f":"Аверин","n":"Михайл","p":"(Михаил)","y":"1903","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК, Удмуртская АССР, Кизнерский р-н, 6 зап.","u":"https://pamyat-naroda.ru/heroes/isp-chelovek_spisok18406530/"},
    {"f":"Афанов","n":"Василий","p":"Дмитриевич","y":"1914","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123509136/"},
    {"f":"Афонов","n":"Василий","p":"Николаевич","y":"1901","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103270115/"},
    {"f":"Афонов","n":"Игнатий","p":"Павлович","y":"1911","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123509219/"},
    {"f":"Ветошкин","n":"Михаил","p":"Афанасьевич","y":"1915","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"","u":"https://pamyat-naroda.ru/heroes/podvig-chelovek_yubileinaya_kartoteka1519157425/"},
    {"f":"Ветошкин","n":"Аркадий","p":"Степанович","y":"1924","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК, 302 оадн ВМБ","u":"https://pamyat-naroda.ru/heroes/isp-chelovek_spisok17011248/"},
    {"f":"Ветошкин","n":"Григорий","p":"Герасимович","y":"1898","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"","u":"https://pamyat-naroda.ru/heroes/memorial-chelovek_vpp1986685156/"},
    {"f":"Ветошкин","n":"Григорий","p":"Герасимович","y":"1908","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"","u":"https://pamyat-naroda.ru/heroes/memorial-chelovek_vpp1986664706/"},
    {"f":"Ветошкин","n":"Дмитрий","p":"Сидорович","y":"1905","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123507949/"},
    {"f":"Ветошкин","n":"Петр","p":"Тимофеевич","y":"1913","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103271361/"},
    {"f":"Зонов","n":"Леонид","p":"Михайлович","y":"1920","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"","u":"https://pamyat-naroda.ru/heroes/person-hero50067429/"},
    {"f":"Ижовкин","n":"Андрей","p":"Николаевич","y":"1920","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123379342/"},
    {"f":"Ижовкин","n":"Иван","p":"Андреевич","y":"1907","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"1164 сп, 11 уч. отрп","u":"https://pamyat-naroda.ru/heroes/person-hero121412078/"},
    {"f":"Карпов","n":"Иван","p":"Ильич","y":"1920","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/memorial-chelovek_dopolnitelnoe_donesenie58876939/"},
    {"f":"Кузнецов","n":"Николай","p":"Иванович","y":"1909","b":"Удмуртская АССР, д. Вишур","s":"357 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103606963/"},
    {"f":"Кузьмин","n":"Михаил","p":"Ефимович","y":"1907","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123508706/"},
    {"f":"Кузьмин","n":"Михаил","p":"Ильич","y":"1909","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123508708/"},
    {"f":"Кузьмин","n":"Николай","p":"Алексеевич","y":"1921","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123381038/"},
    {"f":"Кузьмин","n":"Николай","p":"Ильич","y":"1925","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103670588/"},
    {"f":"Кузьмин","n":"Яков","p":"Алексеевич","y":"1923","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК. Картотека ранений","u":"https://pamyat-naroda.ru/heroes/kld-card_ran51645599/"},
    {"f":"Морозов","n":"Алексей","p":"Иванович","y":"1909","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103625208/"},
    {"f":"Морозов","n":"Роман","p":"Иванович","y":"1911","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero100413642/"},
    {"f":"Оверин","n":"Александр","p":"Терентьевич","y":"1910","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"39 А 381 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero96399160/"},
    {"f":"Оконников","n":"Михаил","p":"Федорович","y":"1925","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103658185/"},
    {"f":"Оконников","n":"Егор","p":"Григорьевич","y":"1918","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103264656/"},
    {"f":"Перевозчиков","n":"Михаил","p":"Григорьевич","y":"1908","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123509600/"},
    {"f":"Перевозчиков","n":"Прохор","p":"Матвеевич","y":"1910","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123509607/"},
    {"f":"Решетников","n":"Павел","p":"Николаевич","y":"1909","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"22 А 98 сд, Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123509712/"},
    {"f":"Романов","n":"Филипп","p":"Кириллович","y":"1922","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК. Картотека ранений","u":"https://pamyat-naroda.ru/heroes/kld-card_ran44107006/"},
    {"f":"Романов","n":"Николай","p":"Кириллович","y":"1925","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103672140/"},
    {"f":"Семаков","n":"Иван","p":"Иванович","y":"1922","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero123402944/"},
    {"f":"Сушаков","n":"Петр","p":"Иванович","y":"1925","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"","u":"https://pamyat-naroda.ru/heroes/person-hero100797404/"},
    {"f":"Хаймин","n":"Николай","p":"Алексеевич","y":"1923","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"320 сп 11 див. Картотека ранений","u":"https://pamyat-naroda.ru/heroes/kld-card_ran33721784/"},
    {"f":"Хасанов","n":"Галимзян","p":"Галеевич","y":"1922","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Ижевский ГВК","u":"https://pamyat-naroda.ru/heroes/person-hero100542451/"},
    {"f":"Хасанов","n":"Гамаутян","p":"Галеевич","y":"1922","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"","u":"https://pamyat-naroda.ru/heroes/sm-person_guk1065149584/"},
    {"f":"Шайхутдинов","n":"Хасанзян","p":"Шарифзянович","y":"1901","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"Кизнерский РВК","u":"https://pamyat-naroda.ru/heroes/person-hero103273251/"},
    {"f":"Широбоков","n":"Федор","p":"Андреевич","y":"1919","b":"Удмуртская АССР, Кизнерский р-н, д. Вишур","s":"","u":"https://pamyat-naroda.ru/heroes/memorial-chelovek_plen307070948/"},
]

def extract_status_from_url_type(url: str) -> str:
    """Определяет статус по типу URL (эвристика)."""
    url_lower = url.lower()

    # memorial-chelovek_plen - военнопленные
    if 'plen' in url_lower:
        return 'Плен'

    # memorial-chelovek_vpp - военно-пересыльный пункт (часто пропавшие)
    if 'vpp' in url_lower:
        return 'Пропал без вести'

    # memorial-chelovek_dopolnitelnoe_donesenie - донесение о потерях
    if 'donesenie' in url_lower:
        return 'Погиб/Пропал'

    # kld-card_ran - картотека ранений
    if 'card_ran' in url_lower:
        return 'Ранен'

    # podvig-chelovek - награды (обычно выжил)
    if 'podvig' in url_lower:
        return 'Награждён'

    # sm-person_guk - сводные данные ГУК
    if 'guk' in url_lower:
        return 'Неизвестен'

    return None

def extract_status_from_html(html: str) -> str:
    """Извлекает статус из HTML страницы."""
    text = html.lower()

    # Приоритет поиска
    if 'погиб' in text or 'убит' in text:
        return 'Погиб'
    elif 'пропал без вести' in text:
        return 'Пропал без вести'
    elif 'умер от ран' in text:
        return 'Умер от ран'
    elif 'умер в плену' in text:
        return 'Умер в плену'
    elif 'военнопленн' in text or 'попал в плен' in text:
        return 'Плен'
    elif 'ранен' in text and 'картотека ранен' in text:
        return 'Ранен'
    elif 'вернулся' in text or 'демобилизован' in text:
        return 'Вернулся'

    return None

def fetch_status(url: str) -> str:
    """Загружает страницу и извлекает статус."""
    # Сначала пробуем по типу URL
    url_status = extract_status_from_url_type(url)
    if url_status and url_status != 'Неизвестен':
        return url_status

    # Загружаем страницу
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            html_status = extract_status_from_html(resp.text)
            if html_status:
                return html_status
    except Exception as e:
        print(f"  Ошибка загрузки {url}: {e}")

    return url_status or 'Неизвестен'

def main():
    print(f"Обогащение статусами {len(confirmed)} записей...")
    print("-" * 60)

    results = []

    for i, soldier in enumerate(confirmed, 1):
        fio = f"{soldier['f']} {soldier['n']} {soldier['p']}"
        url = soldier['u']

        print(f"[{i:2}/{len(confirmed)}] {fio}...")

        status = fetch_status(url)
        soldier['status'] = status
        results.append(soldier)

        print(f"         → {status}")

        # Пауза между запросами
        if i < len(confirmed):
            time.sleep(1)

    # Сохраняем результаты
    output_path = Path("/Users/popov/Downloads/confirmed_with_status.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("-" * 60)
    print(f"Результаты сохранены: {output_path}")

    # Статистика
    stats = {}
    for r in results:
        s = r['status']
        stats[s] = stats.get(s, 0) + 1

    print("\nСтатистика:")
    for status, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {status}: {count}")

if __name__ == "__main__":
    main()
