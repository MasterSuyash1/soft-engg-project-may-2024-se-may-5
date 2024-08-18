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
  useDisclosure,
  Spinner,
  Alert,
  AlertIcon,
  Box
} from '@chakra-ui/react';
import { InfoIcon } from '@chakra-ui/icons';  // Import the icon
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const AboutVideoModal = ({ lessonId }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [videoDetails, setVideoDetails] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen && lessonId) {
      fetchVideoDetails();
    }
  }, [isOpen, lessonId]);

  const fetchVideoDetails = async () => {
    setLoading(true);
    setError(null);
    setVideoDetails('');

    try {
      console.log(`Fetching video details for lessonId: ${lessonId}`);
      const response = await axios.get(`http://127.0.0.1:5000/api/about-video/${lessonId}`);
      setVideoDetails(response.data.message);
    } catch (err) {
      console.error("Error fetching video details:", err);
      setError('Failed to fetch video details');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button colorScheme="teal" onClick={onOpen} leftIcon={<InfoIcon />}>
        About
      </Button>

      <Modal isOpen={isOpen} onClose={onClose}>
  <ModalOverlay />
  <ModalContent 
    width="70%"        // Adjust the width of the modal (80% of the screen width)
    maxWidth="80%"     // Maximum width to prevent the modal from getting too large
    height="60vh"      // Adjust the height of the modal (80% of the viewport height)
    maxHeight="80vh"   // Maximum height to prevent the modal from getting too large
  >
    <ModalHeader>About the Video</ModalHeader>
    <ModalCloseButton />
    <ModalBody>
      {loading ? (
        <Spinner size="lg" />
      ) : error ? (
        <Alert status="error">
          <AlertIcon />
          {error}
        </Alert>
      ) : (
        <Box 
          width="80%" 
          height="300px"  
          maxHeight="400px"  
          overflowY="auto"  
          p={10}  
          border="1px solid #E2E8F0"  
          borderRadius="md"  
        >
          <ReactMarkdown>{videoDetails}</ReactMarkdown>
        </Box>
      )}
    </ModalBody>
    <ModalFooter>
      <Button colorScheme="teal" mr={3} onClick={onClose}>
        Close
      </Button>
    </ModalFooter>
  </ModalContent>
</Modal>

    </>
  );
};

export default AboutVideoModal;
