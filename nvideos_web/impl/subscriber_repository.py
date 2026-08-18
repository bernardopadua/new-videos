# TYPING
from tarfile import StreamError
from typing import override

# ENTITY
from nvideos_web.core.entity.base.base_entity import AuditData
from nvideos_web.core.entity.channel import ChannelMetadata, Channel
from nvideos_web.core.entity.subscriber import Subscriber, SubscriberInput, SubscriberMetadata
from nvideos_web.core.entity.user import UserMetadata

# DB
from nvideos_web.core.entity.user_subscriber import UserSubscriber
from nvideos_web.db.pgcontext import NewVideosDBContext

# SQL BUILDER
from nvideos_web.impl.base.sql_builder import NvSql

# REPOSITORY
from nvideos_web.core.repository.subscriber import SubscriberRepository

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

# ERROR
from nvideos_web.impl.error.subscriber import SubscriberNoInputData

class PgSubscriberRepository(PgRepositoryBase, SubscriberRepository):
    def __init__(self, dbContext: type[NewVideosDBContext]) -> None:
        super().__init__(dbContext=dbContext)
    
    @override
    def selectTotalSubscribers(self, channelId: int) -> int:
        sm = SubscriberMetadata
        channelIdSqlParam, channelIdParamObj = NvSql.createParam("channel_id", channelId)
        stmt = NvSql.formatStmt(
            f"""
            select 1 
              from {sm.tableName()} 
             where {sm.channelId.field} = {channelIdSqlParam}
               and {sm.subscriberIsActive.field} = true;
            """
        )
        with self._db.getConn() as conn:
            cur = conn.cursor()
            result = cur.execute(stmt, params=channelIdParamObj)
            return result.rowcount

    @override
    def selectByChannelIdAndUserId(self, channelId: int, userId: int) -> Subscriber | None:
        sm: type[SubscriberMetadata] = SubscriberMetadata
        channelIdSqlParam, channelIdParamObj = NvSql.createParam("channel_id", channelId)
        userIdSqlParam, userIdParamObj = NvSql.createParam("user_id", userId)

        _, returningSubscriber = NvSql.selectOder(sm.all)

        stmt = NvSql.formatStmt(
            f"""
            select * from {sm.tableName()}
            where {sm.channelId.field} = {channelIdSqlParam}
              and {sm.userId.field} = {userIdSqlParam}
            limit 1;
            """
        )
        params = NvSql.concatParams(channelIdParamObj, userIdParamObj)

        with self._db.getConn() as conn:
            with conn.cursor(row_factory=ModelRowFactory(returningSubscriber)) as cur:
                result = cur.execute(stmt, params=params)
                row = result.fetchone()
                return sm.row(row) if row is not None else None

    @override
    def selectChannelsIdsUserIsSubscribed(self, userId: int) -> list[int]:
        sb = SubscriberMetadata
        
        userIdSqlParam, userIdParamObj = NvSql.createParam("user_id", userId)

        stmt = NvSql.formatStmt(
            f"""
            select {sb.channelId.field} from {sb.tableName()} 
            where {sb.userId.field} = {userIdSqlParam}
              and {sb.subscriberIsActive.field} = true;
            """
        )
        with self._db.getConn() as conn:
            results = conn.execute(stmt, params=userIdParamObj)
            return [ result[0] for result in results.fetchall() ]

    @override
    def selectChannelsUserIsSubscribed(self, userId: int) -> list[Channel] | None:
        sb = SubscriberMetadata
        cc = ChannelMetadata
        userIdSqlParam, userIdParamObj = NvSql.createParam("user_id", userId)
        fieldsCommaSeparated, returningChannel = NvSql.selectOder(
            cc.channelId, cc.channelName, cc.channelAvatarUrl,
            usePrefix=True
        )

        stmt = NvSql.formatStmt(
            f"""
            select {fieldsCommaSeparated} 
              from {sb.tableNamePrefix()} 
              join {cc.tableNamePrefix()} on {sb.channelId.getWithPrefix()} = {cc.channelId.getWithPrefix()}
             where {sb.userId.getWithPrefix()} = {userIdSqlParam}
               and {sb.subscriberIsActive.getWithPrefix()} = true;
            """
        )
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(returningChannel))
            cur.execute(stmt, params=userIdParamObj)
            result = cur.fetchall()
            return [cc.row(row) for row in result] if result else None

    @override
    def create(self, subscriberInputData: SubscriberInput, auditInputData: AuditData) -> UserSubscriber:
        inputFields, inputParams, _ = NvSql.insertFieldsOrder(SubscriberMetadata, subscriberInputData)
        auditFields, auditParams, _ = NvSql.insertFieldsOrder(SubscriberMetadata, auditInputData)
        _, returningSubscriber = NvSql.selectOder(SubscriberMetadata.all)

        stmt = NvSql.formatStmt(
            """
            insert into {table_name}
            ({input_fields},{audit_fields})
            values
            ({input_params},{audit_params})
            returning *;
            """,
            table_name=SubscriberMetadata.tableName(),
            input_fields=inputFields,
            audit_fields=auditFields,

            input_params=inputParams,
            audit_params=auditParams
        )
        paramsExecute = NvSql.parseSqlParams(stmt, inputObject=subscriberInputData, auditObject=auditInputData)

        userFields, userFieldsOrder = NvSql.selectOder(
            UserMetadata.userName, UserMetadata.userSurname,
            UserMetadata.userEmail, UserMetadata.userAvatarUrl,
            UserMetadata.userBirthDate
        )
        stmt2 = NvSql.formatStmt(
            """
            select {user_fields} 
              from {user_table}
             where {user_id_field} = {user_id_value};
            """,
            user_fields=userFields,
            user_table=UserMetadata.tableName(),
            user_id_field=UserMetadata.userId.field,
            user_id_value="%(userId)s"
        )

        with self._db.getConn() as conn:
            with conn.cursor(row_factory=ModelRowFactory(returningSubscriber)) as cur:
                cur.execute(stmt, params=paramsExecute)
                resSub = cur.fetchone()
                usuSub = SubscriberMetadata.row(resSub)
            with conn.cursor(row_factory=ModelRowFactory(userFieldsOrder)) as cur:
                param = { "userId": usuSub.userId }
                cur.execute(stmt2, params=param)
                resUsu = cur.fetchone()
                usu = UserMetadata.row(resUsu)
            conn.commit()
            return UserSubscriber(
                user=usu,
                subscriber=usuSub
            )

    @override
    def updateById(self, subscriberId: int, newSubscriberData: SubscriberInput, auditData: AuditData) -> Subscriber:
        if newSubscriberData.isNone():
            raise SubscriberNoInputData("No input data informed for the subscriber update.")
        
        sm: type[SubscriberMetadata] = SubscriberMetadata
        inputFields = NvSql.updateFields(SubscriberMetadata, newSubscriberData)
        auditFields = NvSql.updateFields(SubscriberMetadata, auditData)

        subscriberIdSqlParam, subscriberIdParamObj = NvSql.createParam("subscriber_id", subscriberId)

        _, returningSubscriber = NvSql.selectOder(sm.all)

        stmt = NvSql.formatStmt(
            f"""
            update {sm.tableName()}
               set {inputFields}, {auditFields}
             where {sm.subscriberId.field} = {subscriberIdSqlParam}
            returning *;
            """
        )

        paramsExecute = NvSql.parseSqlParams(stmt, inputObject=newSubscriberData, auditObject=auditData)
        param = NvSql.concatParams(subscriberIdParamObj, paramsExecute)

        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(returningSubscriber))
            result = cur.execute(stmt, params=param)
            conn.commit()
            return sm.row(result.fetchone())

    @override
    def delete(self, subscriberId: int, auditData: AuditData) -> Subscriber:
        sb: type[SubscriberMetadata] = SubscriberMetadata
        
        _, returningSubscriber = NvSql.selectOder(sb.all)
        
        subscriberIdSqlParam, subscriberIdParamObj = NvSql.createParam("subscriber_id", subscriberId)

        stmt = NvSql.formatStmt(
            f"""
            update {sb.tableName()}
               set {sb.subscriberIsActive.field} = false
             where {sb.subscriberId.field} = {subscriberIdSqlParam}
            returning *;
            """
        )
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(returningSubscriber))
            result = cur.execute(stmt, params=subscriberIdParamObj)
            conn.commit()
            return sb.row(result.fetchone())

    @override
    def checkIdExists(self, subscriberId: int) -> bool:
        raise NotImplementedError()
        return super().checkIdExists(subscriberId)

    @override
    def checkAlreadySubscribed(self, channelId: int, userId: int) -> bool:
        sm: type[SubscriberMetadata] = SubscriberMetadata

        channelIdSqlParam, channelIdParamObj = NvSql.createParam("channel_id", channelId)
        userIdSqlParam, userIdParamObj = NvSql.createParam("user_id", userId)

        stmt = NvSql.formatStmt(
            f"""
            select 1 from {sm.tableName()} 
            where {sm.channelId.field} = {channelIdSqlParam}
              and {sm.userId.field} = {userIdSqlParam}
              and {sm.subscriberIsActive.field} = true;
            """
        )
        param = NvSql.concatParams(channelIdParamObj, userIdParamObj)
        with self._db.getConn() as conn:
            result = conn.execute(stmt, params=param)
            return result.rowcount > 0

