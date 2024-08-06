<<<<<<< HEAD
import React, { useState } from 'react';
=======
import React, { useState, useEffect } from 'react';
>>>>>>> a24dc1c (Made some changes)
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
<<<<<<< HEAD
  ModalFooter,
=======
>>>>>>> a24dc1c (Made some changes)
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  Input,
  Box,
  VStack,
  HStack,
  Avatar,
  useDisclosure,
<<<<<<< HEAD
  Text
=======
  Text,
  keyframes,
  usePrefersReducedMotion,
>>>>>>> a24dc1c (Made some changes)
} from '@chakra-ui/react';
import { ChatIcon } from '@chakra-ui/icons';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

<<<<<<< HEAD
=======
// Define keyframes for jumping animation
const jump = keyframes`
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
`;

// Loading component for bot animation
const LoadingDots = () => {
  const prefersReducedMotion = usePrefersReducedMotion();
  const animation = prefersReducedMotion ? undefined : `${jump} 0.6s infinite`;

  return (
    <Box display="flex" alignItems="center">
      <Box as="span" mx={1} animation={animation}>
        .
      </Box>
      <Box as="span" mx={1} animation={animation} animationDelay="0.2s">
        .
      </Box>
      <Box as="span" mx={1} animation={animation} animationDelay="0.4s">
        .
      </Box>
    </Box>
  );
};

>>>>>>> a24dc1c (Made some changes)
const ChatBotModal = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
<<<<<<< HEAD
=======
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      // Send initial message when the modal is opened
      const initialMessage = 'Hello! How can I assist you today?';
      setMessages([{ text: initialMessage, isUser: false }]);
    }
  }, [isOpen]);
>>>>>>> a24dc1c (Made some changes)

  const handleSendMessage = () => {
    if (inputValue.trim() !== '') {
      setMessages([...messages, { text: inputValue, isUser: true }]);
<<<<<<< HEAD

      axios.post('http://127.0.0.1:5000/chat', { message: inputValue })
        .then(response => {
          setMessages(prev => [
            ...prev,
            { text: response.data.response, isUser: false },
          ]);
        })
        .catch(error => {
          console.error('Error:', error);
          setMessages(prev => [
            ...prev,
            { text: 'Error getting response from the server.', isUser: false },
          ]);
=======
      setIsLoading(true);

      axios
        .post('http://127.0.0.1:5000/api/chat', { message: inputValue })
        .then((response) => {
          setMessages((prev) => [
            ...prev,
            { text: response.data.response, isUser: false },
          ]);
          setIsLoading(false);
        })
        .catch((error) => {
          console.error('Error:', error);
          setMessages((prev) => [
            ...prev,
            { text: 'Error getting response from the server.', isUser: false },
          ]);
          setIsLoading(false);
>>>>>>> a24dc1c (Made some changes)
        });

      setInputValue('');
    }
  };

  return (
    <>
      <Button onClick={onOpen} leftIcon={<ChatIcon />} colorScheme="teal">
        Ask Me
      </Button>

      <Modal isOpen={isOpen} onClose={onClose} size="lg">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Ask Me</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4} align="stretch">
              <Box
                borderWidth={1}
                borderRadius="lg"
                p={4}
                height="400px"
                overflowY="auto"
                bg="gray.50"
              >
                {messages.map((message, index) => (
                  <HStack
                    key={index}
                    justify={message.isUser ? 'flex-end' : 'flex-start'}
                    mb={2}
                  >
                    {!message.isUser && (
                      <Avatar
                        name="Bot"
                        size="sm"
<<<<<<< HEAD
                        src="https://bit.ly/bot-avatar"
=======
                        src="/assets/robot.png" // Ensure this path is correct
>>>>>>> a24dc1c (Made some changes)
                      />
                    )}
                    <Box
                      bg={message.isUser ? 'teal.100' : 'gray.200'}
                      px={4}
                      py={2}
                      borderRadius="lg"
                      maxWidth="70%"
                    >
                      {message.isUser ? (
                        <Text>{message.text}</Text>
                      ) : (
                        <ReactMarkdown>{message.text}</ReactMarkdown>
                      )}
                    </Box>
                    {message.isUser && (
                      <Avatar
                        name="User"
                        size="sm"
<<<<<<< HEAD
                        src="https://bit.ly/user-avatar"
=======
                        src="/assets/user.png" 
>>>>>>> a24dc1c (Made some changes)
                      />
                    )}
                  </HStack>
                ))}
<<<<<<< HEAD
=======
                {isLoading && (
                  <HStack justify="flex-start" mb={2}>
                    <Avatar
                      name="Bot"
                      size="sm"
                      src="/assets/robot.png" 
                      animation={`${jump} 1s infinite`}
                    />
                    <Box
                      bg="gray.200"
                      px={4}
                      py={2}
                      borderRadius="lg"
                      maxWidth="70%"
                    >
                      <LoadingDots />
                    </Box>
                  </HStack>
                )}
>>>>>>> a24dc1c (Made some changes)
              </Box>
              <FormControl>
                <HStack>
                  <Input
                    placeholder="Type your question..."
                    value={inputValue}
<<<<<<< HEAD
                    onChange={e => setInputValue(e.target.value)}
                    onKeyPress={e => {
=======
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => {
>>>>>>> a24dc1c (Made some changes)
                      if (e.key === 'Enter') {
                        handleSendMessage();
                      }
                    }}
                  />
                  <Button colorScheme="teal" onClick={handleSendMessage}>
                    Send
                  </Button>
                </HStack>
              </FormControl>
            </VStack>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default ChatBotModal;
