# TYPING
from typing import override

# PSYCOPG
from psycopg import Connection
from psycopg.cursor import Cursor

# REPOSITORY
from nvideos_web.core.entity.base.constants import VideoPermissions, VideoStatus
from nvideos_web.core.entity.subscriber import SubscriberMetadata
from nvideos_web.core.repository.video import VideoRepository

# ENTITY
from nvideos_web.core.entity.video import (
    Video, VideoInput, VideoMetadata, 
    VideosRecommended, VideosHome
)
from nvideos_web.core.entity.channel import ChannelMetadata
from nvideos_web.core.entity.user import UserMetadata
from nvideos_web.core.entity.base.base_entity import AuditData

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

# ERROR
from nvideos_web.impl.error.video import VideoIsNone

# SQL BUILDER
from nvideos_web.impl.base.sql_builder import NvSql, ParamPgMapObject

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

    def incrementVideoViewCount(self, videoKey: str) -> None: 
        pVideoKey, videoKeyParam = NvSql.createParam("videoKey", videoKey)
        stmt = NvSql.formatStmt(
            f"""
            update {VideoMetadata.tableName()} 
            set {VideoMetadata.videoViewCount.field} = {VideoMetadata.videoViewCount.field} + 1
            where {VideoMetadata.videoKey.field} = {pVideoKey};
            """
        )
        with self._db.getConn() as conn:
            cur = conn.cursor()
            _ = cur.execute(stmt, params=videoKeyParam)
            conn.commit()

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
           and {VideoMetadata.videoKey.getWithPrefix()} = {paramVideoKey};
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
        filterByStatus: str = "",
        videoPermissions: list[str] | None = None,
        conn: Connection | None = None
    ) -> list[Video]:
        vm: type[VideoMetadata] = VideoMetadata
        paramChannelId, channelIdParam = NvSql.createParam("channel_id", channelId)

        paramFilterStatus: ParamPgMapObject | None = None
        paramVideoPermissions: ParamPgMapObject | None = None

        filterStatus = ""
        filterVideoPermission = ""

        if filterByStatus:
            filterStatus, paramFilterStatus = NvSql.createParam("filter_by_status", filterByStatus)
            filterStatus = f" and {VideoMetadata.videoStatus.field} = {filterStatus} "

        if videoPermissions:
            videoPermissionParam, paramVideoPermissions = NvSql.createParam("video_permissions", videoPermissions)
            filterVideoPermission = f" and {VideoMetadata.videoPermission.field} = ANY({videoPermissionParam}) "

        allFields, allFieldsOrder = NvSql.selectOder(
            vm.videoId, vm.videoTitle, vm.videoDescription, vm.videoKey,
            vm.videoStatus, vm.videoThumbUrl, vm.videoViewCount, 
            vm.videoTimeDuration, vm.videoTags, vm.createdAt
        )

        stmt: str = NvSql.formatStmt(
            f"""
            select {allFields} from {vm.tableName()} 
            where {vm.channelId.field} = {paramChannelId}
              and {vm.videoIsActive.field} = true
            {filterStatus}
            {filterVideoPermission}
            order by {vm.createdAt.field} desc
            limit {limit} offset {offset};
            """
        )

        params = channelIdParam
        if paramFilterStatus is not None:
            params = NvSql.concatParams(params, paramFilterStatus)
        if paramVideoPermissions is not None:
            params = NvSql.concatParams(params, paramVideoPermissions)

        if conn is None:
            with self._db.getConn() as conn:
                cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))            
                r = cur.execute(stmt, params=params)
                return [ VideoMetadata.row(row) for row in r.fetchall() ]
        else:
            cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))
            r = cur.execute(stmt, params=params)
            return [ VideoMetadata.row(row) for row in r.fetchall() ]

    @override
    def selectCountAllVideoByChannelId(self, 
        channelId: int, *,
        filterByStatus: str = "",
        videoPermissions: list[str] | None = None,
        conn: Connection | None = None
    ) -> int: 
        cm = ChannelMetadata
        paramChannelId, channelIdParam = NvSql.createParam("channel_id", channelId)
        paramFilterStatus: ParamPgMapObject | None = None
        paramVideoPermissions: ParamPgMapObject | None = None
        
        filterStatus: str = ''
        filterVideoPermission: str = ''

        if videoPermissions:
            videoPermissionParam, paramVideoPermissions = NvSql.createParam("video_permissions", videoPermissions)
            filterVideoPermission = f" and {VideoMetadata.videoPermission.field} = ANY({videoPermissionParam}) "

        if filterByStatus:
            filterStatus, paramFilterStatus = NvSql.createParam("filter_by_status", filterByStatus)
            filterStatus = f" and {VideoMetadata.videoStatus.getWithPrefix()} = {filterStatus} "

        stmt: str = NvSql.formatStmt(
            f"""
            select count(1) from {VideoMetadata.tableNamePrefix()}, {cm.tableNamePrefix()}
            where {VideoMetadata.channelId.getWithPrefix()} = {paramChannelId}
              and {VideoMetadata.channelId.getWithPrefix()} = {cm.channelId.getWithPrefix()}
              and {cm.channelIsActive.getWithPrefix()} = true
              and {VideoMetadata.videoIsActive.getWithPrefix()} = true
              {filterStatus}
              {filterVideoPermission};
            """
        )

        params = channelIdParam
        if paramFilterStatus is not None:
            params = NvSql.concatParams(params, paramFilterStatus)
        if paramVideoPermissions is not None:
            params = NvSql.concatParams(params, paramVideoPermissions)

        if conn is None:
            with self._db.getConn() as conn:
                r = conn.execute(stmt, params=params)
                result = r.fetchone()
                return result[0] if result else 0
        else:
            r = conn.execute(stmt, params=params)
            result = r.fetchone()
            return result[0] if result else 0

    @override
    def selectLimitCountVideoByChannelId(self, *, 
        filterByStatus: str = "", 
        videoPermissions: list[str] | None = None,
        limit: int, channelId: int, offset: int = 0
    ) -> tuple[list[Video], int]:
        with self._db.getConn() as conn:
            resultCount = self.selectCountAllVideoByChannelId(
                channelId, 
                filterByStatus=filterByStatus,
                videoPermissions=videoPermissions, 
                conn=conn
            )
            resultVideos = self.selectLimitVideosByChannelId(
                limit, channelId,
                filterByStatus=filterByStatus,
                videoPermissions=videoPermissions,
                offset=offset, conn=conn
            )
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
        vm = VideoMetadata
        vmO = VideoMetadata.as_(newPrefix="ovm")
        ch = ChannelMetadata.as_(newPrefix="ch")
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
        pVideoKeyEx, paramVideoKeyEx = NvSql.createParam("video_key_ex", videoKey)

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
                and {vm.videoKey.getWithPrefix()} <> {pVideoKeyEx} 
                order by {vm.createdAt.getWithPrefix()} desc
                limit 10
            )

            select * from all_videos_recommended
            
            union
            
            select * from more_videos_of_channel
            
            limit 10;
            """
        )
        params = NvSql.concatParams(paramChannelId, paramVideoKey, paramVideoKeyEx)

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
    def selectLastPublicVideos(self, filter: str, *, limit: int, offset: int = 0) -> tuple[list[VideosHome], bool]:
        vm: type[VideoMetadata] = VideoMetadata
        ch: type[ChannelMetadata] = ChannelMetadata
        fields, _ = NvSql.selectOder(
            vm.videoId, vm.videoKey, vm.videoTitle, 
            vm.videoThumbUrl, vm.videoViewCount, 
            vm.videoTimeDuration, ch.channelId, 
            ch.channelName, ch.channelAvatarUrl,
            usePrefix=True, useAsinFields=True
        )

        pLimit, paramLimit = NvSql.createParam("limit", limit)
        pOffset, paramOffset = NvSql.createParam("offset", offset)
        _, paramHasMore = NvSql.createParam("offset", offset+limit)

        if filter == 'recent':
            orderBy = f" order by {vm.createdAt.getWithPrefix()} desc "
        else:
            orderBy = f" order by {vm.videoViewCount.getWithPrefix()} desc "

        stmt = NvSql.formatStmt(
            f"""
            select {fields} from {vm.tableNamePrefix()}, {ch.tableNamePrefix()}
            where {ch.channelId.getWithPrefix()} = {vm.channelId.getWithPrefix()}
            and {vm.videoPermission.getWithPrefix()} in (E'{VideoPermissions.P_PUBLIC.value}')
            {orderBy}
            limit {pLimit} offset {pOffset};
            """
        )
        params = NvSql.concatParams(paramLimit, paramOffset)
        paramsHasMore = NvSql.concatParams(paramLimit, paramHasMore)

        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(None, additionalModelFields=VideosHome))
            r = cur.execute(stmt, params=params)
            result = [ VideosHome.row(row) for row in r.fetchall() ]
            r = conn.execute(stmt, params=paramsHasMore)
            return result, r.rowcount > 0

    @override
    def selectLastSubcribedVideos(self, filter: str, userId: int, *, limit: int, offset: int = 0) -> tuple[list[VideosHome], bool]:
        sb = SubscriberMetadata
        vm = VideoMetadata
        ch = ChannelMetadata

        fields, _ = NvSql.selectOder(
            vm.videoId, vm.videoKey, vm.videoTitle, 
            vm.videoThumbUrl, vm.videoViewCount, 
            vm.videoTimeDuration, ch.channelId, 
            ch.channelName, ch.channelAvatarUrl,
            usePrefix=True, useAsinFields=True
        )

        pLimit, paramLimit = NvSql.createParam("limit", limit)
        pOffset, paramOffset = NvSql.createParam("offset", offset)
        pUserId, paramUserId = NvSql.createParam("user_id", userId)
        _, paramHasMore = NvSql.createParam("offset", offset+limit)

        if filter == 'recent':
            orderBy = f" order by {vm.createdAt.getWithPrefix()} desc "
        else:
            orderBy = f" order by {vm.videoViewCount.getWithPrefix()} desc "

        stmt = NvSql.formatStmt(
            f"""
            select {fields} from {sb.tableNamePrefix()} 
            join {ch.tableNamePrefix()} on {sb.channelId.getWithPrefix()} = {ch.channelId.getWithPrefix()}
            join {vm.tableNamePrefix()} on {vm.channelId.getWithPrefix()} = {ch.channelId.getWithPrefix()}
            where {sb.userId.getWithPrefix()} = {pUserId}
            and {sb.subscriberIsActive.getWithPrefix()} = true
            and {vm.videoPermission.getWithPrefix()} in (E'{VideoPermissions.P_SUBSCRIBER_ONLY.value}')
            {orderBy}
            limit {pLimit} offset {pOffset};
            """
        )

        params = NvSql.concatParams(paramLimit, paramOffset, paramUserId)
        paramsHasMore = NvSql.concatParams(paramLimit, paramHasMore, paramUserId)

        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(None, additionalModelFields=VideosHome))
            r = cur.execute(stmt, params=params)
            result = [ VideosHome.row(row) for row in r.fetchall() ]
            r = conn.execute(stmt, params=paramsHasMore)
            hasMore = r.rowcount > 0
            return result, hasMore

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
