import { onUnmounted, ref } from 'vue';

const useWebSocket = (url, options = {}) => {
  const reconnectTimeoutId = ref(null);

  const {
    onOpen = () => console.log('✅ WebSocket connected'),
    onMessage = () => {},
    onError = (error) => console.error('❌ WebSocket error:', error),
    onClose = (event) => console.info('🔌 WebSocket disconnected:', event.reason),
    maxRetries = 5,
    reconnectDelay = 3000,
    binaryType,
  } = options;

  const socketRef = ref(null);
  const isLoading = ref(false);
  const isError = ref(false);
  let retryCount = 0;

  const connect = () => {
    isLoading.value = true;

    try {
      const socket = new WebSocket(url);
      if (binaryType) {
        socket.binaryType = 'arraybuffer';
      }
      socketRef.value = socket;

      socket.onopen = () => {
        isError.value = false;
        console.log('🔗 WebSocket connection established');
        retryCount = 0;
        onOpen();
      };

      socket.onmessage = async (event) => {
        let data;

        try {
          if (typeof event.data === 'string') {
            data = JSON.parse(event.data);
          } else if (event.data instanceof ArrayBuffer) {
            data = new DataView(event.data);
          } else if (event.data instanceof Blob) {
            const arrayBuffer = await event.data.arrayBuffer();
            data = new DataView(arrayBuffer);
          } else {
            // noinspection ExceptionCaughtLocallyJS
            throw new Error('Unsupported WebSocket message type.');
          }

          onMessage(data);
        } catch (parseError) {
          isError.value = true;
          console.error('❌ Error parsing WebSocket message:', parseError);
        }
      };

      socket.onerror = (error) => {
        isError.value = true;
        onError(error);
      };

      socket.onclose = (event) => {
        onClose(event);
        if (!event.wasClean && retryCount < maxRetries) {
          isError.value = true;
          console.warn(
            `⚠️ WebSocket closed unexpectedly. Retrying in ${reconnectDelay / 1000} seconds...`
          );
          retryCount += 1;
          reconnectTimeoutId.value = setTimeout(connect, reconnectDelay);
        } else if (retryCount >= maxRetries) {
          isError.value = true;
          console.error('❌ WebSocket reconnection failed. Max retries reached.');
        }
      };
    } catch (error) {
      isError.value = true;
      console.error('❌ Error initializing WebSocket:', error);
    } finally {
      isLoading.value = false;
    }
  };

  const sendMessage = (message) => {
    if (socketRef.value && socketRef.value.readyState === WebSocket.OPEN) {
      socketRef.value.send(JSON.stringify(message));
      // console.log('📤 Message sent:', message);
    } else {
      isError.value = true;
      console.warn('⚠️ WebSocket is not open. Message not sent:', message);
    }
  };

  const close = () => {
    if (socketRef.value) {
      isError.value = false;
      socketRef.value.close();
      console.log('🔌 WebSocket connection closed');
    }
  };

  connect();

  onUnmounted(() => {
    clearTimeout(reconnectTimeoutId);
  });

  return {
    socket: socketRef,
    isLoading,
    isError,
    sendMessage,
    close,
  };
};

export default useWebSocket;
