import React, { useState } from 'react';
import {
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Spinner,
  Box,
  Icon,
  Text,
} from '@chakra-ui/react';
import { AiOutlineRobot } from 'react-icons/ai';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { solarizedlight } from 'react-syntax-highlighter/dist/esm/styles/prism';

const ExplainerModal = ({ question_id }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchExplanation = async () => {
    // Hardcoded session ID
    const sessionId = "d5ab82be-94d1-4923-81e2-cb085f42d477";
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/explainer', {
        session_id: sessionId,
        question_id: question_id,
      });

      setExplanation(response.data.response);
    } catch (error) {
      console.error('Error fetching explanation:', error);
      setExplanation("Failed to fetch explanation.");
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = () => {
    fetchExplanation();
    onOpen();
  };

  return (
    <>
      <Button
        onClick={handleOpen}
        colorScheme="teal"
        variant="outline"
        size="sm"
        mt={2}
        mb={2}
        leftIcon={<Icon as={AiOutlineRobot} />}
      >
        Explain
      </Button>

      <Modal isOpen={isOpen} onClose={onClose} size="lg">
        <ModalOverlay />
        <ModalContent
          maxW="90vw"
          maxH="80vh"
          borderRadius="md"
          boxShadow="lg"
          p={8}
        >
          <ModalHeader>Explanation</ModalHeader>
          <ModalCloseButton />
          <ModalBody
            p={8}
            overflowY="auto"
            maxHeight="70vh"
            fontSize="md"
            lineHeight="tall"
          >
            {loading ? (
              <Box textAlign="center" p={6}>
                <Spinner size="lg" />
              </Box>
            ) : (
              <ReactMarkdown
                components={{
                  code: ({ node, inline, className, children, ...props }) => {
                    const match = /language-(\w+)/.exec(className || '');
                    return !inline && match ? (
                      <Box
                        borderRadius="md"
                        overflow="hidden"
                        mb={4}
                        bg="gray.100"
                        p={8}
                      >
                        <SyntaxHighlighter
                          language={match[1]}
                          style={solarizedlight}
                          {...props}
                        >
                          {String(children).replace(/\n$/, '')}
                        </SyntaxHighlighter>
                      </Box>
                    ) : (
                      <Box
                        as="code"
                        bg="gray.100"
                        p={1}
                        borderRadius="md"
                        {...props}
                      >
                        {children}
                      </Box>
                    );
                  }
                }}
              >
                {explanation}
              </ReactMarkdown>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default ExplainerModal;
