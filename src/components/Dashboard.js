import React from 'react';
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
} from '@chakra-ui/react';
import { ArrowBackIcon } from '@chakra-ui/icons';
import { Link as RouterLink } from 'react-router-dom';

const Dashboard = () => {
  return (
    <Flex minHeight="100vh" direction="column" bg="gray.100">
      <Box bg="white" p={4} boxShadow="md">
        <Flex justify="space-between" align="center">
          <IconButton
            as={RouterLink}
            to="/"
            icon={<ArrowBackIcon />}
            aria-label="Home"
          />
          <Text fontSize="2xl" fontWeight="bold" color="teal.600">
            AlgoMatrix Learning
          </Text>
        </Flex>
      </Box>
      <Flex flex="1">
        <Box w="20%" bg="white" p={4} boxShadow="md">
          <Text fontSize="lg" fontWeight="bold" mb={4} color="teal.600">
            Introduction to Algorithms
          </Text>
          <Accordion allowMultiple>
            <AccordionItem>
              <AccordionButton>
                <Box flex="1" textAlign="left" fontWeight="medium" color="teal.500">
                  Week 1
                </Box>
                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel pb={4}>
                <VStack align="start" spacing={3}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Lecture 1
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Programming Assignments
                  </Link>
                </VStack>
              </AccordionPanel>
            </AccordionItem>
            <AccordionItem>
              <AccordionButton>
                <Box flex="1" textAlign="left" fontWeight="medium" color="teal.500">
                  Week 2
                </Box>
                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel pb={4}>
                <VStack align="start" spacing={3}>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Lecture 2
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Activity Questions
                  </Link>
                  <Link as={RouterLink} to="#" fontWeight="medium" color="teal.500" _hover={{ textDecoration: 'underline' }}>
                    Programming Assignments
                  </Link>
                </VStack>
              </AccordionPanel>
            </AccordionItem>
            {/* Add more weeks as needed */}
          </Accordion>
        </Box>
        <Box flex="1" p={6} bg="white" boxShadow="md" ml={4}>
          <Box borderWidth={1} borderRadius="lg" overflow="hidden" bg="gray.50" p={4}>
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
          </Flex>
        </Box>
      </Flex>
    </Flex>
  );
};

export default Dashboard;
