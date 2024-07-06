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

class PgChannelRepository(PgRepositoryBase, SubscriberRepository):
    def __init__(self, dbContext: Type[NewVideosDBContext]) -> None:
        super().__init__(dbContext=dbContext)
    
    def create(self, subscriberInputData: SubscriberInput, auditInputData: AuditData) -> UserSubscriber:
        inputFields, inputParams, _ = NvSql.insertFieldsOrder(SubscriberMetadata, subscriberInputData)
        auditFields, auditParams, _ = NvSql.insertFieldsOrder(SubscriberMetadata, auditInputData)
        
        # userFields = NvSql.selectOder(
        #     UserMetadata.userName, UserMetadata.userSurname,
        #     UserMetadata.userEmail, UserMetadata.
        # )

        stmt = NvSql.formatStmt(
            """
            insert into {table_name}
            ({input_fields},{audit_fields})
            values
            ({input_params},{audit_params})
            returning {subscriber_id_field} as row_id;

            select {input_fields},{user_fields} 
              from {table_name_prefix},{user_table_prefix}
             where {subuser_id_prefix} = {user_id_prefix};
            """,

        )