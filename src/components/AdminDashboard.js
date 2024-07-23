import React, { useEffect, useState } from 'react';
import { Box, Heading, Text, Button, Table, Thead, Tbody, Tr, Th, Td, Spinner, IconButton } from '@chakra-ui/react';
import { DeleteIcon } from '@chakra-ui/icons';
import axios from 'axios';

const AdminDashboard = () => {
  const [ratings, setRatings] = useState([]);
  const [users, setUsers] = useState([]);
  const [sentiments, setSentiments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showReviews, setShowReviews] = useState(false);
  const [showUsers, setShowUsers] = useState(false);
  const [showSentiment, setShowSentiment] = useState(false);

  const fetchRatings = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/ratings');
      setRatings(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching ratings:', error);
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/users');
      setUsers(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching users:', error);
      setLoading(false);
    }
  };

  const fetchSentiments = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/sentiment_analysis');
      setSentiments(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching sentiments:', error);
      setLoading(false);
    }
  };

  const handleShowReviews = () => {
    setShowReviews(true);
    setShowUsers(false);
    setShowSentiment(false);
    fetchRatings();
  };

  const handleShowUsers = () => {
    setShowUsers(true);
    setShowReviews(false);
    setShowSentiment(false);
    fetchUsers();
  };

  const handleShowSentiments = () => {
    setShowSentiment(true);
    setShowUsers(false);
    setShowReviews(false);
    fetchSentiments();
  };

  const handleBackToDashboard = () => {
    setShowReviews(false);
    setShowUsers(false);
    setShowSentiment(false);
  };

  const handleLogout = () => {
    console.log('Logged out');
    window.location.href = '/login'; // Adjust the path as needed
  };

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/users/${userId}`);
      setUsers(users.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  return (
    <Box
      minHeight="100vh"
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      bg="gray.50"
      py={12}
    >
      <Heading
        fontSize="4xl"
        mb={4}
        bgGradient="linear(to-r, teal.400, teal.600)"
        bgClip="text"
      >
        Admin Dashboard
      </Heading>
      {!showReviews && !showUsers && !showSentiment ? (
        <>
          <Text fontSize="xl" color="gray.600" mb={8}>
            Welcome, Admin!
          </Text>
          <Button
            colorScheme="teal"
            size="lg"
            mb={8}
            onClick={handleShowReviews}
          >
            Show Me Reviews Info
          </Button>
          <Button
            colorScheme="teal"
            size="lg"
            mb={8}
            onClick={handleShowUsers}
          >
            Show Me Users Info
          </Button>
          <Button
            colorScheme="teal"
            size="lg"
            mb={8}
            onClick={handleShowSentiments}
          >
            Show Sentiment Analysis
          </Button>
          <Button
            colorScheme="red"
            size="lg"
            mb={8}
            onClick={handleLogout}
          >
            Logout
          </Button>
        </>
      ) : (
        <>
          <Button
            colorScheme="teal"
            size="lg"
            mb={8}
            onClick={handleBackToDashboard}
          >
            Back to Dashboard
          </Button>
          {loading ? (
            <Spinner size="xl" />
          ) : showReviews ? (
            <Table variant="striped" colorScheme="teal">
              <Thead>
                <Tr>
                  <Th>ID</Th>
                  <Th>User ID</Th>
                  <Th>Audio</Th>
                  <Th>Video</Th>
                  <Th>Content</Th>
                  <Th>Feedback</Th>
                  <Th>Created At</Th>
                </Tr>
              </Thead>
              <Tbody>
                {ratings.map(rating => (
                  <Tr key={rating.id}>
                    <Td>{rating.id}</Td>
                    <Td>{rating.user_id}</Td>
                    <Td>{rating.audio}</Td>
                    <Td>{rating.video}</Td>
                    <Td>{rating.content}</Td>
                    <Td>{rating.feedback}</Td>
                    <Td>{new Date(rating.created_at).toLocaleString()}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          ) : showUsers ? (
            <Table variant="striped" colorScheme="teal">
              <Thead>
                <Tr>
                  <Th>ID</Th>
                  <Th>Username</Th>
                  <Th>Email</Th>
                  <Th>Actions</Th>
                </Tr>
              </Thead>
              <Tbody>
                {users.map(user => (
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
                ))}
              </Tbody>
            </Table>
          ) : (
            <Table variant="striped" colorScheme="teal">
              <Thead>
                <Tr>
                  <Th>Feedback</Th>
                  <Th>Sentiment</Th>
                </Tr>
              </Thead>
              <Tbody>
                {sentiments.map((sentiment, index) => (
                  <Tr key={index}>
                    <Td>{sentiment.feedback}</Td>
                    <Td>{sentiment.sentiment}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          )}
        </>
      )}
    </Box>
  );
};

export default AdminDashboard;
