# BUILT-IN
from typing import override

# ENTITY
from nvideos_web.core.entity.comment import (
    Comment, CommentInput, CommentList, CommentMetadata
)
from nvideos_web.core.entity.base.base_entity import AuditData
from nvideos_web.core.entity.video import VideoMetadata
from nvideos_web.core.entity.user import UserMetadata

# SQL BUILDER
from nvideos_web.impl.base.sql_builder import NvSql

# REPOSITORY
from nvideos_web.core.repository.comment import CommentRepository

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

class PgCommentRepository(PgRepositoryBase, CommentRepository):
    @override
    def selectByVideoKey(self, videoKey: str) -> list[CommentList]:
        cm = CommentMetadata
        vm = VideoMetadata
        us = UserMetadata

        videoKeySqlParam, videoKeyParam = NvSql.createParam("video_key", videoKey)
        commentFieldsCommaStr, _ = NvSql.selectOder(
            cm.commentId,
            cm.commentDescription,
            cm.createdAt,
            us.userName,
            us.userAvatarUrl,
            usePrefix=True, useAsinFields=True
        )

        stmt = NvSql.formatStmt(
            f"""
            select {commentFieldsCommaStr}, 
                (select count(1) 
                   from {cm.tableName()} 
                  where {cm.commentCommentId.field} = {cm.commentId.getWithPrefix()}
                ) as "totalRecomments"
             from {cm.tableNamePrefix()}, {vm.tableNamePrefix()}, {us.tableNamePrefix()}
            where {vm.videoKey.getWithPrefix()} = {videoKeySqlParam}
              and {vm.userId.getWithPrefix()} = {us.userId.getWithPrefix()}
              and {vm.videoId.getWithPrefix()} = {cm.videoId.getWithPrefix()}
              and {cm.commentCommentId.getWithPrefix()} is null
              order by {cm.createdAt.getWithPrefix()} desc;
            """
        )
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(None, additionalModelFields=CommentList))
            r = cur.execute(stmt, params=videoKeyParam)
            result = r.fetchall()
            return [CommentList.row(row) for row in result]

    @override
    def selectChildCommentsByParentCommentId(self, parentCommentId: int) -> list[CommentList]:
        cm = CommentMetadata
        us = UserMetadata

        paramSqlCommentId, commentIdParam = NvSql.createParam("comment_comment_id", parentCommentId)
        commentFieldsCommaStr, _ = NvSql.selectOder(
            cm.commentId,
            cm.commentDescription,
            cm.createdAt,
            us.userName,
            us.userAvatarUrl,
            usePrefix=True, useAsinFields=True
        )

        stmt = NvSql.formatStmt(
            f"""
            select {commentFieldsCommaStr},
                (select count(1) 
                   from {cm.tableName()}
                  where {cm.commentCommentId.field} = {cm.commentId.getWithPrefix()}
                ) as "totalRecomments"
              from {cm.tableNamePrefix()}, {us.tableNamePrefix()}
             where {cm.commentCommentId.getWithPrefix()} = {paramSqlCommentId}
               and {cm.userId.getWithPrefix()} = {us.userId.getWithPrefix()}
               order by {cm.createdAt.getWithPrefix()} desc;
            """
        )
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(None, additionalModelFields=CommentList))
            r = cur.execute(stmt, params=commentIdParam)
            result = r.fetchall()
            return [CommentList.row(row) for row in result]

    @override
    def selectById(self, commentId: int) -> Comment | None:
        ...
    @override
    def create(self, commentInputData: CommentInput, auditInputData: AuditData) -> Comment: 
        ...
    @override
    def checkIdExists(self, commentId: int) -> bool: 
        ...
    @override
    def updateById(self, commentId: int, newCommentData: CommentInput, auditData: AuditData) -> Comment: 
        ...
    @override
    def delete(self, commentId: int, auditData: AuditData) -> Comment: 
        ...