import os
import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
بيانات التطبيق الخاصة بك من تليجرامspan_0span_0
API_ID = 34032166
API_HASH = "40b08873d8243c007cce3b39ac9d3ede"
BOT_TOKEN = "9137312509:AAEMaoA9QmUPMvVJwpTEGTQAG5f_8UOCK9Y"
app = Client(
"all_downloader_bot",
api_id=API_ID,
api_hash=API_HASH,
bot_token=BOT_TOKEN
)
رسالة البدء مع الأزرار الشفافة
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
user_name = message.from_user.first_name
welcome_text = (
f"مرحباً بك يا {user_name} في بوت التحميل الشامل! 🚀\n\n"
"أستطيع مساعدتك في تحميل الفيديوهات أو الصوتيات بدون علامة مائية من:\n"
"• يوتيوب (YouTube)\n"
"• تيك توك (TikTok)\n"
"• إنستجرام (Instagram)\n"
"• سناب شات (Snapchat)\n\n"
"فقط أرسل الرابط وسأعطيك خيارات التحميل فوراً 📥"
)
# زر قناة المطور
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("👨‍💻 قناة المطور", url="https://t.me/s202l")]
])

await message.reply(welcome_text, reply_markup=keyboard)
مراقبة الروابط والتحميل تلقائياً
@app.on_message(filters.text & ~filters.command(["start"]))
async def download_media(client: Client, message: Message):
url = message.text.strip()
# التحقق من أن النص عبارة عن رابط
if not (url.startswith("http://") or url.startswith("https://") or "t.me" in url):
    return

# إرسال رسالة جاري التحميل
processing_msg = await message.reply("⏳ **جاري معالجة الرابط وتحميل الفيديو، انتظر قليلاً...**")

# مجلد مؤقت لحفظ الفيديو
output_dir = "downloads"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# فك روابط تيك توك المختصرة لتجنب مشاكل التوجيه
if "tiktok.com" in url:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        if response.url and "about" not in response.url:
            url = response.url
    except Exception:
        pass

# إعدادات التحميل لكل المنصات
ydl_opts = {
    'format': 'best',
    'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
    'noplaylist': True,
    'quiet': True,
    'geo_bypass': True,
}

file_path = None
try:
    def run_ytdlp():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    file_path = await asyncio.to_thread(run_ytdlp)

    # إرسال الفيديو بعد نجاح التحميل مع زر قناة المطور
    if file_path and os.path.exists(file_path):
        await processing_msg.edit("📤 **جاري رفع الفيديو وإرساله...**")
        
        caption = "🚀 **تم التحميل بنجاح بواسطة @Q3Il3!**"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 قناة المطور", url="https://t.me/s202l")]
        ])

        await message.reply_video(video=file_path, caption=caption, reply_markup=keyboard)
        await processing_msg.delete()
    else:
        await processing_msg.edit("❌ عذراً، لم أستطع تحميل الفيديو. تأكد من صحة الرابط.")

except Exception as e:
    print(f"خطأ أثناء التحميل: {e}")
    clean_err = str(e).replace("[0;31m", "").replace("[0m", "").strip()
    await processing_msg.edit(f"❌ حدث خطأ أثناء التحميل:\n`{clean_err}`")

finally:
    # حذف الملف من السيرفر بعد إرساله للمحافظة على المساحة
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            pass
print("جاري تشغيل بوت التحميل الشامل...")
app.run()