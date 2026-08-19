import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# 从 GitHub Actions 环境变量中读取密钥
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

def generate_chart(filename="chart.png"):
    """本地生成一张演示图表（如数据监控走势图）"""
    plt.figure(figsize=(6, 3), dpi=150)
    plt.plot([1, 2, 3, 4, 5], [10, 25, 18, 30, 42], marker='o', color='#0088cc', linewidth=2)
    plt.title("GitHub Action Metric Report", fontsize=12)
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def send_telegram_photo_report(image_path):
    """发送带 HTML 富文本 Caption 的图片"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    # 构造 HTML 格式的复杂消息
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caption = (
        f"📊 <b>System Daily Monitoring Report</b>\n"
        f"⏱ <i>Generated at: {current_time} (UTC)</i>\n\n"
        f"<blockquote>"
        f"Status: 🟢 <b>HEALTHY</b>\n"
        f"Tasks Executed: <code>5/5 SUCCESS</code>\n"
        f"Response Time: <code>142ms</code>"
        f"</blockquote>\n\n"
        f"🔗 <a href='https://github.com'>View Dashboard Details</a>\n"
        f"#Monitor #GitHubActions #AutoReport"
    )

    data = {
        "chat_id": CHAT_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }

    with open(image_path, "rb") as photo:
        files = {"photo": photo}
        response = requests.post(url, data=data, files=files, timeout=30)
    
    res_data = response.json()
    if not res_data.get("ok"):
        raise RuntimeError(f"Telegram API Error: {res_data}")
    
    print("✅ Report and photo sent successfully!")

if __name__ == "__main__":
    img = generate_chart()
    send_telegram_photo_report(img)
