# -*- coding: utf-8 -*-
"""Kill Netease Pet 模组入口:注册服务端系统,进世界后自动清除官方伙伴。"""

from common.mod import Mod
import server.extraServerApi as serverApi
from mod_log import logger
from killPetScript.killPetConst import ModName, ModVersion, ServerSystemName, ServerSystemClsPath


@Mod.Binding(name=ModName, version=ModVersion)
class KillNeteasePet(object):

    @Mod.InitServer()
    def InitServer(self):
        logger.info("[KillNeteasePet] init server, version=%s", ModVersion)
        serverApi.RegisterSystem(ModName, ServerSystemName, ServerSystemClsPath)

    @Mod.DestroyServer()
    def DestroyServer(self):
        logger.info("[KillNeteasePet] destroy server")
