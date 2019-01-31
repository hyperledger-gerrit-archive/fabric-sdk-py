# Copyright arxanfintech.com 2016 All Rights Reserved.
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

"""
/**
 * Transaction processing in fabric v1.1 is a long operation spanning multiple
 * components (application, endorsing peer, orderer, committing peer) and takes
 * a relatively lengthy period of time (think seconds instead of milliseconds)
 * to complete. As a result the applications must design their handling of the
 * transaction lifecycle in an asynchronous fashion. After the transaction proposal
 * has been successfully [endorsed]{@link Channel#sendTransactionProposal}, and before
 * the transaction message has been successfully [sent]{@link Channel#sendTransaction}
 * to the orderer, the application should register a listener to be notified
 * when the transaction achieves finality, which is when the block
 * containing the transaction gets added to the peer's ledger/blockchain.
 * <br><br>
 * Fabric committing peers provide a block delivery service to publish blocks or
 * filtered blocks to connected fabric-clients. See [connect]{@link ChannelEventHub#connect}
 * on connection options and how this ChannelEventHub may connect to the fabric
 * service. For more information on the service see [deliver]{@link https://hyperledger-fabric.readthedocs.io/en/release-1.4/peer_event_services.html}.
 * A block gets published whenever the committing peer adds a validated block
 * to the ledger.
 * When a fabric-client receives a block it will investigate the block and notify
 * interested listeners with the related contents of the block (e.g. transactionId, status).
 * There are three types of listeners that will get notified by
 * the fabric-client after it receives a published block from the fabric deliver service.
 * <li> A "block listener" gets called for every block received. The listener
 *     will be passed a fully decoded {@link Block} object unless the connection
 *     to the fabric service is using filtered blocks.
 *     See [registerBlockEvent]{@link ChannelEventHub#registerBlockEvent}
 * <li>A "transaction listener" gets called when the specific transaction
 *     is committed (discovered inside a published block). The listener
 *     may also be registered to listen to "all" transactions.
 *     The listener will be passed the transaction id, transaction status and block number.
 *     See [registerTxEvent]{@link ChannelEventHub#registerTxEvent}
 * <li>A "chaincode event listener" gets called when a specific
 *     chaincode event is discovered within a block.
 *     The listener will be passed the block number, transaction id, and
 *     transaction status. The {@link ChaincodeEvent} will be also be passed,
 *     however the payload of the event will not be passed if
 *     the connection to the fabric service is publishing filtered blocks.
 *     See [registerChaincodeEvent]{@link ChannelEventHub#registerChaincodeEvent}
 * <br><br><br>
 * When the fabric-client connects to the peer, it tells the peer which block
 * to begin delivering from. If no start block is provided, then the client will
 * only receive events for the most recently committed block onwards.
 * To avoid missing events in blocks that are published while the client is
 * crashed/offline, the client should record the most recently processed block,
 * and resume event delivery from this block number on startup. In this way,
 * there is no custom recovery path for missed events, and the normal processing
 * code may execute instead. You may also include an endBlock number if you
 * wish to stop listening after receiving a range of events.
 *
 * @example
 * const eh = channel.newChannelEventHub(peer);
 *
 * // register the listener before calling "connect()" so there
 * // is an error callback ready to process an error in case the
 * // connect() call fails
 * eh.registerTxEvent(
 *   'all', // this listener will be notificed of all transactions
 *     (tx, status, block_num) => {
 *        record(tx, status, block_num);
 *        console.log(util.format('Transaction %s has completed', tx));
 *     },
 *     (err) => {
 *        eh.unregisterTxEvent('all');
 *        reportError(err);
 *        console.log(util.format('Error %s! Transaction listener has been ' +
 *                 'deregistered for %s', err, eh.getPeerAddr()));
 *     }
 * );
 *
 * eh.connect();
 *
 * @class
 */
"""

import logging
import sys
import traceback
from collections import Set
from datetime import datetime

from hfc.fabric.peer import Peer
from hfc.protos.common import common_pb2
from hfc.protos.orderer import ab_pb2
from hfc.protos.peer import events_pb2_grpc, transaction_pb2
from hfc.util.channel import create_grpc_channel
from hfc.util.utils import checkAndAddConfigSetting, getConfigSetting, \
    build_channel_header, current_timestamp, build_header

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

_validation_codes = {}
for key in transaction_pb2.TxValidationCode.keys():
    new_key = transaction_pb2.TxValidationCode[key]
    _validation_codes[new_key] = key

# internal use only
NO_START_STOP = 0
START_ONLY = 1
END_ONLY = 2

five_minutes_ms = 5 * 60 * 1000
# Special transaction id to indicate that the transaction listener will be
# notified of all transactions
ALL = 'all'

# Special value for block numbers
NEWEST = 'newest'


class ChannelEventHub(object):
    """
        Constructs a ChannelEventHub object

        Args:
            {Channel} channel - An instance of the Channel class were this
             ChannelEventHub will receive blocks
            {Peer} peer An instance of the Peer class this ChannelEventHub
             connects.

        Returns: {ChannelEventHub} An instance of this class
    """

    def __init__(self, channel, peer):
        _logger.debug('const ')

        # this will hold the last block number received
        self._last_block_seen = None
        self._setReplayDefaults()

        # hashtable of clients registered for chaincode events
        self._chaincodeRegistrants = {}
        # set of clients registered for block events
        self._block_registrant_count = 0
        self._blockRegistrations = {}

        self.connectCallback = None

        # registered transactional events
        self._transactionRegistrations = {}
        # grpc event client interface
        self._event_client = None
        # grpc chat streaming interface
        self._stream = None

        # fabric connection state of this ChannelEventHub
        self._connected = False
        self._connect_running = False
        self._disconnect_running = False

        # using filtered blocks
        self._filtered_stream = True

        # connect count for this instance
        self._current_stream = 0
        # reference to the channel instance holding critical context such as
        # signing identity
        if not channel:
            raise Exception('Missing required argument: channel')

        self._clientContext = channel._clientContext
        self._channel = channel
        # peer node to connect
        # reference to the peer instance holding end point information
        if not peer:
            raise Exception('Missing required argument: peer')

        self._peer = peer

    def getName(self):
        """
            Return the name of this ChannelEventHub, will be the name of the\
             associated peer.
        """
        # TODO
        return self._peer.getName()

    def getPeerAddr(self):
        """
            Return the peer url
        """
        if isinstance(self._peer, Peer):
            return self._peer._endpoint.addr

        return None

    def lastBlockNumber(self):
        """
            The block number of the last block seen

            returns {Long} The block number of the last block seen
        """
        if self._last_block_seen is None:
            raise Exception('This ChannelEventHub has not seen a block from'
                            ' the peer')

        return self._last_block_seen

    def _checkAllowRegistrations(self):
        """
            internal method to check if this ChannelEventHub is allowing new
             event listeners
            If this ChannelEventHub has been configured for a
             startBlock/endBlock of events then only one event listener is
             allowed. Once the connect has been called no new event listener
             will be allowed.
        """
        if not self._allowRegistration:
            raise Exception('This ChannelEventHub is not open to event'
                            ' listener registrations')

    def isconnected(self):
        """
            Is this ChannelEventHub connected to the fabric service?

            Returns {boolean} True if connected to the event source, false
             otherwise
        """
        return self._connected

    def set_peer_addr(self, peer_addr):
        """
            Set fabric event source (peer)

            Args:
                address (str): peer-id:peer-port
        """
        pass

    def connect(self, options, connectCallback):
        """
            Establishes a connection with the fabric peer service.

            The connection will be established asynchronously. If the connection fails to
            get established, the application will be notified via the error callbacks
            from the registerXXXEvent() methods. It is recommended that an application always
            register at least one event listener with an error callback, by calling any one of the
            [registerBlockEvent]{@link ChannelEventHub#registerBlockEvent},
            [registerTxEvent]{@link ChannelEventHub#registerTxEvent} or
            [registerChaincodeEvent]{@link ChannelEventHub#registerChaincodeEvent}
            methods, before calling connect().

        Args:
            {ConnectOptions | boolean} options - Optional. If of type boolean
                then it will be assumed to how to connect to receive full (true)
                or filtered (false) blocks.
            {functon} connectCallback - Optional. This callback will report
                completion of the connection to the peer or  will report
                any errors encountered during connection to the peer. When there
                is an error, this ChannelEventHub will be shutdown (disconnected).
                Callback function should take two parameters as (error, value).
        """

        signedEvent = None
        full_block = None

        # the following supports the users using the boolean parameter to control
        # how to connect to the fabric service for full or filtered blocks
        if isinstance(options, bool):
            full_block = options
        if options is not None and isinstance(options, dict):
            if 'signedEvent' in options:
                signedEvent = options['signedEvent']
            if 'full_block' in options:
                full_block = options['full_block']
        if signedEvent is not None:
            signedEvent = self._validateSignedEvent(signedEvent)
        if connectCallback:
            self.connectCallback = connectCallback

        _logger.debug('connect - start peerAddr:%s' % self.getPeerAddr())
        if (not self._clientContext._userContext and
                not self._clientContext._adminSigningIdentity and
                not signedEvent):
            raise Exception(
                'Error connect the ChannelEventhub to peer, either the clientContext has not been properly initialized, missing userContext or admin identity or missing signedEvent')

        if isinstance(full_block, bool):
            self._filtered_stream = not full_block
            _logger.debug(
                'connect - filtered block stream set to:%s' % self._filtered_stream)
        else:
            _logger.debug('connect - using a filtered block stream by default')

        _logger.debug('connect - signed event:%s' % bool(signedEvent))
        self._connect({'signedEvent': signedEvent})
        _logger.debug('connect - end %s' % self.getPeerAddr())

    def _connect(self, request):
        """Internal use only

            Establishes a connection with the fabric peer service

        Args:
            {InternalConnectOptions} request - internal use only, the options
             to be passed  to the internal method _connect()

        """
        force = False
        signedEvent = None

        if request:
            force = request['force']
            signedEvent = request['signedEvent']
        _logger.debug('_connect - start - %s' % datetime.utcnow())

        if self._connect_running:
            _logger.debug('_connect - connect is running')
            return
        if force and self._connected:
            _logger.debug('_connect - end - already connected')
            return
        if not self._peer:
            raise Exception('Must set peer address before connecting.')

        # clean up
        self._shutdown()

        self._connect_running = True
        self._current_stream += 1
        stream_id = self._current_stream
        _logger.debug('_connect - start stream:%s' % stream_id)

        # TODO
        def connecton_setup_timeout():
            _logger.debug('_connect - timed out after:%s',
                          self._peer._request_timeout)
            self._connect_running = False
            self._disconnect(
                Exception('Unable to connect to the fabric peer service'))

        # check on the keep alive options
        # the keep alive interval
        options = checkAndAddConfigSetting('grpc.keepalive_time_ms', 360000,
                                           self._peer._options)

        # how long should we wait for the keep alive response
        request_timeout_ms = getConfigSetting('request-timeout', 3000)
        options = checkAndAddConfigSetting('grpc.keepalive_timeout_ms',
                                           request_timeout_ms, options)
        options = checkAndAddConfigSetting(
            'grpc.http2.min_time_between_pings_ms', five_minutes_ms, options)

        _logger.debug('_connect - options %s' % options)

        # TODO second arg wait for a file path, change it
        self._channel = create_grpc_channel(self._peer._endpoint.addr,
                                            self._peer._endpoint.creds,
                                            options)
        self._event_client = events_pb2_grpc.DeliverStub(self._channel)

        if self._filtered_stream:
            self._stream = self._event_client.DeliverFiltered()
        else:
            self._stream = self._event_client.Deliver()

        # FIXME
        # self._stream.

        if signedEvent:
            self._sendSignedRegistration(signedEvent)
        else:
            self._sendRegistration()

        _logger.debug('_connect - end stream:%s' % stream_id)

    def disconnect(self):
        """
            Disconnects the ChannelEventHub from the peer event source.
            Will close all event listeners and send an Error object
            with the message "ChannelEventHub has been shutdown" to
            all listeners that provided an "onError" callback.

        """
        if self._disconnect_running:
            _logger.debug('disconnect - disconnect is running')
        else:
            self._disconnect_running = True
            self._disconnect(Exception('ChannelEventHub has been shutdown'))
            self._disconnect_running = False

    def close(self):
        """
            Disconnects the ChannelEventHub from the peer event source.
            Will close all event listeners and send an Error object
            with the message "ChannelEventHub has been shutdown" to
            all listeners that provided an "onError" callback.

        """
        self.disconnect()

    def _disconnect(self, err):
        """Internal method
            Disconnects the connection to the fabric peer service.
            Will close all event listeners and send an `Error` to
            all listeners that provided an "onError" callback.
        """
        _logger.debug('_disconnect - start -- called due to:: %s, peer:%s' % (
            str(err), self.getPeerAddr()))
        self._connected = False
        self._connect_running = False
        self._closeAllCallbacks(err)
        self._shutdown()
        self._setReplayDefaults()

        # one last thing, report to the connect callback
        if self.connectCallback:
            self.connectCallback(err,
                                 self)  # report and ourselves so user will know the source
            self.connectCallback = None

        _logger.debug('_disconnect - end -- called due to:: %s, peer:%s' % (
            str(err), self.getPeerAddr()))

    def _shutdown(self):
        """Internal method
            Closes the grpc stream and service client
        """
        if self._stream:
            _logger.debug('_shutdown - shutdown existing stream')
            self._stream.cancel()
            self._stream.end()
            self._stream = None

        if self._event_client:
            self._event_client.close()

    def _sendRegistration(self):
        """Internal method
            Builds a signed event registration
            and sends it to the peer's event hub.
        """

        # use the admin if available
        txId = self._clientContext.newTransactionID(True)
        signer = self._clientContext._getSigningIdentity(True)

        opt = {
            'identity': signer,
            'txId': txId
        }

        seekPayloadBytes = self.generateUnsignedRegistration(opt)

        sig = signer.sign(seekPayloadBytes)
        signature = bytes(sig)  # TODO, verify correct with fabric-sdk-node

        # building manually or will get protobuf errors on send
        enveloppe = {
            'signature': signature,
            'payload': seekPayloadBytes
        }

        self._stream.write(enveloppe)

    def _validateSignedEvent(self, signedEvent):
        """Internal method
            validate the signedEvent has signature and payload and return the
             signedEvent

        Args:
            {SignedEvent} signedEvent the signed event to be send to peer

        """

        method = '_validateSignedEvent'
        _logger.debug('%s - enter' % method)

        if not signedEvent['signature']:
            raise Exception('Empty signature in signed event')

        if not signedEvent['payload']:
            raise Exception('Empty payload for signed event')

        _logger.debug('%s - exit' % method)

        return {
            'signature': signedEvent.signature,
            'payload': signedEvent.payload
        }

    def _sendSignedRegistration(self, signedEvent):
        """Internal method
            Send a signed event registration to the peer's eventhub
        """

        method = '_sendSignedRegistration'
        _logger.debug('%s - enter', method)
        self._stream.write(signedEvent)

    def generateUnsignedRegistration(self, options):
        """Generate the unsigned fabric service registration, this should be
            signed by the identity's private key.
        """

        method = 'generateUnsignedRegistration'
        _logger.debug('%s - enter', method)

        if not options:
            raise Exception('%s - Missing Required Argument "options"', method)

        identity = options['identity']
        txId = options['txId']
        certificate = options['certificate']
        mspId = options['mspId']

        # either we have both identity and txId, or we have both certificate or mspId
        if identity or txId:
            if not txId:
                raise Exception(
                    '"options.txId" is required to generate unsigned fabric service registration')
            if not identity:
                raise Exception(
                    '"options.identity" is required to generate unsigned fabric service registration')

            if certificate or mspId:
                certificate = None
                mspId = None

        if certificate or mspId:
            if not certificate:
                raise Exception(
                    '"options.certificate" is required to generate unsigned fabric service registration')
            if not mspId:
                raise Exception(
                    '"options.mspId" is required to generate unsigned fabric service registration')

        if not identity:
            # TODO implement Identity and TransactionID classes
            # identity = Identity(certificate, None, mspId)
            # txId = TransactionID(identity, options['admin'] is True)
            pass

        # The behavior when a missing block is encountered
        behavior = ab_pb2.SeekInfo.SeekBehavior.BLOCK_UNTIL_READY
        # build start
        seekStart = ab_pb2.SeekPosition()
        if self._starting_block_number:
            seekSpecifiedStart = ab_pb2.SeekSpecified()
            seekSpecifiedStart.setNumber(self._starting_block_number)
            seekStart.setSpecified(seekSpecifiedStart)
        else:
            seekNewest = ab_pb2.SeekNewest()
            seekStart.setNewest(seekNewest)

        # build stop
        seekStop = ab_pb2.SeekPosition()
        if self._ending_block_newest:
            seekNewest = ab_pb2.SeekNewest()
            seekStop.setNewest(seekNewest)
            behavior = ab_pb2.SeekInfo.SeekBehavior.FAIL_IF_NOT_READY
        else:
            seekSpecifiedStop = ab_pb2.SeekSpecified()
            if self._ending_block_number:
                seekSpecifiedStop.setNumber(self._ending_block_number)
                # user should know the block does not exist
                behavior = ab_pb2.SeekInfo.SeekBehavior.FAIL_IF_NOT_READY
            else:
                seekSpecifiedStop.setNumber(sys.maxsize)
            seekStop.setSpecified(seekSpecifiedStop)

        # seek info with all parts
        seekInfo = ab_pb2.SeekInfo()
        seekInfo.setStart(seekStart)
        seekInfo.setStop(seekStop)
        # BLOCK_UNTIL_READY will mean hold the stream open and keep sending as
        # the blocks come in
        # FAIL_IF_NOT_READY will mean if the block is not there throw an error
        seekInfo.setBehavior(behavior)

        # build the header for use with the seekInfo payload
        seekInfoHeader = build_channel_header(
            common_pb2.HeaderType.DELIVER_SEEK_INFO,
            self._channel._name,
            txId.getTransactionID(),
            self._initial_epoch,
            None,
            current_timestamp(),
            self._clientContext.getClientCertHash()
        )

        seekHeader = build_header(identity, seekInfoHeader,
                                  txId.getNonce())
        seekPayload = common_pb2.Payload()
        seekPayload.setHeader(seekHeader)
        seekPayload.setData(seekInfo.decode(
            'utf-8'))  # TODO, verify correct with fabric-sdk-node
        seekPayloadBytes = seekPayload.decode(
            'utf-8')  # TODO, verify correct with fabric-sdk-node

        return seekPayloadBytes

    def _closeAllCallbacks(self, err):
        """Internal method
            Will close out all callbacks
            Sends an error to all registered event "onError" callbacks
        """

        method = '_closeAllCallbacks - %s' % self.getPeerAddr()
        _logger.debug('%s - start', method)

        _logger.debug('%s - blockOnErrors %s' % (
            method, len(self._blockRegistrations.keys())))
        for key in self._blockRegistrations:
            block_registration = self._blockRegistrations[key]
            if block_registration.onError:
                _logger.debug(
                    '%s - calling block error callback for %s' % (method, key))
                block_registration.onError(err)
            else:
                _logger.debug('%s - no block error callback to call for %s' % (
                    method, key))

        self._blockRegistrations = {}

        _logger.debug('%s - transactionOnErrors %s' % (
            method, len(self._transactionRegistrations.keys())))
        for key in self._transactionRegistrations:
            trans_reg = self._transactionRegistrations[key]
            if trans_reg.onError:
                _logger.debug(
                    '%s - calling transaction error callback for %s' % (
                        method, key))
                trans_reg.onError(err)
            else:
                _logger.debug(
                    '%s - no transaction error callback to call for %s' % (
                        method, key))

        self._transactionRegistrations = {}

        def cc_closer(key):
            cbtable = self._chaincodeRegistrants[key]
            for chaincode_reg in cbtable:
                _logger.debug(
                    '%s - closing this chaincode event ccid:%s eventNameFilter:%s' % (
                        method, chaincode_reg.ccid,
                        chaincode_reg.eventNameFilter))
                if chaincode_reg.event_reg.onError:
                    chaincode_reg.event_reg.onError(err)

        _logger.debug('%s - chaincodeRegistrants %s' % (
            method, len(self._chaincodeRegistrants.keys())))
        for key in self._chaincodeRegistrants:
            cc_closer(key)
        self._chaincodeRegistrants = {}

        _logger.debug('%s - end', method)

    def _checkReplay(self, options):
        """Internal method
            checks the startBlock/endBlock options
            checks that only one registration when using startBlock/endBlock
        """

        _logger.debug('_checkReplay - start')
        result = NO_START_STOP
        have_start_block = False
        have_end_block = False
        converted_options = {}
        if options and 'startBlock' in options:
            try:
                converted_options['start_block'] = int(options['startBlock'])
                have_start_block = True
            except Exception as error:
                raise Exception(
                    'Problem with the startBlock parameter ::%s' % error)
        if options and 'endBlock' in options:
            try:
                end_block = options['endBlock']
                if isinstance(end_block, str):
                    end_block = sys.maxsize
                    self._ending_block_newest = True

                converted_options['end_block'] = int(options['endBlock'])
                have_end_block = True
            except Exception as error:
                raise Exception(
                    'Problem with the endBlock parameter ::%s' % error)

        if (have_start_block or have_end_block) and self._haveRegistrations():
            _logger.error(
                'This ChannelEventHub is already registered with active listeners. Not able options of startBlock:%s endBlock:%s' % (
                    options.startBlock, options.endBlock))
            raise Exception(
                'Only one event registration is allowed when startBlock or endBlock are used')
        if (have_start_block or have_end_block) and (
                self._connected or self._connect_running):
            _logger.error(
                'This ChannelEventHub has already been connected to start receiving blocks. Not able to use options of startBlock:%s endBlock:%s' % (
                    options.startBlock, options.endBlock))
            raise Exception(
                'Event listeners that use startBlock or endBlock must be registered before connecting to the peer channel-based service')

        if have_end_block:
            if have_start_block and converted_options['start_block'] > \
                    converted_options['end_block']:
                raise Exception(
                    '`"startBlock" (%s) must not be larger than "endBlock" (%s})' % (
                        converted_options['start_block'],
                        converted_options['end_block']))

            self._ending_block_number = converted_options['start_block']
            self._allowRegistration = False
            resul = END_ONLY
            _logger.debug(
                '_checkReplay - Event listening will end at block %s' %
                converted_options['end_block'])

        if have_start_block:
            self._starting_block_number = converted_options['start_block']
            self._allowRegistration = False
            result += 1  # will move result to START_ONLY or START_AND_END
            _logger.debug(
                '_checkReplay - Event listening will start at block %s' %
                converted_options['start_block'])

        _logger.debug('_checkReplay - end')

        return result

    def _haveRegistrations(self):
        count = 0
        count = count + len(self._chaincodeRegistrants.keys())
        count = count + len(self._blockRegistrations.keys())
        count = count + len(self._transactionRegistrations.keys())
        return count > 0

    def _checkConnection(self):
        """internal method to check if the connection is ready and if
            not in the ready state disconnect (post an error to all registered)
            and throw and error to enform the caller
        """
        _logger.debug('_checkConnection - start')

        if self._connected or self._connect_running:
            ready = isStreamReady(self)
            _logger.debug(
                '_checkConnection - %s with stream channel ready %s' % self._peer.getUrl(),
                ready)

            if not ready and not self._connect_running:  # Not READY, but trying
                _logger.error('_checkConnection - connection is not ready')
                error = Exception('Connection is not READY')
                self._disconnect(error)
                raise error
        else:
            _logger.debug('_checkConnection - connection has not been started')

        _logger.debug('_checkConnection - end')

    def checkConnection(self, force_reconnect):
        """Returns if the stream is ready. and will attempt a restart when
         forced
        """
        _logger.debug(
            'checkConnection - start force_reconnect:%s' % force_reconnect)
        ready = isStreamReady(self)
        _logger.debug(
            'checkConnection - %s with stream channel ready %s' % self._peer.getUrl(),
            ready)

        if force_reconnect:
            try:
                if self._stream:
                    is_paused = self._stream.isPaused()
                _logger.debug(
                    'checkConnection - grpc isPaused :%s' % is_paused)
                if is_paused:
                    self._stream.resume()
                    _logger.debug('checkConnection - grpc resuming')
                elif not ready:
                    # try to reconnect
                    self._connect_running = False
                    self._connect({'force': True})
            except Exception as error:
                _logger.error(
                    'checkConnection - error :: %s' % traceback.format_exc())
                err = Exception(
                    'Problem during reconnect and the event hub is not connected ::%s' % str(
                        error))
                self._disconnect(err)

        return isStreamReady(self)

    def register_chaincode_event(self, ccid, eventname, onEvent, onError,
                                 options):
        """
            Register a listener to receive chaincode events.

            Args:
                ccid (str): Chaincode id
                eventname (str): regex filter for event name

            Returns:
                callback_index: Callback index object
        """
        _logger.debug('registerChaincodeEvent - start')

        if not ccid:
            raise Exception('Missing "ccid" parameter')
        if not eventname:
            raise Exception('Missing "eventname" parameter')
        if not onEvent:
            raise Exception('Missing "onEvent" parameter')

        self._checkAllowRegistrations()
        default_disconnect = False

        startstop_mode = self._checkReplay(options)

        if startstop_mode > START_ONLY:
            default_disconnect = True

        # TODO implement this class
        event_reg = EventRegistration(onEvent, onError, options, False,
                                      default_disconnect)

        chaincode_reg = ChaincodeRegistration(ccid, eventname, event_reg)
        cbtable = self._chaincodeRegistrants[ccid]

        if not cbtable:
            cbtable = Set()
            self._chaincodeRegistrants[ccid] = cbtable
        cbtable.add(chaincode_reg)
        if startstop_mode > NO_START_STOP:
            self._start_stop_registration = chaincode_reg.event_reg

            unregister_chaincode_event = self.unregister_chaincode_event

            def unregister_action():
                unregister_chaincode_event(chaincode_reg)

            chaincode_reg.event_reg.unregister_action = unregister_action

        self._checkConnection()

        return chaincode_reg

    def unregister_chaincode_event(self, listener_handle, raiseError=None):
        """
            Unregister the chaincode event listener represented by
            the <code>listener_handle</code> object returned by
            the registerChaincodeEvent() method
        """
        _logger.debug('unregisterChaincodeEvent - start')
        if not listener_handle:
            raise Exception('Missing "listener_handle" parameter')

        cbtable = self._chaincodeRegistrants[listener_handle.ccid]
        if not cbtable and raiseError:
            raise Exception(
                'No event registration for chaincode id %s' % listener_handle.ccid)
        elif cbtable:
            cbtable.remove(listener_handle)
            if cbtable.size <= 0:
                del self._chaincodeRegistrants[listener_handle.ccid]

    def register_block_event(self, onEvent, onError, options):
        """
            Register a listener to receive all block committed to this channel.
            The listener's "onEvent" callback gets called on the arrival of every block.

            An error may occur in the connection establishment which runs
            asynchronously. The best practice would be to provide an
            "onError" callback to be notified when this ChannelEventHub has an issue.
        """
        _logger.debug('registerBlockEvent - start')
        if not onEvent:
            raise Exception('Missing "onEvent" parameter')

        self._checkAllowRegistrations()
        default_disconnect = False
        startstop_mode = self._checkReplay(options)
        if startstop_mode > START_ONLY:
            default_disconnect = True

        block_registration_number = ++self._block_registrant_count
        block_registration = EventRegistration(onEvent, onError, options, True,
                                               default_disconnect)
        self._blockRegistrations[
            block_registration_number] = block_registration
        if startstop_mode > NO_START_STOP:
            self._start_stop_registration = block_registration

            unregister_block_event = self.unregister_block_event

            def unregister_action():
                unregister_block_event(block_registration_number)

            block_registration.unregister_action = unregister_action
        self._checkConnection()

        return block_registration_number

    def unregister_block_event(self, block_registration_number,
                               raiseError=None):
        """
            Unregister a prior block event registration.

            Args:
                Callback (function): callback function to unregister
        """
        _logger.debug(
            'unregisterBlockEvent - start  %s' % block_registration_number)
        block_reg = self._blockRegistrations[block_registration_number]
        if not block_reg and raiseError:
            raise Exception(
                'Block listener for block registration number "%s" does not exist' % block_registration_number)
        else:
            del self._blockRegistrations[block_registration_number]

    def register_tx_event(self, txid, onEvent, onError, options):
        """
            Register for transaction events.

            Args:
                txid (str): transaction id
                Callback (function): callback function to receive events
        """
        _logger.debug('registerTxEvent - start')

        if not txid:
            raise Exception('Missing "txid" parameter')
        if not isinstance(txid, str):
            raise Exception('Missing "txid" parameter')
        if not onEvent:
            raise Exception('Missing "onEvent" parameter')

        self._checkAllowRegistrations()
        default_unregister = True
        _txid = txid
        if txid.lower() == ALL:
            _txid = txid.lower()
            default_unregister = False

        temp = self._transactionRegistrations[_txid]
        if temp:
            raise Exception(
                'TransactionId (%s) has already been registered' % txid)
        default_disconnect = False
        startstop_mode = self._checkReplay(options)
        if startstop_mode > START_ONLY:
            default_disconnect = True

        trans_registration = EventRegistration(onEvent, onError, options,
                                               default_unregister,
                                               default_disconnect)
        self._transactionRegistrations[_txid] = trans_registration
        if startstop_mode > NO_START_STOP:
            self._start_stop_registration = trans_registration

            unregister_tx_event = self.unregister_tx_event

            def unregister_action():
                unregister_tx_event(_txid)

            trans_registration.unregister_action = unregister_action

        self._checkConnection()

        return _txid

    def unregister_tx_event(self, txid, raiseError=None):
        """
            Unregister a prior transaction event registration.

            Args:
                txid (str): transaction id
        """
        _logger.debug('unregisterTxEvent txid %s' % txid)
        tx_reg = self._transactionRegistrations[txid]
        if not tx_reg and raiseError:
            raise Exception(
                'Transaction listener for transaction id "%s" does not exist' % txid)
        else:
            del self._transactionRegistrations[txid]

    def _processBlockEvents(self, block):
        """
            private internal method for processing block events
        """

        if len(self._blockRegistrations.keys()) > 0:
            _logger.debug(
                '_processBlockEvents - no registered block event "listeners"')
            return

        # send to all registered block listeners
        for key in self._blockRegistrations.keys():
            block_reg = self._blockRegistrations[key]
            _logger.debug(
                '_processBlockEvents - calling block listener callback')
            block_reg.onEvent(block)

    def _processTxEvents(self, block):
        """
            private internal method for processing tx events
        """

        if len(self._transactionRegistrations.keys()) == 0:
            _logger.debug(
                '_processTxEvents - no registered transaction event "listeners"')
            return

        if block.number:
            _logger.debug(
                '_processTxEvents filtered block num=%s' % block.number)
            if block.filtered_transactions:
                for filtered_transaction in block.filtered_transactions:
                    self._checkTransactionId(filtered_transaction.txid,
                                             filtered_transaction.tx_validation_code,
                                             block.number)
        else:
            _logger.debug(
                '_processTxEvents block num=%s' % block.header.number)

            txStatusCodes = block.metadata.metadata[
                common_pb2.BlockMetadataIndex.TRANSACTIONS_FILTER]
            index = 0
            while index < block.data.data.length:
                channel_header = block.data.data[
                    index].payload.header.channel_header
                self._checkTransactionId(channel_header.tx_id,
                                         txStatusCodes[index],
                                         block.header.number)

    def _checkTransactionId(self, tx_id, val_code, block_num):
        """
            internal utility method
        """

        trans_reg = self._transactionRegistrations[tx_id]
        if trans_reg:
            self._callTransactionListener(tx_id, val_code, block_num,
                                          trans_reg)
        all_trans_reg = self._transactionRegistrations[ALL]
        if all_trans_reg:
            self._callTransactionListener(tx_id, val_code, block_num,
                                          all_trans_reg)

        if trans_reg or all_trans_reg:
            _logger.debug(
                '_callTransactionListener - no call backs found for this transaction %s' % tx_id)

    def _callTransactionListener(self, tx_id, val_code, block_num, trans_reg):
        """
            internal utility method
        """
        _logger.debug(
            '_callTransactionListener - about to call the transaction call back for code=%s tx=%s' % (
                val_code, tx_id))
        status = convertValidationCode(val_code)
        trans_reg.onEvent(tx_id, status, block_num)
        if trans_reg.unregister:
            self.unregisterTxEvent(tx_id)
            _logger.debug(
                '_callTransactionListener - automatically unregister tx listener for %s' % tx_id)
        if trans_reg.disconnect:
            _logger.debug(
                '_callTransactionListener - automatically disconnect')
            self._disconnect(Exception(
                'Shutdown due to disconnect on transaction id registration'))

    def _processChaincodeEvents(self, block):
        """
            private internal method for processing chaincode events
        """

        if len(self._chaincodeRegistrants.keys()) == 0:
            _logger.debug(
                '_processChaincodeEvents - no registered chaincode event "listeners"')
            return

        if block.number:
            if block.filtered_transactions:
                for filtered_transaction in block.filtered_transactions:
                    if filtered_transaction.transaction._actions and filtered_transaction.transaction_actions.chaincode_actions:
                        for chaincode_action in filtered_transaction.transaction_actions.chaincode_actions:
                            self._callChaincodeListener(
                                chaincode_action.chaincode_event, block.number,
                                filtered_transaction.txid,
                                filtered_transaction.tx_validation_code, True)

        else:

            index = 0
            while index < block.data.data.length:
                _logger.debug('_processTxEvents trans index=%s' % index)
                try:
                    env = block.data.data[index]
                    pload = env.payload
                    channel_header = pload.header.channel_header
                    if channel_header.type == 3:  # only ENDORSER_TRANSACTION have chaincode events
                        tx = pload.data
                        if tx and tx.actions:
                            for payload in tx.actions:
                                chaincode_event = payload.action.proposal_response_payload.extension.events
                                _logger.debug(
                                    '_processChaincodeEvents - chaincode_event %s',
                                    chaincode_event)

                                txStatusCodes = block.metadata.metadata[
                                    common_pb2.BlockMetadataIndex.TRANSACTIONS_FILTER]
                                channelHeader = block.data.data[
                                    index].payload.header.channel_header
                                val_code = txStatusCodes[index]

                                self._callChaincodeListener(chaincode_event,
                                                            block.header.number,
                                                            channelHeader.tx_id,
                                                            val_code, False)
                        else:
                            _logger.debug(
                                '_processChaincodeEvents - no transactions or transaction actions')
                    else:
                        _logger.debug(
                            '_processChaincodeEvents - block is not endorser transaction type')
                except Exception as err:
                    _logger.error(
                        'on.data - Error unmarshalling transaction= %s' % str(
                            err))

    def _callChaincodeListener(self, chaincode_event, block_num, tx_id,
                               val_code, filtered):
        """
            private internal method for processing chaincode events
        """

        _logger.debug(
            '_processChaincodeEvents - no registered chaincode event "listeners"')
        cbtable = self._chaincodeRegistrants[chaincode_event.chaincode_id]

        if not cbtable:
            _logger.debug(
                '_callChaincodeListener - no chaincode listeners found')
            return

        tx_status = convertValidationCode(val_code)
        _logger.debug('_callChaincodeListener - txid=%s  val_code=%s' % (
            tx_id, tx_status))

        for chaincode_reg in cbtable:
            if chaincode_event.event_name in chaincode_reg.eventNameFilter:
                _logger.debug(
                    '_callChaincodeListener - calling chaincode listener callback')
                if filtered:
                    # need to remove the payload since with filtered blocks it
                    # has an empty byte array value which is not the real value
                    # we do not want the listener to think that is the value
                    del chaincode_event.payload
                chaincode_reg.event_reg.onEvent(chaincode_event, block_num,
                                                tx_id,
                                                tx_status)
                if chaincode_reg.event_reg.unregister:
                    cbtable.remove(chaincode_reg)
                    _logger.debug(
                        '_callChaincodeListener - automatically unregister tx listener for %s' % tx_id)
                if chaincode_reg.event_reg.disconnect:
                    self._disconnect(Exception(
                        'Shutdown due to disconnect on transaction id registration'))
            else:
                _logger.debug(
                    '_callChaincodeListener - NOT calling chaincode listener callback')

    def _checkReplayEnd(self):
        """
            utility method to mark if this ChannelEventHub has seen the last
            in the range when this event hub is using startBlock/endBlock
        """
        if self._ending_block_number and self._ending_block_number <= self._last_block_seen:
            self._ending_block_seen = True
            if self._start_stop_registration:
                if self._start_stop_registration.unregister:
                    self._start_stop_registration.unregister_action()
                if self._start_stop_registration.disconnect:
                    self._disconnect(Exception(
                        'Shutdown due to end block number has been seen'))

    def _setReplayDefaults(self):
        """
            utility method to reset the replay state
        """

        # these will hold the block numbers to be used when this
        # event hub connects to the remote peer's channel event sevice

        self._starting_block_number = None
        self._ending_block_number = None
        self._ending_block_seen = False
        self._ending_block_newest = False
        # allow self hub to registrar new listeners
        self._allowRegistration = True
        self._start_stop_registration = None


def convertValidationCode(code):
    if isinstance(code, str):
        return code

    return _validation_codes[code];


# Utility method to check if the stream is ready.
# The stream must be readable, writeable and reading to be 'ready'
def isStreamReady(obj):
    method = 'isStreamReady'
    ready = False
    if obj._stream:
        stream = obj._stream
        ready = stream.readable and stream.writable and stream.reading
        _logger.debug('%s - stream.readable %s :: %s' % (
        method, stream.readable, obj.getPeerAddr()))
        _logger.debug('%s - stream.writable %s :: %s' % (
        method, stream.writable, obj.getPeerAddr()))
        _logger.debug('%s - stream.reading %s :: %s' % (
        method, stream.reading, obj.getPeerAddr()))
        _logger.debug('%s - stream.read_status %s :: %s' % (
        method, stream.read_status, obj.getPeerAddr()))
        _logger.debug('%s - stream.received_status %s :: %s' % (
        method, stream.received_status, obj.getPeerAddr()))

    return ready


# The ChaincodeRegistration is used internal to the ChannelEventHub to hold chaincode
# event registration callbacks.
class ChaincodeRegistration(object):

    def __init__(self, ccid, eventNameFilter, event_reg):
        self.ccid = ccid
        self.eventNameFilter = eventNameFilter
        self.event_reg = event_reg


# The EventRegistration is used internally to the ChannelEventHub to hold
# event registration callback and settings.
class EventRegistration(object):

    def __init__(self, onEvent, onError, options, default_unregister,
                 default_disconnect):
        self._onEventFn = onEvent
        self._onErrorFn = onError
        self.unregister = default_unregister
        self.disconnect = default_disconnect
        self.unregister_action = lambda x: x  # do nothing by default

        if options:
            if not options.unregister:
                _logger.debug(
                    'const-EventRegistration - unregister was not defined')
            elif isinstance(options.unregister, bool):
                self.unregister = options.unregister
            else:
                raise Exception(
                    'Event registration has invalid value for "unregister" option')

            if not options.disconnect:
                _logger.debug(
                    'const-EventRegistration - disconnect was not defined')
            elif isinstance(options.disconnect, bool):
                self.disconnect = options.disconnect
            else:
                raise Exception(
                    'Event registration has invalid value for "disconnect" option')

    def onEvent(self, *args):
        try:
            self.onEvent(*args)
        except Exception as error:
            _logger.warning(
                'Event notification callback failed %s' % str(error))

    def onError(self, *args):
        try:
            self.onError(*args)
        except Exception as error:
            _logger.warning(
                'Event notification callback failed %s' % str(error))
