# -*- coding: utf-8 -*-
"""服务端系统:监听实体生成,发现官方伙伴立即销毁。

伙伴由网易引擎按账号宠物数据召唤,不检查实体定义的 is_summonable,
因此只能在实体生成后将其移除。AddEntityServerEvent 对新召唤和
从存档加载的实体都会触发,可以覆盖两种来源。
"""

import server.extraServerApi as serverApi
from mod_log import logger
from killPetScript.killPetConst import PetIdentifier

ServerSystem = serverApi.GetServerSystemCls()


class KillPetServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self._petCount = 0
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "AddEntityServerEvent", self, self.OnAddEntity)
        logger.info("[KillNeteasePet] server system created")

    def Destroy(self):
        self.UnListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "AddEntityServerEvent", self, self.OnAddEntity)

    def OnAddEntity(self, args):
        if args.get("engineTypeStr") != PetIdentifier:
            return
        entityId = args.get("id")
        self._petCount += 1
        logger.info("[KillNeteasePet] destroy pet #%d entityId=%s", self._petCount, entityId)
        if not self.DestroyEntity(entityId):
            # 引擎刚创建实体时可能拒绝立即销毁,延迟一帧重试
            levelId = serverApi.GetLevelId()
            gameComp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            gameComp.AddTimer(0.2, self.DestroyEntity, entityId)
