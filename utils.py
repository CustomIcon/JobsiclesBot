import aiohttp
from attrify import Attrify as atr
import ujson as json
import re
from pyrogram import filters

url = 'https://api.jobsicle.mv/v2'


async def check(method:str, page: int):
    async with aiohttp.ClientSession() as ses:
        async with ses.get(
            url + '/' + method,
            params={'page': page}
        ) as resp:
            data = await resp.read()
            return atr(json.loads(data))
        

async def check_job(job_id: str):
    async with aiohttp.ClientSession() as ses:
        async with ses.get(
            url + '/jobs/' + job_id,
        ) as resp:
            data = await resp.read()
            return atr(json.loads(data))


def page_callback(_, __, query):
    if re.match('page_', query.data):
        return True
    
def job_callback(_, __, query):
    if re.match('job_', query.data):
        return True

page_filter = filters.create(page_callback)
job_filter = filters.create(job_callback)
