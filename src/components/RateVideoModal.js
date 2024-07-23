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
  useDisclosure,
  Text,
  Box,
  Textarea,
  Flex,
} from '@chakra-ui/react';
import { StarIcon } from '@chakra-ui/icons';
import axios from 'axios';

const RateVideoModal = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [ratings, setRatings] = useState({
    audio: 0,
    video: 0,
    content: 0,
  });
  const [feedback, setFeedback] = useState('');

  const handleRating = (category, value) => {
    setRatings({ ...ratings, [category]: value });
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/submit_rating', {
        user_id: 1,  // Replace with actual user ID
        audio: ratings.audio,
        video: ratings.video,
        content: ratings.content,
        feedback: feedback,
      });
      console.log(response.data);
      onClose();
    } catch (error) {
      console.error('Error submitting rating:', error);
    }
  };

  return (
    <>
      <Button onClick={onOpen} color="teal.600" _hover={{ textDecoration: 'underline' }}>
        Rate this Video
      </Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Video Review</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box>
              {['audio', 'video', 'content'].map((category) => (
                <Box key={category} mb={4}>
                  <Text>{category.charAt(0).toUpperCase() + category.slice(1)}</Text>
                  <Flex>
                    {[...Array(5)].map((_, index) => (
                      <StarIcon
                        key={index}
                        cursor="pointer"
                        color={index < ratings[category] ? 'teal.500' : 'gray.300'}
                        onClick={() => handleRating(category, index + 1)}
                      />
                    ))}
                  </Flex>
                </Box>
              ))}
              <Text mb={2}>Feedback</Text>
              <Textarea
                placeholder="Type your comments"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
              />
            </Box>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="teal" mr={3} onClick={handleSubmit}>
              Save
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default RateVideoModal;
