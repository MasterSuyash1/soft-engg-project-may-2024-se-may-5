<<<<<<< HEAD
import React from 'react';
=======
import React, { useEffect } from 'react';
>>>>>>> main
import {
  Box,
  Flex,
  Text,
  Link,
  IconButton,
  VStack,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
<<<<<<< HEAD
} from '@chakra-ui/react';
import { ArrowBackIcon } from '@chakra-ui/icons';
import { Link as RouterLink } from 'react-router-dom';

const Dashboard = () => {
  return (
    <Flex minHeight="100vh" direction="column" bg="gray.100">
      <Box bg="white" p={4} boxShadow="md">
=======
  Button,
  useColorMode,
  useColorModeValue,
} from '@chakra-ui/react';
import { ArrowBackIcon, SunIcon, MoonIcon } from '@chakra-ui/icons';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

import RateVideoModal from './RateVideoModal';
import ChatBotModal from './ChatBotModal';

const Dashboard = () => {
  const { colorMode, toggleColorMode, setColorMode } = useColorMode();
  const bg = useColorModeValue('gray.100', 'gray.900');
  const bgBox = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('teal.600', 'teal.300');
  const textColorAccordion = useColorModeValue('teal.500', 'teal.200');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const videoBoxBg = useColorModeValue('gray.50', 'gray.700');

  const navigate = useNavigate();

  const handleLogout = () => {
    setColorMode('light');
    navigate('/login');
  };

  const MotionIconButton = motion(IconButton);

  return (
    <Flex minHeight="100vh" direction="column" bg={bg}>
      <Box bg={bgBox} p={4} boxShadow="md">
>>>>>>> main
        <Flex justify="space-between" align="center">
          <IconButton
            as={RouterLink}
            to="/"
            icon={<ArrowBackIcon />}
            aria-label="Home"
          />
<<<<<<< HEAD
          <Text fontSize="2xl" fontWeight="bold" color="teal.600">
            AlgoMatrix Learning
          </Text>
        </Flex>
      </Box>
      <Flex flex="1">
        <Box w="20%" bg="white" p={4} boxShadow="md">
          <Text fontSize="lg" fontWeight="bold" mb={4} color="teal.600">
=======
          <Text fontSize="2xl" fontWeight="bold" color={textColor}>
            AlgoMatrix Learning
          </Text>
          <Flex align="center">
            <MotionIconButton
              icon={colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
              onClick={toggleColorMode}
              aria-label="Toggle Dark Mode"
              colorScheme="teal"
              mr={4}
              whileTap={{ scale: 0.9 }}
              transition={{ duration: 0.2 }}
            />
            <Button colorScheme="teal" onClick={handleLogout}>
              Logout
            </Button>
          </Flex>
        </Flex>
      </Box>
      <Flex flex="1">
        <Box w="20%" bg={bgBox} p={4} boxShadow="md">
          <Text fontSize="lg" fontWeight="bold" mb={4} color={textColor}>
>>>>>>> main
            Introduction to Algorithms
          </Text>
          <Accordion allowMultiple>
            <AccordionItem>
              <AccordionButton>
<<<<<<< HEAD
                <Box flex="1" textAlign="left" fontWeight="medium" color="teal.500">
=======
                <Box flex="1" textAlign="left" fontWeight="medium" color={textColorAccordion}>
>>>>>>> main
                  Week 1
                </Box>
                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel pb={4}>
<<<<<<< HEAD
                <VStack align="start" spacing={3}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Lecture 1
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
=======
                <VStack align="start" spacing={3} pl={4}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Lecture 1
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="/programming-assignment" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
>>>>>>> main
                    Programming Assignments
                  </Link>
                </VStack>
              </AccordionPanel>
            </AccordionItem>
            <AccordionItem>
              <AccordionButton>
<<<<<<< HEAD
                <Box flex="1" textAlign="left" fontWeight="medium" color="teal.500">
=======
                <Box flex="1" textAlign="left" fontWeight="medium" color={textColorAccordion}>
>>>>>>> main
                  Week 2
                </Box>
                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel pb={4}>
<<<<<<< HEAD
                <VStack align="start" spacing={3}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Lecture 2
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
=======
                <VStack align="start" spacing={3} pl={4}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Lecture 2
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="/programming-assignment" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
>>>>>>> main
                    Programming Assignments
                  </Link>
                </VStack>
              </AccordionPanel>
            </AccordionItem>
            {/* Add more weeks as needed */}
          </Accordion>
        </Box>
<<<<<<< HEAD
        <Box flex="1" p={6} bg="white" boxShadow="md" ml={4}>
          <Box borderWidth={1} borderRadius="lg" overflow="hidden" bg="gray.50" p={4}>
=======
        <Box flex="1" p={6} bg={bgBox} boxShadow="md" ml={4}>
          <Box borderWidth={1} borderRadius="lg" overflow="hidden" bg={videoBoxBg} p={4} borderColor={borderColor}>
>>>>>>> main
            <iframe
              width="100%"
              height="400px"
              src="https://www.youtube.com/embed/ZA-tUyM_y7s?list=PLUl4u3cNGP63EdVPNLG3ToM6LaEUuStEY"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              title="Lecture Video"
            ></iframe>
          </Box>
<<<<<<< HEAD
          <Flex mt={4} justify="space-around" borderTop="1px solid" borderColor="gray.200" pt={4}>
            <Link as={RouterLink} to="#" color="teal.600" _hover={{ textDecoration: 'underline' }}>
              About
            </Link>
            <Link as={RouterLink} to="#" color="teal.600" _hover={{ textDecoration: 'underline' }}>
              Transcript
            </Link>
            <Link as={RouterLink} to="#" color="teal.600" _hover={{ textDecoration: 'underline' }}>
              Ask me
            </Link>
            <Link as={RouterLink} to="#" color="teal.600" _hover={{ textDecoration: 'underline' }}>
              Rate this Video
            </Link>
=======
          <Flex mt={4} justify="space-around" borderTop="1px solid" borderColor={borderColor} pt={4}>
            <RateVideoModal />
            <ChatBotModal />
>>>>>>> main
          </Flex>
        </Box>
      </Flex>
    </Flex>
  );
};

export default Dashboard;
