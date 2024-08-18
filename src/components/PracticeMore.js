import React, { useEffect, useState, useRef } from 'react';
import { Box, Text, Button, VStack, Radio, RadioGroup, Heading, useToast, Stack, Spinner, useColorModeValue, Divider } from '@chakra-ui/react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const PracticeMore = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const toast = useToast();
  const fetchRef = useRef(false);

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);

  // Extract all useColorModeValue calls to the top level of the component
  const cardBg = useColorModeValue('white', 'gray.800');
  const cardBorder = useColorModeValue('gray.200', 'gray.700');
  const buttonBg = useColorModeValue('teal.500', 'teal.300');
  const buttonTextColor = useColorModeValue('white', 'gray.800');
  const hoverBg = useColorModeValue('teal.600', 'teal.400');
  const textColor = useColorModeValue('gray.600', 'gray.300');
  const headingColor = useColorModeValue('gray.700', 'gray.100');
  const containerBg = useColorModeValue('gray.50', 'gray.900');

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/activity/extra_questions/${lessonId}`);
        
        console.log('API Response:', response.data); // Log the full response for debugging

        // Handle the specific structure of your response
        const quizData = response.data.new_quiz_data;
        
        if (Array.isArray(quizData) && quizData.length > 0) {
          const questions = quizData.map(([index, item]) => ({
            index: index,
            question: item.question,
            options: item.options,
            correctAnswer: item.correct,
            explanation: item.explanation // Include the explanation here
          }));

          setQuestions(questions);

          // Save the correct answers and explanations in session storage using question text as key
          const correctAnswers = quizData.reduce((acc, [_, item]) => {
            acc[item.question] = { correct: item.correct, explanation: item.explanation };
            return acc;
          }, {});

          sessionStorage.setItem('correctAnswers', JSON.stringify(correctAnswers));
          console.log('Correct answers saved:', correctAnswers);
        } else {
          console.error('Unexpected data structure:', response.data);
          toast({
            title: 'Data Error',
            description: 'Questions data not found. Please try again later.',
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
        }

        setLoading(false);
      } catch (error) {
        console.error('Error fetching questions:', error);
        toast({
          title: 'Error fetching extra questions',
          description: 'There was an issue loading the extra questions. Please try again later.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        setLoading(false);
      }
    };

    if (!fetchRef.current) {
      fetchRef.current = true;
      fetchQuestions();
    }
  }, [lessonId, toast]);

  const handleAnswerChange = (questionIndex, value) => {
    setAnswers({
      ...answers,
      [questionIndex]: value,
    });
  };

  const handleSubmit = () => {
    console.log('Submitted answers:', answers);

    // Retrieve the correct answers and explanations from session storage
    const correctAnswersString = sessionStorage.getItem('correctAnswers');
    
    if (!correctAnswersString) {
      toast({
        title: 'Error',
        description: 'Correct answers not found. Please try again later.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    let correctAnswers;

    try {
      correctAnswers = JSON.parse(correctAnswersString);
      console.log('Correct answers retrieved:', correctAnswers);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to parse correct answers.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    // Map question index to question text to check answers correctly
    const answerMap = questions.reduce((acc, { index, question }) => {
      acc[index] = question;
      return acc;
    }, {});

    // Calculate score and show explanations for incorrect answers
    const score = Object.keys(answers).reduce((acc, key) => {
      const questionText = answerMap[key];
      if (questionText && answers[key] === correctAnswers[questionText].correct) {
        return acc + 1;
      } else if (questionText) {
        toast({
          title: `Question ${parseInt(key) + 1}`,
          description: `Your answer: ${answers[key]}. Correct answer: ${correctAnswers[questionText].correct}. Explanation: ${correctAnswers[questionText].explanation}`,
          status: 'info',
          duration: 10000,
          isClosable: true,
        });
      }
      return acc;
    }, 0);

    toast({
      title: `Your score is: ${score}/${Object.keys(correctAnswers).length}`,
      status: 'success',
      duration: 5000,
      isClosable: true,
    });
  };

  return (
    <Box p={8} maxW="900px" mx="auto" bg={containerBg} borderRadius="lg" boxShadow="lg">
      <Heading as="h2" fontSize="2xl" mb={8} textAlign="center" fontWeight="bold" color={headingColor}>
        Practice More
      </Heading>
      {loading ? (
        <Box textAlign="center">
          <Spinner size="xl" color="teal.500" />
          <Text mt={4} fontSize="lg" color={textColor}>Loading questions...</Text>
        </Box>
      ) : questions.length > 0 ? (
        <Stack spacing={8}>
          {questions.map(({ index, question, options }) => (
            <Box 
              key={index} 
              p={6} 
              bg={cardBg} 
              borderRadius="lg" 
              boxShadow="md" 
              border={`1px solid ${cardBorder}`}
            >
              <Text fontWeight="semibold" fontSize="lg" mb={4} color={headingColor}>
                {`${index + 1}. ${question}`}
              </Text>
              <RadioGroup onChange={(value) => handleAnswerChange(index, value)} value={answers[index]}>
                <VStack align="start" spacing={4}>
                  {options.map((option, i) => (
                    <Radio key={i} value={option} size="lg" colorScheme="teal">{option}</Radio>
                  ))}
                </VStack>
              </RadioGroup>
            </Box>
          ))}
          <Button 
            onClick={handleSubmit} 
            size="lg" 
            bg={buttonBg} 
            color={buttonTextColor} 
            _hover={{ bg: hoverBg }} 
            alignSelf="center"
          >
            Submit Answers
          </Button>
        </Stack>
      ) : (
        <Text textAlign="center" fontSize="xl" color={textColor}>No extra questions available.</Text>
      )}
      <Divider mt={8} mb={4} />
      <Button 
        mt={4} 
        colorScheme="teal" 
        variant="outline" 
        onClick={() => navigate(-1)} 
        size="lg"
        alignSelf="center"
      >
        Go Back
      </Button>
    </Box>
  );
};

export default PracticeMore;
