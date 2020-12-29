import unittest
from unittest.mock import patch
import cloudwanderer
from cloudwanderer import AwsUrn


@patch.dict('os.environ', {'AWS_ACCESS_KEY': '111', 'AWS_DEFAULT_REGION': 'eu-west-2'})
class TestResource(unittest.TestCase):

    @patch.dict('os.environ', {'AWS_ACCESS_KEY': '111', 'AWS_DEFAULT_REGION': 'eu-west-2'})
    def setUp(self):
        self.test_urn = AwsUrn(
            account_id='11111111111',
            region='eu-west-2',
            service='ec2',
            resource_type='vpc',
            resource_id='vpc-11111111'
        )

    def test_resource_no_attributes(self):
        resource = cloudwanderer.cloud_wanderer.CloudWandererResource(
            urn=self.test_urn,
            resource_data={'InstanceId': 'i-11111111'}
        )

        assert resource.instance_id == 'i-11111111'
        assert resource.cloudwanderer_metadata.resource_data == {'InstanceId': 'i-11111111'}
        assert resource.cloudwanderer_metadata.secondary_attributes == []

    def test_resource_with_attributes(self):
        resource = cloudwanderer.cloud_wanderer.CloudWandererResource(
            urn=self.test_urn,
            resource_data={'VpcId': 'vpc-11111111', 'CidrBlock': '10.0.0.0/8'},
            secondary_attributes=[{'VpcId': 'vpc-11111111'}]
        )

        assert resource.vpc_id == 'vpc-11111111'
        assert resource.cloudwanderer_metadata.resource_data == {'VpcId': 'vpc-11111111', 'CidrBlock': '10.0.0.0/8'}
        assert resource.cloudwanderer_metadata.secondary_attributes == [
            {'VpcId': 'vpc-11111111'}
        ]

    def test_repr(self):
        resource = cloudwanderer.cloud_wanderer.CloudWandererResource(
            urn=self.test_urn,
            resource_data={'VpcId': 'vpc-11111111', 'CidrBlock': '10.0.0.0/8'},
            secondary_attributes=[{'VpcId': 'vpc-11111111'}]
        )

        assert repr(resource) == str(
            "CloudWandererResource("
            "urn=AwsUrn(account_id='11111111111', region='eu-west-2', service='ec2', "
            "resource_type='vpc', resource_id='vpc-11111111'), "
            "resource_data={'VpcId': 'vpc-11111111', 'CidrBlock': '10.0.0.0/8'}, "
            "secondary_attributes=[{'VpcId': 'vpc-11111111'}])"
        )
