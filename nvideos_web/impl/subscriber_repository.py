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
        inputFields, inputParams, inputFieldsOrder = NvSql.insertFieldsOrder(SubscriberMetadata, subscriberInputData)
        auditFields, auditParams, _ = NvSql.insertFieldsOrder(SubscriberMetadata, auditInputData)
        
        userFields, userFieldsOrder = NvSql.selectOder(
            UserMetadata.userName, UserMetadata.userSurname,
            UserMetadata.userEmail, UserMetadata.userAvatarUrl,
            UserMetadata.userBirthDate,
            usePrefix=True
        )
        inputFieldsPrefix = NvSql.selectOrderToFields(inputFieldsOrder, usePrefix=True)

        selectOrderFields = inputFieldsOrder + userFieldsOrder

        stmt = NvSql.formatStmt(
            """
            insert into {table_name}
            ({input_fields},{audit_fields})
            values
            ({input_params},{audit_params});

            select {input_fields_prefix},{user_fields} 
              from {table_name_prefix},{user_table_prefix}
             where {subuser_id_prefix} = {user_id_prefix}
               and {subscriber_id_prefix} = lastval();
            """,
            table_name=SubscriberMetadata.tableName(),
            input_fields=inputFields,
            audit_fields=auditFields,

            input_params=inputParams,
            audit_params=auditParams,
            subscriber_id_field=SubscriberMetadata.subscriberId.field,
            
            input_fields_prefix=inputFieldsPrefix,
            user_fields=userFields,
            table_name_prefix=SubscriberMetadata.tableNamePrefix(),
            user_table_prefix=UserMetadata.tableNamePrefix(),
            subuser_id_prefix=SubscriberMetadata.userId.getWithPrefix(),
            user_id_prefix=UserMetadata.userId.getWithPrefix(),
            subscriber_id_prefix=SubscriberMetadata.subscriberId.getWithPrefix()
        )
        paramsExecute = NvSql.parseSqlParams(stmt, inputObject=subscriberInputData, auditObject=auditInputData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(selectOrderFields))
            cur.execute(stmt, params=paramsExecute)
            result = cur.fetchone()
            return UserSubscriber(
                user=UserMetadata.row(result),
                subscriber=SubscriberMetadata.row(result)
            )

    def updateById(self, subscriberId: int, newSubscriberData: SubscriberInput, auditData: AuditData) -> Subscriber:
        return super().updateById(subscriberId, newSubscriberData, auditData)

    def delete(self, subscriberId: int, auditData: AuditData) -> Subscriber:
        return super().delete(subscriberId, auditData)

    def checkIdExists(self, subscriberId: int) -> bool:
        return super().checkIdExists(subscriberId)