import asyncio
import logging
import os
import random


from dotenv import load_dotenv


from telegram import Update

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,  # type: ignore
)
from telegram import LinkPreviewOptions


from telegram.constants import ParseMode


from telegram.ext import (
    Application,
    ContextTypes,
    filters,
)

from telegram.ext import (
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
)


from my_modules.some_inline_keyboards import keyboard_options, keyboard_options_aplhabet
from my_modules.some_url_link import ImageLinks, MessageEffectEmojies


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

GOOD_EFFECTS = [
    MessageEffectEmojies.LIKE.value,
    MessageEffectEmojies.HEART.value,
    MessageEffectEmojies.TADA.value,
]


async def start_cmd_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """It will exxecute when /start will come"""

    if update.message is None or update.message.from_user is None:
        print("This should Not happens 🧐🧐🧐")
        return

    user = update.message.from_user

    text = (
        f"Hello {user.full_name} You have just start this bot thanks. "
        f"I will send you this message, and after 3 second i will edit this again."
    )

    link_previes_options = LinkPreviewOptions(
        is_disabled=False,
        url=ImageLinks.RU_IMAGE.value,
        show_above_text=True,
        prefer_small_media=True,
    )

    msg_send = await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        link_preview_options=link_previes_options,
        message_effect_id=random.choice(GOOD_EFFECTS),
    )

    await asyncio.sleep(3)

    await context.bot.edit_message_text(
        text="New TExt after edit",
        chat_id=user.id,
        message_id=msg_send.message_id,
        reply_markup=InlineKeyboardMarkup(keyboard_options_aplhabet),
    )


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """It will exxecute when /start will come"""

    if update.message is None or update.message.from_user is None:
        print("This should Not happens 🧐🧐🧐")
        return

    link_previes_options = LinkPreviewOptions(
        is_disabled=True,
        url=ImageLinks.RU_IMAGE.value,
        show_above_text=True,
        prefer_small_media=True,
    )

    user = update.message.from_user

    text = f"Hello {user.full_name} This is a checking button message."

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        link_preview_options=link_previes_options,
        message_effect_id=random.choice(GOOD_EFFECTS),
        reply_markup=InlineKeyboardMarkup(keyboard_options),
    )
    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        link_preview_options=link_previes_options,
        message_effect_id=random.choice(GOOD_EFFECTS),
        reply_markup=InlineKeyboardMarkup(keyboard_options_aplhabet),
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


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    wher user will press button it should be execute with proper callback data
    """

    if update.callback_query is None:
        print("This shuld not happens as always callback query exists.")
        return

    query = update.callback_query

    await context.bot.answerCallbackQuery(
        callback_query_id=query.id,
        text=f"You have pressed this button.",
        show_alert=True,
    )

    user = query.from_user
    button_data = query.data

    text = (
        f"Hello {user.full_name} The button data which was assign with the button is \n"
        f"<blockquote>{button_data}</blockquote> \n"
        f"The Button Message will delete after 3 Seconds."
    )

    msg_send = await context.bot.send_message(  # type: ignore
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    await asyncio.sleep(3)

    try:
        await context.bot.deleteMessage(
            chat_id=user.id,
            message_id=query.message.message_id,  # type: ignore
        )
    except Exception as e:
        print(f"Message deletion failed: {e}")


async def new_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """When user will want to make anew note."""

    if update.message is None or update.message.from_user is None:
        print("This should Not happens 🧐🧐🧐")
        return

    print("This has not implimented yet.")


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
            command=["help"],
            callback=start_cmd_old,
            block=False,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["start", "st"],
            callback=start_cmd,
            block=False,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["new_note"],
            callback=new_note_cmd,
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

    application.add_handler(
        CallbackQueryHandler(
            callback=button,
            block=False,
        )
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
