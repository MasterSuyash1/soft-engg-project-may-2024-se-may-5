import React, { useEffect, useState } from 'react';
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
  Stack,
  Heading,
  Radio,
  RadioGroup,
  CheckboxGroup,
  Checkbox,
  useToast,
  useBreakpointValue,
  Textarea
} from '@chakra-ui/react';
import { ArrowBackIcon, SunIcon, MoonIcon } from '@chakra-ui/icons';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

import RateVideoModal from './RateVideoModal';
import ChatBotModal from './ChatBotModal';
import AboutVideoModal from './AboutVideoModal';
import TranscriptModal from './TranscriptModal';
import ExplainerModal from './ExplainerModal';
import WeeklyPerformance from './WeeklyPerformance';

import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-python";  // Change this to the mode you need
import "ace-builds/src-noconflict/theme-monokai"; 

const Dashboard = () => {
  const { colorMode, toggleColorMode, setColorMode } = useColorMode();
  const bg = useColorModeValue('gray.50', 'gray.800');
  const bgBox = useColorModeValue('white', 'gray.700');
  const textColor = useColorModeValue('teal.700', 'teal.300');
  const textColorAccordion = useColorModeValue('teal.600', 'teal.200');
  const borderColor = useColorModeValue('gray.300', 'gray.600');
  const videoBoxBg = useColorModeValue('gray.100', 'gray.600');

  const navigate = useNavigate();
  const toast = useToast();

  const [lessons, setLessons] = useState([]);
  const [weeks, setWeeks] = useState([]);
  const [selectedVideoUrl, setSelectedVideoUrl] = useState(null);
  const [selectedLectureId, setSelectedLectureId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [showQuestions, setShowQuestions] = useState(false);
  const [currentQuestionType, setCurrentQuestionType] = useState(null);
  const [editorContent, setEditorContent] = useState('');
  const [questionId, setQuestionId] = useState(null);
  const [output, setOutput] = useState('');
  const [markdownOutput, setMarkdownOutput] = useState('');
  const [language, setLanguage] = useState('python');
  const [QuestionID, setQuestionID] = useState(null);
  const [weekId, setWeekId] = useState(null);
  const [userId, setUserId] = useState(null);
  // const [lesson_id, setLessonID] = useState(null);


  useEffect(() => {
    console.log(localStorage.getItem("user_Id"));
    const fetchWeeks = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/weeks');
        setWeeks(response.data);
      } catch (error) {
        console.error('Error fetching weeks:', error);
      }
    };
  
    fetchWeeks();
  
    if (questions.length > 0) {
      setQuestionId(questions[0].question_id); // Set questionId to the ID of the first question 
      setEditorContent(questions[0].code_template);
      setOutput("");
    }
  
  }, [questions]);
  
  // const handleWeeklyPerformance = async(weekId) => {
  //   console.log("Weekly Performance is clicked");
  //   try{
  //     let user_id = {"user_id": 1}
  //     const response = await axios.get(`http://127.0.0.1:5000/api/weekly_performance/${weekId}`,{user_id});
  //     console.log(response);
  //   }catch (e){
  //     console.error("Error fetching weekly performance:", e);
  //     return []
  //   }

  // } 

  const fetchLessons = async (weekId) => {
    try {
      let user_id = {"user_id": 1}
      const response = await axios.get(`http://127.0.0.1:5000/api/weeks/${weekId}/lessons`);
      return response.data.lessons;
    } catch (error) {
      console.error('Error fetching lessons:', error);
      return [];
    }
  };
  
  const fetchQuestions = async (lessonId, questionType) => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/questions');
      const filteredQuestions = response.data.filter(
        (q) => q.lesson_id === lessonId && q.question_type === questionType 
      );
      console.log(response);
      console.log(filteredQuestions);
      return filteredQuestions;
    } catch (error) {
      console.error('Error fetching questions:', error);
      return [];
    }
  };
  
  const handleLessonClick = async (weekId, lessonId) => {
    setShowQuestions(false); // Switch to video view
    
    const lessons = await fetchLessons(weekId);
    const lesson = lessons.find((l) => l.id === lessonId);
    if (lesson) {
      const videoId = new URL(lesson.video_url).searchParams.get('v');
      const embedUrl = `https://www.youtube.com/embed/${videoId}`;
      setSelectedVideoUrl(embedUrl);
      setSelectedLectureId(lessonId);
      setQuestions(await fetchQuestions(lessonId)); // Fetch questions but do not display yet
    }
  };
  
  const handleQuestionClick = async (weekId, lessonId, questionType) => {
    setShowQuestions(true); // Switch to questions view
    console.log("weekId: ", weekId);
    setWeekId(weekId); // Set the week ID
    console.log("global week Id" + weekId);
    setCurrentQuestionType(questionType); // Set the current question type
    const lessonQuestions = await fetchQuestions(lessonId, questionType);
    setQuestions(lessonQuestions);
    setSelectedLectureId(lessonId);
    
    console.log(questionId);
    setEditorContent()
  };
  
  

  const handleCompile = () => {
    if (questionId == null) {
      console.error('No question ID provided');
      return;
    }
    fetch('http://127.0.0.1:5000/api/compile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question_id: questionId,
        code: editorContent
      }),
    })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        setOutput('Error: ' + data.error);
      } else {
        const outputText = data.results
          .map((result) => `Input: ${JSON.stringify(result.input)}\nExpected Output: ${result.expected_output}\nActual Output: ${result.actual_output}\nPassed: ${result.passed}\n`)
          .join('\n');
        setOutput(outputText);
      }
    })
    .catch((error) => setOutput('Error: ' + error));
  };
  
  const handleSubmit = () => {
    fetch('http://127.0.0.1:5000/api/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code: editorContent,
        question_id: questionId, // Use question_id
        user_id: localStorage.getItem("user_Id"), // Replace with actual user ID
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          setOutput('Error: ' + data.error);
        } else {
          setOutput(`Your submission was successful. You passed ${data.score} out of 3 test cases.`);
        }
      });
  };
  
  const handleLogout = () => {
    setColorMode('light');
    navigate('/login');
  };

  const handleAnswerChange = (questionId, value) => {
    setAnswers(prevAnswers => ({
      ...prevAnswers,
      [questionId]: value,
    }));
  };
  

  const handleSubmitQuestion = async () => {
    try {
      let response = null 
      console.log(weekId)
      if( currentQuestionType === "GQ"){
        response = await axios.post(`http://127.0.0.1:5000/api/graded/quiz/${weekId}`, { 
          answers, 
          user_id: localStorage.getItem("user_Id") 
      });
      }
      else{
        response = await axios.post(`http://127.0.0.1:5000/api/activity/quiz/${selectedLectureId}`, { answers,user_id: localStorage.getItem("user_Id") });
        console.log(response.data);
      }
      
      
      // Adjust for total_score from the backend
      toast({
        title: `Your score is: ${response.data.score}`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error submitting answers',
        description: 'There was an issue submitting your answers. Please try again later.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  

  const handleHint = () => {
    fetch('http://127.0.0.1:5000/api/explainCode', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code: editorContent,
        question_id: questionId,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          setOutput('Error: ' + data.error);
        } else {
          setOutput(data.hint);
        }
      })
      .catch((error) => setOutput('Error: ' + error));
  };

  const handleGetCode = () => {
    fetch('http://127.0.0.1:5000/api/getEfficientCode', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question_id: questionId // Use question_id
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          setOutput('Error: ' + data.error);
        } else {
          setOutput(data.efficient_code);
        }
      });
  };

  const MotionIconButton = motion(IconButton);

  return (
    <Flex minHeight="100vh" direction="column" bg={bg}>
      <Box bg={bgBox} p={4} boxShadow="lg" borderBottomWidth="1px" borderColor={borderColor}>
        <Flex justify="space-between" align="center">
          <IconButton
            as={RouterLink}
            to="/"
            icon={<ArrowBackIcon />}
            aria-label="Home"
            variant="ghost"
            colorScheme="teal"
            size="lg"
          />
          <Text fontSize="4xl" fontWeight="bold" color={textColor}>
            AlgoMatrix Learning
          </Text>
          <Flex align="center">
            <MotionIconButton
              icon={colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
              onClick={toggleColorMode}
              aria-label="Toggle Dark Mode"
              colorScheme="teal"
              size="lg"
              mr={4}
              whileTap={{ scale: 0.9 }}
              transition={{ duration: 0.2 }}
            />
            <Button colorScheme="teal" size="lg" onClick={handleLogout}>
              Logout
            </Button>
          </Flex>
        </Flex>
      </Box>
      <Flex flex="1" p={6} direction={{ base: 'column', md: 'row' }} gap={4}>
        <Box
          w={{ base: '100%', md: '25%' }}
          bg={bgBox}
          p={5}
          boxShadow="lg"
          borderRadius="lg"
          borderWidth="1px"
          borderColor={borderColor}
          maxH="100vh"
          overflowY="auto"
          height="650px"
        >
          <Text fontSize="3xl" fontWeight="semibold" mb={4} color={textColor}>
            Programming in Python
          </Text>
          <Accordion allowMultiple>
            {weeks.map((week) => (
              <AccordionItem key={week.id} borderColor={borderColor} borderRadius="md" mb={2}>
                <AccordionButton _expanded={{ bg: 'teal.200', color: 'teal.800' }}>
                  <Box flex="1" textAlign="left" fontWeight="medium">
                    Week {week.week_no}
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
                <AccordionPanel pb={4}>
                  <VStack align="start" spacing={3} pl={4}>
                    <Accordion allowToggle>
                      <AccordionItem borderColor={borderColor}>
                        <AccordionButton _expanded={{ bg: 'teal.200', color: 'teal.800' }}>
                          <Box flex="1" textAlign="left">
                            Lectures
                          </Box>
                          <AccordionIcon />
                        </AccordionButton>
                        <AccordionPanel pb={4}>
                          {week.lectures.map((lecture) => (
                            <Link
                              key={lecture.id}
                              as={RouterLink}
                              to="#"
                              fontWeight="medium"
                              color={
                                selectedLectureId === lecture.id
                                  ? 'teal.800'
                                  : textColorAccordion
                              }
                              _hover={{
                                textDecoration: 'underline',
                                color: 'teal.800',
                              }}
                              onClick={() => handleLessonClick(week.id, lecture.id)}
                              bg={
                                selectedLectureId === lecture.id
                                  ? 'teal.100'
                                  : 'transparent'
                              }
                              borderRadius="md"
                              p={1}
                            >
                              {lecture.topic}
                            </Link>
                          ))}
                        </AccordionPanel>
                        
                      </AccordionItem>
                      <AccordionItem borderColor={borderColor}>
                        <AccordionButton _expanded={{ bg: 'teal.200', color: 'teal.800' }}>
                          <Box flex="1" textAlign="left">
                            Activity Questions
                          </Box>
                          <AccordionIcon />
                        </AccordionButton>
                        <AccordionPanel pb={4}>
                          {week.lectures.map((lecture) => (
                            <Link
                              key={lecture.id}
                              as={RouterLink}
                              to="#"
                              fontWeight="medium"
                              color={
                                selectedLectureId === lecture.id
                                  ? 'teal.800'
                                  : textColorAccordion
                              }
                              _hover={{
                                textDecoration: 'underline',
                                color: 'teal.800',
                              }}
                              onClick={() =>
                                handleQuestionClick(week.id, lecture.id, 'AQ')
                              }
                              bg={
                                selectedLectureId === lecture.id
                                  ? 'teal.100'
                                  : 'transparent'
                              }
                              borderRadius="md"
                              p={1}
                            >
                              {lecture.topic}
                            </Link>
                          ))}
                        </AccordionPanel>
                      </AccordionItem>
                      <AccordionItem borderColor={borderColor}>
                        <AccordionButton _expanded={{ bg: 'teal.200', color: 'teal.800' }}>
                          <Box flex="1" textAlign="left">
                            Graded Questions
                          </Box>
                          <AccordionIcon />
                        </AccordionButton>
                        <AccordionPanel pb={4}>
                          {week.lectures.map((lecture) => (
                            <Link
                              key={lecture.id}
                              as={RouterLink}
                              to="#"
                              fontWeight="medium"
                              color={
                                selectedLectureId === lecture.id
                                  ? 'teal.800'
                                  : textColorAccordion
                              }
                              _hover={{
                                textDecoration: 'underline',
                                color: 'teal.800',
                              }}
                              onClick={() =>
                                handleQuestionClick(week.id, lecture.id, 'GQ')
                              }
                              bg={
                                selectedLectureId === lecture.id
                                  ? 'teal.100'
                                  : 'transparent'
                              }
                              borderRadius="md"
                              p={1}
                            >
                              {lecture.topic}
                            </Link>
                          ))}
                        </AccordionPanel>
                      </AccordionItem>
                      <AccordionItem borderColor={borderColor}>
                        <AccordionButton _expanded={{ bg: 'teal.200', color: 'teal.800' }}>
                          <Box flex="1" textAlign="left">
                            Programming Questions
                          </Box>
                          <AccordionIcon />
                        </AccordionButton>
                        <AccordionPanel pb={4}>
                          {week.lectures.map((lecture) => (
                            <Link
                              key={lecture.id}
                              as={RouterLink}
                              to="#"
                              fontWeight="medium"
                              color={
                                selectedLectureId === lecture.id
                                  ? 'teal.800'
                                  : textColorAccordion
                              }
                              _hover={{
                                textDecoration: 'underline',
                                color: 'teal.800',
                              }}
                              onClick={() =>
                                handleQuestionClick(week.id, lecture.id, 'PP')
                              }
                              bg={
                                selectedLectureId === lecture.id
                                  ? 'teal.100'
                                  : 'transparent'
                              }
                              borderRadius="md"
                              p={1}
                            >
                              {lecture.topic}
                            </Link>
                          ))}
                        </AccordionPanel>
                      </AccordionItem>
                      <WeeklyPerformance  userId={localStorage.getItem("user_Id")} weekNo={week.id} />
                     </Accordion>
                              
                    </VStack>
                    </AccordionPanel>
                    </AccordionItem>
                      ))}
                    </Accordion>
                  </Box>
                  <Box
                    flex="1"
                    bg={bgBox}
                    p={6}
                    boxShadow="lg"
                    borderRadius="lg"
                    borderWidth="1px"
                    borderColor={borderColor}
                    
                  >

{showQuestions ? (
  <>
    <Heading mb={4} color={textColor} fontSize="xl" fontWeight="semibold">
      {currentQuestionType === 'AQ' 
        ? 'Activity Questions' 
        : currentQuestionType === 'GQ' 
        ? 'Graded Questions' 
        : currentQuestionType === 'PP' 
        ? 'Programming Assignment' 
        : 'Unknown Question Type'}
    </Heading>

    <VStack align="start" spacing={6}>
      {questions.map((question) => (
        <Box key={question.id} w="100%">
          <Text mb={2} color={textColor}>{question.question}</Text>
          {currentQuestionType === 'PP' && (
            <>
              <AceEditor
                mode="python"   // Set the mode according to the programming language
                theme="monokai" // Set the theme
                name="editor"
                editorProps={{ $blockScrolling: true }}
                fontSize={14}
                width="100%"
                height="300px"
                setOptions={{
                  enableBasicAutocompletion: true,
                  enableLiveAutocompletion: true,
                  enableSnippets: true,
                  showLineNumbers: true,
                  tabSize: 4,
                }}
                value={editorContent} // Bind editor content to state
                onChange={(newValue) => setEditorContent(newValue)}
              />
              
              <Stack direction="row" spacing={4} mt={4}>
                <Button colorScheme="blue" onClick={handleCompile}>Test Run</Button>
                <Button colorScheme="yellow" onClick={handleHint}>Codexplainer</Button>
                <Button colorScheme="red" onClick={handleGetCode}>Solution</Button>
                <Button colorScheme="green" onClick={handleSubmit}>Submit</Button>
              </Stack>
    
              {/* Console Output Section */}
              <Box mt={6} bg="gray.800" color="white" p={4} borderRadius="md" maxH="250px" overflowY="auto">
              
                <Textarea
                  value={output}
                  readOnly
                  bg="gray.700"
                  color="white"
                  height="250px"
                  fontFamily="monospace"
                  fontSize="14px"
                  resize="none"
                />
              </Box>
            </>
          )}

          {currentQuestionType !== 'PP' ? (
          question.question_type_MCQ_MSQ === 'MSQ' ? (
            <CheckboxGroup
              value={answers[question.question_id] || []}
              onChange={(values) => handleAnswerChange(question.question_id, values)}
            >
              <Stack direction="column">
                {question.options.map((option, index) => (
                  <Checkbox key={index} value={option} colorScheme="teal">
                    {option}
                  </Checkbox>
                ))}
              </Stack>
            </CheckboxGroup>
            ) : (
              <RadioGroup
                value={answers[question.question_id]}
                onChange={(value) => handleAnswerChange(question.question_id, value)}
              >
                <Stack direction="column">
                  {question.options.map((option, index) => (
                    <Radio key={index} value={option} colorScheme="teal">
                      {option}
                    </Radio>
                  ))}
                </Stack>
              </RadioGroup>
            )
          ) : (
          <Text fontSize="lg" color={textColor} fontWeight="bold" lineHeight="1.5" mb={4}>
            {question.description} 
          </Text>
        )}


          {currentQuestionType === 'AQ' && (
            <Stack direction="row" mt={4}>
              <ExplainerModal question_id={questionId} />
            </Stack>
          )}
        </Box>
      ))}
    </VStack>

    <Stack direction="row" spacing={4} mt={6}>
      {/* Show Submit button only for AQ and GQ */}
      {(currentQuestionType === 'AQ' || currentQuestionType === 'GQ') && (
        <Button
          colorScheme="teal"
          size="lg"
          onClick={handleSubmitQuestion}
        >
          Submit
        </Button>
      )}

      {/* Only show Practice More button for Activity Questions */}
      {currentQuestionType === 'AQ' && (
        <Button
          colorScheme="teal"
          size="lg"
          onClick={() => navigate(`/practice-more/${selectedLectureId}`)}
        >
          Practice More
        </Button>
      )}
    </Stack>
  </>
) 



        : selectedVideoUrl ? (
          <>
            <Box
              as="iframe"
              title="Lecture Video"
              src={selectedVideoUrl}
              width="100%"
              height="650px"
              borderRadius="md"
              boxShadow="lg"
              borderWidth="1px"
              borderColor={borderColor}
              mb={4} // Add margin bottom for spacing
            />

            {/* Modal Buttons below the video */}
            <Stack direction="row" spacing={4} mt={4} justify={"center"}>
              <AboutVideoModal  lessonId={selectedLectureId} />
              <TranscriptModal lessonId={selectedLectureId} />
              <ChatBotModal />
              <RateVideoModal lessonId={selectedLectureId} />
            </Stack>
          </>
        ) : (
          <Text fontSize="xl" color={textColor} textAlign="center">
  <marquee>Welcome to AlgoMatrix Learning! <br/> Please select a lecture to get started.</marquee>
  
  
</Text>


        )}

          
        </Box>
      </Flex>
    </Flex>
  );
};

export default Dashboard;
