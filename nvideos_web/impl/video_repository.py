# TYPING
from typing import override

# PSYCOPG
from psycopg.cursor import Cursor

# REPOSITORY
from nvideos_web.core.repository.video import VideoRepository

# ENTITY
from nvideos_web.core.entity.video import Video, VideoInput, VideoMetadata
from nvideos_web.core.entity.base.base_entity import AuditData

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

# SQL BUILDER
from nvideos_web.impl.base.sql_builder import NvSql

class PgVideoRepository(PgRepositoryBase, VideoRepository):
    @override
    def create(self, videoInputData: VideoInput, auditInputData: AuditData) -> Video: 
        inputFields, inputParams, _ = NvSql.insertFieldsOrder(VideoMetadata, videoInputData)
        auditFields, auditParams, _ = NvSql.insertFieldsOrder(VideoMetadata, auditInputData)
        _, allFieldsOrder = NvSql.selectOder(VideoMetadata.all)

        stmt = NvSql.formatStmt(
            """
            insert into {table_name}
            ({input_fields},{audit_fields})
            values
            ({input_params},{audit_params})
            returning *;
            """,
            table_name=VideoMetadata.tableName(),
            input_fields=inputFields,
            audit_fields=auditFields,
            input_params=inputParams,
            audit_params=auditParams
        )
        paramsInsert = NvSql.parseSqlParams(stmt, inputObject=videoInputData, auditObject=auditInputData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))
            cur.execute(stmt, params=paramsInsert)
            result = cur.fetchone()
            conn.commit()
            return VideoMetadata.row(result)

    @override
    def checkIdExists(self, videoId: int) -> bool: 
        stmt = NvSql.formatStmt(
            "select 1 from {table_name} where {video_id} = {video_id_value};",
            table_name=VideoMetadata.tableName(),
            video_id=VideoMetadata.videoId.field,
            video_id_value=videoId
        )
        with self._db.getConn() as conn:
            r: Cursor = conn.execute(stmt)
            return r.rowcount > 0

    @override
    def checkKeyExists(self, videoKey: str) -> bool: 
        paramVideoKey, videoKeyValue = NvSql.createParam("videoKey", videoKey)
        stmt = NvSql.formatStmt(
            """
            select 1 from {table_name} where {videoKey_field} = {videoKey_value}; 
            """,
            table_name=VideoMetadata.tableName(),
            videoKey_field=VideoMetadata.videoKey.field,
            videoKey_value=paramVideoKey
        )
        with self._db.getConn() as conn:
            r: Cursor = conn.execute(stmt, params=videoKeyValue)
            return r.rowcount > 0

    @override
    def updateById(self, videoId: int, newVideoData: VideoInput, auditData: AuditData) -> Video: 
        if newVideoData.isNone():
            raise Exception("You cant update a record with an empty input.")

        fieldsAudit = NvSql.updateFields(VideoMetadata, inputData=auditData)
        fieldsTable = NvSql.updateFields(VideoMetadata, inputData=newVideoData)

        allFields, allFieldsOrder = NvSql.selectOder(VideoMetadata.all)
        stmt = NvSql.formatStmt(
            """
            update {table_name} 
               set {fields_table}, {fields_audit}
             where {videoId_field} = {video_id}
            returning {returning_fields};
            """, 
            table_name=VideoMetadata.tableName(),
            fields_table=fieldsTable,
            fields_audit=fieldsAudit,
            videoId_field=VideoMetadata.videoId.field,
            video_id=videoId,
            returning_fields=allFields
        )
        paramsUpdate: dict[str, object] = NvSql.parseSqlParams(stmt, inputObject=newVideoData, auditObject=auditData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))
            _ = cur.execute(stmt, params=paramsUpdate)
            result = cur.fetchone()
            conn.commit()
        return VideoMetadata.row(result)

    @override
    def delete(self, videoId: int, auditData: AuditData) -> Video: 
        auditFields = NvSql.updateFields(VideoMetadata, auditData)
        fieldsStr, fieldsOder = NvSql.selectOder(VideoMetadata.all)
        stmt = NvSql.formatStmt(
            """
            update {table_name} set {active_field} = false, {audit_fields} where {videoId_field} = {video_id_value}
            returning {fields_str};
            """,
            table_name=VideoMetadata.tableName(),
            active_field=VideoMetadata.videoIsActive.field,
            audit_fields=auditFields,
            videoId_field=VideoMetadata.videoId.field,
            video_id_value=videoId,
            fields_str=fieldsStr
        )
        paramsUpdate = NvSql.parseSqlParams(stmt, auditData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(fieldsOder))
            _ = cur.execute(stmt, params=paramsUpdate)
            result = cur.fetchone()
            conn.commit()
            return VideoMetadata.row(result)
