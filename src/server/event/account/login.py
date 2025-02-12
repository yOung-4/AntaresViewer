#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2023. Suto-Commune
#  _
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  _
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  _
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : login.py

@Author     : hsn

@Date       : 2/20/24 6:49 PM
"""
import logging
from pathlib import Path

import fastapi
from fastapi import Response

import src.function.format.avi as AVInfo
from src.function.database.db import DB
from src.toml_config import config
from src.utils.crypto import check_password_hash, JWT

logger = logging.getLogger(__name__)
Name = AVInfo.Name()
default_url = Name.default_url
router = fastapi.APIRouter()


@router.get(default_url)
@router.post(default_url)
async def login(uid: str, password: str):
    db = DB(config.DB.db_uri, "Antares_accounts", config.DB.db_username, config.DB.db_password)
    rst = await db.find("users", {"uid": uid})
    if rst:
        user_data = rst[0]
        psw_hash = user_data["password"]
        login_success = check_password_hash(password=password, hash_=psw_hash)
    else:
        return {"code": "403", "message": "Login failed, uid error."}

    if login_success:
        with Path("server.key").open("r", encoding="utf-8") as f:
            key = f.read()
        token = JWT(key).encode({"uid": uid})
        return {"code": "200", "token": token}
    else:
        return {"code": "403", "message": "Login failed, password error."}
