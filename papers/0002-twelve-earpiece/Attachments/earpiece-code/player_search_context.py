from typing import Optional, List
import typing
import pandas as pd
from pydantic import Field

from schemas import context
from schemas.nlc.base_context import BaseContext
from schemas.nlc.competition import CompetitionSeason
from schemas import context
from services.data_integration.specifications import BaseClient
from models.quality import PlayerQualityType
from constants.gender import GenderType, Gender
from services.data_integration.processing.utils import dump_df
from schemas.nlc.error import InvalidContextError
from schemas.nlc.utils import (
    get_competition_llm_prompt,
    get_single_competition_from_llm_disambiguation,
    llm_disambiguate,
)
from schemas.nlc.player_search_range import PlayerSearchRange
from config import config

if typing.TYPE_CHECKING:
    from models.registries import PositionRegistry
    from services.chat_integration.chat_client import ChatClient


class PlayerSearchContext(BaseContext):
    query: str = Field(
        description=(
            "The user query that caused the function to be called. This should be an exact copy of the user input, character by character. "
            "If the user input is a follow up about the player search, the query should be the follow up text, not the original query that triggered the function."
        ),
    )
    gender: GenderType = Field(description="The gender of the players to search for.")
    position: str = Field(
        description=(
            "The position of the players to search for. "
            "This should be the position that the user is interested in. "
            "If the user does not specify a position, ask them to do so."
            "Never assume a position, always ask the user to clarify. "
            "If the user asks for Goalkeepers, answer that you do not include analysis on goalkeepers. "
        ),
    )
    competition: CompetitionSeason = Field(
        description="The competition in which to search for players. If the user specifies more than one competition, ask them to clarify which one they want to use."
    )
    qualities: Optional[List[PlayerQualityType]] = Field(
        default=None,
        description=(
            "The qualities on which to evaluate the players. "
            "Look carefully at the users query and identify between one and three qualities "
            "to evaluate the players on and use these in the list. "
            "If the user does not explicitly specify qualities AND is not asking a ranking/leaderboard question, set it to null. "
            "IMPORTANT: When the user asks a ranking or leaderboard question (e.g. 'who is the top scorer?', 'who has the most assists?', 'who wins the most aerial duels?'), "
            "you MUST infer the most appropriate quality from the list below and set it here. Use the following mapping of common football concepts to qualities: "
            "- Goals / scoring / top scorer → FINISHING (for wingers/strikers) or POACHING (specifically for strikers who score through positioning) "
            "- Assists / chance creation / key passes / big chances created → PROVIDING_TEAMMATES "
            "- Pass completion / passing accuracy / progressive passing → PASSING_QUALITY "
            "- Aerial duels / heading / winning headers → AERIAL_THREAT (attacking) or DEFENSIVE_HEADING (defensive) or WINNING_DUELS (general) "
            "- Dribbling / take-ons / 1v1 → DRIBBLING "
            "- Pressing / high press / defensive intensity → PRESSING "
            "- Tackles / interceptions / ball recoveries → ACTIVE_DEFENCE "
            "- Carrying the ball / ball progression / advancing play → PROGRESSION "
            "- Runs in behind / off-the-ball movement → RUN_QUALITY "
            "- Composure / decision-making under pressure → COMPOSURE "
            "- Overall involvement / touches / influence → INVOLVEMENT "
            "- Efficiency / impact per action → EFFECTIVENESS "
            "- Hold-up play / link-up play / back-to-goal → HOLD_UP_PLAY "
            "- Box presence / penalty area threat → BOX_THREAT "
            "If the user's question clearly implies a ranking criterion, always select the matching quality even if they did not use the exact quality name."
        ),
    )
    search_range: PlayerSearchRange = Field(
        default=PlayerSearchRange(start=0, stop=5),
        description=(
            "A range indicating the range of players to be returned, in a format compatible with slice. "
            "For example, if it is the top (best) five players, search_range should be set to {'start': 0, 'stop': 5}. "
            "If it is the bottom (worst) 10 players, search_range should be set to {'start': -10, 'stop': null}. "
            "If it is the next 5 players after the top 5, search_range should be set to {'start': 5, 'stop': 10}."
        ),
    )
    min_age: Optional[int] = Field(
        default=None, description="The minimum age of the players."
    )
    max_age: Optional[int] = Field(
        default=None,
        description="The maximum age of the players. Set this to 23 if the user asks for young players without specifying an age.",
    )
    min_minutes: Optional[int] = Field(
        default=None,
        description="The minimum number of minutes a player must have played in the competition to be considered.",
    )
    detailed_position: Optional[str] = Field(
        default=None, description="The detailed position of the player."
    )

    async def to_machine_context(
        self,
        api_client: BaseClient,
        chat_client: "ChatClient",
        known_context: Optional[dict] = None,
        *,
        customer_id: str,
        workspace_positions: "PositionRegistry",
        provider: str = "wyscout",
    ) -> context.PlayerSearchContext:
        if config.debug.context_resolution:
            print("query: ", self.query)
            print("parsed: ", self.competition, self.qualities)
            print(self.gender)

        competition_name = f"{self.competition.name} {self.competition.country}"
        # Get dataframe with possible competitions
        df_competitions = await api_client.search_competitions_fulltext(
            customer_id,
            competition_name=competition_name,
            text_weight=0.50,
            ranking_weights=0.0,
            ngrams_weight=0.50,
            limit=20,
            provider=provider,
        )

        if self.gender != Gender.NEUTRAL:
            # Filter the competitions on gender
            df_competitions = df_competitions[
                df_competitions["gender"] == self.gender.name.lower()
            ]

        # Filter the competitions on very low combined score
        df_competitions = pd.DataFrame(
            df_competitions[df_competitions["combined_score"] > 0.5]
        )

        if config.debug.context_resolution:
            print(df_competitions[["competition", "country", "name"]])

        if df_competitions.empty:
            raise InvalidContextError(
                f"Could not find a match for competition {self.competition.name}."
            )

        disambiguation_prompt = get_competition_llm_prompt(
            self.query, self.competition, df_competitions
        )

        instructions = "You are an assistant that selects the most likely football league based on given criteria."
        llm_response = await llm_disambiguate(
            chat_client, instructions, disambiguation_prompt
        )

        if config.debug.context_resolution:
            print(llm_response)

        if llm_response is None:
            raise InvalidContextError(
                f"Could not find a match for competition {self.competition.name}."
            )

        df_single_competition = get_single_competition_from_llm_disambiguation(
            llm_response, df_competitions
        )

        resolved_context = self.get_context(
            df_single_competition, self.qualities, workspace_positions
        )
        return resolved_context

    def get_context(
        self,
        df_single: pd.DataFrame,
        qualities: Optional[List[PlayerQualityType]],
        workspace_positions: "PositionRegistry",
    ) -> context.PlayerSearchContext:
        resolved_competition = context.CompetitionSeason(
            id=pd.Series(df_single["competition"]).iloc[0],
            year=pd.Series(df_single["season"]).iloc[0],
            name=pd.Series(df_single["name"]).iloc[0],
            country=pd.Series(df_single["country"]).iloc[0],
        )

        if qualities is None:
            pos_info = workspace_positions.get_position(self.position)
            resolved_qualities = pos_info.relevant_qualities if pos_info else []
        else:
            resolved_qualities = qualities

        resolved_search_range = context.PlayerSearchRange(
            start=self.search_range.start,
            stop=self.search_range.stop,
        )

        resolved_context = context.PlayerSearchContext(
            query=self.query,
            summary=self.summary,
            position=self.position,
            competition=resolved_competition,
            qualities=resolved_qualities,
            search_range=resolved_search_range,
            min_age=self.min_age,
            max_age=self.max_age,
            min_minutes=self.min_minutes,
            detailed_position=self.detailed_position,
        )
        return resolved_context
