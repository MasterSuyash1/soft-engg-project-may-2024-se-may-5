import React, { useState, useEffect } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
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
  Text,
  keyframes,
  usePrefersReducedMotion,
} from '@chakra-ui/react';
import { FaRobot } from 'react-icons/fa';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { solarizedDarkAtom, solarizedlight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrophone, faStop } from '@fortawesome/free-solid-svg-icons';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { useColorModeValue } from '@chakra-ui/react';

// Define keyframes for jumping animation
const jump = keyframes`
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
`;

// Define keyframes for microphone animation
const micPulse = keyframes`
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
`;

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

const ChatBotModal = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const { transcript, resetTranscript, listening } = useSpeechRecognition();

  useEffect(() => {
    if (isOpen) {
      const initialMessage = 'Hello! How can I assist you today?';
      setMessages([{ text: initialMessage, isUser: false }]);
    }
  }, [isOpen]);

  useEffect(() => {
    if (transcript) {
      setInputValue(transcript);
    }
  }, [transcript]);

  const handleSendMessage = () => {
    if (inputValue.trim() !== '') {
      setMessages([...messages, { text: inputValue, isUser: true }]);
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
        });

      setInputValue('');
      resetTranscript();
    }
  };

  const handleVoiceInput = () => {
    if (SpeechRecognition.browserSupportsSpeechRecognition()) {
      if (!listening) {
        SpeechRecognition.startListening();
        setIsListening(true);
      } else {
        SpeechRecognition.stopListening();
        setIsListening(false);
        handleSendMessage();
      }
    } else {
      alert('Speech Recognition is not supported in this browser.');
    }
  };

  return (
    <>
      <Button onClick={onOpen} leftIcon={<FaRobot />} colorScheme="teal">
        Ask Me
      </Button>

      <Modal isOpen={isOpen} onClose={onClose} size="4xl"> 
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Ask Me</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={5} align="stretch">
              <Box
                borderWidth={2}
                borderRadius="lg"
                p={4}
                height="450px"
                width="100%"  
                overflowY="auto"
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
                        src="/assets/robot.png"
                      />
                    )}
                    <Box
                      bg={message.isUser ? 'teal.100' : 'gray.200'}
                      px={8}
                      py={2}
                      borderRadius="lg"
                      maxWidth={message.isUser ? "85%" : "90%"} 
                      wordBreak="break-word"
                    >
                      {message.isUser ? (
                        <Text >{message.text}</Text>
                      ) : (
                        <ReactMarkdown
                          components={{
                            code({ node, inline, className, children, ...props }) {
                              const match = /language-(\w+)/.exec(className || '');
                              return !inline && match ? (
                                <SyntaxHighlighter
                                  children={String(children).replace(/\n$/, '')}
                                  style={solarizedlight}
                                  language={match[1]}
                                  PreTag="div"
                                  {...props}
                                />
                              ) : (
                                <code className={className} {...props}>
                                  {children}
                                </code>
                              );
                            },
                          }}
                        >
                          {message.text}
                        </ReactMarkdown>
                      )}
                    </Box>
                    {message.isUser && (
                      <Avatar
                        name="User"
                        size="sm"
                        src="/assets/user.png"
                      />
                    )}
                  </HStack>
                ))}
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
                      maxWidth="100%"
                    >
                      <LoadingDots />
                    </Box>
                  </HStack>
                )}
              </Box>
              <FormControl>
                <HStack>
                  <Input
                    placeholder="Type your question..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        handleSendMessage();
                      }
                    }}
                  />
                  <Button colorScheme="teal" onClick={handleSendMessage}>
                    Send
                  </Button>
                  <Button
                    colorScheme={isListening ? 'red' : 'blue'}
                    onClick={handleVoiceInput}
                    leftIcon={
                      <FontAwesomeIcon
                        icon={isListening ? faStop : faMicrophone}
                        style={{
                          animation: isListening ? `${micPulse} 0.6s infinite` : 'none'
                        }}
                      />
                    }
                  >
                    {isListening ? 'Stop' : 'Speak'}
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
