import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = "Токен бота"  
CHAT_ID = "Айді чату" 

def send_telegram_message(text: str):
    """
    Відправляє текстове повідомлення в Telegram-чат за допомогою бота.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print(f"Помилка при відправці в Telegram: {response.text}")


def get_auto_ria_listings(
    brand_id: int,
    city_name: str,
    gearbox_id: int,
    max_mileage: int,
    max_price_usd: int,
    pages_to_check: int = 1
):
    results = []
    
    base_url = (
        "https://auto.ria.com/uk/search/"
        "?indexName=auto"
        f"&brand.id[0]={brand_id}"        # ідентифікатор бренду
        "&categories.main.id=1"          # легкові
        "&price.currency=1"              # USD
        f"&price.USD.lte={max_price_usd}"# max ціна у USD
        "&abroad.not=0"                  # не з-за кордону
        "&custom.not=1"                  # розмитнені
        f"&gearboxes.id={gearbox_id}"    # ідентифікатор коробки передач
        f"&mileage.lte={max_mileage}"    # максимальний пробіг
    )


    search_url = base_url + f"&city.name={city_name}"

    for page in range(1, pages_to_check + 1):
        url = search_url + f"&page={page}"
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Сторінка {page}: помилка доступу (статус {response.status_code})")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        

        listings = soup.select("section.ticket-item")
        
        for item in listings:

            title_tag = item.select_one(".ticket-title a")
            if not title_tag:
                continue
            
            link = title_tag.get("href", "").strip()
            title_text = title_tag.get_text(strip=True)

            # Ціна
            price_tag = item.select_one("div.price-ticket")
            if price_tag:
                price_text = price_tag.get_text(strip=True)
            else:
                price_text = "N/A"

            # Пробіг
            mileage_tag = item.select_one("li.item-char.js-race")
            if mileage_tag:
                mileage_text = mileage_tag.get_text(strip=True)
            else:
                mileage_text = "N/A"

            results.append({
                "title": title_text,
                "link": link,
                "price": price_text,
                "mileage": mileage_text
            })

    return results


if __name__ == "__main__":

    brand_id = 79         # Toyota
    city_name = "Kyiv"    
    gearbox_id = 2        # Автомат
    max_mileage = 400  
    max_price_usd = 8000  

    # Обходимо перші дві сторінки
    cars = get_auto_ria_listings(
        brand_id, 
        city_name, 
        gearbox_id, 
        max_mileage, 
        max_price_usd, 
        pages_to_check=2
    )

    if cars:
        lines = []
        for i, car in enumerate(cars, start=1):
            line = (
                f"<b>{i}. {car['title']}</b>\n"
                f"Ціна: {car['price']}\n"
                f"Пробіг: {car['mileage']}\n"
                f"Посилання: {car['link']}"
            )
            lines.append(line)
        full_message = "\n\n".join(lines)
        send_telegram_message(full_message)
    else:
        send_telegram_message("Нових авто за заданими параметрами не знайдено.")
    
    for i, car in enumerate(cars, start=1):
        print(f"{i}. {car['title']}")
        print(f"   Ціна: {car['price']}")
        print(f"   Пробіг: {car['mileage']}")
        print(f"   Посилання: {car['link']}")
        print("-" * 50)
