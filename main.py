import os


import logging

from dotenv import load_dotenv

from telegram import Update
from telegram import LinkPreviewOptions

from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

from telegram.constants import ParseMode

from my_modules.some_url_link import (
    ImageLinks,
    MessageEffectEmojies,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """It will exxecute when /start will come"""

    if update.message is None or update.message.from_user is None:
        print("This should Not happens 🧐🧐🧐")
        return

    user = update.message.from_user

    text = (
        f"Hello {user.full_name} You have just start this bot thanks. "
        f"The link is: Nothing"
    )

    link_previes_options = LinkPreviewOptions(
        is_disabled=False,
        url=ImageLinks.RU_IMAGE.value,
        show_above_text=True,
        prefer_small_media=True,
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        link_preview_options=link_previes_options,
        message_effect_id=MessageEffectEmojies.HEART.value,
    )


async def echo_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is just come when normal text message is received by user"""

    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        print("This should Not happens 🧐🧐🧐")
        return

    user = update.message.from_user
    user_msg = update.message.text

    text = f"Hello {user.full_name} You have send me: \n\n" f"{user_msg.upper()}"
    await context.bot.send_message(user.id, text, ParseMode.HTML)


def main() -> None:
    """STarting the bot"""

    load_dotenv()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if BOT_TOKEN is None:
        print(
            ".no .env file or env file has not any bot token. Please make sure the token is there and re run this program."
        )
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler(
            command=["start", "st"],
            callback=start_cmd,
            block=False,
        )
    )

    application.add_handler(
        MessageHandler(
            filters=filters.TEXT,
            callback=echo_msg,
            block=False,
        )
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
