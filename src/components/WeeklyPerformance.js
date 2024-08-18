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
  Text,
  List,
  ListItem,
  ListIcon,
  OrderedList,
  ScaleFade,
  useColorMode,
  useColorModeValue,
} from '@chakra-ui/react';
import { CheckCircleIcon } from '@chakra-ui/icons';
import axios from 'axios';

const WeeklyPerformance = ({ userId, weekNo }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  
  // Ensure useColorModeValue is called at the top level
  const modalBg = useColorModeValue('white', 'gray.800');
  const bodyBg = useColorModeValue('gray.50', 'gray.900');
  const boxBg = useColorModeValue('white', 'gray.700');

  const fetchPerformance = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/weekly_performance_analysis', {
        user_id: userId,
        week_no: weekNo,
      });
      setPerformance(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = () => {
    fetchPerformance();
    onOpen();
  };

  return (
    <>
      <Button
        onClick={handleOpen}
        colorScheme="teal"
        variant="outline"
        size="md"
        mt={4}
        mb={4}
        transition="all 0.2s"
        _hover={{ transform: 'scale(1.05)' }}
        _active={{ transform: 'scale(0.95)' }}
      >
        View Weekly Performance
      </Button>

      

      <Modal isOpen={isOpen} onClose={onClose} size="xl" motionPreset="slideInBottom">
        <ModalOverlay />
        <ModalContent
          maxW="90vw"
          maxH="80vh"
          borderRadius="xl"
          boxShadow="2xl"
          bg={modalBg}  
        >
          <ModalHeader fontSize="2xl" fontWeight="bold">
            Weekly Performance Analysis
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody
            p={8}
            overflowY="auto"
            maxHeight="70vh"
            bg={bodyBg} 
            borderRadius="md"
          >
            {loading ? (
              <Box textAlign="center" p={6}>
                <Spinner size="xl" speed="0.65s" />
              </Box>
            ) : error ? (
              <Text color="red.500" fontWeight="bold">{error}</Text>
            ) : performance ? (
              <ScaleFade initialScale={0.9} in={true}>
                <Text fontSize="lg" mb={6} fontWeight="semibold">Performance Scores</Text>
                <List spacing={4} mb={6}>
                  <ListItem>
                    <ListIcon as={CheckCircleIcon} color="teal.400" />
                    AQ Score: {parseFloat(performance.performance.aq_score)}
                  </ListItem>
                  <ListItem>
                    <ListIcon as={CheckCircleIcon} color="teal.400" />
                    GP Score: {parseFloat(performance.performance.gp_score)}
                  </ListItem>
                  <ListItem>
                    <ListIcon as={CheckCircleIcon} color="teal.400" />
                    GQ Score: {parseFloat(performance.performance.gq_score)}
                  </ListItem>
                  <ListItem>
                    <ListIcon as={CheckCircleIcon} color="teal.400" />
                    Overall AI Score: {parseFloat(performance.performance.overall_ai_score).toFixed(2)}
                  </ListItem>
                  <ListItem>
                    <ListIcon as={CheckCircleIcon} color="teal.400" />
                    PM Score: {parseFloat(performance.performance.pm_score)}
                  </ListItem>
                  <ListItem>
                    <ListIcon as={CheckCircleIcon} color="teal.400" />
                    PP Score: {parseFloat(performance.performance.pp_score)}
                  </ListItem>
                </List>

                <Text fontSize="lg" mb={6} fontWeight="semibold">SWOT Analysis</Text>
                <Box
                  borderWidth="1px"
                  borderRadius="lg"
                  p={6}
                  mb={6}
                  bg={boxBg}  
                  shadow="sm"
                >
                  <Text fontWeight="bold" mb={2}>Opportunities:</Text>
                  <OrderedList spacing={3} mb={4}>
                    {performance.swot_analysis.opportunities.map((item, index) => (
                      <ListItem key={index}>{item}</ListItem>
                    ))}
                  </OrderedList>
                  <Text fontWeight="bold" mb={2}>Strengths:</Text>
                  <OrderedList spacing={3} mb={4}>
                    {performance.swot_analysis.strengths.map((item, index) => (
                      <ListItem key={index}>{item}</ListItem>
                    ))}
                  </OrderedList>
                  <Text fontWeight="bold" mb={2}>Threats:</Text>
                  <OrderedList spacing={3} mb={4}>
                    {performance.swot_analysis.threats.map((item, index) => (
                      <ListItem key={index}>{item}</ListItem>
                    ))}
                  </OrderedList>
                  <Text fontWeight="bold" mb={2}>Weaknesses:</Text>
                  <OrderedList spacing={3}>
                    {performance.swot_analysis.weaknesses.map((item, index) => (
                      <ListItem key={index}>{item}</ListItem>
                    ))}
                  </OrderedList>
                </Box>
              </ScaleFade>
            ) : (
              <Text>No performance data available.</Text>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default WeeklyPerformance;
