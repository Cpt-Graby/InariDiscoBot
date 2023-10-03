import settings
import discord
from discord.ext import commands
from scoreTraker import * 

logger = settings.logging.getLogger("bot")
log_channel = settings.DISCORD_LOG_CHANNEL 
bilan_channel = settings.DISCORD_LOG_CHANNEL 

        
def main():

    Tableau = ScoreTracker()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    emoji1 = '\N{THUMBS UP SIGN}'  # or '\U0001f44d' or '👍'
    emojiX = '\N{THUMBS DOWN SIGN}'    

    @bot.event
    async def on_ready():
        logger.info(f"User:{bot.user} (ID: {bot.user.id})")

    @bot.command(aliases=['add', 'score'])
    async def add_score(ctx, score: int = 0):
        """Permet d'annoncer que tu achetes quelques choses aux BDE """
        channel_log = bot.get_channel(log_channel)
        if (score >= 0):
            Tableau.add_score(str(ctx.author), score)
            await channel_log.send(f"{ctx.author} add the {score}")
            await ctx.message.add_reaction(emoji1)
        else:
            await ctx.send(f"Score negativ pas accepte!")
            await ctx.message.add_reaction(emojiX)

    @bot.command(hidden=True, aliases=['late'])
    async def add_late_score(ctx, name:str, date: str = "0-0-0", score: int = 0):
        """Permet d'annoncer que tu achetes quelques choses aux BDE """
        channel_log = bot.get_channel(log_channel)
        if (score >= 0):
            Tableau.add_score(name, score, str(date))
            await channel_log.send(f"{ctx.author} add late the {score} for {date}")
            await ctx.message.add_reaction(emoji1)
        else:
            await ctx.send(f"Score negativ pas accepte!")
            await ctx.message.add_reaction(emojiX)

    @bot.command(hidden=True, aliases=['ranking'])
    async def printTableau(ctx):
        ranking = Tableau.get_current_ranking()
        await ctx.send(f"{ranking}")

    @bot.command(aliases=['rank'])
    async def printplayer(ctx, name: str):
        ranking = Tableau.print_scores_for_participant(name)
        await ctx.send(f"{ranking}")

    @bot.command(hidden=True, aliases=['save'])
    async def saveCsv(ctx, name: str):
        ranking = Tableau.save_scores_to_csv(name)
        await ctx.send(f"{name} saved in the docker")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__== "__main__":
    main()
