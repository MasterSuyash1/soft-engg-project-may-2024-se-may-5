import React, { useState } from 'react';
import {
  Box,
  Flex,
  Text,
  Button,
  Select,
  VStack,
  Spinner,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import { ArrowBackIcon } from '@chakra-ui/icons';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';

const sampleQuestion = {
  title: "Sum of Two Numbers",
  description: "Write a function that takes two numbers and returns their sum.",
  testCases: [
    { input: "1, 2", output: "3" },
    { input: "10, 20", output: "30" },
    { input: "-1, 1", output: "0" },
  ],
};

const ProgrammingAssignment = () => {
  const [language, setLanguage] = useState("javascript");
  const [code, setCode] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState(null);

  const runCode = () => {
    setIsRunning(true);
    // Simulate running the code and checking test cases
    setTimeout(() => {
      setResult("All test cases passed!");
      setIsRunning(false);
    }, 2000);
  };

  return (
    <Flex minHeight="100vh" direction="column" bg="gray.100">
      <Box bg="white" p={4} boxShadow="md">
        <Flex justify="space-between" align="center">
          <Button as={RouterLink} to="/dashboard" leftIcon={<ArrowBackIcon />} colorScheme="teal">
            Back to Dashboard
          </Button>
          <Text fontSize="2xl" fontWeight="bold" color="teal.600">
            Programming Assignment
          </Text>
        </Flex>
      </Box>
      <Flex flex="1" p={6} bg="white" boxShadow="md" m={4} borderRadius="lg">
        <VStack align="start" spacing={4} w="40%" pr={4} borderRight="1px solid #E2E8F0">
          <Text fontSize="xl" fontWeight="bold">{sampleQuestion.title}</Text>
          <Text>{sampleQuestion.description}</Text>
          <Box w="100%" p={4} borderWidth={1} borderRadius="lg" bg="gray.50">
            <Text fontWeight="bold">Test Cases:</Text>
            {sampleQuestion.testCases.map((testCase, index) => (
              <Box key={index} p={2} borderWidth={1} borderRadius="md" mt={2}>
                <Text><strong>Input:</strong> {testCase.input}</Text>
                <Text><strong>Expected Output:</strong> {testCase.output}</Text>
              </Box>
            ))}
          </Box>
        </VStack>
        <VStack align="start" spacing={4} w="60%" pl={4}>
          <Select
            value={language}
            onChange={e => setLanguage(e.target.value)}
            placeholder="Select Language"
            mt={4}
            w="100%"
          >
            <option value="javascript">JavaScript</option>
            <option value="python">Python</option>
            {/* Add more languages as needed */}
          </Select>
          <Box w="100%" borderWidth={1} borderRadius="lg" overflow="hidden" mt={4} bg="black">
            <Editor
              value={code}
              onValueChange={code => setCode(code)}
              highlight={code => highlight(code, languages[language])}
              padding={10}
              style={{
                fontFamily: '"Fira code", "Fira Mono", monospace',
                fontSize: 14,
                backgroundColor: "#2D2D2D",
                color: "#F8F8F2",
                minHeight: "300px",
                lineHeight: "1.5",
              }}
            />
          </Box>
          <Button
            colorScheme="teal"
            onClick={runCode}
            isLoading={isRunning}
            loadingText="Running"
            mt={4}
            w="100%"
          >
            Run
          </Button>
          {result && (
            <Alert status="success" mt={4} w="100%">
              <AlertIcon />
              {result}
            </Alert>
          )}
          {isRunning && (
            <Spinner size="xl" mt={4} />
          )}
        </VStack>
      </Flex>
    </Flex>
  );
};

export default ProgrammingAssignment;
