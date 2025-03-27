from typing import Any, Callable, Dict, List, Optional, Union

from fastapi import UploadFile
from pydantic import BaseModel

from agno.agent import Agent
from agno.playground.operator import format_tools
from agno.team import Team


class AgentModel(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None


class AgentGetResponse(BaseModel):
    agent_id: Optional[str] = None
    name: Optional[str] = None
    model: Optional[AgentModel] = None
    add_context: Optional[bool] = None
    tools: Optional[List[Dict[str, Any]]] = None
    memory: Optional[Dict[str, Any]] = None
    storage: Optional[Dict[str, Any]] = None
    knowledge: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    instructions: Optional[Union[List[str], str, Callable]] = None

    @classmethod
    def from_agent(self, agent: Agent) -> "AgentGetResponse":
        return AgentGetResponse(
            agent_id=agent.agent_id,
            name=agent.name,
            model=AgentModel(
                name=agent.model.name or agent.model.__class__.__name__ if agent.model else None,
                model=agent.model.id if agent.model else None,
                provider=agent.model.provider or agent.model.__class__.__name__ if agent.model else None,
            ),
            add_context=agent.add_context,
            tools=format_tools(agent.get_tools()) if agent.get_tools() else None,
            memory={"name": agent.memory.db.__class__.__name__} if agent.memory and agent.memory.db else None,
            storage={"name": agent.storage.__class__.__name__} if agent.storage else None,
            knowledge={"name": agent.knowledge.__class__.__name__} if agent.knowledge else None,
            description=agent.description,
            instructions=agent.instructions,
        )


class AgentRunRequest(BaseModel):
    message: str
    agent_id: str
    stream: bool = True
    monitor: bool = False
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    files: Optional[List[UploadFile]] = None


class AgentRenameRequest(BaseModel):
    name: str
    user_id: str


class AgentSessionsResponse(BaseModel):
    title: Optional[str] = None
    session_id: Optional[str] = None
    session_name: Optional[str] = None
    created_at: Optional[int] = None


class WorkflowRenameRequest(BaseModel):
    name: str


class WorkflowRunRequest(BaseModel):
    input: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class WorkflowSessionResponse(BaseModel):
    title: Optional[str] = None
    session_id: Optional[str] = None
    session_name: Optional[str] = None
    created_at: Optional[int] = None


class WorkflowGetResponse(BaseModel):
    workflow_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    storage: Optional[str] = None


class WorkflowsGetResponse(BaseModel):
    workflow_id: str
    name: str
    description: Optional[str] = None


class TeamModel(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None


class TeamGetResponse(BaseModel):
    team_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[str] = None
    model: Optional[TeamModel] = None
    success_criteria: Optional[str] = None
    instructions: Optional[Union[List[str], str, Callable]] = None
    members: Optional[List[Union[AgentGetResponse, "TeamGetResponse"]]] = None
    expected_output: Optional[str] = None
    context: Optional[str] = None
    enable_agentic_context: Optional[bool] = None
    response_model: Optional[str] = None
    storage: Optional[Dict[str, Any]] = None
    memory: Optional[Dict[str, Any]] = None

    @classmethod
    def from_team(self, team: Team) -> "TeamGetResponse":
        return TeamGetResponse(
            team_id=team.team_id,
            name=team.name,
            model=TeamModel(
                name=team.model.name or team.model.__class__.__name__ if team.model else None,
                model=team.model.id if team.model else None,
                provider=team.model.provider or team.model.__class__.__name__ if team.model else None,
            ),
            success_criteria=team.success_criteria,
            instructions=team.instructions,
            description=team.description,
            expected_output=team.expected_output,
            context=team.context,
            enable_agentic_context=team.enable_agentic_context,
            response_model=team.response_model,
            mode=team.mode,
            storage={"name": team.storage.__class__.__name__} if team.storage else None,
            memory={"name": team.memory.__class__.__name__} if team.memory else None,
            members=[
                AgentGetResponse.from_agent(member)
                if isinstance(member, Agent)
                else TeamGetResponse.from_team(member)
                if isinstance(member, Team)
                else None
                for member in team.members
            ],
        )


class TeamRunRequest(BaseModel):
    input: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class TeamSessionResponse(BaseModel):
    title: Optional[str] = None
    session_id: Optional[str] = None
    session_name: Optional[str] = None
    created_at: Optional[int] = None


class TeamRenameRequest(BaseModel):
    name: str
    user_id: str
