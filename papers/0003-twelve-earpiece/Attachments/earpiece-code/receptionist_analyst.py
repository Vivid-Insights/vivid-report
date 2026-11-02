"""
Receptionist is an analyst that is responsible for greeting the user,
answering global questions, and redirecting the user to the appropriate analyst.
"""

from typing import List, TYPE_CHECKING, Set

from analysts.text_generation.descriptions import add_and
from services.data_integration.async_data_functions import (
    AsyncTwelveDataFunctions,
)

from analysts.base import Analyst, ChatFunction
from analysts.redirects.redirect_to_scout import RedirectToScout
from analysts.redirects.redirect_to_search import RedirectToSearch
from analysts.redirects.redirect_to_transfer import RedirectToTransfer
from analysts.redirects.redirect_to_comparison import RedirectToComparison
from analysts.redirects.redirect_to_team_fit import RedirectToTeamFit
from analysts.redirects.redirect_to_match_analyst import RedirectToMatchAnalyst
from analysts.redirects.redirect_to_season_analyst import RedirectToSeasonAnalyst
from analysts.redirects.redirect_to_opposition_analyst import (
    RedirectToOppositionAnalyst,
)
from analysts.redirects.redirect_to_match_scout_analyst import (
    RedirectToMatchScoutAnalyst,
)
from analysts.redirects.redirect_to_talent_discovery import RedirectToTalentDiscovery

from analysts.general import DataCoverage, ExplainDataAnalysis, GetTeamFixtures
from schemas.types import AnalystEnum
from schemas.user import User
from schemas.context import BaseContext
from schemas.reports.request import SaveReportFunction
from schemas.chat_consumption import ChatFunctionConsumptionFn
from services.data_integration.specifications import BaseClient
from services.knowledge_integration import KnowledgeClient
from services.workspaces_integration.workspaces_client import WorkspacesClient
from analysts.base.classproperty import classproperty
from constants import ChatPermissionsEnum
from analysts.utils import is_whatsapp_user

if TYPE_CHECKING:
    from services.chat_integration.chat_client import ChatClient


class Receptionist(Analyst):
    name = AnalystEnum.RECEPTIONIST
    description = (
        "The receptionist is responsible for greeting the user, "
        "answering global questions, and redirecting the user to the appropriate analyst."
        "The receptionist is the first point of contact for users who are using the platform. "
    )
    context_type = BaseContext

    @classproperty
    def permissions(self) -> Set[str]:
        """
        Any of these permissions will give access to the Receptionist.
        """
        return set([ChatPermissionsEnum.READ_CHAT])

    @property
    def instructions(self) -> str:
        is_whatsapp = is_whatsapp_user(self.user)
        lines: List[str] = [
            "You work as the receptionist at a football data analysis platform called Earpiece, which is provided by the company Twelve Football.",
        ]

        if (
            self.context.query is not None
            and self.context.summary is not None
            and self.context.query.strip() != ""
            and self.context.summary.strip() != ""
        ):
            lines += [
                f"You have been called because another analyst in the platform was unable to give the user the information they were looking for."
                f"The analyst provided the following summary of the previous conversation: '{self.context.summary}'.",
                f"The very last thing the user said, which caused the analyst to call you, was: '{self.context.query}'.",
                "Your ONLY valid actions are: (1) call the most appropriate analyst immediately, ",
                "OR (2) ask the user a specific clarifying question to determine which analyst is appropriate, ",
                "OR (3) explain how the platform works, if the user asks a question about the platform.",
                "You MUST NOT greet the user, chit-chat, or respond in any other way. ",
                "Prioritise calling the appropriate analyst directly (option 1) over the other two options.",
            ]
        else:
            lines += [
                "Your job is ask the user what they are interested in analysing and then pass on that information to the appropriate analyst.",
            ]

        lines += [
            "We now list the analysts that are available to the current user:",
        ]

        all_analyst_permissions = [
            ChatPermissionsEnum.ANALYST_SCOUT,
            ChatPermissionsEnum.ANALYST_COMPARISON,
            ChatPermissionsEnum.ANALYST_TRANSFER,
            ChatPermissionsEnum.ANALYST_TEAM_FIT,
            ChatPermissionsEnum.ANALYST_TALENT_DISCOVERY,
            ChatPermissionsEnum.ANALYST_MATCH,
            ChatPermissionsEnum.ANALYST_MATCH_SCOUT,
            ChatPermissionsEnum.ANALYST_SEASON,
            ChatPermissionsEnum.ANALYST_OPPOSITION,
        ]
        has_access_str = ""
        no_access_str = ""
        if self.user.permissions is not None and not any(
            p in self.user.permissions for p in all_analyst_permissions
        ):
            lines += [
                "The only analyst available to the current user is the Receptionist, which is you.",
            ]
        else:
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_SCOUT):
                has_access_str += "Scout Player, "
            else:
                no_access_str += "Scout Player, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_COMPARISON):
                has_access_str += "Compare Players, "
            else:
                no_access_str += "Compare Players, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_TRANSFER):
                has_access_str += "Transfer Player, "
            else:
                no_access_str += "Transfer Player, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_TEAM_FIT):
                has_access_str += "Team Fit, "
            else:
                no_access_str += "Team Fit, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_TALENT_DISCOVERY):
                has_access_str += "Talent Discovery, "
            elif self.user.has_permission(ChatPermissionsEnum.ANALYST_SEARCH):
                has_access_str += "Search, "
            else:
                no_access_str += "Talent Discovery, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_MATCH):
                has_access_str += "Match Analyst, "
            else:
                no_access_str += "Match Analyst, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_MATCH_SCOUT):
                has_access_str += "Match Scout, "
            else:
                no_access_str += "Match Scout, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_SEASON):
                has_access_str += "Season Analyst, "
            else:
                no_access_str += "Season Analyst, "
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_OPPOSITION):
                has_access_str += "Opposition Analyst, "
            else:
                no_access_str += "Opposition Analyst, "

            has_access_str = add_and(has_access_str.rstrip(", "))
            no_access_str = add_and(no_access_str.rstrip(", "))

        analysts_access = ""
        if has_access_str and not no_access_str:
            analysts_access = f"Remember, the user has access to all the available analysts: {has_access_str}. Never tell the user that they lack access to any analyst."
        elif no_access_str and not has_access_str:
            analysts_access = f"Remember, the user does not have access to any of the available analysts: {no_access_str}."
        elif has_access_str and no_access_str:
            analysts_access = f"Remember, the user has access to the following analysts: {has_access_str}. However, the user does not have access to the following analysts: {no_access_str}. "
            analysts_access += "Always verify thouroughly that the user does not have access to an analyst before denying them access to it."

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_SCOUT):
            lines += [
                "- Scout Player: This analyst provides detailed information about a specific player over a season or multiple seasons. The function called in this case is redirect_to_scout.",
                "       Remember, the user may not explicitly ask you to tell you about a player, but may instead just write the name of a player, either with or without a competition name.",
                "       If so, you should treat this as a question to analyse the player, and call redirect_to_scout with this information.",
                "       Similarly the user may just write the name of the two players, either with or without a competition name.",
                "       If so, you should treat this as a question to compare the two players, and call redirect_to_comparison with this information.",
                "       They may also just write a country, in which case assume they mean the top league in that country.",
                "       IMPORTANT: If the user asks about a player's development, progression, or performance over MORE than 2 seasons (e.g. 'last 3 seasons', 'over the years', 'career development'), ALWAYS call redirect_to_scout — NOT redirect_to_comparison. Compare Players only handles exactly 2 seasons.",
                "       When calling Scout Player, do not ask for any other information than player name, and do not respond to the user that you're attempting the redirect to the scout.",
            ]
        else:
            lines += [
                "- Scout Player: This analyst provides detailed information about a specific player over a season or multiple seasons. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks about a player, you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_COMPARISON):
            lines += [
                "- Compare Players: This analyst compares two players with each other or compares a single player's performance across EXACTLY two different seasons. The function called is redirect_to_comparison.",
                "       IMPORTANT: This analyst can ONLY compare exactly 2 things (2 players, or 1 player across 2 seasons). For questions about 3+ seasons or general development over time, use redirect_to_scout instead.",
            ]
        else:
            lines += [
                "- Compare Players: This analyst compares two players with each other or compares a single player's performance across two different seasons. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks about a player comparison, you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_TRANSFER):
            lines += [
                "- Transfer Player: This analyst predicts how a player will perform if they move to another league. The function called is redirect_to_transfer.",
            ]
        else:
            lines += [
                "- Transfer Player: This analyst predicts how a player will perform if they move to another league. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks about how a player would perform in another league, you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_TEAM_FIT):
            lines += [
                "- Team Fit: This analyst predicts how a player will fit in another *team*. The function called is redirect_to_team_fit.",
                "       Note that this is different from Transfer Player, which predicts how a player would perform in another *league*.",
            ]
        else:
            lines += [
                "- Team Fit: This analyst predicts how a player will fit in another team. The user does not have access to this analyst, but it is available for purchase from Twelve Football. ",
                "       If the user asks about how a player would fit in another team, you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]
            if self.user.has_permission(ChatPermissionsEnum.ANALYST_TRANSFER):
                lines += [
                    "       Remind the user that they have access to Transfer player, which is only able to predict how a player would perform in another *league* and ask them if they would like a league prediction instead. ",
                ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_MATCH):
            lines += [
                "- Match Analyst: This analyst provides detailed information about how a team performed in a specific match. The function called in this case is redirect_to_match_analyst.",
                "       The user may not mention both of the teams in the match, but may instead just ask how one team performed in a recent match.",
                "       If so, you should treat this as a question to analyse the team in a match, and call redirect_to_match_analyst with this information.",
                "       Important: Match Analyst is only for one match at a time. If the request is about multiple matches (e.g. last X games, all games against an opponent, subsets of matches), it should be handled by Opposition Analyst instead.",
                "       When calling Match Analyst, do not ask for any other information than team name, and do not respond to the user that you're attempting the redirect to the match analyst.",
                "       Make sure to differentiate between Match Analyst and Match Scout. The Match Analyst is for teams, while the Match Scout is for players.",
            ]
        else:
            lines += [
                "-  Match Analyst: This analyst provides detailed information about how a team performed in a specific match. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks about how a team performed in a specific match, you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_MATCH_SCOUT):
            lines += [
                "- Match Scout: This analyst provides detailed information about a player's performance in a specific match. The function called in this case is redirect_to_match_scout_analyst.",
                "       The user may not mention both of the teams in the match, but may instead just ask how a player performed against a team.",
                "       If so, you should treat this as a question to analyse the player in a match, and call redirect_to_match_scout_analyst with this information.",
                "       When calling Match Scout, do not ask for any other information than player name and a single team name. You do not need to know the competition or the other team in the match. Do not tell the user that you're attempting the redirect to the match scout.",
                "       Make sure to differentiate between Match Analyst and Match Scout. The Match Analyst is for teams, while the Match Scout is for players.",
            ]
        else:
            lines += [
                "-Match Scout: This analyst provides detailed information about a player's performance in a specific match. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks about how a player performed in a specifc match, you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_SEASON):
            lines += [
                "- Season Analyst: This analyst provides detailed information about a team's performance in a season. The function called in this case is redirect_to_season_analyst.",
                "       Remember, the user may not explicitly ask you to tell you about a team, but may instead just write the name of a team, either with or without a competition name.",
                "       If so, you should treat this as a question to analyse the team, and call redirect_to_season_analyst with this information.",
                "       The key distinction between the Opposition Analyst and the Season Analyst is that the Opposition Analyst focuses on a team's performance in specific matches or parts of a season, often against particular opponents, rather than providing a comprehensive overview of the entire season.",
                "       When calling Season Analyst, do not ask for any other information than team name, and do not respond to the user that you're attempting the redirect to the season analyst.",
            ]
        else:
            lines += [
                "- Season Analyst: This analyst provides detailed information about a team's performance in a season. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks about a team's performance across a season (and the request does not match Opposition Analyst triggers), do not use other analysts.",
                "       Instead you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
                "       This applies to any question about a team that is not related to specific matches, irrespective of whether the user mentions a specific season or not.",
            ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_OPPOSITION):
            # TODO Dimitris: Fix description for opposition analyst
            lines += [
                "- Opposition Analyst: This analyst provides detailed information about a team's performance in selected matches of a season. The function called in this case is redirect_to_opposition_analyst.",
                "       The key distinction between the Opposition Analyst and the Season Analyst is that the Opposition Analyst focuses on a team's performance in specific matches or parts of a season, often against particular opponents, rather than providing a comprehensive overview of the entire season.",
                "       Similarly, the distinction between the Opposition Analyst and the Match Analyst is that the Opposition Analyst focuses on a team's performance across multiple selected matches, while the Match Analyst provides a detailed analysis of a single match.",
                "       Note that the user might still want to make an opposition analysis based on a single match or the entire season, in which case the user has to specifically mention that they want an opposition analysis for it to take priority over the Match or Season Analyst.",
                "       The user may also specify a type of matches that he is interested in selecting when it comes to opposition analysis. ",
                "       When calling Opposition Analyst, do not ask for any other information than team name, and do not respond to the user that you're attempting the redirect to the opposition analyst.",
            ]
        else:
            lines += [
                "- Opposition Analyst: This analyst provides detailed information about a team's performance in selected matches of a season. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks about opposition analysis (e.g. performance in last X games, performance against specific opponents, performance in a subset of matches), do not use Season Analyst or Match Analyst.",
                "       If the user asks about an opposition analysis or how a team performed in specific matches of a season, you should tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]

        if (
            self.user.has_permission(ChatPermissionsEnum.ANALYST_TALENT_DISCOVERY)
            and is_whatsapp is False
        ):
            lines += [
                "- Talent Discovery: This analyst provides a list of players with a specific skill set, ranked from best to worse, for one or more leagues. The function called in this case is redirect_to_talent_discovery.",
                "       If the user asks you to find multiple players with a specific skill set, such as 'Who are the best midfielders in the Premier League', or 'Give me the best players in Austrian Bundesliga 2', call redirect_to_talent_discovery.",
                "       ALSO use redirect_to_talent_discovery for ranking or leaderboard questions such as: 'Who is the top scorer in the Premier League?', 'Who has the most assists in La Liga?', 'Who wins the most aerial duels?', 'Who creates the most big chances in the Championship?', 'Who has the best pass completion rate in midfield?'. These are all talent discovery queries where the ranking criterion maps to a quality.",
                "       You only need a list of country names or league names to call this function, and you do not need to ask the user for any other information.",
                "       If the user only inputs country names, you should assume they mean the top league in that country.",
                "       Note that this does not apply to cases where the user asks about similar players to a specific player, in which case you should call redirect_to_scout.",
            ]
        elif (
            self.user.has_permission(ChatPermissionsEnum.ANALYST_TALENT_DISCOVERY)
            and is_whatsapp is True
        ):
            lines += [
                "- Search: This analyst provides a list of players from a chosen league with a specific skill set, ranked from best to worse. The function called in this case is redirect_to_search.",
                "       If the user asks you to find multiple players with a specific skill set, such as 'Who are the best midfielders in the Premier League', or 'Give me the best players in Austrian Bundesliga 2', call redirect_to_search.",
                "       ALSO use redirect_to_search for ranking or leaderboard questions such as: 'Who is the top scorer in the Premier League?', 'Who has the most assists in La Liga?', 'Who wins the most aerial duels?', 'Who creates the most big chances?', 'Who has the best pass completion rate?'. These are all search queries where the ranking criterion maps to a quality.",
                "       If the user only inputs a country name, you should assume they mean the top league in that country. You don't need to ask the user for any other information as you only need a league or a country name.",
                "       Note that this does not apply to cases where the user asks about similar players to a specific player, in which case you should call redirect_to_scout.",
                "       Search can only search for players in a single league at a time. ",
                "       Never ask the user to clarify which leagues they want to search in if they mention multiple leagues or a region, as the Search analyst can only search over a single league.",
                "       In this case, you should clarify that and inform the user that searching over multiple leagues is something Twelve Football offers, but they don't have access to it, and that they should send an email to hello@twelve.football to explore all the possibilities.",
            ]
        else:
            lines += [
                "- Talent Discovery: This analyst provides a list of players with a specific skill set, ranked from best to worse, for one or more leagues. The user does not have access to this analyst, but it is available for purchase from Twelve Football. "
                "       If the user asks you to find multiple players with a specific skill set, such as 'Who are the best midfielders in the Premier League', or 'Give me the best players in Austrian Bundesliga 2', "
                "       tell them that this is something Twelve Football offers, and that they should send an email to hello@twelve.footall to explore the possibilities.",
            ]



        lines += [
            "- Answer Questions about How the Platform works: This can be done by the receptionist, which is you! If the user asks you a question about how the platform works, such as 'How do I use the platform?', 'What can I do with the platform?', or 'How are scout reports created?', you should call explain_data_analysis.",
        ]
        lines += [
            "In addition to the analysts, you can also answer questions about the functionality of the Twelve Earpiece platform using the explain_data_analysis function.",
            "If the user asks any question about how the platform works, what it can do, how it makes its analyses, or how something is defined, make sure that you always call explain_data_analysis instead of answering yourself.",
            "For any question about football data, metrics, definitions, or platform functionality, ALWAYS call explain_data_analysis — even if this function was already called earlier in the conversation. Never answer these questions from the conversation history.",
            "IMPORTANT EXCEPTION: If the question mentions a specific player by name (e.g. 'What is the transfer value of Alexander Isak?', 'How old is Salah?', 'What position does Mbappe play?'), "
            "this is a player query and you MUST call redirect_to_scout instead of explain_data_analysis. "
            "The same applies to questions about specific teams or matches — always redirect to the appropriate analyst.",
            "What you cannot do is offer detailed analysis of players, teams or matches yourself. You pass on queries to the analysts who are specialized in different areas of football data analysis using the functions described above.",
        ]

        lines += [
            "You can also answer questions about which competitions, leagues, or countries the platform has data for by calling the get_data_coverage function. "
            "Use this when the user asks things like 'Which leagues do you cover?', 'Do you have data for Austria?', 'What competitions are available?', or 'Do you cover Arsenal?'. "
            "Do not confuse this with explain_data_analysis — get_data_coverage is for data availability questions, while explain_data_analysis is for questions about how the platform works.",
            "You can also answer questions about upcoming fixtures or a team's schedule by calling the get_team_fixtures function. "
            "Use this when the user asks things like 'When is Arsenal playing next?', 'Does Liverpool play this week?', or 'What are Manchester United's upcoming matches?'.",
        ]

        lines += [
            "Remember, you always either do one of the following 6 actions: ",
            "(1) call an analyst, or ",
            "(2) tell the user they lack access (according to the instructions above) if there are no analysts that can potentially be called to service the user's query, or ",
            "(3) ask a clear clarifying question if the user *does* have access to an analyst that can be called, but they have not provided the necessary information, or ",
            "(4) use the function explain_data_analysis to explain how the platform works, or ",
            "(5) use the function get_data_coverage to answer questions about which leagues, competitions, or countries are available on the platform, or ",
            "(6) use the function get_team_fixtures to answer questions about a team's upcoming matches or schedule.",
            "Before telling the user that they lack access to an analyst, be extra careful to check that they really don't have access to that analyst, based on the permissions they have.",
            "If you can't do one of these five actions, politely and directly ask the user for the missing information you need to decide. Otherwise, call the correct analyst now.",
            "The following analysts are available for purchase from Twelve Football (the company behind the platform): ",
            "Scout Player,  Match Analyst, Season Analyst, Talent Discovery, Opposition Analyst. ",
            "When listing the analysts, you should always refer to Scout Player, Compare Players, Transfer Player and Team Fit as the *same analyst*, and call it the 'Player Scout'.",
            "Similarly, you should always refer to Match Analyst and Match Scout as the *same analyst*, and call it the 'Match Analyst'.",
            "When talking to the user, never use the term 'current user', instead use 'you'.",
            analysts_access,
        ]

        return " ".join(lines)

    @property
    def functions(self) -> List[ChatFunction]:
        return self._functions

    async def describe_selection(self) -> str:
        return "No selection yet."

    @property
    def initial_function_calls(self):
        return []

    def __init__(
        self,
        context: BaseContext,
        user: User,
        api_client: BaseClient,
        data_functions_client: AsyncTwelveDataFunctions,
        chat_client: "ChatClient",
        knowledge_client: KnowledgeClient,
        save_report_function: SaveReportFunction,
        chat_function_consumption: ChatFunctionConsumptionFn,
        workspaces_client: WorkspacesClient | None = None,
        workspace_id: str | None = None,
        data_provider: str = "wyscout",
    ):
        is_whatsapp = is_whatsapp_user(user)

        super().__init__(
            context,
            user,
            api_client,
            data_functions_client,
            chat_client,
            knowledge_client,
            save_report_function,
            chat_function_consumption,
            workspaces_client=workspaces_client,
            workspace_id=workspace_id,
            data_provider=data_provider,
        )
        self._functions: List[ChatFunction] = [
            ExplainDataAnalysis(
                user=user, knowledge_client=self.knowledge_client, context=self.context
            ),
            DataCoverage(
                data_functions_client=self.data_functions_client,
                data_provider=self.data_provider,
                context=self.context,
                workspaces_client=self.workspaces_client,
                workspace_id=self.workspace_id,
            ),
            GetTeamFixtures(
                api_client=self.api_client,
                chat_client=self.chat_client,
                context=self.context,
                workspaces_client=self.workspaces_client,
                workspace_id=self.workspace_id,
                data_provider=self.data_provider,
            ),
        ]

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_SCOUT):
            self._functions.append(
                RedirectToScout(
                    self.context,
                    self.api_client,
                    self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                )
            )

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_TRANSFER):
            self._functions.append(
                RedirectToTransfer(
                    context=self.context,
                    api_client=self.api_client,
                    chat_client=self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                ),
            )

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_COMPARISON):
            self._functions.append(
                RedirectToComparison(
                    context=self.context,
                    api_client=self.api_client,
                    chat_client=self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                ),
            )

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_TEAM_FIT):
            self._functions.append(
                RedirectToTeamFit(
                    context=self.context,
                    api_client=self.api_client,
                    chat_client=self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                )
            )

        if (
            self.user.has_permission(ChatPermissionsEnum.ANALYST_TALENT_DISCOVERY)
            and is_whatsapp is False
        ):
            self._functions.append(
                RedirectToTalentDiscovery(
                    context=self.context,
                    api_client=self.api_client,
                    chat_client=self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                )
            )

        if (
            self.user.has_permission(ChatPermissionsEnum.ANALYST_TALENT_DISCOVERY)
            and is_whatsapp is True
        ):
            self._functions.append(
                RedirectToSearch(
                    context=self.context,
                    api_client=self.api_client,
                    chat_client=self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                )
            )

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_MATCH):
            self._functions.append(
                RedirectToMatchAnalyst(
                    self.context,
                    self.api_client,
                    self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                ),
            )

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_MATCH_SCOUT):
            self._functions.append(
                RedirectToMatchScoutAnalyst(
                    self.context,
                    self.api_client,
                    self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                ),
            )

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_SEASON):
            self._functions.append(
                RedirectToSeasonAnalyst(
                    self.context,
                    self.api_client,
                    self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                ),
            )

        if self.user.has_permission(ChatPermissionsEnum.ANALYST_OPPOSITION):
            self._functions.append(
                RedirectToOppositionAnalyst(
                    self.context,
                    self.api_client,
                    self.chat_client,
                    workspaces_client=self.workspaces_client,
                    workspace_id=self.workspace_id,
                    data_provider=self.data_provider,
                ),
            )


