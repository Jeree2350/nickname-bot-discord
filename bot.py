import discord
import re
import json

# Cargar token desde config.json
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["token"]
CANAL_OBJETIVO = "nombre_ic"  # Nombre exacto del canal

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necesario para cambiar nicknames

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name != CANAL_OBJETIVO:
        return

    contenido = message.content.strip()

    if re.match(r'^[A-Z][a-z]+_[A-Z][a-z]+$', contenido):
        try:
            await message.author.edit(nick=contenido)
            await message.channel.send(f'Listo, te llamas **{contenido}** ahora.')
        except discord.Forbidden:
            await message.channel.send('No tengo permisos para cambiar tu nickname.')
        except Exception as e:
            await message.channel.send(f'Error inesperado: {e}')
    else:
        await message.channel.send('Formato incorrecto. Usa: Nombre_Apellido (con mayúsculas).')

client.run(TOKEN)
