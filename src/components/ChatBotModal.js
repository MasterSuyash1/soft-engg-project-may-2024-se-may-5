import React, { useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
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
  Text
} from '@chakra-ui/react';
import { ChatIcon } from '@chakra-ui/icons';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const ChatBotModal = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleSendMessage = () => {
    if (inputValue.trim() !== '') {
      setMessages([...messages, { text: inputValue, isUser: true }]);

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
                        src="https://bit.ly/bot-avatar"
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
                        src="https://bit.ly/user-avatar"
                      />
                    )}
                  </HStack>
                ))}
              </Box>
              <FormControl>
                <HStack>
                  <Input
                    placeholder="Type your question..."
                    value={inputValue}
                    onChange={e => setInputValue(e.target.value)}
                    onKeyPress={e => {
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
