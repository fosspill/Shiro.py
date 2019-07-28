from discord.ext import commands
from library import exceptions

import pycountry
import re


class RangeInt(commands.Converter):
    """Convert to int if number is in range"""
    def __init__(self, min_num, max_num):
        self.min_num = min_num
        self.max_num = max_num

    async def convert(self, ctx, argument):
        try:
            argument = int(float(argument))
            if argument in range(self.min_num, self.max_num + 1):
                return argument
        except:
            pass

        raise exceptions.NotInRange(argument, self.min_num, self.max_num)


class Prefix(commands.Converter):
    """Converts to str if values length is in range"""
    async def convert(self, ctx, argument):
        if 1 <= len(argument) <= 10 and argument.isalnum():
            return argument

        raise exceptions.NotPrefix(argument)


class Bool(commands.Converter):
    """Converts to bool value if it's the specified"""
    def __init__(self, bool=None):
        self.bool = bool

    async def convert(self, ctx, argument):
        argument = argument.lower()
        if argument in ["true", "enable", "enabled", "on", "activate", "activated", "1"]:
            argument = True
        elif argument in ["false", "disable", "disabled", "off", "deactivate", "deactivated", "0"]:
            argument = False

        if (self.bool is None and isinstance(argument, bool)) or self.bool is argument:
            return argument

        raise exceptions.NotBool(argument, bool)


class Nothing(commands.Converter):
    """Converts to None if value is meant to be nothing"""
    async def convert(self, ctx, argument):
        argument = argument.lower()
        if argument in ["none", "nil", "reset", "0", "empty"]:
            return None

        raise exceptions.NotNothing


class Language(commands.Converter):
    """Converts to language value if it's the specified"""
    async def convert(self, ctx, argument):
        argument = argument.lower()
        available_languages = ctx.bot.get_languages()

        for language in pycountry.languages:
            if getattr(language, "name", None) == argument.capitalize():
                if getattr(language, "alpha_2", None) in available_languages:
                    return language.alpha_2
            elif getattr(language, "alpha_2", None) == argument:
                if getattr(language, "alpha_2") in available_languages:
                    return language.alpha_2
            elif getattr(language, "alpha_3", None) == argument:
                if getattr(language, "alpha_2", None) in available_languages:
                    return language.alpha_2

        raise exceptions.NotLanguage(argument, available_languages)


class YoutubeUrl(commands.Converter):
    """Convert to youtube url if video is available"""
    async def convert(self, ctx, argument):
        results = await ctx.bot.lavalink.get_tracks(argument)
        if results and results["tracks"]:
            video_id = re.search("((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", argument)[0]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url

        raise exceptions.NotYoutubeUrl(argument)


class Anime(commands.ColourConverter):
    """Convert to anime"""
    async def convert(self, ctx, argument):
