# TYPING
from typing import Type

# ENTITY
from nvideos_web.core.entity.base.base_entity import AuditData
from nvideos_web.core.entity.channel import Channel, ChannelInput, ChannelMetadata

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# SQL BUILDER
from nvideos_web.impl.base.sql_builder import NvSql

# REPOSITORY
from nvideos_web.core.repository.channel_repository import ChannelRepository

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

class PgChannelRepository(ChannelRepository):
    def __init__(self, dbContext: Type[NewVideosDBContext]) -> None:
        super().__init__(dbContext=dbContext)

    def create(self, channelInputData: ChannelInput, auditInputData: AuditData) -> Channel:
        stmt = """
            insert into {table_name}
            ({fields})
            values
            
        """