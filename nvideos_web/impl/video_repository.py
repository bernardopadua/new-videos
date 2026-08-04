# TYPING
from typing import override

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
            cur = conn.cursor(row_factory=ModelRowFactory.getRowFactory(allFieldsOrder))
            cur.execute(stmt, params=paramsInsert)
            result = cur.fetchone()
            conn.commit()
            return VideoMetadata.row(result)

    @override
    def checkIdExists(self, videoId: int) -> bool: 
        pass

    @override
    def updateById(self, videoId: int, newVideoData: VideoInput, auditData: AuditData) -> Video: 
        pass

    @override
    def delete(self, videoId: int, auditData: AuditData) -> Video: 
        pass
