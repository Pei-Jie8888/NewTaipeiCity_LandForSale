import requests
from bs4 import BeautifulSoup
import re
import emoji

#lineNotify設定
def lineNotifyMessage(token, msg, imgUrl):

    # hearders 這兩項必帶
    # token 為 LINE Notinfy 申請的權杖
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type":  "application/x-www-form-urlencoded"
    }

    # message : 要顯示的文字
    # imageThumbnail、imageFullsize : 要顯示的圖片
    # stickerPackageId、stickerId : 貼圖
    message = {'message': msg, 'imageThumbnail':imgUrl,'imageFullsize':imgUrl}
    
    #透過 POST 傳送
    req = requests.post("https://notify-api.line.me/api/notify", headers = headers, data = message)
    
    return req.status_code

# 要抓取頁面的Url
url = "https://land.591.com.tw/list?type=2&kind=11&region=3&sort=posttime_desc&sale_price=$_2000$"

# 自訂 Request Headers
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Host": "land.591.com.tw",
}

response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all divs containing the item information
item_infos = soup.find_all("div", class_="item-info")

for item in item_infos:
    # 標題
    title_tag = item.find("a", class_="link")
    title = title_tag.getText().strip() if title_tag else "N/A"

    # 詳細資訊的 URL
    detailUrl = title_tag['href'] if title_tag else "N/A"

    # 第一张照片 (extracting only the first image from the image slider)
    img_tag = item.find_previous_sibling("div", class_="item-img").find("img")
    img_url = img_tag.get("data-src") if img_tag else "N/A"

    # 價格
    price_div = item.find("div", class_="item-info-price")
    price = price_div.getText().strip() if price_div else "N/A"

    # 簡易說明
    word_details = []
    item_info_txts = item.find_all("div", class_="item-info-txt")
    for txt in item_info_txts:
        word_details.append(txt.getText().strip())
    wordDetail = " | ".join(word_details)

    # 更新時間點
    uptime_tag = item.find("span", class_="tag refresh")
    uptime = uptime_tag.getText().strip() if uptime_tag else "N/A"

    # Check if the update time is within 3 hours
    # Handle "分鐘前更新" and "小時前更新"
    if "分鐘前更新" in uptime:
        minutes_pattern = re.compile('(.*)(?=分鐘)')
        minutes = re.search(minutes_pattern, uptime).group(1)
        if int(minutes) <= 720:  # 720 minutes = 24 hours
            within_3_hours = True
    elif "小時前更新" in uptime:
        hours_pattern = re.compile('(.*)(?=小時)')
        hours = re.search(hours_pattern, uptime).group(1)
        if int(hours) <= 24:
            within_3_hours = True
    else:
        within_3_hours = False

    if within_3_hours:
        # Prepare the LINE message with emojis
        msg = (f"\n小幫手來啦~ 😊\n土地更新資訊啦! 💥\n📢  {title}\n💵  {price}\n📝  {wordDetail}\n⏰  {uptime}\n\n🎉  看更詳細點↓網址 \n{detailUrl}")

        # Print the message to be sent to LINE
        print(msg)
        print('-------------')

        # 傳送LINE訊息
        lineNotifyMessage("qx3hVGmJODYzL7oQsfxc04AitR8QBmnN8G0YeGsAy4Z", msg, img_url)