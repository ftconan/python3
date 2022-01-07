"""
# @author: magician
# @file:   pydantic_demo.py
# @date:   2022/1/7
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.class_validators import validator
from pydantic.error_wrappers import ValidationError
from pydantic.tools import parse_obj_as


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []
    header_name: str = Field(alias='表头', min_length=1, max_length=64)

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('name', 'header_name', pre=True)
    def name_check(cls, *args):
        print(','.join([*args]))


if __name__ == '__main__':
    # external_data = {
    #     '11id': '123',
    #     'signup_ts': '2019-06-01 12:22',
    #     'friends': [1, 2, '3'],
    #     '表头': 'head',
    # }
    # try:
    #     user = User(**external_data)
    #     print(user.dict())
    # except ValidationError as e:
    #     print(e.errors())
    #     # print(e.json())

    external_data_list = [
        {
            'id': '123',
            'name': 'a',
            'signup_ts': '2019-06-01 12:22',
            'friends': [1, 2, '3'],
            '表头': 'head',
        },
        {
            'id': '123',
            'name': 'b',
            'signup_ts': '2019-06-01 12:22',
            'friends': [1, 2, '3'],
            '表头': 'head',
        }
    ]
    try:
        user_list = parse_obj_as(List[User], external_data_list)
        print([dict(user) for user in user_list])
    except ValidationError as e:
        print(e.errors())
