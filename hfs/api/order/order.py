# Copyright IBM Corp. 2016 All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging

import rx

from hfs.protos import ab_pb2
from hfs.protos.ab_pb2 import BroadcastMessage
from hfs.util.channel import channel

logger = logging.getLogger(__name__)


class Order(object):
    def __init__(self, target, pem=None, opts=None):
        self.stub = ab_pb2.AtomicBroadcastStub(channel(target, pem, opts))

    def sendBroadcast(self, data, timeout=30):
        logger.debug('Orderer.sendBroadcast - start')

        if data is None or data == '':
            logger.debug('Orderer.sendBroadcast ERROR - missing data')
            err = ValueError("Missing data - Nothing to order")
            return rx.Observable.just(err)

        request = BroadcastMessage(data)
        self.stub.Broadcast.future(request=request, timeout=timeout)
