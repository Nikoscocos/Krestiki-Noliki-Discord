import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix="")

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_square_button:", ":white_square_button:", ":white_square_button:",
                 ":white_square_button:", ":white_square_button:", ":white_square_button:",
                 ":white_square_button:", ":white_square_button:", ":white_square_button:",
                 ":white_square_button:", ":white_square_button:", ":white_square_button:",
                 ":white_square_button:", ":white_square_button:", ":white_square_button:",]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("Сейчас ходит <@" + str(player1.id) + "> на поле.")
        elif num == 2:
            turn = player2
            await ctx.send("Сейчас ходит <@" + str(player2.id) + "> на поле.")
    else:
        await ctx.send("Уже запущена игра. Закончите,сначала эту,а потом приступайте к новой.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_square_button:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " Победил!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Ничья. Ну ничего,победила дружба.")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Чтобы разместить на поле крестик или нолик,напишите place и цифру,куда хотите поставить крестик или нолик.")
        else:
            await ctx.send("Сейчас не твой ход.")
    else:
        await ctx.send("Запустите новую игру командой tictctoe.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Упомяните два человека для использования данной команды. Пример: tictactoe @Nikoscocos @Nikoscocos API.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Упомяните нормально,по правилам. Пример: tictactoe @Nikoscocos @Nikoscocos API.")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Используй после команды place цифры только от 1 до 9 и никаких прочих символов и эмодзи.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Неправильное размещение или место на поле уже занято. Правила ходов в команде place")

client.run("твой токен бота")
