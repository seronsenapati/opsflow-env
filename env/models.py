from pydantic import BaseModel
from typing import List, Dict, Any, Union

class Observation(BaseModel):
    task_type: str
    data: Union[Dict[str, Any], List[Any]]

class Action(BaseModel):
    decision: Dict

class Reward(BaseModel):
    score: float
