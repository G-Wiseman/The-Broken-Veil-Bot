import discord
from botlogic import *
from NumberInputModal import *




class LogStatButtons(discord.ui.View):
    def __init__(self, name, spec_stat, guild, timeout=900):
        super().__init__(timeout=timeout)
        self.message = None
        self.name = name
        self.guild = guild
        self.positive = 1
        self.multiplier = 1
        self.spec_stat_type = spec_stat
        self.inner_button = self.SpecificStatButton(self, timeout)



        # Add a seperate button for the specific stat so the name can be decided upon creation
        spec_button_View= self.inner_button
        spec_button = spec_button_View.children[0]
        spec_button.label = spec_stat
        self.add_item(spec_button)

    # Define an inner class to deal with a weird issue of naming the button upon it's creation depending on which character is used.
    # This is awful and janky, and I hope I can find a better way
    # The outer class passes itself to the inn
    class SpecificStatButton(discord.ui.View):
        def __init__(self, outer, timeout):
            super().__init__(timeout=1000)
            self.outer = outer

        @discord.ui.button(label="NO LABEL", row = 1, style=discord.ButtonStyle.primary)
        async def character_specific_log(self, interaction:discord.Interaction, button:discord.ui.Button):
            input_value = self.outer.positive * self.outer.multiplier
            prior_value, new_value = handle_log(self.outer.name.lower(), "Character Specific", input_value, self.outer.guild)
            await interaction.response.edit_message(content= f"{self.outer.name}'s {self.outer.spec_stat_type} has been changed from {prior_value} to {new_value}!")
            return


    @discord.ui.button(label=f"Multiplier: 1", style=discord.ButtonStyle.green)
    async def multiplier_modal_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        modal = NumInput(self.multiplier)
        await interaction.response.send_modal(modal)
        await modal.wait()
        message_id = self.message.id
        self.multiplier = modal.multiplier
        button.label = f"Multiplier: {self.multiplier}"
        if self.multiplier < 0:
            button.style = discord.ButtonStyle.red

        elif self.multiplier > 0:
            button.style = discord.ButtonStyle.green

        else:
            button.style = discord.ButtonStyle.grey


        await interaction.followup.edit_message(message_id=message_id, view=self)

    @discord.ui.button(label="Kills",style=discord.ButtonStyle.primary)
    async def kill_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        await interaction.response.edit_message(content= f"{self.name}'s kills have been changed from {prior_value} to {new_value}!")
        return

    @discord.ui.button(label="Unconscious",style=discord.ButtonStyle.primary)
    async def unconc_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        await interaction.response.edit_message(content= f"{self.name}'s times unconscious have been changed from {prior_value} to {new_value}!")
        return

    @discord.ui.button(label="Death",style=discord.ButtonStyle.primary)
    async def death_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        await interaction.response.edit_message(content= f"{self.name}'s deaths have been changed from {prior_value} to {new_value}!")
        return

    @discord.ui.button(label="Final Kill",style=discord.ButtonStyle.primary)
    async def final_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        await interaction.response.edit_message(content= f"{self.name}'s \"How do you want to do this moments\" have been changed from {prior_value} to {new_value}!")
        return


    @discord.ui.button(label="Max Damage",style=discord.ButtonStyle.primary)
    async def max_dam_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        if prior_value < new_value:
            await interaction.response.edit_message(content= f"{self.name}'s max damage has been changed from {prior_value} to {new_value}!")
            return
        else:
            await interaction.response.edit_message(content= f"{self.name}'s max damage is already {prior_value}. Do more damage next time!")

    @discord.ui.button(label="Healing Dealt",style=discord.ButtonStyle.primary)
    async def healing_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        await interaction.response.edit_message(content= f"{self.name}'s healing dealt has been changed from {prior_value} to {new_value}!")
        return

    @discord.ui.button(label="Nat 20",style=discord.ButtonStyle.primary)
    async def crit_succ_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        await interaction.response.edit_message(content= f"{self.name}'s Nat 20s have been changed from {prior_value} to {new_value}!")
        return

    @discord.ui.button(label="Nat 1",style=discord.ButtonStyle.primary)
    async def crit_fail_button(self, interaction:discord.Interaction ,button:discord.ui.Button):
        input_value = self.positive * self.multiplier
        prior_value, new_value = handle_log(self.name.lower(), button.label, input_value, self.guild)
        await interaction.response.edit_message(content= f"{self.name}'s Nat 1s have been changed from {prior_value} to {new_value}!")
        return


    @discord.ui.button(label="Close Menu", style=discord.ButtonStyle.red, row = 3)
    async def cancel_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if self.message != None: #Just check that a message actually got placed here... It can't happen upon __init__
            await self.message.delete()


class LeaderBoardMenu(discord.ui.View):
    def __init__(self, guild, timeout = 60):
        super().__init__(timeout=timeout)
        self.message = None
        self.guild = guild

    def create_leaderboard_output(self, label) -> str:
        sorted_stats = get_leaderboard_list(self.guild, label)
        output_message = f"__**Leaderboard for {label}**__\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value}\n"
            count += 1
        return output_message


    @discord.ui.button(label="Kills",style=discord.ButtonStyle.primary)
    async def kill_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        output_message = self.create_leaderboard_output(button.label)
        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return

    @discord.ui.button(label="Unconscious",style=discord.ButtonStyle.primary)
    async def unconc_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        sorted_stats = get_leaderboard_list(self.guild, button.label)
        output_message = f"***Leaderboard for {button.label}***\n\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value} {button.label}\n"
            count += 1

        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return

    @discord.ui.button(label="Death",style=discord.ButtonStyle.primary)
    async def death_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        sorted_stats = get_leaderboard_list(self.guild, button.label)
        output_message = f"***Leaderboard for {button.label}***\n\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value} {button.label}\n"
            count += 1

        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return

    @discord.ui.button(label="Final Kill",style=discord.ButtonStyle.primary)
    async def final_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        sorted_stats = get_leaderboard_list(self.guild, button.label)
        output_message = f"***Leaderboard for {button.label}***\n\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value} {button.label}\n"
            count += 1

        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return


    @discord.ui.button(label="Max Damage",style=discord.ButtonStyle.primary)
    async def max_dam_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        sorted_stats = get_leaderboard_list(self.guild, button.label)
        output_message = f"***Leaderboard for {button.label}***\n\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value} {button.label}\n"
            count += 1

        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return

    @discord.ui.button(label="Healing Dealt",style=discord.ButtonStyle.primary)
    async def healing_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        sorted_stats = get_leaderboard_list(self.guild, button.label)
        output_message = f"***Leaderboard for {button.label}***\n\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value} {button.label}\n"
            count += 1

        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return

    @discord.ui.button(label="Nat 20",style=discord.ButtonStyle.primary)
    async def crit_succ_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        sorted_stats = get_leaderboard_list(self.guild, button.label)
        output_message = f"***Leaderboard for {button.label}***\n\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value} {button.label}\n"
            count += 1

        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return

    @discord.ui.button(label="Nat 1",style=discord.ButtonStyle.primary)
    async def crit_fail_button(self, interaction:discord.Interaction,button:discord.ui.Button):
        sorted_stats = get_leaderboard_list(self.guild, button.label)
        output_message = f"***Leaderboard for {button.label}***\n\n"
        count = 1
        for stat_char_tup in sorted_stats:
            stat_value = stat_char_tup[0]
            character = stat_char_tup[1]
            output_message += f"*{count}.* {character.get_name()} has {stat_value} {button.label}\n"
            count += 1

        new_view = LeaderBoardSingle(self.guild)
        new_view.message = self.message
        await interaction.response.edit_message(content = output_message, view = new_view)
        return

    @discord.ui.button(label="Close Menu", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if self.message != None: #Just check that a message actually got placed here... It can't happen upon __init__
            await self.message.delete()

class LeaderBoardSingle(discord.ui.View):
    def __init__(self, guild, timeout=60):
        super().__init__(timeout=timeout)
        self.message = None
        self.guild = guild

    @discord.ui.button(label="Back", style = discord.ButtonStyle.red)
    async def back_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        view = LeaderBoardMenu(self.guild)
        content = "What stat would you like to see the Leaderboard for?"
        view.message = self.message
        await interaction.response.edit_message(content=content, view = view)
