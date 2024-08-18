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

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', { email, password });
      if (response.status === 200) {
        toast({
          title: response.data.is_admin ? 'Admin login successful.' : 'Login successful.',
          description: response.data.is_admin ? 'Welcome, Admin!' : "You've successfully logged in.",
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
        if (response.data.is_admin) {
          navigate('/admin-dashboard');
        } else {
          // console.log(response.data.user_Id);
          localStorage.setItem('user_Id', response.data.user_Id);
          navigate('/dashboard');
        }
      }
    } catch (error) {
      toast({
        title: 'Login failed.',
        description: 'Invalid email or password.',
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
            Sign in to your account
          </Heading>
          <Text mb={6} color="gray.600">
            Welcome back! Please enter your details.
          </Text>
        </Box>
        <Box my={4} textAlign="left">
          <form onSubmit={handleSubmit}>
            <FormControl isRequired>
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
                Sign In
              </Button>
              <Text align="center">
                Don't have an account?{' '}
                <Link as={RouterLink} to="/signup" color="teal.500">
                  Sign Up
                </Link>
              </Text>
            </Stack>
          </form>
        </Box>
      </Box>
    </Box>
  );
};

export default Login;
