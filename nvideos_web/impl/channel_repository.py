# TYPING
from typing import override

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
    def __init__(self, dbContext: type[NewVideosDBContext]) -> None:
        super().__init__(dbContext=dbContext)

    @override
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
            _ = cur.execute(stmt, params=paramsParsed)
            result = cur.fetchone()
            conn.commit()
            return ChannelMetadata.row(result)
    
    @override
    def checkIdExists(self, channelId: int) -> bool:
        stmt = NvSql.formatStmt(
            "select 1 from {table_name} where {channel_id} = {channel_id_value};",
            table_name=ChannelMetadata.tableName(),
            channel_id=ChannelMetadata.channelId.field,
            channel_id_value=channelId
        )
        with self._db.getConn() as conn:
            r = conn.execute(stmt)
            return r.rowcount > 0

    @override
    def updateById(self, channelId: int, newChannelData: ChannelInput, auditData: AuditData) -> Channel:
        channelFields = NvSql.updateFields(ChannelMetadata, newChannelData)
        auditFields = NvSql.updateFields(ChannelMetadata, auditData)
        
        sqlFieldsReturn, sqlFieldsOrder = NvSql.selectOder(ChannelMetadata.all)

        stmt = NvSql.formatStmt(
            """
            update {table_name} 
               set {channel_fields}, {audit_fields} 
             where {channel_id} = {channel_id_value}
             returning {sql_Fields_return};
            """,
            table_name=ChannelMetadata.tableName(),
            channel_fields=channelFields,
            audit_fields=auditFields,
            channel_id=ChannelMetadata.channelId.field,
            channel_id_value=channelId,
            sql_fields_return=sqlFieldsReturn
        )
        paramsUpdate = NvSql.parseSqlParams(stmt, inputObject=newChannelData, auditObject=auditData)
    
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(sqlFieldsOrder))
            cur.execute(stmt)
            result = cur.fetchone()
            conn.commit()
            return ChannelMetadata.row(result)

    @override
    def delete(self, channelId: int, auditData: AuditData) -> Channel:
        auditFields = NvSql.updateFields(ChannelMetadata, auditData)
        fieldsStr, fieldsOder = NvSql.selectOder(ChannelMetadata.all)
        stmt = NvSql.formatStmt(
            """
            update {table_name} set {active_field} = false, {audit_fields} where {channel_id_field} = {channel_id_value}
            returning {fields_str};
            """,
            table_name=ChannelMetadata.tableName(),
            active_field=ChannelMetadata.channelIsActive.field,
            audit_fields=auditFields,
            channel_id_field=ChannelMetadata.userId.field,
            channel_id_value=channelId,
            fields_str=fieldsStr
        )
        paramsUpdate = NvSql.parseSqlParams(stmt, auditData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(fieldsOder))
            cur.execute(stmt, params=paramsUpdate)
            result = cur.fetchone()
            conn.commit()
            return ChannelMetadata.row(result)