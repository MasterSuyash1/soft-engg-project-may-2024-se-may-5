import React, { useState } from 'react';
import {
  Box,
  Heading,
  Text,
  Button,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Spinner,
  IconButton,
  Flex,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  VStack,
} from '@chakra-ui/react';
import { DeleteIcon } from '@chakra-ui/icons';
import axios from 'axios';

// Reusable Table Component
const DataTable = ({ headers, data, renderRow, loading }) => {
  if (loading) return <Spinner size="xl" />;
  return (
    <Table variant="simple" colorScheme="teal" size="md">
      <Thead>
        <Tr>
          {headers.map((header, index) => (
            <Th key={index}>{header}</Th>
          ))}
        </Tr>
      </Thead>
      <Tbody>
        {data.map((item, index) => (
          <React.Fragment key={index}>
            {renderRow(item, index)}
          </React.Fragment>
        ))}
      </Tbody>
    </Table>
  );
};

const AdminDashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState('dashboard');

  const fetchData = async (endpoint, method = 'get') => {
    setLoading(true);
    try {
      const response = method === 'post' ? await axios.post(endpoint) : await axios.get(endpoint);
      setData(response.data);
    } catch (error) {
      console.error(`Error fetching data from ${endpoint}:`, error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewChange = (newView, endpoint, method = 'get') => {
    setView(newView);
    fetchData(endpoint, method);
  };

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/users/${userId}`);
      setData(data.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleLogout = () => {
    console.log('Logged out');
    window.location.href = '/login';
  };

  const renderReviewRow = (rating) => (
    <Tr key={rating.id}>
      <Td>{rating.id}</Td>
      <Td>{rating.user_id}</Td>
      <Td>{rating.lesson_id}</Td>
      <Td>{rating.audio}</Td>
      <Td>{rating.video}</Td>
      <Td>{rating.content}</Td>
      <Td>{rating.feedback}</Td>
      <Td>{new Date(rating.created_at).toLocaleString()}</Td>
    </Tr>
  );

  const renderUserRow = (user) => (
    <Tr key={user.id}>
      <Td>{user.id}</Td>
      <Td>{user.username}</Td>
      <Td>{user.email}</Td>
      <Td>
        <IconButton
          colorScheme="red"
          icon={<DeleteIcon />}
          onClick={() => handleDeleteUser(user.id)}
        />
      </Td>
    </Tr>
  );

  const renderSentimentRow = (summary, index) => {
    const sentimentPercentage = summary.sentiment * 100;
    const sliderColor = sentimentPercentage < 50 ? 'red.400' : 'teal.400';

    return (
      <Box
        key={`sentiment-box-${index}`}
        width="100%"
        border="1px"
        borderColor="gray.200"
        p={4}
        mb={4}
        borderRadius="md"
        bg="white"
        shadow="sm"
      >
        <Flex justifyContent="space-between" alignItems="center" mb={4}>
          <Text fontWeight="bold">Lesson {summary.lesson_id}:</Text>
          <Flex alignItems="center" width="70%">
            <Slider value={sentimentPercentage} isReadOnly flex="1" mr={4}>
              <SliderTrack bg="teal.100">
                <SliderFilledTrack bg={sliderColor} />
              </SliderTrack>
              <SliderThumb boxSize={0} />
            </Slider>
            <Text fontSize="lg">{sentimentPercentage.toFixed(2)}%</Text>
          </Flex>
        </Flex>
        <Text fontWeight="bold" mb={2}>Feedback Summary:</Text>
        <Text mb={2}>{summary.feedback_summary}</Text>
        <Text fontWeight="bold" mb={2}>Suggestions:</Text>
        <Text>{summary.suggestions}</Text>
      </Box>
    );
  };

  return (
    <Box minHeight="100vh" bg="gray.50" py={12} px={10} display="flex" justifyContent="center" alignItems="center">
      <Box
        width={['90%', '80%', '60%', '80%']}
        bg="white"
        borderRadius="md"
        p={6}
        shadow="lg"
      >
        <Heading fontSize="3xl" mb={4} textAlign="center" bgGradient="linear(to-r, teal.400, teal.600)" bgClip="text">
          Admin Dashboard
        </Heading>

        {view === 'dashboard' ? (
          <VStack spacing={6} alignItems="center">
            <Text fontSize="xl" color="gray.600">
              Welcome, Admin!
            </Text>
            <Button
              colorScheme="teal"
              width="50%"
              onClick={() => handleViewChange('reviews', 'http://127.0.0.1:5000/api/ratings')}
            >
              Show Me Reviews Info
            </Button>
            <Button
              colorScheme="teal"
              width="50%"
              onClick={() => handleViewChange('users', 'http://127.0.0.1:5000/api/users')}
            >
              Show Me Users Info
            </Button>
            <Button
              colorScheme="teal"
              width="50%"
              onClick={() => handleViewChange('sentiment', 'http://127.0.0.1:5000/api/sentiment_analysis', 'post')}
            >
              Show Sentiment Analysis
            </Button>
            <Button colorScheme="red" width="50%" onClick={handleLogout}>
              Logout
            </Button>
          </VStack>
        ) : (
          <VStack spacing={8} alignItems="start" width="100%">
            <Button colorScheme="teal" size="lg" onClick={() => setView('dashboard')}>
              Back to Dashboard
            </Button>

            {view === 'reviews' && (
              <DataTable
                headers={['ID', 'User ID', 'Lesson ID', 'Audio', 'Video', 'Content', 'Feedback', 'Created At']}
                data={data}
                renderRow={renderReviewRow}
                loading={loading}
              />
            )}

            {view === 'users' && (
              <DataTable
                headers={['ID', 'Username', 'Email', 'Actions']}
                data={data}
                renderRow={renderUserRow}
                loading={loading}
              />
            )}

            {view === 'sentiment' && (
              <>
                <Heading fontSize="2xl" mb={4} color="teal.600">
                  Course Content Analysis
                </Heading>
                
                <DataTable
                  headers={[' ']}
                  data={data.lecture_feedback_summaries || []}
                  renderRow={renderSentimentRow}
                  loading={loading}
                />
              </>
            )}
          </VStack>
        )}
      </Box>
    </Box>
  );
};

export default AdminDashboard;
