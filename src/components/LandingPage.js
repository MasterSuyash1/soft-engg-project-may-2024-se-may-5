import React from 'react';
import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Stack,
  Text,
  Image,
} from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import logo from '../assets/logo.png'; // Import the image

const LandingPage = () => {
  return (
    <Box bg="gray.900" minH="100vh" color="white">
      <Container maxW="container.xl">
        <Flex
          align="center"
          justify="space-between"
          direction={{ base: 'column', md: 'row' }}
          py={12}
        >
          <Box mb={{ base: 8, md: 0 }}>
            <Image
              src={logo} // Use the imported image
              alt="Learning"
              borderRadius="lg"
              boxShadow="xl"
              maxWidth="400px"
            />
          </Box>
          <Stack spacing={6} textAlign={{ base: 'center', md: 'left' }}>
            <Heading
              as="h1"
              size="2xl"
              fontWeight="bold"
              bgGradient="linear(to-r, cyan.400, purple.500)"
              bgClip="text"
            >
              Welcome to AlgoMatrix Learning
            </Heading>
            <Text fontSize="xl" color="gray.300">
              Enhance your skills with our interactive learning modules and
              expert-led courses.
            </Text>
            <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
              <Button
                as={RouterLink}
                to="/login"
                colorScheme="purple"
                size="lg"
              >
                Login
              </Button>
              <Button
                as={RouterLink}
                to="/signup"
                size="lg"
                colorScheme="purple"
                variant="outline"
              >
                Sign Up
              </Button>
            </Stack>
          </Stack>
        </Flex>
      </Container>
    </Box>
  );
};

export default LandingPage;
