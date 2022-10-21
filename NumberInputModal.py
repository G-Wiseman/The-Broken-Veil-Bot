import discord
import discord.ui as ui


class NumInput(ui.Modal, title = "Change number multiplier"):
    def __init__(self, multiplier):
        super().__init__()
        self.multiplier = multiplier


    name = ui.TextInput(label='Name')

    async def on_submit(self, interaction:discord.Interaction):
        try:
            new_mult = int(self.children[0].value)
        except:
            await interaction.response.defer()
            return

        self.multiplier = new_mult
        await interaction.response.defer()
        self.stop()
