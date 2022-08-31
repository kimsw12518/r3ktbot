import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import bs4
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

songlist=[]
inloop=0
bot = commands.Bot(command_prefix='!렉트봇 ')

@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(status=discord.Status.online, activity=None)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!렉트봇 도움말 "))

@bot.command()
async def 도움말(ctx,message='d'):
    if message == '들어와':
        await ctx.send(embed=discord.Embed(title='!렉트봇 들어와', description='렉트봇을 통화방에 부를수 있어요',color=0xffaa00))
    elif message == '나가':
        await ctx.send(embed=discord.Embed(title='!렉트봇 나가', description='렉트봇을 통화방에서 내보낼수 있어요',color=0xffaa00))
    elif message == '노래불러':
        await ctx.send(embed=discord.Embed(title='!렉트봇 노래불러 (URL)', description='통화방에서 유튜브 영상을 재생할 수 있어요',color=0xffaa00))
    elif message == '일시정지':
        await ctx.send(embed=discord.Embed(title='!렉트봇 일시정지', description='재생중인 노래를 일시정지 할 수 있어요',color=0xffaa00))
    elif message == '다시재생':
        await ctx.send(embed=discord.Embed(title='!렉트봇 다시재생', description='일시정지한 노래를 다시 재생 할 수 있어요',color=0xffaa00))
    elif message == '노래멈춰':
        await ctx.send(embed=discord.Embed(title='!렉트봇 노래멈춰', description='재생중인 노래를 멈출 수 있어요',color=0xffaa00))
    else:
        await ctx.send(embed = discord.Embed(title='들어와, 나가, 노래불러, 일시정지, 다시재생, 노래멈춰',description='!렉트봇 도움말 (명령어)로 추가 설명을 볼 수 있어요!',color= 0xffaa00))

@bot.command()
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed=discord.Embed(title='얍!', description='들어왔지롱', color=0xffaa00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(embed=discord.Embed(title='음성 채널에 참가한 뒤에 불러주세요!', description='어디로 오라고는 알려줘야 할거아냐...', color=0xffaa00))

@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
        await ctx.send(embed = discord.Embed(title='슝!', description='빠빠이ㅣ', color=0xffaa00))
    except:
        await ctx.send(embed = discord.Embed(title='저 거기 없는데요...?',description='바부네 바부 ㅋㅎㅋㅎㅋ',color= 0xffaa00))

@bot.command()
async def 노래불러(ctx, *, url):
    global songlist
    global inloop
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    songlist.append(url)
    if vc.is_playing():
        await ctx.send("대기열에 추가되었습니다!")
    if inloop==0:
        inloop=1
        while len(songlist)!=0:
            if not vc.is_playing():
                link=songlist[0]
                songlist.remove(songlist[0])
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(link, download=False)
                URL = info['formats'][0]['url']
                vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + link + " 을(를) 재생하고 있습니다.", color = 0xffaa00))
                global entireText
                entireText=link
            time.sleep(1)
        inloop=0

@bot.command()
async def 목록(ctx):
    global songlist
    await ctx.send(f'{songlist}')

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = entireText + " 을(를) 일시정지 했습니다.", color = 0xffaa00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = entireText  + " 을(를) 다시 재생했습니다.", color = 0xffdd00))

@bot.command()
async def 노래멈춰(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = entireText  + " 을(를) 종료했습니다.", color = 0xff4400))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

bot.run('ODc3NDEzNjI5NDI5OTQwMjc0.YRyRHg.a_gfX9IO0_5lyrWeQ5EFinLtHOI')
#bot.run('ODc4MjExNDgzMTAyNzQ4NzAy.YR94LQ.552SUkH58By3_8Xd_mCerpZOXZE')
