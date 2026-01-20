import random
import discord
from discord.ext import commands
import os

# ----------------------------
# INTENTS & BOT
# ----------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# CONFIGURACIÓN
# ----------------------------

# TU ID (BYPASS TOTAL)
OWNER_ID = 943735654683123733

# IDs DE ROLES PERMITIDOS
ROLES_GACHA = [
    1279986789792092211,
    963144919977963542,
    1266609086565449811,
    1266609714205294703
]

ROLES_MOD = [
    1266609714205294703,
    1266609086565449811,
    963144919977963542
]

# ----------------------------
# FUNCIONES DE PERMISOS
# ----------------------------
def tiene_rol_permitido(member, roles_permitidos):
    if member.id == OWNER_ID:
        return True
    return any(rol.id in roles_permitidos for rol in member.roles)

def tiene_rol_mod(member):
    if member.id == OWNER_ID:
        return True
    return any(rol.id in ROLES_MOD for rol in member.roles)

# ----------------------------
# GACHA
# ----------------------------
ultimo_resultado = {}

@bot.command()
async def gacha(ctx):
    if not tiene_rol_permitido(ctx.author, ROLES_GACHA):
        await ctx.send("❌ No tienes permiso para usar este comando.")
        return

    categorias = [
        {
            "nombre": "🦊 Categoría Zorro",
            "poder": "Débil",
            "peso": 40,
            "texto": "Empiezas desde lo más bajo. Ingenio y supervivencia serán tu mayor arma.",
            "gif": "https://cdn.discordapp.com/attachments/1451359615664001094/1451359615915790458/5fc63ee8856144bd436b8d61b99e90d0.gif"
        },
        {
            "nombre": "🐺 Categoría Lobo",
            "poder": "Débil / Fuerte bajo",
            "peso": 25,
            "texto": "No eres el más fuerte, pero sabes cazar en grupo.",
            "gif": "https://cdn.discordapp.com/attachments/1451359913715564666/1451359914088992860/897979zrsa8e1.gif"
        },
        {
            "nombre": "🐯 Categoría Tigre",
            "poder": "Fuerte bajo",
            "peso": 15,
            "texto": "Fuerza natural. Pocos se atreverán a desafiarte.",
            "gif": "https://cdn.discordapp.com/attachments/1451360111779123271/1451360112110338068/beast-gohan-gohan.gif"
        },
        {
            "nombre": "😈 Categoría Demonio",
            "poder": "Fuerte",
            "peso": 10,
            "texto": "El poder oscuro fluye por tus venas. El miedo te precede.",
            "gif": "https://cdn.discordapp.com/attachments/1451360296668233861/1451360297087402066/chainsaw-chainsaw-man.gif"
        },
        {
            "nombre": "🐲 Categoría Dragón",
            "poder": "Fuerte alto",
            "peso": 7,
            "texto": "Eres una calamidad viviente. Tu sola presencia impone respeto.",
            "gif": "https://cdn.discordapp.com/attachments/1451360493758451868/1451360494953697363/211562.gif"
        },
        {
            "nombre": "👑 Categoría Dios",
            "poder": "Fuerte total",
            "peso": 3,
            "texto": "Has nacido como una entidad absoluta. El mundo se doblará ante ti.",
            "gif": "https://cdn.discordapp.com/attachments/1451360784226586635/1451360785019175103/alien-x-ben10.gif"
        }
    ]

    usuario = ctx.author.id

    while True:
        resultado = random.choices(
            categorias,
            weights=[c["peso"] for c in categorias]
        )[0]

        if ultimo_resultado.get(usuario) != resultado["nombre"]:
            break

    ultimo_resultado[usuario] = resultado["nombre"]

    embed = discord.Embed(
        title="🌌 Resultado de Inicio",
        description=(
            f"**{resultado['nombre']}**\n"
            f"Poder: **{resultado['poder']}**\n\n"
            f"{resultado['texto']}"
        ),
        color=0x8e44ad
    )

    embed.set_image(url=resultado["gif"])
    embed.set_footer(text=f"Jugador: {ctx.author.name}")

    await ctx.send(embed=embed)

# ----------------------------
# MODERACIÓN
# ----------------------------
@bot.command()
async def ban(ctx, user: discord.Member, *, reason="Sin razón"):
    if not tiene_rol_mod(ctx.author):
        await ctx.send("❌ No tienes permiso para usar este comando.")
        return
    await user.ban(reason=reason)
    await ctx.send(f"🔨 {user} fue baneado.\nRazón: {reason}")

@bot.command()
async def mute(ctx, user: discord.Member, *, reason="Sin razón"):
    if not tiene_rol_mod(ctx.author):
        await ctx.send("❌ No tienes permiso para usar este comando.")
        return

    rol = discord.utils.get(ctx.guild.roles, name="Muted")
    if not rol:
        rol = await ctx.guild.create_role(name="Muted")
        for canal in ctx.guild.channels:
            await canal.set_permissions(rol, send_messages=False)

    await user.add_roles(rol)
    await ctx.send(f"🔇 {user} fue muteado.\nRazón: {reason}")

# ----------------------------
# INICIAR BOT
# ----------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
