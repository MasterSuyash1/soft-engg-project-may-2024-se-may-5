import React, { useEffect } from 'react';
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
        <Flex justify="space-between" align="center">
          <IconButton
            as={RouterLink}
            to="/"
            icon={<ArrowBackIcon />}
            aria-label="Home"
          />
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
            Introduction to Algorithms
          </Text>
          <Accordion allowMultiple>
            <AccordionItem>
              <AccordionButton>
                <Box flex="1" textAlign="left" fontWeight="medium" color={textColorAccordion}>
                  Week 1
                </Box>
                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel pb={4}>
                <VStack align="start" spacing={3} pl={4}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Lecture 1
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="/programming-assignment" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Programming Assignments
                  </Link>
                </VStack>
              </AccordionPanel>
            </AccordionItem>
            <AccordionItem>
              <AccordionButton>
                <Box flex="1" textAlign="left" fontWeight="medium" color={textColorAccordion}>
                  Week 2
                </Box>
                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel pb={4}>
                <VStack align="start" spacing={3} pl={4}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Lecture 2
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="/programming-assignment" fontWeight="medium" color={textColorAccordion} _hover={{ textDecoration: 'underline' }}>
                    Programming Assignments
                  </Link>
                </VStack>
              </AccordionPanel>
            </AccordionItem>
            {/* Add more weeks as needed */}
          </Accordion>
        </Box>
        <Box flex="1" p={6} bg={bgBox} boxShadow="md" ml={4}>
          <Box borderWidth={1} borderRadius="lg" overflow="hidden" bg={videoBoxBg} p={4} borderColor={borderColor}>
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
          <Flex mt={4} justify="space-around" borderTop="1px solid" borderColor={borderColor} pt={4}>
            <RateVideoModal />
            <ChatBotModal />
          </Flex>
        </Box>
      </Flex>
    </Flex>
  );
};

export default Dashboard;
