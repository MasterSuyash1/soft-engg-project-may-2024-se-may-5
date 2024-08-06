import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import SignUp from './components/SignUp';
<<<<<<< HEAD
import Dashboard from './components/Dashboard'; // Import the Dashboard component
=======
import Dashboard from './components/Dashboard';
import ProgrammingAssignment from './components/ProgrammingAssignment';
import AdminDashboard from './components/AdminDashboard'; // Import the AdminDashboard component
>>>>>>> main

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
<<<<<<< HEAD
          <Route path="/dashboard" element={<Dashboard />} /> {/* Add the Dashboard route */}
=======
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/programming-assignment" element={<ProgrammingAssignment />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} /> {/* Add the AdminDashboard route */}
>>>>>>> main
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
<<<<<<< HEAD

=======
>>>>>>> main
