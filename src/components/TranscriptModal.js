import React, { useEffect, useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  Text,
  Spinner,
  Alert,
  AlertIcon,
  Box,
  Flex,
  VStack,
  useDisclosure,
  Icon,
} from '@chakra-ui/react';
import { FaFileAlt } from 'react-icons/fa';
import axios from 'axios';

const TranscriptModal = ({ lessonId }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [transcriptData, setTranscriptData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen && lessonId) {
      fetchTranscript();
    }
  }, [isOpen, lessonId]);

  const fetchTranscript = async () => {
    setLoading(true);
    setError(null);
    setTranscriptData(null);

    try {
      console.log(`Fetching transcript for lessonId: ${lessonId}`);
      const response = await axios.get(`http://127.0.0.1:5000/api/transcript_notes/${lessonId}`);
      setTranscriptData(response.data);
    } catch (err) {
      console.error("Error fetching transcript:", err);
      setError('Failed to fetch transcript data');
    } finally {
      setLoading(false);
    }
  };

  const renderTranscriptLine = (line) => {
    const timestampMatch = line.match(/^(\d{1,2}:\d{2})(:)(.*)/);

    if (timestampMatch) {
      const timestamp = timestampMatch[1];
      const text = timestampMatch[3].trim();

      return (
        <Flex
          key={timestamp}
          mb={4}
          p={4}
          bgGradient="linear(to-r, teal.50, teal.100)"
          borderRadius="md"
          borderWidth="1px"
          borderColor="teal.200"
          boxShadow="md"
          alignItems="center"
          transition="background 0.3s"
          _hover={{ bgGradient: "linear(to-r, teal.100, teal.200)" }}
        >
          <Text flex="0 0 100px" fontWeight="bold" fontSize="lg" color="teal.600" mr={5}>
            {timestamp}:
          </Text>
          <Text flex="1" whiteSpace="pre-line" color="gray.800" fontSize="lg">
            {text}
          </Text>
        </Flex>
      );
    } else {
      return (
        <Text flex="1" whiteSpace="pre-line" ml="120px" fontSize="lg">
          {line}
        </Text>
      );
    }
  };

  return (
    <>
      <Button
        leftIcon={<Icon as={FaFileAlt} />}
        colorScheme="teal"
        onClick={onOpen}
        boxShadow="md"
        _hover={{ boxShadow: "lg" }}
        size="md"
      >
        Transcript
      </Button>

      <Modal isOpen={isOpen} onClose={onClose} size="3xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader fontSize="3xl" fontWeight="bold" color="teal.700">Video Transcript and Notes</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {loading ? (
              <VStack spacing={5} align="center">
                <Spinner size="xl" color="teal.500" />
                <Text fontSize="lg">Loading transcript...</Text>
              </VStack>
            ) : error ? (
              <Alert status="error" borderRadius="md" p={4}>
                <AlertIcon />
                {error}
              </Alert>
            ) : transcriptData ? (
              <VStack spacing={8} align="start">
                {/* Transcript Section */}
                {transcriptData.transcript_text && (
                  <Box width="100%">
                    <Text fontSize="xl" fontWeight="bold" mb={4} color="teal.700">
                      Transcript:
                    </Text>
                    <Box
                      p={8}
                      borderRadius="md"
                      borderWidth="1px"
                      borderColor="gray.200"
                      boxShadow="lg"
                      maxHeight="500px"
                      overflowY="auto"
                    >
                      {transcriptData.transcript_text.split('\n').map((line, index) => (
                        <React.Fragment key={index}>
                          {renderTranscriptLine(line)}
                        </React.Fragment>
                      ))}
                    </Box>
                  </Box>
                )}

                {/* Notes Section */}
                {transcriptData.notes && (
                  <Box width="100%">
                    <Text fontSize="xl" fontWeight="bold" mb={4} color="teal.700">
                      Notes:
                    </Text>
                    <Box
                      dangerouslySetInnerHTML={{ __html: transcriptData.notes }}
                      p={8}
                      borderRadius="md"
                      borderWidth="1px"
                      borderColor="gray.200"
                      boxShadow="lg"
                      minHeight="150px"
                      maxHeight="250px"
                      overflowY="auto"
                    />
                  </Box>
                )}

                {/* Important Topics Section */}
                {transcriptData.important_topics && (
                  <Box width="100%">
                    <Text fontSize="xl" fontWeight="bold" mb={4} color="teal.700">
                      Important Topics:
                    </Text>
                    <Box
                      dangerouslySetInnerHTML={{ __html: transcriptData.important_topics }}
                      p={8}
                      borderRadius="md"
                      borderWidth="1px"
                      borderColor="gray.200"
                      boxShadow="lg"
                      minHeight="150px"
                      maxHeight="250px"
                      overflowY="auto"
                    />
                  </Box>
                )}
              </VStack>
            ) : (
              <Text fontSize="lg">No transcript available.</Text>
            )}
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="teal" mr={4} onClick={onClose} boxShadow="md" _hover={{ boxShadow: "lg" }} size="lg">
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default TranscriptModal;
