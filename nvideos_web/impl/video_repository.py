# TYPING
from typing import override

# PSYCOPG
from psycopg import Connection
from psycopg.cursor import Cursor

# REPOSITORY
from nvideos_web.core.entity.base.constants import VideoPermissions
from nvideos_web.core.repository.video import VideoRepository

# ENTITY
from nvideos_web.core.entity.video import Video, VideoInput, VideoMetadata, VideosRecommended
from nvideos_web.core.entity.channel import ChannelMetadata
from nvideos_web.core.entity.user import UserMetadata
from nvideos_web.core.entity.base.base_entity import AuditData

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

# ERROR
from nvideos_web.impl.error.video import VideoIsNone

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
    def selectByVideoKey(self, videoKey: str, *, conn: Connection | None = None) -> Video | None:
       paramVideoKey, videoKeyParam = NvSql.createParam("videoKey", videoKey)
       videoFields, allFieldsOrder = NvSql.selectOder(VideoMetadata.all, usePrefix=True)
       stmt = NvSql.formatStmt(
           f"""
           select {videoFields} from {VideoMetadata.tableNamePrefix()}, 
           {ChannelMetadata.tableNamePrefix()},
           {UserMetadata.tableNamePrefix()}
           where {VideoMetadata.channelId.getWithPrefix()} = {ChannelMetadata.channelId.getWithPrefix()}
           and {ChannelMetadata.userId.getWithPrefix()} = {UserMetadata.userId.getWithPrefix()}
           and {VideoMetadata.videoKey.getWithPrefix()} = {paramVideoKey}
           """,
       )
       with self._db.getConn() as conn:
           cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))
           _ = cur.execute(stmt, params=videoKeyParam)
           result = cur.fetchone()
           return None if result is None else VideoMetadata.row(result)

    @override
    def selectLimitVideosByChannelId(self, limit: int, 
        channelId: int, *, offset: int = 0, 
        conn: Connection | None = None
    ) -> list[Video]:
        vm: type[VideoMetadata] = VideoMetadata
        paramChannelId, channelIdParam = NvSql.createParam("channel_id", channelId)
        allFields, allFieldsOrder = NvSql.selectOder(
            vm.videoId, vm.videoTitle, vm.videoDescription, vm.videoKey,
            vm.videoStatus, vm.videoThumbUrl, vm.videoViewCount, 
            vm.videoTimeDuration, vm.videoTags
        )

        stmt: str = NvSql.formatStmt(
            f"""
            select {allFields} from {vm.tableName()} 
            where {vm.channelId.field} = {paramChannelId}
            order by {vm.createdAt.field} desc
            limit {limit} offset {offset};
            """
        )
        if conn is None:
            with self._db.getConn() as conn:
                cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))            
                r = cur.execute(stmt, params=channelIdParam)
                return [ VideoMetadata.row(row) for row in r.fetchall() ]
        else:
            cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))
            r = cur.execute(stmt, params=channelIdParam)
            return [ VideoMetadata.row(row) for row in r.fetchall() ]

    @override
    def selectCountAllVideoByChannelId(self, 
        channelId: int, *,
        conn: Connection | None = None
    ) -> int: 
        paramChannelId, channelIdParam = NvSql.createParam("channel_id", channelId)
        stmt: str = NvSql.formatStmt(
            f"""
            select count(1) from {VideoMetadata.tableName()} 
            where {VideoMetadata.channelId.field} = {paramChannelId};
            """
        )

        if conn is None:
            with self._db.getConn() as conn:
                r = conn.execute(stmt, params=channelIdParam)
                result = r.fetchone()
                return result[0] if result else 0
        else:
            r = conn.execute(stmt, params=channelIdParam)
            result = r.fetchone()
            return result[0] if result else 0

    @override
    def selectLimitCountVideoByChannelId(self, *, limit: int, channelId: int, offset: int = 0) -> tuple[list[Video], int]:
        with self._db.getConn() as conn:
            resultCount = self.selectCountAllVideoByChannelId(channelId=channelId, conn=conn)
            resultVideos = self.selectLimitVideosByChannelId(limit=limit, channelId=channelId, offset=offset, conn=conn)
            return resultVideos, resultCount

    @override
    def selectVideoKeyByIdAndRecommended(self, videoKey: str) -> tuple[Video, list[VideosRecommended]]:
        with self._db.getConn() as conn:
            video = self.selectByVideoKey(videoKey=videoKey, conn=conn)
            
            if video is None:
                raise VideoIsNone("Video is None")

            videosRecommended = self.selectRecommendedVideos(videoKey=videoKey, channelId=video.channelId, conn=conn)
            return video, videosRecommended

    @override
    def selectRecommendedVideos(self, videoKey: str, channelId: int, *, conn: Connection | None = None) -> list[VideosRecommended]:
        vm: type[VideoMetadata] = VideoMetadata
        vmO: VideoMetadata = VideoMetadata.as_(newPrefix="ovm")
        ch: ChannelMetadata = ChannelMetadata.as_(newPrefix="ch")
        fields, _ = NvSql.selectOder(
            vm.videoId, vm.videoKey, vm.videoTitle, 
            vm.videoThumbUrl, vm.videoViewCount, vm.videoTimeDuration, vm.videoPermission, ch.channelId, ch.channelName,
            usePrefix=True,
            useAsinFields=True
        )
        fieldsOvm, _ = NvSql.selectOder(
            vmO.videoId, vmO.videoKey, vmO.videoTitle, 
            vmO.videoThumbUrl, vmO.videoViewCount, vmO.videoTimeDuration, vmO.videoPermission, ch.channelId, ch.channelName,
            usePrefix=True,
            useAsinFields=True
        )   
        pChannelId, paramChannelId = NvSql.createParam("channel_id", channelId)
        pVideoKey, paramVideoKey = NvSql.createParam("video_key", videoKey)

        stmt: str = NvSql.formatStmt(
            f"""
            with all_videos_recommended AS (
                select {fieldsOvm} 
                  from {vm.tableNamePrefix()} 
                join {vmO.tableNamePrefix()} on 
                    {vmO.videoTags.getWithPrefix()} && {vm.videoTags.getWithPrefix()} and
                    {vmO.videoId.getWithPrefix()} <> {vm.videoId.getWithPrefix()}
                join {ch.tableNamePrefix()} on {vmO.channelId.getWithPrefix()} = {ch.channelId.getWithPrefix()}
                where {vm.videoKey.getWithPrefix()} = {pVideoKey}
                  and {vmO.videoPermission.getWithPrefix()} in (E'{VideoPermissions.P_PUBLIC.value}', E'{VideoPermissions.P_SUBSCRIBER_ONLY.value}')
                order by {vmO.createdAt.getWithPrefix()} desc
                limit 10
            ),
            more_videos_of_channel as (
                select {fields} from {vm.tableNamePrefix()}, {ch.tableNamePrefix()}
                where {vm.channelId.getWithPrefix()} = {pChannelId}
                and {ch.channelId.getWithPrefix()} = {vm.channelId.getWithPrefix()}
                and (select count(1) from all_videos_recommended) < 10
                order by {vm.createdAt.getWithPrefix()} desc
                limit 10
            )

            select * from all_videos_recommended
            
            union
            
            select * from more_videos_of_channel
            
            limit 10;
            """
        )
        params = NvSql.concatParams(paramChannelId, paramVideoKey)

        if conn is None:
            with self._db.getConn() as conn:
                cur = conn.cursor(row_factory=ModelRowFactory(None, additionalModelFields=VideosRecommended))
                r = cur.execute(stmt, params=params)
                return [ VideosRecommended.row(row) for row in r.fetchall() ]
        else:
            cur = conn.cursor(row_factory=ModelRowFactory(None, additionalModelFields=VideosRecommended))
            r = cur.execute(stmt, params=params)
            return [ VideosRecommended.row(row) for row in r.fetchall() ]


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
    def updateStatusByVideoKey(self, videoKey: str, newVideoData: VideoInput, auditData: AuditData) -> Video: 
        if newVideoData.isNone():
            raise Exception("You cant update a record with an empty input.")

        fieldsAudit = NvSql.updateFields(VideoMetadata, inputData=auditData)
        fieldsTable = NvSql.updateFields(VideoMetadata, inputData=newVideoData)

        allFields, allFieldsOrder = NvSql.selectOder(VideoMetadata.all)
        
        videoKeyParam, videoKeyParamValue = NvSql.createParam("videoKeyParam", videoKey)

        stmt = NvSql.formatStmt(
            """
            update {table_name} 
               set {fields_table}, {fields_audit}
             where {videoKey_field} = {video_key}
            returning {returning_fields};
            """, 
            table_name=VideoMetadata.tableName(),
            fields_table=fieldsTable,
            fields_audit=fieldsAudit,
            videoKey_field=VideoMetadata.videoKey.field,
            video_key=videoKeyParam,
            returning_fields=allFields
        )
        paramsUpdate: dict[str, object] = NvSql.parseSqlParams(
            stmt, 
            inputObject=newVideoData, 
            auditObject=auditData,
            additionalParams=videoKeyParamValue
        )
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
