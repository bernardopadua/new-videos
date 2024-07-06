import unittest

from nvideos_web.core.entity.base.base_entity import ModelField, ModelFieldKeyWord

from nvideos_web.core.entity.user import UserMetadata
from nvideos_web.core.entity.channel import ChannelMetadata

class TestEntities(unittest.TestCase):
    # -------------------- Asserting classes    
    def test_userMetadataFieldsOwner(self):
        for k in dir(UserMetadata):
            attr = getattr(UserMetadata, k)
            if isinstance(attr, ModelField) or isinstance(attr, ModelFieldKeyWord):
                self.assertEquals(attr.owner, UserMetadata)
            
    def test_channelMetadataFieldsOwner(self):
        isOwnerOk = True
        for k in dir(ChannelMetadata):
            attr = getattr(ChannelMetadata, k)
            if isinstance(attr, ModelField) or isinstance(attr, ModelFieldKeyWord):
                self.assertEquals(attr.owner, ChannelMetadata)


    # -------------------- Asserting instances
    def test_userMetadataInstanceOwnerOk(self):
        isOwnerOk = True
        instanceUser = UserMetadata(newPrefix="tst")

        for k in dir(instanceUser):
            attr = getattr(instanceUser, k)
            if (isinstance(attr, ModelField) or 
                isinstance(attr, ModelFieldKeyWord)) \
                and attr.owner != instanceUser:
                isOwnerOk = False
                break
        
        self.assertTrue(isOwnerOk)
    
    def test_channelMetadataInstanceOwnerOk(self):
        isOwnerOk = True
        instanceUser = ChannelMetadata(newPrefix="tst")

        for k in dir(instanceUser):
            attr = getattr(instanceUser, k)
            if (isinstance(attr, ModelField) or 
                isinstance(attr, ModelFieldKeyWord)) \
                and attr.owner != instanceUser:
                isOwnerOk = False
                break
        
        self.assertTrue(isOwnerOk)

def suite_entities_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestEntities("test_userMetadataFieldsOwner"))
    suite.addTest(TestEntities("test_channelMetadataFieldsOwner"))
    suite.addTest(TestEntities("test_userMetadataInstanceOwnerOk"))
    suite.addTest(TestEntities("test_channelMetadataInstanceOwnerOk"))
    return suite