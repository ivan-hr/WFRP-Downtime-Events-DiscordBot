# -*- coding: utf-8 -*-
import os
import random
import discord
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  # Add this line to enable the Message Content intent

# Set the bot prefix (e.g., !roll)
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the table to roll from with ranges
table = [
    (1, 3, '**Beschuldigter Verbündeter**\nEiner deiner Verbündeten oder nahen Bekannten wird eines schrecklichen Verbrechens angeklagt. Ein Charakter mit der Gildenlizenz eines Advokaten kann eine Unternehmung dafür aufwenden, den Verbündeten mit dem Gelingen eines **durchschnittlichen (+20) Wissen-(Gesetz)-Wurf** zu befreien. Anderenfalls kann die Gruppe 3 Unternehmungen dafür aufwenden, die Unschuld ihres Verbündeten zu beweisen (oder ein Alibi zu konstruieren, falls er es wirklich war). Wenn der Verbündete befreit wurde, erhältst du einen *Großen Gefallen (siehe Tu mir einen Gefallen…, auf Seite 198)* zur künftigen Verwendung. Falls nicht, hängt dein Verbündeter!'),
    (4, 6, '**Arkane Auktion**\nDie Habseligkeiten eines kürzlich verstorbenen Nachbarn werden versteigert, darunter auch ein altes, staubiges Buch unbekannter Herkunft. Wenn du dazu imstande bist, 10 GK zu zahlen, ist das Buch dein! Abgesehen von anderen Dingen, die das Buch nach Wahl des SL enthalten kann, erhält jeder Charakter der Akademiker-Klasse, der sich an der Unternehmung **Recherche** versucht, +20 auf seinen Wurf.'),
    (7, 10, '**Verraten!**\nEin Freund, Familienmitglied oder Verbündeter wendet sich gegen dich, und die Auswirkungen die das hat, werden dein nächstes Abenteuer beeinflussen. Wenn du keine Freunde, Familienmitglieder oder Verbündete hast, dann vergeht die Zeit zwischen den Abenteuern ohne Vorkommnisse, ist aber ein wenig langweilig.'),
    (11, 14, '**Ab durch die Mitte**\nIrgendein nutzloser Stallknecht muss die Stalltür offengelassen haben und nun ist dein Pferd durchgegangen! Wenn dir ein **durchschnittlicher (+20) Abrichten-(Pferd)-Wurf** gelingt, dann weiß dein gut ausgebildetes Tier, welche Hand es füttert, und kehrt zurück. Misslingt der Wurf, dann wirst du dein Ross wohl nie wiedersehen. Wenn du kein Pferd besitzt, dann hast du dir an einem deiner Füße eine schmerzhafte neue Blase gelaufen.'),
    (15, 18, '**He, du hast mein Bier verschüttet! **\nEine unwichtige Streiterei im Ort wächst sich zur Fehde aus. Der SL entscheidet, wen du beleidigt hast und wie dies geschah. Diese Person wird sich die Gelegenheit zu einer hübschen kleinen Rache nicht entgehen lassen, vielleicht sogar schon im nächsten Abenteuer …'),
    (19, 21, '**Razzien**\nDie Wache führt gerade eine Serie von Razzien gegen die örtliche Unterwelt durch. Charaktere der Klasse Gesetzlose können keine Gelder über **Einnahmen-Unternehmunge**n erhalten, und wenn Gesetzlose eine **Bankgeschäfte**-Unternehmung durchführen, dann können sie als Investition nur solche mit maximalem Risiko wählen, da derzeit kein angesehenes Bankhaus ihr Schwarzgeld annehmen möchte.'),
    (22, 25, '**Der Steuereintreiber naht**\nDer Ort wird von einem unerwarteten Besuch des Steuereintreibers (und seiner stattlichen Eskorte von Soldaten) heimgesucht. Alle Charaktere verlieren 30 Prozent ihrer aktuellen Geldmittel, noch ehe irgendetwas für Unternehmungen eingesetzt werden konnte.'),
    (26, 29, '**Falsches Silber**\nZum Schrecken der Kaufleute gehen in der Gegend gefälschte Münzen um. Ein Fünftel aller Münzen ist betroffen. Charaktere, die eine Bankgeschäfte-Unternehmung durchführen, werden 20% des angelegten Geldes verlieren, und Charaktere, die eine Einnahmen-Unternehmung durchführen, erhalten dadurch 20% weniger Geld.'),
    (30, 33, '**Schwimmender Profit**\nFür alle, die mit dem Fluss Geschäfte machen, laufen diese wirklich gut. Wenn jemand mit der Klasse Flussvolk eine **Einnahmen**-Unternehmung durchführt, dann verdient er dabei 50% mehr.'),
    (34, 36, '**Vorgewarnt heißt vorbereitet**\nDu erhältst ein kryptisches Omen durch einen Strigani-Mystiker oder einen Magister des Himmelsordens. Während des nächsten Abenteuers ist dein Maximum an Glückspunkten um 1 erhöht.'),
    (37, 40, '**Festivitäten Es wird gefeiert!**\nBesprich die Art der Feierlichkeit mit dem SL. Die Möglichkeiten reichen von einer örtlichen Hochzeit über eine gute Ernte bis zu einer öffentlichen Hinrichtung! Du wirst sehr vom Anlass (und dessen Nachwirkungen) in Anspruch genommen und verlierst eine Unternehmung.'),
    (41, 44, '**Schreckliches Wetter**\nDas Wetter wird äußerst schlecht. Während des nächsten Abenteuers werden alle Würfe für soziale Interaktionen mit -10 abgehandelt (weil jeder schlechter Stimmung ist) und die Lebensmittelpreise steigen um 20%.'),
    (45, 48, '**Wundervolles Wetter**\nDas prachtvolle Wetter inspiriert dich und sorgt für gute Stimmung. Du kannst ein zusätzliches kurzfristiges Ziel wählen. Wenn es erreicht wurde, wird es nicht durch ein neues ersetzt.'),
    (49, 52, '**Örtliche Missernte**\nNahrung wird äußerst knapp und gerade das einfache Volk leidet sehr. Charaktere der Klasse Landvolk können keine **Einnahmen-Unternehmunge**n durchführen, und für die Dauer des nächsten Abenteuers sind die Nahrungsmittelpreise in dieser Region doppelt so hoch.'),
    (53, 56, '**Üble Heimsuchung**\nIm Ort geht der Blutschiss um. Führe einen **einfachen (+40) Widerstands-Wurf** durch. Gelingt er, wirst du nicht betroffen. Misslingt er, kennen du und die Wäscher-Gilde einander bald ziemlich gut. Details zum Blutschiss auf Seite 186.'),
    (57, 60, '**Monströse Komplikationen**\nEin Monster (das der SL auswählt, siehe **Kapitel 12: Bestiarium**) verbreitet Angst und Schrecken in der örtlichen Bevölkerung. Einnahmen- Unternehmungen werfen nichts ab, solange die Gefahr nicht gebannt wurde. Die Charaktere können je eine Unternehmung opfern, um sich der Sache anzunehmen (diese Begegnung sollte im Rollenspiel ausgetragen werden). Wenn ihr Erfolg habt, bekommt jeder eine freie Einnahmen-Unternehmung, die die individuellen Belohnungen vor Ort darstellt, und es wird ein Fest zu euren Ehren ausgerichtet. Scheitert ihr oder kümmert sich die Gruppe nicht darum, dann zieht das Monster irgendwann weiter oder wird von Rivalen getötet.'),
    (61, 63, '**Morrs Umarmung**\nEiner der Freunde, Verwandten oder Verbündeten des Charakters stirbt. Der Tod könnte natürliche Ursachen haben, ein Unfall gewesen sein oder auf irgendetwas Finsteres hindeuten …'),
    (64, 65, '**Neumond**\nDie Nächte sind derzeit besonders dunkel. Alle Gesetzlosen, die eine **Einnahmen-Unternehmung** angehen, haben einen Bonus von +20 Prozent auf den Gewinn.'),
    (66, 67, '**Alte Schulden**\nJemand fordert einen **Großen Gefallen** oder einen **Erheblichen Gefallen** von dir ein. Sich damit zu befassen wird Teil eures nächsten Abenteuers sein und du verlierst eine Unternehmung, da du dich darauf vorbereiten musst.'),
    (68, 69, '**Gelegenheiten kommen des Weges**\nMarschierende Soldaten, wohlhabende Kaufleute oder reisende Adelige kommen durch das Gebiet und auch die Charaktere können versuchen, an ihnen zu verdienen und ihren Schnitt zu machen. Charaktere der Klassen Bürger und Landvolk haben bei **Einnahmen-Unternehmunge**n einen Bonus von +50% auf den Gewinn.'),
    (70, 71, '**Ruhe und Frieden**\nEs sind Zeiten wie diese, die dich daran erinnern, worum es im Leben wirklich geht: Guten Schlaf und feinen Käse. Das nächste Abenteuer trittst du sehr entspannt und zufrieden an.'),
    (72, 73, '**Hausierer**\nEin sehr gewitzter und weitgereister Hausierer kommt vorbei, der viel Spaß an Klatsch und Tratsch hat. Für den Preis eines guten Bieres (3 G) erhältst du einen Bonus von +10 auf jede **Neueste-Nachrichten-Unternehmung**.'),
    (74, 76, '**Erkranktes Tier**\nEines deiner Tiere erkrankt; führe einen **herausfordernden (+0) Tierpflege-Wurf** durch. Gelingt er, kommt dein Tier durch. Falls nicht, stirbt die unglückliche Kreatur. Falls du keine Tiere hast, suchen dich böse Omen nach Wahl des SL heim.'),
    (77, 79, '**Ausgenommen**\nEhe du eine **Bankgeschäfte**-Unternehmung durchführen kannst, wird dein verstecktes Geld bis auf den letzten Groschen gestohlen. Wenn die versteckte Summe weniger als 1 GK betrug, stehlen die Diebe auch noch dein wertvollstes Ausrüstungsstück.'),
    (80, 82, '**Unruhen**\nDas gemeine Volk ist aufgebracht über die Reichen und Mächtigen! Charaktere der Klasse Adel können keine **Einnahmen-Unternehmunge**n durchführen, denn selbst mit Leibwächtern ist es draußen derzeit nicht sicher genug, um seinen Geschäften nachzugehen. Des Weiteren muss sofort für jede Anlage bei einer angesehenen Bank gewürfelt werden (siehe Seite 196), denn die Unsicherheit und die Gewaltausbrüche haben diese Bank möglicherweise ihre Geschäfte beenden lassen. Allerdings erhalten Spieler, die sich an der Unternehmung **Aufwiegeln** versuchen, +10 bei allen zugehörigen Würfen.'),
    (83, 85, '**Lange Finger**\nDeine Börse wurde geleert! Du verlierst die Hälfte des Geldes, mit dem du aus dem letzten Abenteuer gekommen bist.'),
    (86, 88, '**Verdacht der Ketzerei**\nDu fällst einem Hexenjäger ins Auge, der dich verdächtigt, mit Mutanten, Kultisten oder Schlimmerem zu verkehren, während du dich bei deinen sogenannten „Abenteurern“ herumtreibst. Es erfordert einen **sehr schweren (-30) Charme-Wurf**, den Hexenjäger von deiner Unschuld zu überzeugen. Ein Misslingen des Wurfes kann dir eine äußerst hartnäckige Nemesis bescheren, die dir in der Zukunft gewiss noch viel Ärger bereiten wird …'),
    (89, 91, '**Unter Verdacht**\nDie eher ungewöhnlichen Reisen der Gruppe haben Verdacht erregt, ebenso wie ihr plötzlicher Wohlstand. Alle Charaktere müssen eine ihrer Unternehmungen opfern, um ihre Unschuld zu beweisen. Charaktere der Klasse Gesetzlose können bis zum nächsten Abenteuer kein Geld über **Einnahmen-Unternehmunge**n verdienen.'),
    (92, 94, '**Ereignislos**\nWenig Interessantes passiert, was dich vielleicht in so große Langeweile versetzt, dass du nun erst recht Appetit auf Risiken hast!'),
    (95, 97, '**Unerwartete Wertschätzung**\nJemand, dem du in der Vergangenheit geholfen hast, nutzt seine Chance, einen Teil seiner Schuld zu begleichen. Was genau deine Belohnung ist, sollte von deinen früheren Taten und den NSC abhängen, denen du während des Spiels oder in deiner Hintergrundgeschichte geholfen hast. Die Dankbarkeit könnte in Form eines einzelnen, qualitativ hochwertigen Gegenstandes oder einer Börse mit Silber (die zu Beginn des nächsten Abenteuers zur Verfügung steht) auftreten. Natürlich ist nicht alles Gold was glänzt, und so manches Geschenk kommt mit Hintergedanken …'),
    (98, 100, '**Söldner anwerben**\nEiner oder mehrere seltene Söldner tauchen in der nächsten Siedlung auf und suchen nach Arbeit, vielleicht ein tileanischer Duellist mit gefürchtetem Ruf, die sogenannten Vogelmenschen von Catrazza, kontraktlose Oger unter dem Befehl eines Halbling-Hauptmannes oder andere, eher unwahrscheinliche Gesellen. Die Söldner werden interessierte Charaktere gern in kriegerischen Fähigkeiten oder Talenten unterweisen, mit einer Ermäßigung der Kosten um 20%, sofern die SC die Unternehmungen **Unterweisung** oder **Besonderes Lernen** wählen. Zusätzlich erhalten alle Charaktere, die die Unternehmung **Kampfübungen** durchführen, einen Bonus von +20 auf alle zugehörigen Würfe.')
]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Ereignisse zwischen den Abenteuern
@bot.command()
async def event(ctx):
    print("Roll command executed")
    roll_value = random.randint(1, 100)
    result = None

    for low, high, outcome in table:
        if low <= roll_value <= high:
            result = outcome
            break

    if result:
        await ctx.send(f'{ctx.author.mention} **[{roll_value}]**: {result}')
    else:
        await ctx.send(f'{ctx.author.mention} **[{roll_value}]**: No result found')

# Verfügbarkeitsprüfung
def is_item_available(item_name, settlement, rarity):
    availability = {
        "Verbreitet": {"Dorf": 100, "Kleinstadt": 100, "Stadt": 100},
        "Knapp": {"Dorf": 30, "Kleinstadt": 60, "Stadt": 90},
        "Selten": {"Dorf": 15, "Kleinstadt": 30, "Stadt": 45},
    }

    if rarity not in availability or settlement not in availability[rarity]:
        raise ValueError("Invalid settlement or rarity provided")

    random_percentage = random.randint(1, 100)
    return random_percentage <= availability[rarity][settlement], random_percentage

@bot.command(name="avail")
async def check_availability(ctx, *args):
    try:
        input_str = ' '.join(args)
        item_name, settlement, rarity = [s.strip() for s in input_str.split(',')]  # Changed the order here
        is_available, dice_roll = is_item_available(item_name, settlement, rarity)
        
        if is_available:
            await ctx.send(f"{ctx.author.mention} **[{dice_roll}]**: Der Gegenstand **{item_name}** mit der Verfügbarkeit '{rarity}' ist im Siedlungstyp '{settlement}' verfügbar.")
        else:
            await ctx.send(f"{ctx.author.mention} **[{dice_roll}]**: Der Gegenstand '{item_name}' mit der Verfügbarkeit '{rarity}' ist im Siedlungstyp '{settlement}' nicht verfügbar.")
    except ValueError as e:
        await ctx.send(str(e))
 

# Replace 'YOUR_BOT_TOKEN' with the token from the Discord Developer Portal
bot.run('YOUR_BOT_TOKEN')
