import discord
import os
from discord.ext import commands
from discord.ui import Button, View
import random

# 인텐트 설정
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# 봇 초기화
bot = commands.Bot(command_prefix="!", intents=intents)

class VerificationView(View):
    def __init__(self, user):
        super().__init__(timeout=180)  # 3분 후에 View가 만료됨.
        self.user = user
        self.code = random.randint(10000, 99999)  # 5자리 무작위 코드 생성

    @discord.ui.button(label="인증하기", style=discord.ButtonStyle.green)
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.user:  # 버튼을 누른 사용자 확인
            await interaction.response.send_message("이 버튼은 당신을 위한 것이 아닙니다.", ephemeral=True)
            return

        # 사용자에게 코드 입력 요청
        await interaction.response.send_message(f"다음 코드를 입력해주세요: `{self.code}`", ephemeral=True)

        def check(m):
            return m.author == self.user and m.content.isdigit() and int(m.content) == self.code

        msg = await bot.wait_for('message', check=check, timeout=60.0)  # 사용자 응답 대기

        if msg:
            role = discord.utils.get(msg.guild.roles, id=1213756988996067332)  # 역할 ID로 역할 객체 가져오기
            await self.user.add_roles(role)  # 사용자에게 역할 부여
            await interaction.followup.send(f"{self.user.mention}, 인증이 완료되었습니다!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready.")

@bot.command()
async def 인증시작(ctx):
    verification_view = VerificationView(ctx.author)
    await ctx.send("아래 버튼을 눌러 인증을 완료해주세요.", view=verification_view)

# 여기에 봇의 토큰을 넣으세요. 실제 토큰을 공유하지 않는 것이 중요합니다.

accass_token = os.environ["BOT_TOKEN"]
bot.run(accas_token)
