import os
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BITLY_TOKEN = os.getenv("BITLY_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)  # ✅ Gunakan bot sebagai parameter

async def shorten_url(long_url):
    """Memendekkan URL menggunakan Bitly API"""
    headers = {
        "Authorization": f"Bearer {BITLY_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"long_url": long_url}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api-ssl.bitly.com/v4/shorten", json=data, headers=headers) as response:
            res_data = await response.json()
            print("Bitly Response:", res_data)  # ✅ Debug log

            if response.status == 200 and "link" in res_data:
                return res_data["link"]
    
    return long_url  # Jika gagal, gunakan link asli

async def generate_caption(link):
    """Membuat caption otomatis dengan link yang telah dipendekkan"""
    return f"🔥 Cek produk menarik ini! 🔥\n🔗 {link} \n🛒 Beli sekarang sebelum kehabisan!"

@dp.message()
async def process_message(message: Message):
    """Memproses pesan dari pengguna dan mengirim balasan"""
    user_link = message.text.strip()

    if "shopee.co.id" in user_link or "tokopedia.com" in user_link:
        short_link = await shorten_url(user_link)  # 🔗 Perpendek link
        caption = await generate_caption(short_link)
        await message.answer(caption)
    else:
        await message.answer("❌ Kirim link Shopee atau Tokopedia yang valid.")

async def main():
    """Menjalankan bot dengan polling"""
    print("✅ Bot sedang berjalan...")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
