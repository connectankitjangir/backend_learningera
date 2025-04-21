import requests

TELEGRAM_BOT_TOKEN = '7718527285:AAGdmXZUPmDKpfzx1y72FyaWs-7VxHtJMno'
TELEGRAM_CHAT_ID = '5775875863'

def send_result(data):
    # Format the message with all typing test data
    message = (
        f"🧑‍💻 *Typing Test Results*\n\n"
        f"📊 *Performance Metrics*\n"
        f"• Gross Speed: {data['gross_typing_speed']} WPM\n"
        f"• Net Speed: {data['net_typing_speed']} WPM\n"
        f"• Error Rate: {data['error_percentage']}%\n\n"
        f"❌ *Errors Breakdown*\n"
        f"• Capitalization: {len(data['capital_errors'])} errors\n"
        f"• Spelling: {len(data['spelling_errors'])} errors\n"
        f"• Space: {len(data['space_errors'])} errors\n"
        f"• Punctuation: {len(data['punctuation_errors'])} errors\n"
        f"• Transposition: {len(data['transposition_errors'])} errors\n"
        f"• Omission: {len(data['omission_errors'])} errors\n\n"
        f"📝 *Passage Details*\n"
        f"• Passage ID: {data['passage_id']}\n"
        f"• Words Matched: {len(data['matched_word_list'])}\n"
        f"• Total Words: {len(data['given_passage_words'])}\n\n"
        f"📋 *Raw Data*\n"
        f"```\n"
        f"Given Passage: {' '.join(data['given_passage_words'])}\n"
        f"Typed Passage: {' '.join(data['typed_passage_words'])}\n"
        f"Capital Errors: {data['capital_errors']}\n"
        f"Spelling Errors: {data['spelling_errors']}\n"
        f"Space Errors: {data['space_errors']}\n"
        f"Punctuation Errors: {data['punctuation_errors']}\n"
        f"Transposition Errors: {data['transposition_errors']}\n"
        f"Omission Errors: {data['omission_errors']}\n"
        f"```"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
