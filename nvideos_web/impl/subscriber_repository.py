# TYPING
from typing import Type

# ENTITY
from nvideos_web.core.entity.base.base_entity import AuditData
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

class PgSubscriberRepository(PgRepositoryBase, SubscriberRepository):
    def __init__(self, dbContext: Type[NewVideosDBContext]) -> None:
        super().__init__(dbContext=dbContext)
    
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

    def updateById(self, subscriberId: int, newSubscriberData: SubscriberInput, auditData: AuditData) -> Subscriber:
        raise NotImplementedError()
        return super().updateById(subscriberId, newSubscriberData, auditData)

    def delete(self, subscriberId: int, auditData: AuditData) -> Subscriber:
        raise NotImplementedError()
        return super().delete(subscriberId, auditData)

    def checkIdExists(self, subscriberId: int) -> bool:
        raise NotImplementedError()
        return super().checkIdExists(subscriberId)