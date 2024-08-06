<<<<<<< HEAD
import React, { useState } from 'react';
=======
import React, { useState } from "react";
>>>>>>> a24dc1c (Made some changes)
import {
  Box,
  Flex,
  Text,
  Button,
<<<<<<< HEAD
  Select,
=======
>>>>>>> a24dc1c (Made some changes)
  VStack,
  Spinner,
  Alert,
  AlertIcon,
<<<<<<< HEAD
} from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import { ArrowBackIcon } from '@chakra-ui/icons';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';
=======
  Select,
} from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";
import { ArrowBackIcon } from "@chakra-ui/icons";
import Editor from "@monaco-editor/react";
import axios from "axios";
>>>>>>> a24dc1c (Made some changes)

const sampleQuestion = {
  title: "Sum of Two Numbers",
  description: "Write a function that takes two numbers and returns their sum.",
  testCases: [
    { input: "1, 2", output: "3" },
    { input: "10, 20", output: "30" },
    { input: "-1, 1", output: "0" },
  ],
};

<<<<<<< HEAD
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
=======
const supportedThemes = [
  "vs-dark",
  "light",
  "hc-black",
  // Add more themes as needed
];

const ProgrammingAssignment = () => {
  const [code, setCode] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState("");
  const [theme, setTheme] = useState("vs-dark");
  const [language, setLanguage] = useState("python");

  const runCode = async () => {
    setIsRunning(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/compile", {
        code: code,
        lang: language,
      });

      if (response.data.error) {
        setResult(`Error: ${response.data.error}`);
      } else {
        setResult(response.data.output || "No output");
      }
    } catch (error) {
      setResult(`Error: ${error.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleEditorChange = (value) => {
    setCode(value);
>>>>>>> a24dc1c (Made some changes)
  };

  return (
    <Flex minHeight="100vh" direction="column" bg="gray.100">
      <Box bg="white" p={4} boxShadow="md">
        <Flex justify="space-between" align="center">
<<<<<<< HEAD
          <Button as={RouterLink} to="/dashboard" leftIcon={<ArrowBackIcon />} colorScheme="teal">
=======
          <Button
            as={RouterLink}
            to="/dashboard"
            leftIcon={<ArrowBackIcon />}
            colorScheme="teal"
          >
>>>>>>> a24dc1c (Made some changes)
            Back to Dashboard
          </Button>
          <Text fontSize="2xl" fontWeight="bold" color="teal.600">
            Programming Assignment
          </Text>
        </Flex>
      </Box>
      <Flex flex="1" p={6} bg="white" boxShadow="md" m={4} borderRadius="lg">
        <VStack align="start" spacing={4} w="40%" pr={4} borderRight="1px solid #E2E8F0">
<<<<<<< HEAD
          <Text fontSize="xl" fontWeight="bold">{sampleQuestion.title}</Text>
=======
          <Text fontSize="xl" fontWeight="bold">
            {sampleQuestion.title}
          </Text>
>>>>>>> a24dc1c (Made some changes)
          <Text>{sampleQuestion.description}</Text>
          <Box w="100%" p={4} borderWidth={1} borderRadius="lg" bg="gray.50">
            <Text fontWeight="bold">Test Cases:</Text>
            {sampleQuestion.testCases.map((testCase, index) => (
              <Box key={index} p={2} borderWidth={1} borderRadius="md" mt={2}>
<<<<<<< HEAD
                <Text><strong>Input:</strong> {testCase.input}</Text>
                <Text><strong>Expected Output:</strong> {testCase.output}</Text>
=======
                <Text>
                  <strong>Input:</strong> {testCase.input}
                </Text>
                <Text>
                  <strong>Expected Output:</strong> {testCase.output}
                </Text>
>>>>>>> a24dc1c (Made some changes)
              </Box>
            ))}
          </Box>
        </VStack>
        <VStack align="start" spacing={4} w="60%" pl={4}>
          <Select
<<<<<<< HEAD
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
=======
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            placeholder="Select Theme"
            mt={4}
            w="100%"
          >
            {supportedThemes.map((themeName) => (
              <option key={themeName} value={themeName}>
                {themeName.charAt(0).toUpperCase() + themeName.slice(1)}
              </option>
            ))}
          </Select>
          <Box
            w="100%"
            borderWidth={1}
            borderRadius="lg"
            overflow="hidden"
            mt={4}
            bg="black"
          >
            <Editor
              height="300px"
              language={language}
              theme={theme}
              value={code}
              onChange={handleEditorChange}
              options={{
                fontFamily: '"Fira code", "Fira Mono", monospace',
                fontSize: 14,
                lineNumbers: "on",
>>>>>>> a24dc1c (Made some changes)
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
<<<<<<< HEAD
          {result && (
            <Alert status="success" mt={4} w="100%">
              <AlertIcon />
              {result}
            </Alert>
          )}
          {isRunning && (
            <Spinner size="xl" mt={4} />
          )}
=======
          <Box
            w="100%"
            borderWidth={1}
            borderRadius="lg"
            mt={4}
            p={4}
            bg="gray.900"
            color="white"
            whiteSpace="pre-wrap"
            fontFamily='"Fira code", "Fira Mono", monospace'
            minHeight="200px"
          >
            {typeof result === 'string' ? result : JSON.stringify(result, null, 2)}
            {isRunning && <Spinner size="xl" />}
          </Box>
>>>>>>> a24dc1c (Made some changes)
        </VStack>
      </Flex>
    </Flex>
  );
};

export default ProgrammingAssignment;
