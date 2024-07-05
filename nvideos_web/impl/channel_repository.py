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
from nvideos_web.core.repository.channel import ChannelRepository

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

class PgChannelRepository(PgRepositoryBase, ChannelRepository):
    def __init__(self, dbContext: Type[NewVideosDBContext]) -> None:
        super().__init__(dbContext=dbContext)

    def create(self, channelInputData: ChannelInput, auditInputData: AuditData) -> Channel:
        inputFieldsInsert, inputParamsFields, inputOrder = NvSql.insertFieldsOrder(ChannelMetadata, channelInputData)
        auditFieldsInsert, auditParamsFields, auditOrder = NvSql.insertFieldsOrder(ChannelMetadata, auditInputData)

        fieldsOrder = inputOrder + auditOrder

        stmt = NvSql.formatStmt(
            """
            insert into {table_name}
            ({fields_input},{fields_audit})
            values
            ({input_params},{audit_params})
            returning {fields_input},{fields_audit};
            """,
            table_name=ChannelMetadata.tableName(),
            fields_input=inputFieldsInsert,
            fields_audit=auditFieldsInsert,
            input_params=inputParamsFields,
            audit_params=auditParamsFields
        )
        paramsParsed = NvSql.parseSqlParams(stmt, inputObject=channelInputData, auditObject=auditInputData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(fieldsOrder))
            cur.execute(stmt, params=paramsParsed)
            result = cur.fetchone()
            conn.commit()
            return ChannelMetadata.row(result)
    
    def updateById(self, channelId: int, newChannelData: ChannelInput, auditData: AuditData) -> Channel:
        raise NotImplementedError()
    
    def delete(self, channelId: int, auditData: AuditData) -> Channel:
        raise NotImplementedError()