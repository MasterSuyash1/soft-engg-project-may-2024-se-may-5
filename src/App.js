import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import SignUp from './components/SignUp';
import Dashboard from './components/Dashboard';
import AdminDashboard from './components/AdminDashboard';
import PracticeMore from './components/PracticeMore';
import WeeklyPerformance from './components/WeeklyPerformance';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} /> {/* Add the AdminDashboard route */}
          <Route path="/practice-more/:lessonId" element={<PracticeMore />} /> {/* Update the PracticeMore route */}
          <Route path="/weekly-performance/:userId/:weekNo" element={<WeeklyPerformance />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
