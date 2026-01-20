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

# ===== SISTEMA GACHA DE RASGOS RACIALES =====

@bot.command()
async def rasgo(ctx):
    rasgos = [
        {
            "nombre": "Nacido del Dragón",
            "descripcion": "Eres cercano a los dragones, su sangre corre por tus venas y te vuelve imparable.",
            "gif": "https://cdn.discordapp.com/attachments/1453984015236337737/1453984016037445684/super-shenron-shenron.gif"
        },
        {
            "nombre": "No-Muerto",
            "descripcion": "Has cruzado la línea entre la vida y la muerte, tu existencia desafía el orden natural.",
            "gif": "https://cdn.discordapp.com/attachments/1453983897485574307/1453983897665667092/lich-the-lich.gif"
        },
        {
            "nombre": "Gigante",
            "descripcion": "Eres cercano a los gigantes, lo que te otorga una presencia y fuerza abrumadoras.",
            "gif": "https://cdn.discordapp.com/attachments/1453983753402847302/1453983754069610526/IMG_1357.gif"
        },
        {
            "nombre": "Ángel",
            "descripcion": "La luz divina guía tus acciones y tu existencia irradia pureza y determinación.",
            "gif": "https://cdn.discordapp.com/attachments/1453983560372588671/1453983561060319355/gabriel-apostate-of-hate.gif"
        },
        {
            "nombre": "Demonio",
            "descripcion": "El caos y el poder infernal forman parte de ti, otorgándote una voluntad indomable.",
            "gif": "https://cdn.discordapp.com/attachments/1453983431661981756/1453983431989002353/picture_pc_aeb1c9db9f50978baaf13f29d9a4b628.webp"
        },
        {
            "nombre": "Semi-Humano",
            "descripcion": "Tu naturaleza híbrida te permite adaptarte a cualquier situación con facilidad.",
            "gif": "https://cdn.discordapp.com/attachments/1453983305560232049/1453983305799303168/princess-connect-cat-girl.gif"
        },
        {
            "nombre": "Cyborg",
            "descripcion": "La tecnología y la carne se fusionan en ti, superando los límites del cuerpo humano.",
            "gif": "https://cdn.discordapp.com/attachments/1453983138668609698/1453983138907947078/cyborg-ray-fisher.gif"
        },
        {
            "nombre": "Humano",
            "descripcion": "Eres humano, y aun así tu potencial es infinito gracias a tu determinación.",
            "gif": "https://cdn.discordapp.com/attachments/1453982882430455809/1453982883680092181/konosuba-kazuma.gif"
        }
    ]

    rasgo_elegido = random.choice(rasgos)

    embed = discord.Embed(
        title=f"🧬 Rasgo obtenido: {rasgo_elegido['nombre']}",
        description=rasgo_elegido["descripcion"],
        color=discord.Color.purple()
    )

    embed.set_image(url=rasgo_elegido["gif"])
    embed.set_footer(text=f"Rasgo obtenido por {ctx.author.display_name}")

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
