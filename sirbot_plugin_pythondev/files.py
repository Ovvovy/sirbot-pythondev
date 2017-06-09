import re
import logging

from sirbot.slack.hookimpl import hookimpl
from sirbot.slack.message import Attachment, Select

logger = logging.getLogger('sirbot.pythondev')


async def file(command, slack, *_):
    response = command.response()

    if command.text == 'intro':
        response.response_type = 'in_channel'
        response.text = 'https://pythondev.slack.com/files/mikefromit/F25EDF4KW/Intro_Doc'  # noQa
    elif command.text == 'what to do':
        response.response_type = 'in_channel'
        response.text = 'https://pythondev.slack.com/files/ndevox/F4A137J0J/What_to_do_next_on_your_Python_journey'  # noQa
    else:
        att = Attachment(
            title='Choose a file to show',
            fallback='Choose a file to show',
            callback_id='choose_file'
        )

        data = [
            {
                'text': 'Intro doc',
                'value': 'intro_doc'
            },
            {
                'text': 'What to do doc',
                'value': 'what_to_do_doc'
            }
        ]

        select = Select(
            name='choose_file',
            text='Choose a file',
            options=data
        )
        att.actions.append(select)
        response.attachments.append(att)

    await slack.send(response)


async def choose_file(action, slack, *_):
    value = action.action['selected_options'][0]['value']
    response = action.response()

    if value == 'intro_doc':
        response.replace_original = False
        response.text = 'https://pythondev.slack.com/files/mikefromit/F25EDF4KW/Intro_Doc'  # noQa
    elif value == 'what_to_do_doc':
        response.replace_original = False
        response.text = 'https://pythondev.slack.com/files/ndevox/F4A137J0J/What_to_do_next_on_your_Python_journey'  # noQa
    else:
        response.text = '''Sorry we could not find this file'''

    await slack.send(response)


async def intro_doc(message, slack, *_):
    response = message.response()
    response.text = 'https://pythondev.slack.com/files/mikefromit/F25EDF4KW/Intro_Doc'  # noqa
    await slack.send(response)


async def what_to_do(message, slack, *_):
    response = message.response()
    response.text = 'https://pythondev.slack.com/files/ndevox/F4A137J0J/What_to_do_next_on_your_Python_journey'  # noqa
    await slack.send(response)


@hookimpl
def register_slack_commands():
    commands = [
        {
            'command': '/file',
            'func': file,
            'public': False
        }
    ]

    return commands


@hookimpl
def register_slack_actions():
    commands = [
        {
            'callback_id': 'choose_file',
            'func': choose_file,
            'public': False
        }
    ]

    return commands


@hookimpl
def register_slack_messages():
    commands = [

        {
            'match': 'intro doc',
            'func': intro_doc,
            'mention': True,
            'flags': re.IGNORECASE
        },
        {
            'match': 'what to do',
            'func': what_to_do,
            'mention': True,
            'flags': re.IGNORECASE
        },
    ]

    return commands
