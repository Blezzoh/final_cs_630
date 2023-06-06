# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import badges_pb2 as badges__pb2


class BadgeServiceStub(object):
    """badge service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MigrateData = channel.unary_unary(
                '/badge.BadgeService/MigrateData',
                request_serializer=badges__pb2.MigrationRequest.SerializeToString,
                response_deserializer=badges__pb2.MigrationReply.FromString,
                )
        self.GetBadges = channel.unary_unary(
                '/badge.BadgeService/GetBadges',
                request_serializer=badges__pb2.BadgeRequest.SerializeToString,
                response_deserializer=badges__pb2.Badges.FromString,
                )
        self.GetBadgesMysql = channel.unary_unary(
                '/badge.BadgeService/GetBadgesMysql',
                request_serializer=badges__pb2.Connection.SerializeToString,
                response_deserializer=badges__pb2.Badges.FromString,
                )
        self.GetStreamBadge = channel.unary_stream(
                '/badge.BadgeService/GetStreamBadge',
                request_serializer=badges__pb2.BadgeRequest.SerializeToString,
                response_deserializer=badges__pb2.Badge.FromString,
                )
        self.GetStreamBadgeMysql = channel.unary_stream(
                '/badge.BadgeService/GetStreamBadgeMysql',
                request_serializer=badges__pb2.Connection.SerializeToString,
                response_deserializer=badges__pb2.Badge.FromString,
                )


class BadgeServiceServicer(object):
    """badge service definition
    """

    def MigrateData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBadges(self, request, context):
        """get all badges as a list
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBadgesMysql(self, request, context):
        """get all badges as a list from mysql table
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStreamBadge(self, request, context):
        """get all badges in a stream
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStreamBadgeMysql(self, request, context):
        """get all badges in a stream from mysql table
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BadgeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MigrateData': grpc.unary_unary_rpc_method_handler(
                    servicer.MigrateData,
                    request_deserializer=badges__pb2.MigrationRequest.FromString,
                    response_serializer=badges__pb2.MigrationReply.SerializeToString,
            ),
            'GetBadges': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBadges,
                    request_deserializer=badges__pb2.BadgeRequest.FromString,
                    response_serializer=badges__pb2.Badges.SerializeToString,
            ),
            'GetBadgesMysql': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBadgesMysql,
                    request_deserializer=badges__pb2.Connection.FromString,
                    response_serializer=badges__pb2.Badges.SerializeToString,
            ),
            'GetStreamBadge': grpc.unary_stream_rpc_method_handler(
                    servicer.GetStreamBadge,
                    request_deserializer=badges__pb2.BadgeRequest.FromString,
                    response_serializer=badges__pb2.Badge.SerializeToString,
            ),
            'GetStreamBadgeMysql': grpc.unary_stream_rpc_method_handler(
                    servicer.GetStreamBadgeMysql,
                    request_deserializer=badges__pb2.Connection.FromString,
                    response_serializer=badges__pb2.Badge.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'badge.BadgeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BadgeService(object):
    """badge service definition
    """

    @staticmethod
    def MigrateData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/badge.BadgeService/MigrateData',
            badges__pb2.MigrationRequest.SerializeToString,
            badges__pb2.MigrationReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBadges(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/badge.BadgeService/GetBadges',
            badges__pb2.BadgeRequest.SerializeToString,
            badges__pb2.Badges.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBadgesMysql(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/badge.BadgeService/GetBadgesMysql',
            badges__pb2.Connection.SerializeToString,
            badges__pb2.Badges.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStreamBadge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/badge.BadgeService/GetStreamBadge',
            badges__pb2.BadgeRequest.SerializeToString,
            badges__pb2.Badge.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStreamBadgeMysql(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/badge.BadgeService/GetStreamBadgeMysql',
            badges__pb2.Connection.SerializeToString,
            badges__pb2.Badge.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
