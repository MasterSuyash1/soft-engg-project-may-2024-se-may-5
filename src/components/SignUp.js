import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Stack,
  Heading,
  Text,
  useToast,
  InputGroup,
  InputRightElement,
  Link,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import axios from 'axios';

const SignUp = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/signup', { username, email, password });
      if (response.status === 201) {
        toast({
          title: 'Account created.',
          description: "You've successfully created an account.",
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
        navigate('/login');
      }
    } catch (error) {
      toast({
        title: 'Signup failed.',
        description: 'There was an error creating your account.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handlePasswordVisibility = () => setShowPassword(!showPassword);

  return (
    <Box
      minHeight="100vh"
      display="flex"
      alignItems="center"
      justifyContent="center"
      bg="gray.50"
      py={12}
    >
      <Box
        p={8}
        maxWidth="400px"
        borderWidth={1}
        borderRadius="lg"
        boxShadow="lg"
        bg="white"
        transition="transform 0.2s"
        _hover={{ transform: 'scale(1.05)' }}
      >
        <Box textAlign="center">
          <Heading
            fontSize="2xl"
            mb={4}
            bgGradient="linear(to-r, teal.400, teal.600)"
            bgClip="text"
          >
            Create your account
          </Heading>
          <Text mb={6} color="gray.600">
            Sign up to get started!
          </Text>
        </Box>
        <Box my={4} textAlign="left">
          <form onSubmit={handleSubmit}>
            <FormControl isRequired>
              <FormLabel>Username</FormLabel>
              <Input
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </FormControl>
            <FormControl mt={4} isRequired>
              <FormLabel>Email</FormLabel>
              <Input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </FormControl>
            <FormControl mt={4} isRequired>
              <FormLabel>Password</FormLabel>
              <InputGroup>
                <Input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <InputRightElement h="full">
                  <Button
                    variant="ghost"
                    onClick={handlePasswordVisibility}
                  >
                    {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                  </Button>
                </InputRightElement>
              </InputGroup>
            </FormControl>
            <Stack spacing={6} mt={4}>
              <Button
                width="full"
                type="submit"
                colorScheme="teal"
                size="lg"
              >
                Sign Up
              </Button>
              <Text align="center">
                Already have an account?{' '}
                <Link as={RouterLink} to="/login" color="teal.500">
                  Login
                </Link>
              </Text>
            </Stack>
          </form>
        </Box>
      </Box>
    </Box>
  );
};

export default SignUp;
