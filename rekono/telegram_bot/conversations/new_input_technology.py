import logging

from parameters.serializers import InputTechnologySerializer
from telegram import ParseMode
from telegram.ext import CallbackContext, ConversationHandler
from telegram.update import Update
from telegram.utils.helpers import escape_markdown
from telegram_bot.context import PROJECT, STATES, TARGET
from telegram_bot.conversations.ask import ask_for_project, ask_for_target
from telegram_bot.conversations.cancel import cancel
from telegram_bot.conversations.selection import clear
from telegram_bot.conversations.states import CREATE
from telegram_bot.messages.errors import create_error_message
from telegram_bot.messages.parameters import (ASK_FOR_NEW_INPUT_TECHNOLOGY,
                                              NEW_INPUT_TECHNOLOGY)
from telegram_bot.security import get_chat

logger = logging.getLogger()                                                    # Rekono logger


def new_input_technology(update: Update, context: CallbackContext) -> int:
    '''Request new input technology creation via Telegram Bot.

    Args:
        update (Update): Telegram Bot update
        context (CallbackContext): Telegram Bot context

    Returns:
        int: Conversation state
    '''
    chat = get_chat(update)                                                     # Get Telegram chat
    if chat and context.chat_data is not None:
        if PROJECT in context.chat_data:                                        # Project already selected
            # Configure next steps
            context.chat_data[STATES] = [(CREATE, ASK_FOR_NEW_INPUT_TECHNOLOGY)]
            return ask_for_target(update, context, chat)                        # Ask for target selection
        else:                                                                   # No selected project
            context.chat_data[STATES] = [                                       # Configure next steps
                (None, ask_for_target),
                (CREATE, ASK_FOR_NEW_INPUT_TECHNOLOGY)
            ]
            return ask_for_project(update, context, chat)                       # Ask for project creation
    return ConversationHandler.END                                              # Unauthorized: end conversation


def create_input_technology(update: Update, context: CallbackContext) -> int:
    '''Create new input technology via Telegram Bot.

    Args:
        update (Update): Telegram Bot update
        context (CallbackContext): Telegram Bot context

    Returns:
        int: Conversation state
    '''
    clear(context, [STATES])                                                    # Clear Telegram context
    chat = get_chat(update)                                                     # Get Telegram chat
    if chat and context.chat_data is not None and update.effective_message:
        if update.effective_message.text == '/cancel':                          # Check if cancellation is requested
            return cancel(update, context)                                      # Cancel operation
        name = update.effective_message.text
        version = None
        if name and ' - ' in name:
            aux = name.split(' - ')
            name = aux[0]
            version = aux[1]
        serializer = InputTechnologySerializer(                                 # Prepare input technology data
            data={'target': context.chat_data[TARGET].id, 'name': name, 'version': version}
        )
        if serializer.is_valid():                                               # Input technology is valid
            input_technology = serializer.save()                                # Create input technology
            logger.info(
                f'[Telegram Bot] New input technology {input_technology.id} has been created',
                extra={'user': chat.user.id}
            )
            update.effective_message.reply_text(                                # Confirm input technology creation
                NEW_INPUT_TECHNOLOGY.format(
                    name=escape_markdown(input_technology.name, version=2),
                    target=escape_markdown(input_technology.target.target, version=2)
                ), parse_mode=ParseMode.MARKDOWN_V2
            )
        else:                                                                   # Invalid input technology data
            logger.info(
                '[Telegram Bot] Attempt of input technology creation with invalid data',
                extra={'user': chat.user.id}
            )
            # Send error details
            update.effective_message.reply_text(
                create_error_message(serializer.errors),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            # Re-ask for the new input technology
            update.effective_message.reply_text(ASK_FOR_NEW_INPUT_TECHNOLOGY)
            return CREATE                                                       # Repeat the current state
    clear(context, [TARGET])                                               # Clear Telegram context
    return ConversationHandler.END                                              # End conversation
