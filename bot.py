from client import app
import asyncio
import logging
from pyrogram import filters, types, idle, errors
import utils
from pykeyboard import InlineKeyboard

logging.basicConfig(level=logging.INFO)

jobs_default = """
**📖 Current Page**: `{}`

- Showing __{}__ Jobs out of __{}__ Jobs
"""


@app.on_message(filters.command('jobs'))
async def jobs_msg(client, message):
    keyboard = InlineKeyboard()
    data = await utils.check('jobs', 1)
    last_page = int(data.links.last.replace('?page=', ''))
    keyboard.paginate(last_page, 1, 'page_{number}')
    btn = []
    to_append = []
    for job in data.data:
        to_append.append(types.InlineKeyboardButton(job.title[:25], callback_data=f'job_{job.id}'))
        if len(to_append) > 1:
            btn.append(to_append)
            to_append = []
            if to_append:
                btn.append(to_append)
    btn.append(keyboard.inline_keyboard[0])
    try:
        await message.edit(
            jobs_default.format(
                data.meta.current_page,
                data.meta.to,
                data.meta.total
            ),
            reply_markup=types.InlineKeyboardMarkup(btn)
        )
    except errors.MessageIdInvalid:
        await message.reply(
            jobs_default.format(
                data.meta.current_page,
                data.meta.to,
                data.meta.total
            ),
            reply_markup=types.InlineKeyboardMarkup(btn)
        )


@app.on_callback_query(utils.page_filter)
async def page_btn(client, query):
    keyboard = InlineKeyboard()
    page = int(query.data.split('_')[1])
    data = await utils.check('jobs', page)
    last_page = int(data.links.last.replace('?page=', ''))
    keyboard.paginate(last_page, page, 'page_{number}')
    btn = []
    to_append = []
    for job in data.data:
        to_append.append(types.InlineKeyboardButton(
            job.title[:25],
            callback_data=f'job_{job.id}')
        )
        if len(to_append) > 1:
            btn.append(to_append)
            to_append = []
            if to_append:
                btn.append(to_append)
    btn.append(keyboard.inline_keyboard[0])
    try:
        await query.message.edit(
            jobs_default.format(
                data.meta.current_page,
                data.meta.to,
                data.meta.total
            ),
            reply_markup=types.InlineKeyboardMarkup(btn)
        )
    except errors.MessageNotModified:
        return await query.answer()
    await query.answer()
    
@app.on_callback_query(utils.job_filter)
async def job_btn(client, query):
    job_id = query.data.split('_')[1]
    btn = []
    data = (await utils.check_job(job_id)).data
    text = f"**Company:**\n{data.company.name} {'✅' if data.company.is_verified else ''}\n\n"
    text += f"**Job Title:** `{data.title}`\n"
    text += f"**Catagory:** `{data.category}`\n"
    text += f"**Type:** `{data.type}`\n"
    text += f"**Experience:** `{data.experience}`\n"
    text += f"**Qualification:** `{data.qualification}`\n"
    text += f"**Salary:** `{data.salary_range}`\n"
    text += f"**Location:** `{data.location}`\n"
    text += f"**No. of Vacancies:** `{data.no_of_vacancies}`\n"
    text += f"\n**Description:**\n__{data.description}__\n"
    text += f"**Due Date:** `{data.due_date}`\n"
    if data.ref_no:
        text += f"**Ref No.:** `{data.ref_no}`\n"
    text += f"**Created at:** `{data.created_at}`\n"
    text += f"**Updated at:** `{data.updated_at}`\n"
    if data.attachment:
        btn.append(types.InlineKeyboardButton('Attachment', url=data.attachment))
    btn.append(types.InlineKeyboardButton('Back', callback_data='back_btn'))
    await query.message.edit(
        text,
        reply_markup=types.InlineKeyboardMarkup([btn])
    )
    await query.answer()

@app.on_callback_query(filters.regex('back_btn'))
async def back_btn(client, query):
    await asyncio.gather(
        jobs_msg(client, query.message)
    )
    



asyncio.run(app.run())